# Copyright (c) 2018 AngelLiang
# Copyright (c) 2023 Hewlett Packard Enterprise Development LP
# MIT License

import datetime as dt
import logging
from multiprocessing.util import Finalize
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

import sqlalchemy
from celery import Celery, current_app, schedules
from celery.beat import ScheduleEntry, Scheduler
from celery.utils.time import maybe_make_aware
from kombu.utils.json import dumps, loads

from rdbbeat.db.models import CrontabSchedule, PeriodicTask, PeriodicTaskChanged

# This scheduler must wake up more frequently than the
# regular of 5 minutes because it needs to take external
# changes to the schedule into account.
DEFAULT_MAX_INTERVAL = 5  # seconds

ADD_ENTRY_ERROR = """\
Cannot add entry %r to database schedule: %r. Contents: %r
"""


logger = logging.getLogger(__name__)


class ModelEntry(ScheduleEntry):
    """Scheduler entry taken from database row."""

    model_schedules = (
        # (schedule_type, model_type, model_field)
        (schedules.crontab, CrontabSchedule, "crontab"),
    )
    save_fields = ["last_run_at", "total_run_count", "no_changes"]

    def __init__(
        self,
        model: schedules.schedule,
        session_scope: Callable,
        app: Celery = None,
        **kw: Any,
    ) -> None:
        """Initialize the model entry."""
        self.app = app or current_app._get_current_object()
        self.session = kw.get("session")
        self.session_scope = session_scope
        self.model = model
        self.name = model.name
        self.task = model.task
        self.schedule = model.schedule
        self.args = loads(model.args or "[]")
        self.kwargs = loads(model.kwargs or "{}")

        logger.debug(f"schedule: {self.schedule}")

        self.options = {}
        for option in ["queue", "exchange", "routing_key", "expires", "priority"]:
            value = getattr(model, option)
            if value is None:
                continue
            self.options[option] = value

        self.total_run_count = model.total_run_count
        self.enabled = model.enabled

        if not model.last_run_at:
            model.last_run_at = self._default_now()
        self.last_run_at = model.last_run_at

        # update tzinfo since it may not be present
        self.last_run_at = self.last_run_at.replace(tzinfo=self.app.timezone)

    def _disable(self, model: schedules.schedule) -> None:
        model.no_changes = True
        self.model.enabled = self.enabled = model.enabled = False
        if self.session:
            self.session.add(model)
            self.session.commit()
        else:
            with self.session_scope() as session:
                session.add(model)
                session.commit()

    def is_due(self) -> bool:
        if not self.model.enabled:
            # 5 second delay for re-enable.
            return schedules.schedstate(False, 5.0)

        # START DATE: only run after the `start_time`, if one exists.
        if self.model.start_time is not None:
            now = maybe_make_aware(self._default_now())
            start_time = self.model.start_time.replace(tzinfo=self.app.timezone)
            if now < start_time:
                # The datetime is before the start date - don't run.
                _, delay = self.schedule.is_due(self.last_run_at)
                # use original delay for re-check
                return schedules.schedstate(False, delay)

        # ONE OFF TASK: Disable one off tasks after they've ran once
        if self.model.one_off and self.model.enabled and self.model.total_run_count > 0:
            self.model.enabled = False  # disable
            self.model.total_run_count = 0  # Reset
            self.model.no_changes = False  # Mark the model entry as changed
            save_fields = ("enabled",)  # the additional fields to save
            self.save(save_fields)

            return schedules.schedstate(False, None)  # Don't recheck

        return self.schedule.is_due(self.last_run_at)

    def _default_now(self) -> dt.datetime:
        now = self.app.now()
        # The PyTZ datetime must be localised for the scheduler to work
        # Keep in mind that timezone arithmatic
        # with a localized timezone may be inaccurate.
        # return now.tzinfo.localize(now.replace(tzinfo=None))
        return now.replace(tzinfo=self.app.timezone)

    def __next__(self) -> ScheduleEntry:
        # should be use `self._default_now()` or `self.app.now()` ?
        self.model.last_run_at = self.app.now()
        self.model.total_run_count += 1
        self.model.no_changes = True
        return self.__class__(self.model, self.session_scope)

    next = __next__  # for 2to3

    def save(self, fields: Tuple = tuple()) -> None:
        """
        :params fields: tuple, the additional fields to save
        """
        # Object may not be synchronized, so only
        # change the fields we care about.
        with self.session_scope() as session:
            obj = session.query(PeriodicTask).get(self.model.id)

            for field in self.save_fields:
                setattr(obj, field, getattr(self.model, field))
            for field in fields:
                setattr(obj, field, getattr(self.model, field))
            session.add(obj)
            session.commit()

    @classmethod
    def to_model_schedule(
        cls, session: sqlalchemy.orm.Session, schedule: schedules.schedule
    ) -> Tuple[CrontabSchedule, str]:
        for schedule_type, model_type, model_field in cls.model_schedules:
            # change to schedule
            schedule = schedules.maybe_schedule(schedule)
            if isinstance(schedule, schedule_type):
                model_schedule = model_type.from_schedule(session, schedule)  # type: ignore
                return model_schedule, model_field

        raise ValueError(f"Cannot convert schedule type {schedule!r} to model")

    @classmethod
    def from_entry(
        cls, name: str, session_scope: Callable, app: Celery = None, **entry: Dict
    ) -> "PeriodicTask":
        """

        **entry sample:

            {'task': 'celery.backend_cleanup',
             'schedule': schedules.crontab('0', '4', '*'),
             'options': {'expires': 43200}}

        """
        with session_scope() as session:
            periodic_task = session.query(PeriodicTask).filter_by(name=name).first()
            if not periodic_task:
                periodic_task = PeriodicTask(name=name)
            temp = cls._unpack_fields(session, **entry)
            periodic_task.update(**temp)
            session.add(periodic_task)
            try:
                session.commit()
            except sqlalchemy.exc.IntegrityError as exc:
                logger.error(exc)
                session.rollback()
            except Exception as exc:
                logger.error(exc)
                session.rollback()
            res = cls(periodic_task, app=app, session_scope=session_scope, session=session)
            return res

    @classmethod
    def _unpack_fields(
        cls,
        session: sqlalchemy.orm.Session,
        schedule: schedules.schedule,
        args: Optional[Any] = None,
        kwargs: Optional[Dict] = None,
        options: Optional[Dict] = None,
        **entry: Dict,
    ) -> Dict:
        """

        **entry sample:

            {'task': 'celery.backend_cleanup',
             'schedule': <crontab: 0 4 * * * (m/h/d/dM/MY)>,
             'options': {'expires': 43200}}

        """
        model_schedule, model_field = cls.to_model_schedule(session, schedule)
        entry.update(
            # the model_id which to relationship
            {model_field + "_id": model_schedule.id},  # type: ignore [dict-item]
            args=dumps(args or []),
            kwargs=dumps(kwargs or {}),
            **cls._unpack_options(**options or {}),
        )
        return entry

    @classmethod
    def _unpack_options(
        cls,
        queue: Optional[str] = None,
        exchange: Optional[str] = None,
        routing_key: Optional[str] = None,
        priority: Optional[int] = None,
        one_off: Optional[bool] = None,
        expires: Any = None,  # anti-pattern, 281 changes the type
        **kwargs: Dict,
    ) -> Dict:
        data = {
            "queue": queue,
            "exchange": exchange,
            "routing_key": routing_key,
            "priority": priority,
            "one_off": one_off,
        }
        if expires:
            if isinstance(expires, int):
                expires = dt.datetime.utcnow() + dt.timedelta(seconds=expires)
            elif isinstance(expires, dt.datetime):
                pass
            else:
                raise ValueError("expires value error")
            data["expires"] = expires
        return data


class DatabaseScheduler(Scheduler):
    Entry = ModelEntry
    Model = PeriodicTask
    Changes = PeriodicTaskChanged

    _schedule = None
    _last_timestamp = None
    _initial_read = True
    _heap_invalidated = False

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the database scheduler."""
        self.app = kwargs["app"]
        self.session_scope: Callable = kwargs.get("session_scope") or self.app.conf.get(
            "session_scope"
        )
        self._dirty: Set[Any] = set()
        Scheduler.__init__(self, *args, **kwargs)
        self._finalize = Finalize(self, self.sync, exitpriority=5)
        self.max_interval = (
            kwargs.get("max_interval")
            or self.app.conf.beat_max_loop_interval
            or DEFAULT_MAX_INTERVAL
        )

    def setup_schedule(self) -> None:
        """override"""
        logger.info("setup_schedule")
        self.install_default_entries(self.schedule)
        self.update_from_dict(self.app.conf.beat_schedule)

    def all_as_schedule(self) -> Dict:
        logger.debug("DatabaseScheduler: Fetching database schedule")
        with self.session_scope() as session:
            # get all enabled PeriodicTask
            models = session.query(self.Model).filter_by(enabled=True).all()
            s = {}
            for model in models:
                try:
                    s[model.name] = self.Entry(
                        model, app=self.app, session_scope=self.session_scope, session=session
                    )
                except ValueError:
                    pass
            return s

    def schedule_changed(self) -> bool:
        with self.session_scope() as session:
            changes = session.query(self.Changes).get(1)
            if not changes:
                changes = self.Changes(id=1)
                session.add(changes)
                session.commit()
                return False

            last, ts = self._last_timestamp, changes.last_update
            try:
                if ts and ts > (last if last else ts):
                    return True
            finally:
                self._last_timestamp = ts
            return False

    def reserve(self, entry: ScheduleEntry) -> ScheduleEntry:
        """override

        It will be called in parent class.
        """
        new_entry = next(entry)
        # Need to store entry by name, because the entry may change
        # in the mean time.
        self._dirty.add(new_entry.name)
        return new_entry

    def sync(self) -> None:
        """override"""
        logger.info("Writing entries...")
        _tried = set()
        _failed = set()
        try:
            while self._dirty:
                name = self._dirty.pop()
                try:
                    self.schedule[name].save()  # save to database
                    logger.debug(f"{name} save to database")
                    _tried.add(name)
                except KeyError as exc:
                    logger.error(exc)
                    _failed.add(name)
        except sqlalchemy.exc.IntegrityError as exc:
            logger.exception("Database error while sync: %r", exc)
        except Exception as exc:
            logger.exception(exc)
        finally:
            # retry later, only for the failed ones
            self._dirty |= _failed

    def update_from_dict(self, mapping: Dict) -> None:
        s = {}
        for name, entry_fields in mapping.items():
            # {'task': 'celery.backend_cleanup',
            #  'schedule': schedules.crontab('0', '4', '*'),
            #  'options': {'expires': 43200}}
            try:
                entry = self.Entry.from_entry(
                    name, session_scope=self.session_scope, app=self.app, **entry_fields
                )
                if entry.model.enabled:
                    s[name] = entry
            except Exception as exc:
                logger.error(ADD_ENTRY_ERROR, name, exc, entry_fields)

        # update self.schedule
        self.schedule.update(s)

    def install_default_entries(self, data: Dict) -> None:
        entries: Dict = {}
        if self.app.conf.result_expires:
            entries.setdefault(
                "celery.backend_cleanup",
                {
                    "task": "celery.backend_cleanup",
                    "schedule": schedules.crontab("0", "4", "*"),
                    "options": {"expires": 12 * 3600},
                },
            )
        self.update_from_dict(entries)

    def schedules_equal(self, *args: Any, **kwargs: Dict) -> bool:
        if self._heap_invalidated:
            self._heap_invalidated = False
            return False
        return super(DatabaseScheduler, self).schedules_equal(*args, **kwargs)

    @property
    def schedule(self) -> Scheduler:
        initial = update = False
        if self._initial_read:
            logger.debug("DatabaseScheduler: initial read")
            initial = update = True
            self._initial_read = False
        elif self.schedule_changed():
            # when you updated the `PeriodicTasks` model's `last_update` field
            logger.info("DatabaseScheduler: Schedule changed.")
            update = True

        if update:
            self.sync()
            self._schedule = self.all_as_schedule()
            # the schedule changed, invalidate the heap in Scheduler.tick
            if not initial:
                self._heap: List[Any] = []
                self._heap_invalidated = True
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(
                    "Current schedule:\n%s",
                    "\n".join(repr(entry) for entry in self._schedule.values()),
                )
        # logger.debug(self._schedule)
        return self._schedule

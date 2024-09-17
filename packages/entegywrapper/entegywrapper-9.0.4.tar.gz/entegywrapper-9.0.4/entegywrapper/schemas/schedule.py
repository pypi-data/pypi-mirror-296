from typing import Any, Optional
from .content import Content


class SessionSegment(Content):
    externalReference: Optional[str] = None
    multiLinks: list[Any] = []


class Session(Content):
    segments: list[SessionSegment] = []


class SessionGroup(Content):
    sessions: list[Session] = []


class ScheduleDay(Content):
    children: list[Session | SessionGroup]


class Schedule(Content):
    days: list[ScheduleDay]

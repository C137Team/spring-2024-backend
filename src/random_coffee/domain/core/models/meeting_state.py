from enum import Enum


class MeetingStateEnum(Enum):
    PLANNED = 'PLANNED'
    REJECTED = 'REJECTED'
    SCHEDULED = 'SCHEDULED'
    CANCELLED = 'CANCELLED'
    OCCUR = 'OCCUR'
    COMPLETED = 'COMPLETED'

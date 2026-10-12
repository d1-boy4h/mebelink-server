from enum import StrEnum


class ProjectStatus(StrEnum):
    NOT_IN_PROGRESS = 'not_in_progress'
    IN_PROGRESS     = 'in_progress'
    POSTPONED       = 'postponed'
    COMPLETED       = 'completed'

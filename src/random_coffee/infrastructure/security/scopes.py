from enum import Enum


class AccessScopeEnum(Enum):
    read_schedule = 'read_schedule'
    edit_schedule = 'edit_schedule'
    approve_identification_request = 'approve_identification_request'
    access_vitals = 'access_vitals'
    teach = 'teach'

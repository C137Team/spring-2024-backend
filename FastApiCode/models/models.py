from enum import Enum
from pydantic import BaseModel
from datetime import datetime

db = []

class MeetingType(Enum):
    Offline = 1
    Offline_office = 2
    Online = 3

class Duration(Enum):
    Ten_Minute = 10
    Fifteen_Minute = 15
    Thirty_Minute = 30

class MeetingState(str, Enum):
    pending = "Pending"
    created = "Created"
    planned = "Planned"
    occur = "Occur"
    completed = "Completed"
    cancelled = "Cancelled"
    rejected = "Rejected"

class UserProfile(BaseModel):
    username: str
    email: str
    tg_login: str
    role: str
    organization: str
    post: str
    agreed_meeting: bool = False

class Meeting(BaseModel):
    participants: list
    date_time: datetime
    place: str
    meeting_type: MeetingType
    duration: Duration
    state: MeetingState

class Organization(BaseModel):
    name: str

class Person(BaseModel):
    full_name: str
    location_city: str = None
    preferences: str = None

class Employee(BaseModel):
    organization: Organization
    position: str
    department: str = None

class Role(str, Enum):
    organisation_administrator = "Organisation administrator"
    employee = "Employee"
    meeting_participant = "Meeting participant"

class Post(BaseModel):
    title: str

class OrganisationUnit(BaseModel):
    name: str
from dataclasses import dataclass


@dataclass
class ProceedWanderDTO:
    organisation_id: int


@dataclass
class ProceedWanderResponseDTO:
    total_wanderring: int

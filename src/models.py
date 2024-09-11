from dataclasses import dataclass

@dataclass
class BaseClassification:
    db_name: str
    owner_email: str
    manager_email: str
    classification: str

@dataclass
class UserInformation:
    row_id: int
    user_id: str
    user_state: str
    user_manager: str


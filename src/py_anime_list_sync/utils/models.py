from dataclasses import dataclass


@dataclass
class AuthenticatedAccount:
    id: int
    tracker: str
    account_name: str

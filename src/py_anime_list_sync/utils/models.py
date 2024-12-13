from dataclasses import dataclass


@dataclass
class AuthenticatedAccount:
    tracker: str
    account_name: str

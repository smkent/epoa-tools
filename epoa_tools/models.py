from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str


@dataclass
class MyInfo:
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[Address] = None

    @property
    def is_anonymous(self) -> bool:
        return not self.name


@dataclass
class PayTransparencyComplaint:
    my_info: MyInfo
    company_name: str
    company_email: Optional[str] = None
    company_phone: Optional[str] = None
    company_mailing_address: Optional[Address] = None
    additional_information: Optional[str] = None
    evidence_files: List[str] = field(default_factory=list)
    redact_words: List[str] = field(default_factory=list)

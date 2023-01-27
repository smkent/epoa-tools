from dataclasses import dataclass
from typing import Optional


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
    company_address: Optional[Address] = None
    company_mailing_address: Optional[Address] = None

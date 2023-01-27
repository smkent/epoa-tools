from .models import MyInfo, PayTransparencyComplaint
from .pdf import fill_pdf


def main() -> None:
    my_info = MyInfo(name="Anon E. Mouse", email="example@example.com")
    ptc = PayTransparencyComplaint(my_info=my_info, company_name="ACME Corp")
    print(ptc)
    fill_pdf(ptc)

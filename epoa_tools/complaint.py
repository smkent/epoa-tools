from datetime import datetime

from slugify import slugify

from .models import MyInfo, PayTransparencyComplaint
from .pdf import create_pdf


def main() -> None:
    my_info = MyInfo(name="Anon E. Mouse", email="example@example.com")
    ptc = PayTransparencyComplaint(my_info=my_info, company_name="ACME Corp")
    output_file = "{}-pay-transparency-complaint.pdf".format(
        slugify(
            f"{ptc.my_info.name}-{ptc.company_name}"
            f"-{datetime.now().strftime('%Y%m%d')}"
        )
    )
    create_pdf(ptc, output_file, overwrite=True)

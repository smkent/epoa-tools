from argparse import ArgumentParser
from datetime import datetime

from slugify import slugify

from .models import MyInfo, PayTransparencyComplaint
from .pdf import create_pdf


def build_pay_transparency_complaint() -> PayTransparencyComplaint:
    ap = ArgumentParser()
    ap.add_argument(
        "--name",
        dest="my_name",
        metavar="full name",
        help="Complainant full name",
    )
    ap.add_argument(
        "--email",
        dest="my_email",
        metavar="address",
        help="Complainant contact email",
    )
    ap.add_argument("company_name", help="Company name")
    args = ap.parse_args()

    my_info = MyInfo(name=args.my_name, email=args.my_email)
    return PayTransparencyComplaint(
        my_info=my_info, company_name=args.company_name
    )


def main() -> None:
    ptc = build_pay_transparency_complaint()
    output_file = "{}-pay-transparency-complaint.pdf".format(
        slugify(
            f"{ptc.my_info.name or 'anonymous'}-{ptc.company_name}"
            f"-{datetime.now().strftime('%Y%m%d')}"
        )
    )
    create_pdf(ptc, output_file, overwrite=True)

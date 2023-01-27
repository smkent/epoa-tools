from argparse import ArgumentParser
from datetime import datetime

from slugify import slugify

from .complaint import ComplaintForm
from .models import MyInfo, PayTransparencyComplaint


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
    ap.add_argument(
        "-r",
        "--redact",
        dest="redact_words",
        metavar="word",
        nargs="+",
        help="Redact this word from evidence files",
    )
    ap.add_argument(
        "-i",
        "--addinfo",
        "--additional-information",
        dest="additional_information",
        metavar="text",
        help="Additional complaint information text",
    )
    ap.add_argument(
        "evidence_files",
        metavar="evidence_file",
        nargs="*",
        help="Evidence file(s)",
    )
    args = ap.parse_args()
    return PayTransparencyComplaint(
        my_info=MyInfo(name=args.my_name, email=args.my_email),
        company_name=args.company_name,
        additional_information=args.additional_information,
        evidence_files=args.evidence_files,
        redact_words=args.redact_words,
    )


def main() -> None:
    ptc = build_pay_transparency_complaint()
    output_file = "{}-pay-transparency-complaint.pdf".format(
        slugify(
            f"{ptc.my_info.name or 'anonymous'}-{ptc.company_name}"
            f"-{datetime.now().strftime('%Y%m%d')}"
        )
    )
    cf = ComplaintForm(ptc)
    cf.pdf(output_file, overwrite=True)

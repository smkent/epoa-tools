import subprocess
import sys
import tempfile
from datetime import datetime
from importlib import resources
from pathlib import Path
from typing import Dict, Iterable, Tuple

from fdfgen import forge_fdf

from .models import PayTransparencyComplaint

FORM_FILE = "F700-200-000.pdf"


def _run(*cmd: str) -> None:
    print("+ " + " ".join(cmd), file=sys.stderr)
    subprocess.call(cmd)


def form_path() -> Path:
    package = "epoa_tools.data"
    try:
        with resources.as_file(  # type: ignore
            resources.files(package).joinpath(FORM_FILE)  # type: ignore
        ) as path:
            return path  # type: ignore
    except AttributeError:
        with resources.path(package, FORM_FILE) as path:
            return path


def complaint_to_fdf(
    data: PayTransparencyComplaint,
) -> Iterable[Tuple[str, str]]:
    name = data.my_info.name or "Anonymous"

    fdf_fields: Dict[str, str] = {}
    fdf_fields.update(
        {
            # Section A
            "Name (As it appears on your ID - First Middle Last Name)": name,
            "Preferred Language": "English",
        }
    )
    if data.my_info.address:
        fdf_fields.update(
            {
                "Mailing Address": data.my_info.address.street,
                "Mailing Address City": data.my_info.address.city,
                "Mailing Address State": data.my_info.address.state,
                "Mailing Address Zip Code": str(data.my_info.address.zip_code),
            }
        )
    fdf_fields.update(
        {
            "Phone Number": data.my_info.phone or "",
            "Email Address": data.my_info.email or "",
            "Starting Date with this Employer": "",
            "Are you still employed with the employer?": "Choice1",  # "No"
            'If "No", last date employed': "",
            "Reason for Leaving": "Don't Know/Other",
            "Reason for Leaving: Don't Know/Other Specified": "",
            "What kind of work do you do?": "",
            (
                "Not providing wage or salary range, benefits, and other"
                " compensation on a job posting"
            ): "Yes",
            # Section B
            "Name of Company (Business Name)": data.company_name,
            "Company Contact (Owner, Manager, or Supervisor) Name": (
                data.company_name
            ),
            "Company Mailing Address (if different from where you worked)": (
                data.company_name
            ),
            "Company Mailing Address City": data.company_name,
            "Company Mailing Address State": data.company_name,
            "Company Mailing Address Zip Code": data.company_name,
            "Company Phone Number": data.company_name,
            "Company Email Address": data.company_name,
            "Is the company still in business?": "Yes",
            # Section C
            (
                "By submitting this form, I am confirming the"
                " information provided is accurate and true."
                " I am also agreeing to cooperate and"
                " communicate with my assigned investigator."
                " My name on this form constitutes my signature"
            ): "Yes",
            # Section D
            "Signature (Print or Type)": name,
            "Signature Date": str(datetime.now().strftime("%B %-d, %Y")),
        }
    )
    return fdf_fields.items()


def create_pdf(
    complaint_info: PayTransparencyComplaint,
    output_file: str = "output.pdf",
    overwrite: bool = False,
) -> None:
    if not overwrite and Path(output_file).exists():
        raise Exception(f"{output_file} already exists")
    with tempfile.TemporaryDirectory() as td:
        fdf_file = Path(td) / "form.fdf"
        filled_file = Path(td) / "filled.pdf"
        with open(fdf_file, "wb") as f:
            f.write(forge_fdf("", complaint_to_fdf(complaint_info)))
        _run(
            "pdftk",
            str(form_path()),
            "fill_form",
            str(fdf_file),
            "output",
            str(filled_file),
            "flatten",
        )
        _run(
            "pdftk",
            str(filled_file),
            *complaint_info.evidence_files,
            "cat",
            "output",
            output_file,
        )

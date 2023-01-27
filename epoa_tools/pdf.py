import datetime
import subprocess
import tempfile
from importlib import resources
from pathlib import Path

from fdfgen import forge_fdf

FORM_FILE = "F700-200-000.pdf"


FDF_FIELDS = {
    # Section A
    "Name (As it appears on your ID - First Middle Last Name)": "Anonymous",
    "Preferred Language": "English",
    "Mailing Address": "N/A",
    "Mailing Address City": "N/A",
    "Mailing Address State": "N/A",
    "Mailing Address Zip Code": "N/A",
    "Phone Number": "N/A",
    "Email Address": "example@example.com",
    "Starting Date with this Employer": "N/A",
    "Are you still employed with the employer?": "Choice1",  # "No"
    'If "No", last date employed': "N/A",
    "Reason for Leaving": "Don't Know/Other",
    "Reason for Leaving: Don't Know/Other Specified": "N/A",
    "What kind of work do you do?": "Identify violations of RCW 49.58.110",
    (
        "Not providing wage or salary range, benefits, and other"
        " compensation on a job posting"
    ): "Yes",
    # Section B
    "Is the company still in business?": "Yes",
    # Section C
    (
        "By submitting this form, I am confirming the information provided"
        " is accurate and true. I am also agreeing to cooperate and"
        " communicate with my assigned investigator."
        " My name on this form constitutes my signature"
    ): "Yes",
    # Section D
    "Signature (Print or Type)": "John Q. Public",
    "Signature Date": str(datetime.datetime.now().strftime("%B %-d, %Y")),
}


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


def fill_pdf() -> None:
    with tempfile.TemporaryDirectory() as td:
        fdf_file = Path(td) / "form.fdf"
        with open(fdf_file, "wb") as f:
            f.write(forge_fdf("", FDF_FIELDS.items()))
        cmd = [
            "pdftk",
            str(form_path()),
            "fill_form",
            str(fdf_file),
            "output",
            "output.pdf",
            "flatten",
        ]
        print("+ " + " ".join(cmd))
        subprocess.call(cmd)

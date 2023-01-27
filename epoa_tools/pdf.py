import subprocess
import sys
import tempfile
from datetime import datetime
from importlib import resources
from pathlib import Path
from typing import Dict, Iterable, Tuple

from fdfgen import forge_fdf
from reportlab.lib.pagesizes import LETTER  # type: ignore
from reportlab.lib.styles import getSampleStyleSheet  # type: ignore
from reportlab.lib.units import cm  # type: ignore
from reportlab.platypus import Paragraph, SimpleDocTemplate  # type: ignore

from .models import PayTransparencyComplaint
from .redactor import redact

FORM_FILE = "F700-200-000.pdf"


def _run(*cmd: str) -> None:
    print("+ " + " ".join(cmd), file=sys.stderr)
    subprocess.call(cmd)


class ComplaintForm:
    def __init__(self, complaint_data: PayTransparencyComplaint):
        self.data = complaint_data

    def pdf(self, output_file: str, overwrite: bool = False) -> None:
        if not overwrite and Path(output_file).exists():
            raise Exception(f"{output_file} already exists")
        with tempfile.TemporaryDirectory() as td:
            fdf_file = Path(td) / "form-data.fdf"
            filled_file = Path(td) / "form-filled.pdf"
            additional_info_file = Path(td) / "additional_info.pdf"
            with open(fdf_file, "wb") as f:
                f.write(forge_fdf("", self._complaint_data_to_form_data()))
            _run(
                "pdftk",
                str(self._complaint_form()),
                "fill_form",
                str(fdf_file),
                "output",
                str(filled_file),
                "flatten",
            )
            self._create_additional_info_pdf(additional_info_file)
            evidence_files = self._redact_evidence_files()
            concat_files = (
                file_name
                for file_name in (
                    str(filled_file),
                    str(additional_info_file),
                    *evidence_files,
                )
                if Path(file_name).exists()
            )
            _run("pdftk", *concat_files, "cat", "output", output_file)

    def _complaint_form(self) -> Path:
        package = "epoa_tools.data"
        try:
            with resources.as_file(  # type: ignore
                resources.files(package).joinpath(FORM_FILE)  # type: ignore
            ) as path:
                return path  # type: ignore
        except AttributeError:
            with resources.path(package, FORM_FILE) as path:
                return path

    def _complaint_data_to_form_data(
        self,
    ) -> Iterable[Tuple[str, str]]:
        data = self.data
        name = data.my_info.name or "Anonymous"

        fdf_fields: Dict[str, str] = {}
        fdf_fields.update(
            {
                # Section A
                (
                    "Name (As it appears on your ID"
                    " - First Middle Last Name)"
                ): name,
                "Preferred Language": "English",
            }
        )
        if data.my_info.address:
            fdf_fields.update(
                {
                    "Mailing Address": data.my_info.address.street,
                    "Mailing Address City": data.my_info.address.city,
                    "Mailing Address State": data.my_info.address.state,
                    "Mailing Address Zip Code": str(
                        data.my_info.address.zip_code
                    ),
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
                (
                    "Company Mailing Address"
                    " (if different from where you worked)"
                ): data.company_name,
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

    def _create_additional_info_pdf(self, additional_info_file: Path) -> None:
        def _text(text: str) -> str:
            return text.replace("\n", "<br />")

        if not self.data.additional_information:
            return

        doc = SimpleDocTemplate(
            str(additional_info_file),
            pagesize=LETTER,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )
        doc.build(
            [
                Paragraph(
                    _text("Additional complaint information\n\n"),
                    getSampleStyleSheet()["Heading1"],
                ),
                Paragraph(
                    _text(self.data.additional_information),
                    getSampleStyleSheet()["Normal"],
                ),
            ]
        )

    def _redact_evidence_files(self) -> Iterable[str]:
        redacted_evidence_files = []
        for i, evidence_file in enumerate(self.data.evidence_files):
            redacted_file = f"evidence-{i}.pdf"
            redact(evidence_file, redacted_file)
            redacted_evidence_files.append(redacted_file)
        return redacted_evidence_files

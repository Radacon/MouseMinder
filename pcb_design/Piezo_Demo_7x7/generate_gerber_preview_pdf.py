from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "tmp" / "pdfs" / "gerber_layers_raw.pdf" / "Piezo_Demo_7x7.pdf"
DRILL = ROOT / "tmp" / "pdfs" / "Piezo_Demo_7x7-drl_map.pdf"
OUTPUT = ROOT / "output" / "pdf" / "Piezo_Demo_7x7_Gerber_Preview.pdf"

LAYERS = [
    "Front copper (F.Cu)",
    "Back copper (B.Cu)",
    "Front solder mask (F.Mask)",
    "Back solder mask (B.Mask)",
    "Front silkscreen (F.Silkscreen)",
    "Back silkscreen (B.Silkscreen) - manufacturing view",
    "Board outline (Edge.Cuts)",
    "Drill map",
]


def cover_page() -> PdfReader:
    buf = BytesIO()
    width, height = landscape(A4)
    c = canvas.Canvas(buf, pagesize=(width, height))
    navy = HexColor("#172A46")
    blue = HexColor("#2474C6")
    gray = HexColor("#536171")

    c.setFillColor(navy)
    c.rect(0, height - 115, width, 115, stroke=0, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 29)
    c.drawString(44, height - 63, "Piezo Demo 7x7")
    c.setFont("Helvetica", 14)
    c.drawString(45, height - 88, "Gerber fabrication preview")

    c.setFillColor(blue)
    c.roundRect(44, height - 175, 240, 34, 7, stroke=0, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(164, height - 163, "224 x 224 mm  |  2-layer FR-4")

    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(44, height - 220, "Included views")
    c.setFont("Helvetica", 11)
    y = height - 247
    for index, label in enumerate(LAYERS, start=1):
        c.setFillColor(blue)
        c.circle(52, y + 3, 8, stroke=0, fill=1)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(52, y, str(index))
        c.setFillColor(gray)
        c.setFont("Helvetica", 11)
        c.drawString(70, y, label)
        y -= 28

    c.setFillColor(HexColor("#F2F5F8"))
    c.roundRect(420, 145, 365, 180, 10, stroke=0, fill=1)
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(445, 290, "Preview notes")
    c.setFillColor(gray)
    c.setFont("Helvetica", 10.5)
    notes = [
        "Bottom layers use native fabrication orientation.",
        "Drill shapes are shown at their plotted sizes.",
        "Use the Gerber ZIP for manufacture, not this PDF.",
        "Generated October 22, 2026.",
    ]
    note_y = 260
    for note in notes:
        c.drawString(445, note_y, "- " + note)
        note_y -= 28

    c.setFillColor(gray)
    c.setFont("Helvetica", 9)
    c.drawString(44, 28, "Piezo_Demo_7x7 - fabrication review document")
    c.drawRightString(width - 44, 28, "Page 1 of 9")
    c.save()
    buf.seek(0)
    return PdfReader(buf)


def footer_overlay(width: float, height: float, label: str, page_number: int) -> PdfReader:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=(width, height))
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, width, 24, stroke=0, fill=1)
    c.setStrokeColor(HexColor("#CFD7E1"))
    c.line(28, 24, width - 28, 24)
    c.setFillColor(HexColor("#172A46"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(30, 8, label)
    c.setFont("Helvetica", 8)
    c.drawRightString(width - 30, 8, f"Page {page_number} of 9")
    c.save()
    buf.seek(0)
    return PdfReader(buf)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    writer.add_page(cover_page().pages[0])

    source_pages = list(PdfReader(RAW).pages) + list(PdfReader(DRILL).pages)
    if len(source_pages) != len(LAYERS):
        raise RuntimeError(f"Expected {len(LAYERS)} fabrication pages, found {len(source_pages)}")

    for page_number, (page, label) in enumerate(zip(source_pages, LAYERS), start=2):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        page.merge_page(footer_overlay(width, height, label, page_number).pages[0])
        writer.add_page(page)

    writer.add_metadata(
        {
            "/Title": "Piezo Demo 7x7 Gerber Preview",
            "/Author": "KiCad fabrication export",
            "/Subject": "Visual preview of PCB fabrication layers and drill map",
        }
    )
    with OUTPUT.open("wb") as output_file:
        writer.write(output_file)


if __name__ == "__main__":
    main()

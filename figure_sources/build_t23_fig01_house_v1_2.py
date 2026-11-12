#!/usr/bin/env python3
"""T23 Figure 1: readable house-style conceptual information-flow diagram.

Standalone vector Figure 1 (480x95 pt) used in the revised 15-page T23 SSRN paper.
This is a conceptual diagram; no numerical model, data, or portfolio calculation changes.
The single-line tiny in-graphic note is intentionally removed: its claim is
already represented in the unchanged formal Figure 1 manuscript caption.
Requires reportlab and the authorized Liberation Serif regular/bold TTF.
"""
import argparse
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

W, H = 480, 95


def generate(path: Path, font_dir: Path):
    normal = font_dir / "LiberationSerif-Regular.ttf"
    bold = font_dir / "LiberationSerif-Bold.ttf"
    if not normal.is_file() or not bold.is_file():
        raise RuntimeError("Required embedded Liberation Serif fonts missing")
    pdfmetrics.registerFont(TTFont("T23HouseRegular", str(normal)))
    pdfmetrics.registerFont(TTFont("T23HouseBold", str(bold)))
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=(W, H), pageCompression=1)
    dark = HexColor("#26394D")
    edge = HexColor("#9CA9B7")
    light = HexColor("#F5F7F9")
    blue = HexColor("#3D5F81")

    def label(x, y, text, size=8.2):
        c.setFillColor(dark)
        c.setFont("T23HouseBold", size)
        c.drawString(x, y, text)

    def node(x, y, width, rows, size=8):
        c.setStrokeColor(edge)
        c.setFillColor(light)
        c.roundRect(x, y, width, 29, 3, stroke=1, fill=1)
        c.setFillColor(dark)
        c.setFont("T23HouseRegular", size)
        for i, line in enumerate(rows):
            c.drawCentredString(x + width / 2, y + 19.2 - i * 9.4, line)

    def arrow(x1, y1, x2, y2):
        c.setStrokeColor(blue)
        c.setLineWidth(.85)
        c.line(x1, y1, x2, y2)
        c.setFillColor(blue)
        p = c.beginPath()
        if y1 == y2:
            p.moveTo(x2, y2)
            p.lineTo(x2 - 4, y2 + 2)
            p.lineTo(x2 - 4, y2 - 2)
        else:
            p.moveTo(x2, y2)
            p.lineTo(x2 - 2, y2 - 4)
            p.lineTo(x2 + 2, y2 - 4)
        p.close()
        c.drawPath(p, stroke=0, fill=1)

    label(2, 69, "Price-information")
    label(2, 60, "baseline")
    label(2, 30, "Added macro")
    label(2, 21, "information")

    price = [
        (97, 65, ["Own-asset", "price history"]),
        (172, 65, ["Price-history", "features"]),
        (247, 65, ["Forecasting", "model"]),
        (322, 65, ["Cross-asset", "ranking"]),
        (397, 81, ["Top-N equal-weight", "portfolio"]),
    ]
    for x, width, rows in price:
        node(x, 57, width, rows, 7.7 if x == 397 else 7.95)
    for i in range(4):
        x, width, _ = price[i]
        arrow(x + width + 1, 71.5, price[i + 1][0] - 3, 71.5)

    macro = [
        (97, 65, ["Historical-vintage", "FRED-MD data"]),
        (172, 65, ["Lagged macro", "information"]),
        (247, 65, ["Macro", "representation"]),
    ]
    for x, width, rows in macro:
        node(x, 9, width, rows, 7.55 if x == 97 else 8.0)
    for i in range(2):
        x, width, _ = macro[i]
        arrow(x + width + 1, 23.5, macro[i + 1][0] - 3, 23.5)
    arrow(279.5, 39, 279.5, 54)
    c.showPage()
    c.save()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output_pdf", type=Path)
    ap.add_argument("--font-dir", type=Path, required=True)
    args = ap.parse_args()
    generate(args.output_pdf, args.font_dir)


if __name__ == "__main__":
    main()

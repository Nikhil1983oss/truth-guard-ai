from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

import os


def generate_report(
    output_path,
    filename,
    media_type,
    analysis
):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1d5fa7"),
        spaceAfter=10
    )

    heading_style = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading2"],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1d5fa7"),
        spaceBefore=14,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#26364a")
    )

    small_style = ParagraphStyle(
        "SmallCustom",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#607086")
    )

    story = []


    # ========================================================
    # HEADER
    # ========================================================

    story.append(
        Paragraph(
            "TruthGuard AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Digital Trust & Forensic Analysis Report",
            heading_style
        )
    )

    story.append(
        Spacer(1, 5)
    )


    # ========================================================
    # FILE INFORMATION
    # ========================================================

    story.append(
        Paragraph(
            "File Information",
            heading_style
        )
    )

    file_data = [
        ["Filename", filename],
        ["Media Type", media_type or "Unknown"],
    ]

    file_table = Table(
        file_data,
        colWidths=[45 * mm, 125 * mm]
    )

    file_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#eaf2fb")
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#c8d5e4")
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica"
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
        ])
    )

    story.append(file_table)

    story.append(
        Spacer(1, 12)
    )


    # ========================================================
    # AI ASSESSMENT
    # ========================================================

    story.append(
        Paragraph(
            "AI Assessment",
            heading_style
        )
    )

    verdict = analysis.get(
        "verdict",
        "UNKNOWN"
    )

    fake_score = analysis.get(
        "fake_score",
        0
    )

    real_score = analysis.get(
        "real_score",
        0
    )

    risk_score = analysis.get(
        "risk_score",
        0
    )

    risk_level = analysis.get(
        "risk_level",
        "UNKNOWN"
    )

    assessment_data = [
        ["AI Verdict", verdict],
        ["Manipulation Probability", f"{fake_score}%"],
        ["Authentic Probability", f"{real_score}%"],
        ["Overall Risk Score", str(risk_score)],
        ["Risk Level", risk_level],
    ]

    assessment_table = Table(
        assessment_data,
        colWidths=[65 * mm, 105 * mm]
    )

    assessment_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#eaf2fb")
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#c8d5e4")
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
        ])
    )

    story.append(
        assessment_table
    )


    # ========================================================
    # FORENSICS
    # ========================================================

    forensics = analysis.get(
        "forensics",
        {}
    )

    story.append(
        Paragraph(
            "Digital Forensics",
            heading_style
        )
    )


    # --------------------------------------------------------
    # METADATA
    # --------------------------------------------------------

    metadata = forensics.get(
        "metadata",
        {}
    )

    metadata_risk = metadata.get(
        "metadata_risk",
        0
    )

    metadata_findings = metadata.get(
        "findings",
        []
    )


    # --------------------------------------------------------
    # COMPRESSION
    # --------------------------------------------------------

    compression = forensics.get(
        "compression",
        {}
    )

    compression_risk = compression.get(
        "compression_risk",
        0
    )

    compression_findings = compression.get(
        "findings",
        []
    )


    # --------------------------------------------------------
    # ARTIFACTS
    # --------------------------------------------------------

    artifacts = forensics.get(
        "artifacts",
        {}
    )

    artifact_risk = artifacts.get(
        "artifact_risk",
        0
    )

    artifact_findings = artifacts.get(
        "findings",
        []
    )


    # --------------------------------------------------------
    # ELA
    # --------------------------------------------------------

    ela = forensics.get(
        "ela",
        {}
    )

    ela_risk = ela.get(
        "ela_risk",
        0
    )

    ela_mean = ela.get(
        "ela_mean",
        0
    )

    ela_max = ela.get(
        "ela_max",
        0
    )

    ela_finding = ela.get(
        "finding",
        "ELA unavailable"
    )

    forensic_data = [
        ["Signal", "Risk", "Finding"],

        [
            "Metadata",
            f"{metadata_risk}%",
            "; ".join(metadata_findings)
        ],

        [
            "Compression",
            f"{compression_risk}%",
            "; ".join(compression_findings)
        ],

        [
            "Image Artifacts",
            f"{artifact_risk}%",
            "; ".join(artifact_findings)
        ],

        [
            "ELA",
            f"{ela_risk}%",
            ela_finding
        ],
    ]

    forensic_table = Table(
        forensic_data,
        colWidths=[
            40 * mm,
            25 * mm,
            105 * mm
        ],
        repeatRows=1
    )

    forensic_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1d5fa7")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#c8d5e4")
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
        ])
    )

    story.append(
        forensic_table
    )


    # ========================================================
    # ELA STATISTICS
    # ========================================================

    story.append(
        Paragraph(
            "ELA Statistics",
            heading_style
        )
    )

    ela_stats = [
        ["Mean Intensity", str(ela_mean)],
        ["Maximum Intensity", str(ela_max)],
        ["ELA Risk", f"{ela_risk}%"],
        ["Finding", ela_finding],
    ]

    ela_table = Table(
        ela_stats,
        colWidths=[
            55 * mm,
            115 * mm
        ]
    )

    ela_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#eaf2fb")
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#c8d5e4")
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
        ])
    )

    story.append(
        ela_table
    )


    # ========================================================
    # ELA IMAGE
    # ========================================================

    ela_image = ela.get(
        "ela_image"
    )

    if ela_image and os.path.exists(
        ela_image
    ):

        story.append(
            Paragraph(
                "ELA Visual Evidence",
                heading_style
            )
        )

        story.append(
            Image(
                ela_image,
                width=160 * mm,
                height=100 * mm,
                kind="proportional"
            )
        )

        story.append(
            Spacer(1, 8)
        )

        story.append(
            Paragraph(
                "The ELA image highlights differences "
                "between the original JPEG and a "
                "recompressed version. ELA is a forensic "
                "clue and does not independently prove "
                "image manipulation.",
                small_style
            )
        )


    # ========================================================
    # AI MODEL
    # ========================================================

    model_name = analysis.get(
        "model",
        "TruthGuard AI Detector"
    )

    story.append(
        Paragraph(
            "AI Model",
            heading_style
        )
    )

    story.append(
        Paragraph(
            model_name,
            normal_style
        )
    )

    story.append(
        Spacer(1, 15)
    )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    story.append(
        Paragraph(
            "<b>Important:</b> TruthGuard AI provides "
            "automated risk assessment and forensic clues. "
            "Results should be treated as supporting evidence "
            "rather than absolute proof of authenticity or "
            "manipulation.",
            small_style
        )
    )


    # ========================================================
    # BUILD PDF
    # ========================================================

    doc.build(story)

    return output_path
from PIL import Image, ExifTags
import os


def analyze_metadata(image_path: str):
    """
    Analyze image metadata for forensic signals.

    Returns a metadata risk score from 0-100.
    This is a heuristic signal, not proof of manipulation.
    """

    risk_score = 0
    findings = []

    try:
        image = Image.open(image_path)

        # --------------------------------------
        # Basic file information
        # --------------------------------------

        file_size = os.path.getsize(image_path)

        width, height = image.size

        # --------------------------------------
        # EXIF metadata
        # --------------------------------------

        exif_data = image.getexif()

        if exif_data:
            findings.append("EXIF metadata present")

            readable_exif = {}

            for tag_id, value in exif_data.items():

                tag_name = ExifTags.TAGS.get(
                    tag_id,
                    str(tag_id)
                )

                readable_exif[tag_name] = str(value)

            # Software/editor information
            software = readable_exif.get("Software", "")

            if software:
                software_lower = software.lower()

                findings.append(
                    f"Software metadata: {software}"
                )

                editing_tools = [
                    "photoshop",
                    "gimp",
                    "adobe",
                    "lightroom",
                    "canva",
                    "pixlr",
                    "paint.net"
                ]

                if any(
                    tool in software_lower
                    for tool in editing_tools
                ):
                    risk_score += 35
                    findings.append(
                        "Image editing software detected in metadata"
                    )

        else:
            findings.append("No EXIF metadata found")

            # Missing metadata alone is NOT evidence of a fake.
            risk_score += 5

        # --------------------------------------
        # Very small files
        # --------------------------------------

        if file_size < 10_000:
            risk_score += 10
            findings.append(
                "Unusually small image file"
            )

        # --------------------------------------
        # Very unusual dimensions
        # --------------------------------------

        if width < 100 or height < 100:
            risk_score += 5
            findings.append(
                "Very low image resolution"
            )

        # --------------------------------------
        # Keep score within 0-100
        # --------------------------------------

        risk_score = min(risk_score, 100)

        return {
            "metadata_risk": risk_score,
            "file_size_bytes": file_size,
            "width": width,
            "height": height,
            "has_exif": bool(exif_data),
            "findings": findings
        }

    except Exception as e:

        return {
            "metadata_risk": 0,
            "file_size_bytes": 0,
            "width": 0,
            "height": 0,
            "has_exif": False,
            "findings": [
                f"Metadata analysis error: {str(e)}"
            ]
        }
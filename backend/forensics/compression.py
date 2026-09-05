from PIL import Image
import os


def analyze_compression(image_path: str):
    """
    Analyze basic image compression characteristics.

    This produces a heuristic compression risk signal.
    It does NOT prove that an image is manipulated.
    """

    risk_score = 0
    findings = []

    try:

        image = Image.open(image_path)

        file_size = os.path.getsize(image_path)

        width, height = image.size

        pixel_count = width * height

        # --------------------------------------
        # File size per pixel
        # --------------------------------------

        if pixel_count > 0:

            bytes_per_pixel = file_size / pixel_count

        else:

            bytes_per_pixel = 0

        # --------------------------------------
        # JPEG analysis
        # --------------------------------------

        if image.format == "JPEG":

            findings.append("JPEG compression detected")

            # Pillow exposes JPEG quantization tables
            quantization = getattr(
                image,
                "quantization",
                None
            )

            if quantization:

                tables = list(
                    quantization.values()
                )

                average_quantization = sum(
                    sum(table) / len(table)
                    for table in tables
                ) / len(tables)

                if average_quantization > 120:

                    risk_score += 20

                    findings.append(
                        "Strong JPEG compression detected"
                    )

                elif average_quantization > 80:

                    risk_score += 10

                    findings.append(
                        "Moderate JPEG compression detected"
                    )

        else:

            findings.append(
                f"Image format: {image.format}"
            )

        # --------------------------------------
        # Very low bytes-per-pixel
        # --------------------------------------

        if bytes_per_pixel < 0.10:

            risk_score += 15

            findings.append(
                "Very high compression relative to image dimensions"
            )

        # --------------------------------------
        # Limit score
        # --------------------------------------

        risk_score = min(risk_score, 100)

        return {
            "compression_risk": risk_score,
            "format": image.format,
            "bytes_per_pixel": round(
                bytes_per_pixel,
                4
            ),
            "findings": findings
        }

    except Exception as e:

        return {
            "compression_risk": 0,
            "format": None,
            "bytes_per_pixel": 0,
            "findings": [
                f"Compression analysis error: {str(e)}"
            ]
        }
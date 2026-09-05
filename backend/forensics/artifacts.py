from PIL import Image, ImageStat, ImageFilter


def analyze_artifacts(image_path: str):
    """
    Analyze simple image-level visual artifacts.

    This is a heuristic forensic signal.
    It is not a standalone deepfake detector.
    """

    risk_score = 0
    findings = []

    try:

        image = Image.open(image_path).convert("RGB")

        # --------------------------------------
        # Image statistics
        # --------------------------------------

        statistics = ImageStat.Stat(image)

        mean_brightness = sum(
            statistics.mean
        ) / 3

        stddev = sum(
            statistics.stddev
        ) / 3

        # --------------------------------------
        # Extremely low variation
        # --------------------------------------

        if stddev < 10:

            risk_score += 10

            findings.append(
                "Very low image texture variation"
            )

        # --------------------------------------
        # Extremely high variation
        # --------------------------------------

        elif stddev > 100:

            risk_score += 5

            findings.append(
                "High pixel variation detected"
            )

        # --------------------------------------
        # Edge analysis
        # --------------------------------------

        grayscale = image.convert("L")

        edges = grayscale.filter(
            ImageFilter.FIND_EDGES
        )

        edge_statistics = ImageStat.Stat(edges)

        edge_mean = edge_statistics.mean[0]

        if edge_mean < 2:

            risk_score += 10

            findings.append(
                "Very low edge detail"
            )

        elif edge_mean > 50:

            risk_score += 5

            findings.append(
                "High edge activity detected"
            )

        # --------------------------------------
        # Final score
        # --------------------------------------

        risk_score = min(
            risk_score,
            100
        )

        if not findings:

            findings.append(
                "No strong basic artifact indicators detected"
            )

        return {
            "artifact_risk": risk_score,
            "mean_brightness": round(
                mean_brightness,
                2
            ),
            "pixel_stddev": round(
                stddev,
                2
            ),
            "edge_mean": round(
                edge_mean,
                2
            ),
            "findings": findings
        }

    except Exception as e:

        return {
            "artifact_risk": 0,
            "mean_brightness": 0,
            "pixel_stddev": 0,
            "edge_mean": 0,
            "findings": [
                f"Artifact analysis error: {str(e)}"
            ]
        }
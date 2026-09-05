def calculate_risk(
    fake_score,
    metadata_risk=0,
    compression_risk=0,
    artifact_risk=0,
    ela_risk=0
):
    """
    Calculate TruthGuard overall risk score.

    These weights are prototype heuristics and are
    not calibrated accuracy measurements.
    """

    # --------------------------------------
    # Signal weights
    # --------------------------------------

    ai_weight = 0.60
    metadata_weight = 0.10
    compression_weight = 0.10
    artifact_weight = 0.10
    ela_weight = 0.10

    # --------------------------------------
    # Weighted risk calculation
    # --------------------------------------

    risk_score = (
        fake_score * ai_weight
        + metadata_risk * metadata_weight
        + compression_risk * compression_weight
        + artifact_risk * artifact_weight
        + ela_risk * ela_weight
    )

    risk_score = round(
        risk_score,
        2
    )

    # --------------------------------------
    # Risk level
    # --------------------------------------

    if risk_score < 30:

        risk_level = "LOW"

    elif risk_score < 65:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level
    }
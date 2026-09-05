import cv2
import os
import tempfile

from detectors.image_detector import analyze_image


def analyze_video(video_path: str, max_frames: int = 12):
    """
    Prototype video deepfake analysis.

    The existing image deepfake model is applied to sampled
    video frames. This is not a dedicated video-trained model.
    """

    capture = cv2.VideoCapture(video_path)

    if not capture.isOpened():
        raise ValueError("Unable to open video file")

    fps = capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps <= 0:
        fps = 30

    duration = frame_count / fps if frame_count > 0 else 0

    # Sample approximately max_frames frames
    if frame_count > 0:
        interval = max(
            1,
            frame_count // max_frames
        )
    else:
        interval = 1

    results = []

    frame_index = 0
    analyzed_count = 0

    temp_directory = tempfile.mkdtemp(
        prefix="truthguard_video_"
    )

    try:

        while True:

            success, frame = capture.read()

            if not success:
                break

            if frame_index % interval == 0:

                timestamp = frame_index / fps

                frame_path = os.path.join(
                    temp_directory,
                    f"frame_{frame_index}.jpg"
                )

                cv2.imwrite(
                    frame_path,
                    frame
                )

                try:

                    result = analyze_image(
                        frame_path
                    )

                    fake_score = result["fake_score"]
                    real_score = result["real_score"]

                    results.append({
                        "frame": analyzed_count + 1,
                        "frame_index": frame_index,
                        "timestamp": round(timestamp, 2),
                        "fake_score": fake_score,
                        "real_score": real_score,
                        "verdict": result["verdict"]
                    })

                    analyzed_count += 1

                except Exception as e:

                    results.append({
                        "frame": analyzed_count + 1,
                        "frame_index": frame_index,
                        "timestamp": round(timestamp, 2),
                        "fake_score": 0,
                        "real_score": 0,
                        "verdict": "ANALYSIS_ERROR",
                        "error": str(e)
                    })

                if analyzed_count >= max_frames:
                    break

            frame_index += 1

    finally:
        capture.release()

    valid_results = [
        item
        for item in results
        if item["verdict"] != "ANALYSIS_ERROR"
    ]

    if not valid_results:
        raise ValueError(
            "No video frames could be analyzed"
        )

    fake_scores = [
        item["fake_score"]
        for item in valid_results
    ]

    real_scores = [
        item["real_score"]
        for item in valid_results
    ]

    average_fake = sum(fake_scores) / len(fake_scores)
    average_real = sum(real_scores) / len(real_scores)

    suspicious_frames = [
        item
        for item in valid_results
        if item["fake_score"] >= 65
    ]

    # Video-level heuristic risk
    risk_score = round(
        average_fake * 0.70
        + (
            len(suspicious_frames)
            / len(valid_results)
        ) * 30,
        2
    )

    if risk_score < 30:
        risk_level = "LOW"

    elif risk_score < 65:
        risk_level = "MEDIUM"

    else:
        risk_level = "HIGH"

    if average_fake >= average_real:
        verdict = "LIKELY_MANIPULATED"
    else:
        verdict = "LIKELY_AUTHENTIC"

    return {
        "verdict": verdict,

        "fake_score": round(
            average_fake,
            2
        ),

        "real_score": round(
            average_real,
            2
        ),

        "risk_score": risk_score,

        "risk_level": risk_level,

        "video_info": {
            "fps": round(fps, 2),
            "frame_count": frame_count,
            "duration_seconds": round(
                duration,
                2
            ),
            "frames_analyzed": len(
                valid_results
            )
        },

        "suspicious_frames": suspicious_frames,

        "frame_results": results,

        "model": (
            "prithivMLmods/"
            "deepfake-detector-model-v1 "
            "(frame-level analysis)"
        )
    }
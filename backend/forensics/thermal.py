import cv2
import os
import numpy as np


def analyze_thermal(image_path: str):

    try:

        # ---------------------------------------------------------
        # READ IMAGE
        # ---------------------------------------------------------

        img = cv2.imread(
            image_path
        )


        if img is None:

            return {
                "thermal_score": 0,
                "thermal_mean_intensity": 0,
                "thermal_finding": (
                    "Unable to read image"
                ),
                "thermal_image": None
            }


        # ---------------------------------------------------------
        # CONVERT TO GRAYSCALE
        # ---------------------------------------------------------

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )


        # ---------------------------------------------------------
        # CREATE PSEUDOCOLOR HEATMAP
        # ---------------------------------------------------------

        thermal = cv2.applyColorMap(
            gray,
            cv2.COLORMAP_JET
        )


        # ---------------------------------------------------------
        # CREATE OUTPUT DIRECTORY
        # ---------------------------------------------------------

        thermal_dir = os.path.join(
            os.path.dirname(image_path),
            "thermal"
        )

        os.makedirs(
            thermal_dir,
            exist_ok=True
        )


        # ---------------------------------------------------------
        # OUTPUT FILE
        # ---------------------------------------------------------

        basename = os.path.splitext(
            os.path.basename(image_path)
        )[0]


        thermal_filename = (
            f"{basename}_thermal.jpg"
        )


        thermal_path = os.path.join(
            thermal_dir,
            thermal_filename
        )


        # ---------------------------------------------------------
        # SAVE IMAGE
        # ---------------------------------------------------------

        success = cv2.imwrite(
            thermal_path,
            thermal
        )


        if not success:

            return {
                "thermal_score": 0,
                "thermal_mean_intensity": 0,
                "thermal_finding": (
                    "Unable to save heatmap"
                ),
                "thermal_image": None
            }


        # ---------------------------------------------------------
        # IMAGE INTENSITY
        # ---------------------------------------------------------

        mean_intensity = float(
            np.mean(gray)
        )


        # ---------------------------------------------------------
        # HEURISTIC SCORE
        # ---------------------------------------------------------

        if mean_intensity < 30:

            score = 10

            finding = (
                "Very dark regions detected"
            )

        elif mean_intensity < 80:

            score = 20

            finding = (
                "Unusual intensity distribution detected"
            )

        elif mean_intensity < 150:

            score = 30

            finding = (
                "Moderate intensity variation detected"
            )

        else:

            score = 0

            finding = (
                "No major intensity anomaly detected"
            )


        # ---------------------------------------------------------
        # RETURN
        # ---------------------------------------------------------

        return {

            "thermal_score": score,

            "thermal_mean_intensity": round(
                mean_intensity,
                2
            ),

            "thermal_finding": finding,

            "thermal_image": (
                f"/uploads/thermal/{thermal_filename}"
            )
        }


    except Exception as e:

        return {

            "thermal_score": 0,

            "thermal_mean_intensity": 0,

            "thermal_finding": (
                f"Heatmap analysis error: {str(e)}"
            ),

            "thermal_image": None
        }
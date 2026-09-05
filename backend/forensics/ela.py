from PIL import Image, ImageChops, ImageEnhance
import os


def analyze_ela(image_path: str):

    temp_path = None

    try:

        # ---------------------------------------------------------
        # OPEN ORIGINAL IMAGE
        # ---------------------------------------------------------

        original = Image.open(image_path)

        original_format = original.format

        image = original.convert("RGB")


        # ---------------------------------------------------------
        # ELA WORKS BEST WITH JPEG
        # ---------------------------------------------------------

        if original_format not in ("JPEG", "JPG"):

            return {
                "ela_risk": 0,
                "ela_mean": 0,
                "ela_max": 0,
                "finding": (
                    "ELA works best with JPEG images. "
                    f"Detected format: {original_format}"
                ),
                "ela_image": None
            }


        # ---------------------------------------------------------
        # RECOMPRESS IMAGE
        # ---------------------------------------------------------

        temp_path = image_path + ".temp.jpg"

        image.save(
            temp_path,
            "JPEG",
            quality=90
        )


        # ---------------------------------------------------------
        # LOAD RECOMPRESSED IMAGE
        # ---------------------------------------------------------

        recompressed = Image.open(
            temp_path
        ).convert("RGB")


        # ---------------------------------------------------------
        # CALCULATE DIFFERENCE
        # ---------------------------------------------------------

        difference = ImageChops.difference(
            image,
            recompressed
        )


        extrema = difference.getextrema()


        max_difference = max(
            channel[1]
            for channel in extrema
        )


        scale = 255 / max(
            max_difference,
            1
        )


        # ---------------------------------------------------------
        # ENHANCE ELA VISUALIZATION
        # ---------------------------------------------------------

        ela_image = ImageEnhance.Brightness(
            difference
        ).enhance(scale)


        # ---------------------------------------------------------
        # CALCULATE ELA STATISTICS
        # ---------------------------------------------------------

        gray = ela_image.convert("L")

        pixels = list(
            gray.getdata()
        )


        mean_value = (
            sum(pixels) / len(pixels)
            if pixels
            else 0
        )


        max_value = (
            max(pixels)
            if pixels
            else 0
        )


        # ---------------------------------------------------------
        # ELA RISK
        # ---------------------------------------------------------

        if mean_value >= 35:

            ela_risk = 35

            finding = (
                "Strong ELA variation detected"
            )

        elif mean_value >= 20:

            ela_risk = 20

            finding = (
                "Moderate ELA variation detected"
            )

        elif mean_value >= 10:

            ela_risk = 10

            finding = (
                "Low ELA variation detected"
            )

        else:

            ela_risk = 0

            finding = (
                "No strong ELA variation detected"
            )


        # ---------------------------------------------------------
        # CREATE ELA DIRECTORY
        # ---------------------------------------------------------

        ela_directory = os.path.join(
            os.path.dirname(image_path),
            "ela"
        )

        os.makedirs(
            ela_directory,
            exist_ok=True
        )


        # ---------------------------------------------------------
        # CREATE ELA IMAGE NAME
        # ---------------------------------------------------------

        base_name = os.path.splitext(
            os.path.basename(image_path)
        )[0]


        ela_filename = (
            f"{base_name}_ela.jpg"
        )


        ela_path = os.path.join(
            ela_directory,
            ela_filename
        )


        # ---------------------------------------------------------
        # SAVE ELA IMAGE
        # ---------------------------------------------------------

        ela_image.save(
            ela_path,
            "JPEG",
            quality=95
        )


        # ---------------------------------------------------------
        # DELETE TEMP FILE
        # ---------------------------------------------------------

        if os.path.exists(temp_path):

            os.remove(temp_path)

            temp_path = None


        # ---------------------------------------------------------
        # RETURN RESULT
        # ---------------------------------------------------------

        return {

            "ela_risk": ela_risk,

            "ela_mean": round(
                mean_value,
                2
            ),

            "ela_max": int(
                max_value
            ),

            "finding": finding,

            # IMPORTANT:
            # Frontend App.jsx uses this key
            "ela_image": (
                f"/uploads/ela/{ela_filename}"
            )
        }


    except Exception as e:

        # ---------------------------------------------------------
        # CLEANUP TEMP FILE
        # ---------------------------------------------------------

        if (
            temp_path
            and
            os.path.exists(temp_path)
        ):

            try:

                os.remove(
                    temp_path
                )

            except Exception:

                pass


        # ---------------------------------------------------------
        # ERROR RESPONSE
        # ---------------------------------------------------------

        return {

            "ela_risk": 0,

            "ela_mean": 0,

            "ela_max": 0,

            "finding": (
                f"ELA analysis error: {str(e)}"
            ),

            "ela_image": None
        }
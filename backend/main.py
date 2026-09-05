# ============================================================
# TRUTHGUARD AI - BACKEND
# FastAPI Backend
# ============================================================

import os
import uuid
import json
import mimetypes

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from fastapi.responses import FileResponse


# ============================================================
# DATABASE
# ============================================================

from database.database import (
    init_database,
    save_analysis,
    get_history,
    get_analysis,
    delete_analysis
)


# ============================================================
# IMAGE AI
# ============================================================

from detectors.image_detector import (
    analyze_image
)


# ============================================================
# IMAGE FORENSICS
# ============================================================

from forensics.metadata import (
    analyze_metadata
)

from forensics.compression import (
    analyze_compression
)

from forensics.artifacts import (
    analyze_artifacts
)

from forensics.ela import (
    analyze_ela
)


# ============================================================
# RISK ENGINE
# ============================================================

from fusion.risk_engine import (
    calculate_risk
)


# ============================================================
# WEBSITE SCANNER
# ============================================================

from services.website_scanner import (
    scan_website
)


# ============================================================
# PDF REPORT
# IMPORTANT:
# report_service.py contains generate_report()
# ============================================================

from services.report_service import (
    generate_report
)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="TruthGuard AI",
    description=(
        "AI-powered digital trust, "
        "deepfake detection and "
        "website threat analysis platform."
    ),
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================================
# DIRECTORIES
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads"
)


REPORT_DIR = os.path.join(
    BASE_DIR,
    "reports"
)


WEB_SCREENSHOT_DIR = os.path.join(
    REPORT_DIR,
    "web_screenshots"
)


os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


os.makedirs(
    REPORT_DIR,
    exist_ok=True
)


os.makedirs(
    WEB_SCREENSHOT_DIR,
    exist_ok=True
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/uploads",
    StaticFiles(
        directory=UPLOAD_DIR
    ),
    name="uploads"
)


app.mount(
    "/web-screenshots",
    StaticFiles(
        directory=WEB_SCREENSHOT_DIR
    ),
    name="web-screenshots"
)


# ============================================================
# TEMPORARY ANALYSIS MEMORY
# ============================================================

analysis_store = {}


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

init_database()


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "project": "TruthGuard AI",
        "status": "online",
        "message": (
            "TruthGuard AI backend "
            "is running successfully."
        )
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health():

    return {
        "status": "healthy",
        "service": "TruthGuard AI API"
    }


# ============================================================
# MEDIA TYPE DETECTION
# ============================================================

def detect_media_type(
    filename: str,
    content_type: str | None
):

    filename = (
        filename
        or ""
    ).lower()

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    image_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".bmp",
        ".gif"
    ]

    for extension in image_extensions:

        if filename.endswith(
            extension
        ):

            return "image"

    # --------------------------------------------------------
    # VIDEO
    # --------------------------------------------------------

    video_extensions = [
        ".mp4",
        ".avi",
        ".mov",
        ".mkv",
        ".webm"
    ]

    for extension in video_extensions:

        if filename.endswith(
            extension
        ):

            return "video"

    # --------------------------------------------------------
    # AUDIO
    # --------------------------------------------------------

    audio_extensions = [
        ".mp3",
        ".wav",
        ".m4a",
        ".aac",
        ".ogg",
        ".flac"
    ]

    for extension in audio_extensions:

        if filename.endswith(
            extension
        ):

            return "audio"

    # --------------------------------------------------------
    # CONTENT TYPE FALLBACK
    # --------------------------------------------------------

    if content_type:

        if content_type.startswith(
            "image/"
        ):

            return "image"

        if content_type.startswith(
            "video/"
        ):

            return "video"

        if content_type.startswith(
            "audio/"
        ):

            return "audio"

    return None


# ============================================================
# ANALYZE MEDIA
# ============================================================

@app.post("/api/analyze")
async def analyze_media(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )


    # ========================================================
    # DETECT MEDIA TYPE
    # ========================================================

    media_type = detect_media_type(
        file.filename,
        file.content_type
    )


    if media_type is None:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Upload an image, video or audio file."
            )
        )


    # ========================================================
    # GENERATE FILE ID
    # ========================================================

    file_id = str(
        uuid.uuid4()
    )


    # ========================================================
    # SAFE FILE NAME
    # ========================================================

    original_filename = os.path.basename(
        file.filename
    )


    safe_filename = (
        f"{file_id}_"
        f"{original_filename}"
    )


    file_path = os.path.join(
        UPLOAD_DIR,
        safe_filename
    )


    # ========================================================
    # SAVE FILE
    # ========================================================

    file_bytes = await file.read()


    with open(
        file_path,
        "wb"
    ) as output_file:

        output_file.write(
            file_bytes
        )


    file_size = os.path.getsize(
        file_path
    )


    # ========================================================
    # COMMON RESPONSE
    # ========================================================

    result = {

        "file_id":
            file_id,

        "filename":
            original_filename,

        "media_type":
            media_type,

        "file_size":
            file_size,

        "file_url":
            f"/uploads/{safe_filename}"
    }


    # ========================================================
    # IMAGE ANALYSIS
    # ========================================================

    if media_type == "image":

        try:

            # ------------------------------------------------
            # AI DETECTION
            # ------------------------------------------------

            ai_result = analyze_image(
                file_path
            )


            # ------------------------------------------------
            # METADATA
            # ------------------------------------------------

            try:

                metadata_result = (
                    analyze_metadata(
                        file_path
                    )
                )

            except Exception as e:

                metadata_result = {

                    "metadata_risk": 0,

                    "finding":
                        f"Metadata analysis error: {str(e)}"
                }


            # ------------------------------------------------
            # COMPRESSION
            # ------------------------------------------------

            try:

                compression_result = (
                    analyze_compression(
                        file_path
                    )
                )

            except Exception as e:

                compression_result = {

                    "compression_risk": 0,

                    "finding":
                        f"Compression analysis error: {str(e)}"
                }


            # ------------------------------------------------
            # ARTIFACTS
            # ------------------------------------------------

            try:

                artifact_result = (
                    analyze_artifacts(
                        file_path
                    )
                )

            except Exception as e:

                artifact_result = {

                    "artifact_risk": 0,

                    "finding":
                        f"Artifact analysis error: {str(e)}"
                }


            # ------------------------------------------------
            # ELA
            # ------------------------------------------------

            try:

                ela_result = analyze_ela(
                    file_path
                )

            except Exception as e:

                ela_result = {

                    "ela_risk": 0,

                    "ela_mean": 0,

                    "ela_max": 0,

                    "finding":
                        f"ELA analysis error: {str(e)}",

                    "ela_image": None
                }


            # ------------------------------------------------
            # AI FAKE SCORE
            # ------------------------------------------------

            fake_score = float(
                ai_result.get(
                    "fake_score",
                    0
                )
            )


            # ------------------------------------------------
            # FORENSIC RISKS
            # ------------------------------------------------

            metadata_risk = float(
                metadata_result.get(
                    "metadata_risk",
                    0
                )
            )


            compression_risk = float(
                compression_result.get(
                    "compression_risk",
                    0
                )
            )


            artifact_risk = float(
                artifact_result.get(
                    "artifact_risk",
                    0
                )
            )


            ela_risk = float(
                ela_result.get(
                    "ela_risk",
                    0
                )
            )


            # ------------------------------------------------
            # OVERALL RISK
            # ------------------------------------------------

            risk_result = calculate_risk(

                fake_score=fake_score,

                metadata_risk=metadata_risk,

                compression_risk=compression_risk,

                artifact_risk=artifact_risk,

                ela_risk=ela_risk
            )


            # ------------------------------------------------
            # FINAL RESULT
            # ------------------------------------------------

            result.update({

                "verdict":
                    ai_result.get(
                        "verdict",
                        "UNKNOWN"
                    ),

                "fake_score":
                    ai_result.get(
                        "fake_score",
                        0
                    ),

                "real_score":
                    ai_result.get(
                        "real_score",
                        0
                    ),

                "model":
                    ai_result.get(
                        "model",
                        "TruthGuard AI"
                    ),

                "risk_score":
                    risk_result.get(
                        "risk_score",
                        0
                    ),

                "risk_level":
                    risk_result.get(
                        "risk_level",
                        "LOW"
                    ),

                "metadata":
                    metadata_result,

                "compression":
                    compression_result,

                "artifacts":
                    artifact_result,

                "ela":
                    ela_result,

                "analysis_type":
                    "AI + Digital Forensics"
            })


        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Image analysis failed: "
                    f"{str(e)}"
                )
            )


    # ========================================================
    # VIDEO ANALYSIS
    # ========================================================

    elif media_type == "video":

        try:

            from detectors.video_detector import (
                analyze_video
            )


            video_result = analyze_video(
                file_path
            )


            result.update(
                video_result
            )


            result["analysis_type"] = (
                "Frame-level AI video analysis"
            )


        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Video analysis failed: "
                    f"{str(e)}"
                )
            )


    # ========================================================
    # AUDIO ANALYSIS
    # ========================================================

    elif media_type == "audio":

        try:

            from detectors.audio_detector import (
                analyze_audio
            )


            audio_result = analyze_audio(
                file_path
            )


            result.update(
                audio_result
            )


            result["analysis_type"] = (
                "Audio analysis"
            )


        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Audio analysis failed: "
                    f"{str(e)}"
                )
            )


    # ========================================================
    # MEMORY STORE
    # ========================================================

    analysis_store[
        file_id
    ] = result


    # ========================================================
    # SAVE IMAGE ANALYSIS TO DATABASE
    # ========================================================

    try:

        save_analysis(

            file_id,

            original_filename,

            media_type,

            result
        )

    except Exception as e:

        print(
            "Database save warning:",
            e
        )


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return result


# ============================================================
# QUICK WEBSITE URL SCANNER
# ============================================================

@app.post("/api/scan-website")
async def scan_website_url(
    payload: dict
):

    url = payload.get(
        "url"
    )


    if not url:

        raise HTTPException(
            status_code=400,
            detail="URL is required."
        )


    url = url.strip()


    if not url:

        raise HTTPException(
            status_code=400,
            detail="URL cannot be empty."
        )


    # --------------------------------------------------------
    # NORMALIZE
    # --------------------------------------------------------

    if not url.startswith(
        (
            "http://",
            "https://"
        )
    ):

        url = "https://" + url


    # --------------------------------------------------------
    # BASIC URL ANALYSIS
    # --------------------------------------------------------

    from urllib.parse import (
        urlparse
    )


    try:

        parsed = urlparse(
            url
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid URL."
        )


    hostname = (
        parsed.hostname
        or ""
    ).lower()


    # --------------------------------------------------------
    # SUSPICIOUS TERMS
    # --------------------------------------------------------

    suspicious_terms = [

        "login",
        "verify",
        "verification",
        "password",
        "account",
        "bank",
        "payment",
        "wallet",
        "crypto",
        "otp",
        "claim",
        "prize",
        "free",
        "urgent",
        "security-alert",
        "confirm"
    ]


    found_terms = []


    url_lower = url.lower()


    for term in suspicious_terms:

        if term in url_lower:

            found_terms.append(
                term
            )


    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    risk_score = 0

    findings = []


    if parsed.scheme != "https":

        risk_score += 20

        findings.append(
            "Website is not using HTTPS."
        )


    if len(
        found_terms
    ) >= 4:

        risk_score += 40

        findings.append(
            "Multiple suspicious URL keywords detected."
        )

    elif len(
        found_terms
    ) >= 2:

        risk_score += 25

        findings.append(
            "Suspicious URL keywords detected."
        )

    elif len(
        found_terms
    ) == 1:

        risk_score += 10

        findings.append(
            "Potentially sensitive URL keyword detected."
        )


    if len(hostname) > 50:

        risk_score += 10

        findings.append(
            "Unusually long domain name."
        )


    if hostname.count("-") >= 3:

        risk_score += 10

        findings.append(
            "Domain contains multiple hyphens."
        )


    risk_score = min(
        risk_score,
        100
    )


    if risk_score >= 65:

        risk_level = "HIGH"

        verdict = "SUSPICIOUS"

    elif risk_score >= 30:

        risk_level = "MEDIUM"

        verdict = "CAUTION"

    else:

        risk_level = "LOW"

        verdict = "LOW_RISK"


    return {

        "url":
            url,

        "domain":
            hostname,

        "https":
            parsed.scheme == "https",

        "risk_score":
            risk_score,

        "risk_level":
            risk_level,

        "verdict":
            verdict,

        "suspicious_terms":
            found_terms,

        "findings":
            findings,

        "scanner":
            "TruthGuard AI URL Heuristic Scanner",

        "disclaimer":
            (
                "This URL scanner uses heuristic "
                "signals. It does not guarantee that "
                "a website is safe or malicious."
            )
    }


# ============================================================
# FULL WEBSITE BROWSER SCAN
# ============================================================

@app.post("/api/full-web-scan")
async def full_web_scan(
    payload: dict
):

    url = payload.get(
        "url"
    )


    if not url:

        raise HTTPException(
            status_code=400,
            detail="URL is required."
        )


    url = url.strip()


    if not url:

        raise HTTPException(
            status_code=400,
            detail="URL cannot be empty."
        )


    if not url.startswith(
        (
            "http://",
            "https://"
        )
    ):

        url = "https://" + url


    try:

        # IMPORTANT:
        # scan_website() is async

        result = await scan_website(
            url
        )


        return result


    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


    except Exception as e:

        print(
            "FULL WEB SCAN ERROR:",
            e
        )


        raise HTTPException(
            status_code=500,
            detail=(
                "Full website scan failed: "
                f"{str(e)}"
            )
        )


# ============================================================
# HISTORY
# ============================================================

@app.get("/api/history")
def history():

    try:

        return get_history()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Could not load history: "
                f"{str(e)}"
            )
        )


# ============================================================
# GET SINGLE HISTORY ITEM
# ============================================================

@app.get("/api/history/{file_id}")
def history_item(
    file_id: str
):

    # --------------------------------------------------------
    # MEMORY FIRST
    # --------------------------------------------------------

    if file_id in analysis_store:

        return analysis_store[
            file_id
        ]


    # --------------------------------------------------------
    # DATABASE FALLBACK
    # --------------------------------------------------------

    try:

        saved = get_analysis(
            file_id
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "History lookup failed: "
                f"{str(e)}"
            )
        )


    if saved is None:

        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )


    analysis = saved.get(
        "analysis"
    )


    if analysis:

        return analysis


    return saved


# ============================================================
# DELETE HISTORY
# ============================================================

@app.delete("/api/history/{file_id}")
def delete_history(
    file_id: str
):

    try:

        deleted = delete_analysis(
            file_id
        )


        if deleted == 0:

            raise HTTPException(
                status_code=404,
                detail="History item not found."
            )


        analysis_store.pop(
            file_id,
            None
        )


        return {

            "success":
                True,

            "message":
                "History item deleted."
        }


    except HTTPException:

        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Could not delete history: "
                f"{str(e)}"
            )
        )


# ============================================================
# PDF FORENSIC REPORT
# ============================================================

@app.get("/api/report/{file_id}")
def generate_pdf_report(
    file_id: str
):

    # --------------------------------------------------------
    # GET ANALYSIS
    # --------------------------------------------------------

    analysis = (
        analysis_store.get(
            file_id
        )
    )


    # --------------------------------------------------------
    # DATABASE FALLBACK
    # --------------------------------------------------------

    if analysis is None:

        try:

            saved = get_analysis(
                file_id
            )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Could not retrieve "
                    "analysis: "
                    f"{str(e)}"
                )
            )


        if saved:

            analysis = saved.get(
                "analysis"
            )


            if analysis is None:

                analysis = saved


    # --------------------------------------------------------
    # NOT FOUND
    # --------------------------------------------------------

    if analysis is None:

        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )


    # --------------------------------------------------------
    # OUTPUT PATH
    # --------------------------------------------------------

    output_filename = (
        f"TruthGuard_Report_"
        f"{file_id}.pdf"
    )


    output_path = os.path.join(
        REPORT_DIR,
        output_filename
    )


    # --------------------------------------------------------
    # GENERATE REPORT
    # --------------------------------------------------------

    try:

        # Your report_service.py uses:
        # generate_report()

        generated_path = generate_report(
            analysis,
            output_path
        )


    except TypeError:

        # ----------------------------------------------------
        # Compatibility fallback
        # Some versions of report_service.py may accept
        # only analysis.
        # ----------------------------------------------------

        try:

            generated_path = generate_report(
                analysis
            )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=(
                    "PDF generation failed: "
                    f"{str(e)}"
                )
            )


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "PDF generation failed: "
                f"{str(e)}"
            )
        )


    # --------------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------------

    if not generated_path:

        generated_path = output_path


    if not os.path.exists(
        generated_path
    ):

        raise HTTPException(
            status_code=500,
            detail=(
                "PDF was not created."
            )
        )


    # --------------------------------------------------------
    # RETURN PDF
    # --------------------------------------------------------

    return FileResponse(

        generated_path,

        media_type="application/pdf",

        filename=output_filename
    )


# ============================================================
# STARTUP
# ============================================================

@app.on_event(
    "startup"
)
async def startup_event():

    print()
    print(
        "================================================"
    )
    print(
        "        TRUTHGUARD AI BACKEND"
    )
    print(
        "================================================"
    )
    print(
        "API:              http://127.0.0.1:8000"
    )
    print(
        "Docs:             http://127.0.0.1:8000/docs"
    )
    print(
        "Website Scanner:  ENABLED"
    )
    print(
        "Full Web Scan:    ENABLED"
    )
    print(
        "Image AI:         ENABLED"
    )
    print(
        "Video Analysis:   ENABLED"
    )
    print(
        "Audio Analysis:   ENABLED"
    )
    print(
        "History:          ENABLED"
    )
    print(
        "PDF Reports:      ENABLED"
    )
    print(
        "================================================"
    )
    print()
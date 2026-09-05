# 🛡️ TruthGuard AI

> AI-powered Digital Trust & Verification Platform

TruthGuard AI is a cybersecurity and digital-forensics prototype designed to help users assess whether digital media may be manipulated, AI-generated, or suspicious.

The platform combines pretrained AI models with digital forensic signals to produce an explainable assessment rather than relying on a single indicator.

## 🚀 Project Overview

The rapid growth of generative AI has made manipulated images, videos, and other digital content increasingly difficult to identify.

TruthGuard AI aims to provide a single platform where users can:

- Analyze images for possible AI-generated or manipulated content
- Analyze videos using sampled-frame analysis
- Perform basic audio analysis
- Inspect digital-forensic indicators
- Calculate an overall risk score
- Review previous analyses
- Generate forensic PDF reports
- Scan website URLs for suspicious page-level indicators

> **Important:** TruthGuard AI is a prototype decision-support system. Its results are risk indicators, not absolute proof that content is genuine or manipulated.

## ✨ Current Features

### 🖼️ Image Deepfake Detection

- Pretrained deepfake image classification model
- Fake/manipulation probability
- Authentic probability
- AI verdict
- Overall risk score
- Risk level

Current image detector:

`prithivMLmods/deepfake-detector-model-v1`

The model is used as a pretrained component. TruthGuard AI does not claim the model's published benchmark accuracy as the accuracy of the complete TruthGuard system.

### 🎬 Video Analysis

TruthGuard AI can analyze video content by:

1. Loading the video with OpenCV
2. Sampling selected frames
3. Applying the image detection model to sampled frames
4. Combining frame-level results into a video assessment

This is a prototype approach and is not a dedicated video-specific deepfake model.

### 🎧 Audio Analysis

The project includes a basic audio-analysis pipeline for uploaded audio content.

Advanced voice-cloning detection and speech-to-text verification are planned improvements.

## 🔬 Digital Forensics

TruthGuard AI supplements AI predictions with additional forensic signals.

### Metadata Analysis

Checks available file metadata and EXIF-related information.

### Compression Analysis

Examines file format and compression-related characteristics.

### Image Artifact Analysis

Looks for basic image-level artifact indicators.

### Error Level Analysis (ELA)

ELA compares an image with a JPEG-recompressed version and visualizes differences.

The system reports:

- ELA mean intensity
- ELA maximum intensity
- ELA risk indicator
- ELA heatmap

> ELA is a forensic clue and does not independently prove image manipulation.

### Visual Forensic Heatmap

The project generates a pseudocolor image-intensity heatmap.

> This is an **image-intensity visualization**, not a real thermal-camera measurement.

## 🧠 Risk Fusion

TruthGuard combines several signals into a prototype overall risk score.

| Signal | Weight |
|---|---:|
| AI manipulation score | 60% |
| Metadata | 10% |
| Compression | 10% |
| Image artifacts | 10% |
| ELA | 10% |

Risk levels:

- **LOW** — below 30
- **MEDIUM** — 30 to 64
- **HIGH** — 65 or above

These weights are prototype heuristics and are not statistically calibrated.

## 🌐 Website Threat Scanner

TruthGuard AI includes a URL/page-level website scanner that can inspect indicators such as:

- HTTPS usage
- Suspicious keywords
- Password forms
- External form actions
- External links
- Redirects
- Download links
- Suspicious JavaScript patterns
- Iframes
- Security headers
- External domains
- Basic page structure

The scanner is intended as a heuristic warning system. It does not replace a commercial malware scanner, sandbox, browser security service, or threat-intelligence platform.

## 📊 Analysis History

TruthGuard AI uses SQLite to store analysis records including:

- Filename
- Media type
- Verdict
- Fake score
- Real score
- Risk score
- Risk level
- Analysis timestamp
- Full analysis JSON

Users can view and delete previous analysis records from the application.

## 📄 Forensic PDF Reports

The backend can generate PDF reports containing:

- File information
- AI verdict
- Risk assessment
- AI probabilities
- Forensic signals
- Model information
- ELA information
- Disclaimer

# 🏗️ Technology Stack

## Frontend

- React
- JavaScript
- Vite
- Axios
- CSS

## Backend

- Python
- FastAPI
- Uvicorn
- SQLite

## AI / Machine Learning

- PyTorch
- TorchVision
- Hugging Face Transformers
- Pretrained deepfake image classification model

## Computer Vision / Forensics

- OpenCV
- Pillow
- NumPy
- ELA
- Metadata analysis
- Compression analysis
- Artifact analysis

## Reporting

- ReportLab

# 📁 Project Structure

```text
truth guard-ai/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   └── schemas/
│   ├── config/
│   ├── database/
│   │   └── database.py
│   ├── detectors/
│   │   ├── image_detector.py
│   │   ├── video_detector.py
│   │   └── audio_detector.py
│   ├── forensics/
│   │   ├── metadata.py
│   │   ├── compression.py
│   │   ├── artifacts.py
│   │   ├── ela.py
│   │   └── thermal.py
│   ├── fusion/
│   │   └── risk_engine.py
│   ├── services/
│   │   ├── report_service.py
│   │   └── website_scanner.py
│   ├── uploads/
│   ├── reports/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
├── tests/
├── sample_data/
├── docs/
├── .gitignore
└── README.md
```

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "truth guard-ai"
```

## 2. Backend Setup

```powershell
cd backend
python -m venv venv
.env\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Backend:

`http://127.0.0.1:8000`

Swagger API documentation:

`http://127.0.0.1:8000/docs`

## 3. Frontend Setup

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

`http://localhost:5173`

# 🔗 Application Architecture

```text
                 ┌──────────────────────┐
                 │      React UI        │
                 │     Vite + JS        │
                 └──────────┬───────────┘
                            │
                         REST API
                            │
                            ▼
                 ┌──────────────────────┐
                 │      FastAPI         │
                 │      Backend         │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
       AI Detection     Forensics      Web Scanner
             │              │              │
             ▼              ▼              ▼
       PyTorch / HF     Pillow/OpenCV   Requests/BS4
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                    ┌───────────────┐
                    │ Risk Fusion   │
                    └───────┬───────┘
                            ▼
                 ┌────────────────────┐
                 │ Result + Evidence  │
                 └─────────┬──────────┘
                           │
                 ┌─────────┴──────────┐
                 ▼                    ▼
              SQLite              PDF Report
```

# 🔌 Main API Endpoints

The backend currently includes API functionality for areas such as:

```text
POST /api/analyze
GET  /api/history
GET  /api/history/{file_id}
DELETE /api/history/{file_id}
GET  /api/report/{file_id}
POST /api/full-web-scan
```

The exact available endpoints depend on the current backend implementation.

# 🧪 Example Workflow

```text
Upload Image
     ↓
Preprocessing
     ↓
AI Deepfake Detection
     ↓
Metadata Analysis
     ↓
Compression Analysis
     ↓
Artifact Analysis
     ↓
ELA
     ↓
Risk Fusion
     ↓
Verdict + Evidence
     ↓
SQLite History
     ↓
PDF Report
```

# 🔐 Security Considerations

The project is intended as a prototype and should be hardened before production deployment.

Important areas include:

- File-size limits
- File-type validation
- Secure upload handling
- SSRF protection for URL scanning
- Request timeouts
- Private-network blocking
- Authentication and authorization
- Rate limiting
- Malware-safe file processing
- Secure secret management
- Production CORS configuration
- Sandboxed media processing

Never commit API keys, passwords, or `.env` files to GitHub.

# 🚧 Future Development

- [ ] Advanced video-specific deepfake detection
- [ ] Improved audio deepfake / voice-cloning detection
- [ ] OCR for text extracted from images
- [ ] Speech-to-text processing
- [ ] Claim verification
- [ ] Misinformation verification
- [ ] Evidence/source verification
- [ ] Web-source credibility analysis
- [ ] Advanced multimodal fusion
- [ ] Browser-based JavaScript website scanning
- [ ] Improved forensic visualization
- [ ] Model benchmarking on independent datasets
- [ ] User authentication
- [ ] Production deployment
- [ ] API rate limiting
- [ ] More comprehensive automated tests

# 🎯 Project Objective

The objective of TruthGuard AI is to provide an accessible platform that combines **AI detection, digital forensics, risk scoring, and explainable evidence** to help users make more informed decisions about suspicious digital content.

# ⚠️ Disclaimer

TruthGuard AI is a research/prototype project.

AI-generated-content detection and digital forensics are probabilistic fields. No individual model or forensic signal should be treated as absolute proof of authenticity or manipulation.

A TruthGuard result should be interpreted as an **assessment of available evidence**, not a definitive legal or forensic conclusion.

# 👨‍💻 Development Status

**Current status:** Active prototype development.

Implemented areas include:

- Image AI detection
- Video frame-based analysis
- Basic audio analysis
- Digital forensic signals
- ELA visualization
- Image-intensity heatmap
- Risk scoring
- SQLite history
- PDF reporting
- Quick website URL scanning

Additional verification and multimodal capabilities are under development.

---

## ⭐ TruthGuard AI

**Detect. Verify. Trust.**

Built as a cybersecurity and digital-trust project focused on combating manipulated media, suspicious digital content, and online threats.

import React, { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";


// ============================================================
// WEB STAT
// ============================================================

function WebStat({ title, value }) {
  return (
    <div className="web-stat">
      <span>{title}</span>
      <strong>{value}</strong>
    </div>
  );
}


// ============================================================
// FULL WEB SCAN RESULT
// ============================================================

function FullWebResult({ data }) {
  if (!data) return null;

  const risk = Number(data.risk_score || 0);

  let riskClass = "low";

  if (risk >= 65) {
    riskClass = "high";
  } else if (risk >= 30) {
    riskClass = "medium";
  }

  return (
    <div className="full-web-result">

      <div className="result-card-header">
        <div>
          <div className="result-label">
            FULL WEB SCAN
          </div>

          <h2>
            {data.title || "Website Analysis"}
          </h2>

          <p className="website-url-result">
            {data.final_url || data.url}
          </p>
        </div>

        <div className={`web-risk-circle ${riskClass}`}>
          <strong>{risk}</strong>
          <span>/100</span>
        </div>
      </div>


      <div className={`web-verdict ${riskClass}`}>
        {data.verdict || "SCAN COMPLETE"}
        <span>
          {data.risk_level || "UNKNOWN"} RISK
        </span>
      </div>


      {/* BASIC INFORMATION */}

      <div className="web-result-section">

        <h3>🌐 Website Information</h3>

        <div className="web-stats-grid">

          <WebStat
            title="Domain"
            value={data.domain || "N/A"}
          />

          <WebStat
            title="HTTPS"
            value={data.https ? "✓ Enabled" : "✕ Disabled"}
          />

          <WebStat
            title="Status"
            value={data.status_code || "N/A"}
          />

          <WebStat
            title="Pages"
            value={`${data.pages_scanned || 1}/${data.page_limit || 5}`}
          />

        </div>

      </div>


      {/* PAGE STRUCTURE */}

      <div className="web-result-section">

        <h3>📊 Page Structure</h3>

        <div className="web-stats-grid">

          <WebStat
            title="Forms"
            value={data.page_structure?.forms || 0}
          />

          <WebStat
            title="Password Forms"
            value={data.page_structure?.password_forms || 0}
          />

          <WebStat
            title="Links"
            value={data.page_structure?.links || 0}
          />

          <WebStat
            title="Scripts"
            value={data.page_structure?.scripts || 0}
          />

          <WebStat
            title="Iframes"
            value={data.page_structure?.iframes || 0}
          />

          <WebStat
            title="Images"
            value={data.page_structure?.images || 0}
          />

          <WebStat
            title="External Links"
            value={data.page_structure?.external_links || 0}
          />

          <WebStat
            title="Downloads"
            value={data.page_structure?.download_links || 0}
          />

        </div>

      </div>


      {/* FORMS */}

      {data.forms && (
        <div className="web-result-section">

          <h3>📝 Form Analysis</h3>

          <div className="web-stats-grid">

            <WebStat
              title="Total Forms"
              value={data.forms.total || 0}
            />

            <WebStat
              title="Password Forms"
              value={data.forms.password_forms || 0}
            />

            <WebStat
              title="External Actions"
              value={data.forms.external_actions || 0}
            />

          </div>

        </div>
      )}


      {/* LINKS */}

      {data.links && (
        <div className="web-result-section">

          <h3>🔗 Link Analysis</h3>

          <div className="web-stats-grid">

            <WebStat
              title="Total"
              value={data.links.total || 0}
            />

            <WebStat
              title="Internal"
              value={data.links.internal || 0}
            />

            <WebStat
              title="External"
              value={data.links.external || 0}
            />

            <WebStat
              title="Downloads"
              value={data.links.downloads || 0}
            />

          </div>

        </div>
      )}


      {/* JAVASCRIPT */}

      {data.scripts && (
        <div className="web-result-section">

          <h3>⚙️ JavaScript Analysis</h3>

          <div className="web-stats-grid">

            <WebStat
              title="Scripts"
              value={data.scripts.total_scripts || 0}
            />

            <WebStat
              title="Inline"
              value={data.scripts.inline_scripts || 0}
            />

            <WebStat
              title="External"
              value={data.scripts.external_scripts || 0}
            />

            <WebStat
              title="Suspicious JS"
              value={
                data.scripts.suspicious_javascript
                  ? "⚠ Detected"
                  : "✓ None"
              }
            />

          </div>

        </div>
      )}


      {/* SECURITY HEADERS */}

      {data.security_headers && (

        <div className="web-result-section">

          <h3>🔐 Security Headers</h3>

          <div className="web-security-grid">

            {Object.entries(
              data.security_headers
            ).map(([key, value]) => (

              <div
                className="security-header-item"
                key={key}
              >

                <span>{key}</span>

                <strong>
                  {value
                    ? "✓ Present"
                    : "✕ Missing"}
                </strong>

              </div>

            ))}

          </div>

        </div>
      )}


      {/* EXTERNAL DOMAINS */}

      {data.external_domains?.length > 0 && (

        <div className="web-result-section">

          <h3>🌍 External Domains</h3>

          <div className="web-tags">

            {data.external_domains.map(
              (domain, index) => (

                <span key={index}>
                  {domain}
                </span>

              )
            )}

          </div>

        </div>
      )}


      {/* SUSPICIOUS KEYWORDS */}

      {data.suspicious_keywords?.length > 0 && (

        <div className="web-result-section">

          <h3>⚠️ Suspicious Keywords</h3>

          <div className="web-tags warning-tags">

            {data.suspicious_keywords.map(
              (keyword, index) => (

                <span key={index}>
                  {keyword}
                </span>

              )
            )}

          </div>

        </div>
      )}


      {/* FINDINGS */}

      <div className="web-result-section">

        <h3>🛡️ Security Findings</h3>

        {data.findings?.length > 0 ? (

          <div className="web-findings">

            {data.findings.map(
              (finding, index) => (

                <div
                  className="web-finding"
                  key={index}
                >
                  ⚠️ {finding}
                </div>

              )
            )}

          </div>

        ) : (

          <div className="web-no-findings">
            ✓ No major heuristic findings detected.
          </div>

        )}

      </div>


      {/* SCREENSHOT */}

      {data.screenshot && (

        <div className="web-result-section">

          <h3>📸 Website Preview</h3>

          <img
            className="website-screenshot"
            src={`${API_URL}${data.screenshot}`}
            alt="Website preview"
          />

        </div>

      )}


      {/* DISCLAIMER */}

      <div className="web-disclaimer">

        ℹ️{" "}
        {data.disclaimer ||
          "This scanner uses heuristic webpage signals and does not guarantee that a website is safe or malicious."}

      </div>

    </div>
  );
}


// ============================================================
// MAIN APP
// ============================================================

function App() {

  const [activeTab, setActiveTab] =
    useState("Image");

  const [selectedFile, setSelectedFile] =
    useState(null);

  const [previewUrl, setPreviewUrl] =
    useState(null);

  const [result, setResult] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [websiteUrl, setWebsiteUrl] =
    useState("");

  const [websiteResult, setWebsiteResult] =
    useState(null);

  const [websiteLoading, setWebsiteLoading] =
    useState(false);

  const [fullWebResult, setFullWebResult] =
    useState(null);

  const [fullWebLoading, setFullWebLoading] =
    useState(false);

  const [history, setHistory] =
    useState([]);

  const [showHistory, setShowHistory] =
    useState(false);


  const tabs = [
    "Image",
    "Video",
    "Audio",
    "Claim",
    "Website"
  ];


  // ==========================================================
  // HISTORY
  // ==========================================================

  useEffect(() => {
    loadHistory();
  }, []);


  async function loadHistory() {

    try {

      const response = await fetch(
        `${API_URL}/api/history`
      );

      if (!response.ok) return;

      const data =
        await response.json();

      setHistory(
        Array.isArray(data)
          ? data
          : []
      );

    } catch (err) {

      console.error(
        "History error:",
        err
      );

    }
  }


  // ==========================================================
  // TAB
  // ==========================================================

  function selectTab(tab) {

    setActiveTab(tab);

    setResult(null);
    setError("");

    if (tab !== "Website") {

      setWebsiteResult(null);
      setFullWebResult(null);

    }

  }


  // ==========================================================
  // FILE SELECT
  // ==========================================================

  function handleFileChange(event) {

    const file =
      event.target.files?.[0];

    if (!file) return;

    setSelectedFile(file);

    setResult(null);

    setError("");

    if (previewUrl) {

      URL.revokeObjectURL(
        previewUrl
      );

    }

    setPreviewUrl(
      URL.createObjectURL(file)
    );

  }


  // ==========================================================
  // ANALYZE MEDIA
  // ==========================================================

  async function analyzeFile() {

    if (!selectedFile) {

      setError(
        "Please select a file first."
      );

      return;

    }


    setLoading(true);
    setError("");
    setResult(null);


    try {

      const formData =
        new FormData();

      formData.append(
        "file",
        selectedFile
      );


      const response =
        await fetch(
          `${API_URL}/api/analyze`,
          {
            method: "POST",
            body: formData
          }
        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Analysis failed."
        );

      }


      setResult(data);

      loadHistory();

    } catch (err) {

      setError(
        err.message ||
        "Analysis failed."
      );

    } finally {

      setLoading(false);

    }

  }


  // ==========================================================
  // QUICK URL SCAN
  // ==========================================================

  async function scanWebsite() {

    if (!websiteUrl.trim()) {

      setError(
        "Please enter a website URL."
      );

      return;

    }


    setWebsiteLoading(true);

    setWebsiteResult(null);
    setFullWebResult(null);

    setError("");


    try {

      const response =
        await fetch(
          `${API_URL}/api/scan-website`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json"
            },

            body: JSON.stringify({
              url:
                websiteUrl.trim()
            })
          }
        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "URL scan failed."
        );

      }


      setWebsiteResult(data);

    } catch (err) {

      setError(
        err.message ||
        "URL scan failed."
      );

    } finally {

      setWebsiteLoading(false);

    }

  }


  // ==========================================================
  // FULL WEB SCAN
  // ==========================================================

  async function fullWebScan() {

    if (!websiteUrl.trim()) {

      setError(
        "Please enter a website URL."
      );

      return;

    }


    setFullWebLoading(true);

    setFullWebResult(null);
    setWebsiteResult(null);

    setError("");


    try {

      const response =
        await fetch(
          `${API_URL}/api/full-web-scan`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json"
            },

            body: JSON.stringify({
              url:
                websiteUrl.trim()
            })
          }
        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Full web scan failed."
        );

      }


      setFullWebResult(data);

    } catch (err) {

      console.error(err);

      setError(
        err.message ||
        "Full web scan failed."
      );

    } finally {

      setFullWebLoading(false);

    }

  }


  // ==========================================================
  // DELETE HISTORY
  // ==========================================================

  async function deleteHistory(fileId) {

    if (
      !window.confirm(
        "Delete this analysis?"
      )
    ) {
      return;
    }


    try {

      await fetch(
        `${API_URL}/api/history/${fileId}`,
        {
          method: "DELETE"
        }
      );

      loadHistory();

    } catch (err) {

      setError(
        "Could not delete history."
      );

    }

  }


  // ==========================================================
  // VIEW HISTORY
  // ==========================================================

  async function viewHistory(fileId) {

    try {

      const response =
        await fetch(
          `${API_URL}/api/history/${fileId}`
        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Could not load analysis."
        );

      }


      setResult(data);

      setShowHistory(false);


      if (
        data.media_type === "video"
      ) {

        setActiveTab("Video");

      } else if (
        data.media_type === "audio"
      ) {

        setActiveTab("Audio");

      } else {

        setActiveTab("Image");

      }

    } catch (err) {

      setError(
        err.message
      );

    }

  }


  // ==========================================================
  // PDF
  // ==========================================================

  function generateReport(fileId) {

    window.open(
      `${API_URL}/api/report/${fileId}`,
      "_blank"
    );

  }


  // ==========================================================
  // RISK CLASS
  // ==========================================================

  function riskClass(score) {

    const value =
      Number(score || 0);

    if (value >= 65) {
      return "high";
    }

    if (value >= 30) {
      return "medium";
    }

    return "low";

  }


  // ==========================================================
  // MEDIA SECTION
  // ==========================================================

  function renderMedia() {

    return (

      <section className="upload-section">

        <div className="upload-icon">
          📁
        </div>

        <h2>
          Upload {activeTab}
        </h2>

        <p>
          Select a file to analyze with TruthGuard AI
        </p>


        <label className="choose-file">

          Choose File

          <input
            type="file"
            accept={
              activeTab === "Image"
                ? "image/*"
                : activeTab === "Video"
                ? "video/*"
                : "audio/*"
            }
            onChange={
              handleFileChange
            }
          />

        </label>


        {selectedFile && (

          <div className="selected-file">

            Selected file:

            <strong>
              {selectedFile.name}
            </strong>

          </div>

        )}


        {previewUrl &&
          activeTab === "Image" && (

            <div className="media-preview">

              <img
                src={previewUrl}
                alt="Preview"
              />

            </div>

          )}


        {previewUrl &&
          activeTab === "Video" && (

            <div className="media-preview">

              <video
                src={previewUrl}
                controls
              />

            </div>

          )}


        {previewUrl &&
          activeTab === "Audio" && (

            <div className="media-preview">

              <audio
                src={previewUrl}
                controls
              />

            </div>

          )}


        <button
          className="analyze-button"
          onClick={analyzeFile}
          disabled={
            !selectedFile ||
            loading
          }
        >

          {loading
            ? "⏳ Analyzing..."
            : "🔍 Analyze with TruthGuard AI"}

        </button>

      </section>

    );

  }


  // ==========================================================
  // CLAIM
  // ==========================================================

  function renderClaim() {

    return (

      <section className="upload-section">

        <div className="upload-icon">
          🔎
        </div>

        <h2>
          Claim Verification
        </h2>

        <p>
          Text-based misinformation verification
          will be connected next.
        </p>

        <div className="claim-info">

          <p>
            TruthGuard AI will verify:
          </p>

          <ul>

            <li>
              Claim credibility
            </li>

            <li>
              Supporting evidence
            </li>

            <li>
              Contradicting evidence
            </li>

            <li>
              Source reliability
            </li>

          </ul>

        </div>

      </section>

    );

  }


  // ==========================================================
  // WEBSITE
  // ==========================================================

  function renderWebsite() {

    return (

      <section className="upload-section website-section">

        <div className="upload-icon">
          🌐
        </div>

        <h2>
          Website Threat Scanner
        </h2>

        <p>
          Analyze websites for suspicious
          security and webpage indicators.
        </p>


        <input
          className="website-input"
          type="text"
          placeholder="https://example.com"
          value={websiteUrl}
          onChange={(event) =>
            setWebsiteUrl(
              event.target.value
            )
          }
        />


        <div className="website-buttons">

          <button
            className="website-scan-button"
            onClick={scanWebsite}
            disabled={
              websiteLoading ||
              fullWebLoading
            }
          >

            {websiteLoading
              ? "⏳ Scanning..."
              : "🔎 URL Scan"}

          </button>


          <button
            className="website-full-button"
            onClick={fullWebScan}
            disabled={
              websiteLoading ||
              fullWebLoading
            }
          >

            {fullWebLoading
              ? "⏳ Full Web Scan..."
              : "🌐 Full Web Scan"}

          </button>

        </div>


        {/* QUICK RESULT */}

        {websiteResult && (

          <div className="website-quick-result">

            <div className="result-card-header">

              <div>

                <div className="result-label">
                  URL ANALYSIS
                </div>

                <h2>
                  {websiteResult.domain}
                </h2>

                <p>
                  {websiteResult.url}
                </p>

              </div>


              <div
                className={`web-risk-circle ${
                  riskClass(
                    websiteResult.risk_score
                  )
                }`}
              >

                <strong>
                  {websiteResult.risk_score}
                </strong>

                <span>
                  /100
                </span>

              </div>

            </div>


            <div
              className={`web-verdict ${
                riskClass(
                  websiteResult.risk_score
                )
              }`}
            >

              {websiteResult.verdict}

              <span>
                {websiteResult.risk_level}
              </span>

            </div>


            {websiteResult.findings?.length > 0 && (

              <div className="web-findings">

                {websiteResult.findings.map(
                  (finding, index) => (

                    <div
                      className="web-finding"
                      key={index}
                    >
                      ⚠️ {finding}
                    </div>

                  )
                )}

              </div>

            )}

          </div>

        )}


        {/* FULL RESULT */}

        {fullWebResult && (

          <FullWebResult
            data={fullWebResult}
          />

        )}

      </section>

    );

  }


  // ==========================================================
  // RESULTS
  // ==========================================================

  function renderResults() {

    if (!result) return null;


    const risk =
      Number(
        result.risk_score || 0
      );


    return (

      <section className="results-section">

        <div className="result-card-header">

          <div>

            <div className="result-label">
              ANALYSIS COMPLETE
            </div>

            <h2>
              {result.filename}
            </h2>

          </div>


          <div
            className={`web-risk-circle ${
              riskClass(risk)
            }`}
          >

            <strong>
              {risk}
            </strong>

            <span>
              /100
            </span>

          </div>

        </div>


        <div
          className={`verdict-card ${
            riskClass(risk)
          }`}
        >

          <h2>
            {result.verdict ||
              "ANALYSIS COMPLETE"}
          </h2>

          <p>
            Risk Level:{" "}
            {result.risk_level ||
              "N/A"}
          </p>

        </div>


        <div className="score-grid">

          <div className="score-card">

            <span>
              Manipulation
            </span>

            <strong>
              {result.fake_score ?? 0}%
            </strong>

          </div>


          <div className="score-card">

            <span>
              Authentic
            </span>

            <strong>
              {result.real_score ?? 0}%
            </strong>

          </div>


          <div className="score-card">

            <span>
              File Size
            </span>

            <strong>

              {result.file_size
                ? `${(
                    result.file_size /
                    1024
                  ).toFixed(1)} KB`
                : "N/A"}

            </strong>

          </div>

        </div>


        {/* FORENSICS */}

        {result.metadata && (

          <>

            <h3 className="section-title">
              🔬 Digital Forensics
            </h3>

            <div className="forensics-grid">

              <div className="forensic-card">

                <span>
                  Metadata
                </span>

                <strong>
                  {result.metadata
                    ?.metadata_risk ?? 0}
                </strong>

              </div>


              <div className="forensic-card">

                <span>
                  Compression
                </span>

                <strong>
                  {result.compression
                    ?.compression_risk ?? 0}
                </strong>

              </div>


              <div className="forensic-card">

                <span>
                  Artifacts
                </span>

                <strong>
                  {result.artifacts
                    ?.artifact_risk ?? 0}
                </strong>

              </div>


              <div className="forensic-card">

                <span>
                  ELA
                </span>

                <strong>
                  {result.ela
                    ?.ela_risk ?? 0}
                </strong>

              </div>

            </div>

          </>

        )}


        {/* ELA */}

        {result.ela?.ela_image && (

          <div className="ela-section">

            <h3>
              🖼️ Visual Forensics — ELA
            </h3>

            <img
              src={`${API_URL}/uploads/${result.ela.ela_image
                .split("\\")
                .pop()
                .split("/")
                .pop()}`}
              alt="ELA analysis"
            />

          </div>

        )}


        {/* TECHNICAL */}

        <div className="technical-section">

          <h3>
            Technical Evidence
          </h3>

          <pre>
            {JSON.stringify(
              result,
              null,
              2
            )}
          </pre>

        </div>


        {/* PDF */}

        {result.file_id && (

          <button
            className="report-button"
            onClick={() =>
              generateReport(
                result.file_id
              )
            }
          >

            📄 Generate Forensic PDF Report

          </button>

        )}

      </section>

    );

  }


  // ==========================================================
  // HISTORY
  // ==========================================================

  function renderHistory() {

    if (!showHistory) {
      return null;
    }


    return (

      <section className="history-section">

        <div className="history-header">

          <div>

            <div className="result-label">
              HISTORY
            </div>

            <h2>
              Previous Analyses
            </h2>

          </div>


          <button
            onClick={loadHistory}
            className="history-refresh"
          >
            ↻ Refresh
          </button>

        </div>


        {history.length === 0 ? (

          <p>
            No previous analyses.
          </p>

        ) : (

          <div className="history-list">

            {history.map((item) => (

              <div
                className="history-item"
                key={item.file_id}
              >

                <div>

                  <strong>
                    {item.filename}
                  </strong>

                  <span>
                    {item.media_type}
                  </span>

                  <small>
                    {item.created_at}
                  </small>

                </div>


                <div className="history-actions">

                  <button
                    onClick={() =>
                      viewHistory(
                        item.file_id
                      )
                    }
                  >
                    View
                  </button>

                  <button
                    onClick={() =>
                      deleteHistory(
                        item.file_id
                      )
                    }
                  >
                    Delete
                  </button>

                </div>

              </div>

            ))}

          </div>

        )}

      </section>

    );

  }


  // ==========================================================
  // MAIN UI
  // ==========================================================

  return (

    <div className="app">

      {/* NAVBAR */}

      <nav className="navbar">

        <div className="brand">

          <span>
            🛡️
          </span>

          <strong>
            TruthGuard AI
          </strong>

        </div>


        <div className="navbar-right">

          <button
            className="history-button"
            onClick={() =>
              setShowHistory(
                !showHistory
              )
            }
          >

            📋 History

          </button>


          <span className="system-status">
            AI SYSTEM ONLINE
          </span>

        </div>

      </nav>


      {/* HERO */}

      <main>

        <section className="hero">

          <div className="hero-badge">
            🛡️ DIGITAL TRUST & VERIFICATION
          </div>


          <h1>

            Detect.
            <span>
              Verify.
            </span>

            <br />

            Trust.

          </h1>


          <p>

            TruthGuard AI analyzes digital content
            using artificial intelligence and digital
            forensic signals to identify potentially
            manipulated media and suspicious websites.

          </p>

        </section>


        {/* TABS */}

        <div className="tabs">

          {tabs.map((tab) => (

            <button
              key={tab}
              className={
                activeTab === tab
                  ? "tab active"
                  : "tab"
              }
              onClick={() =>
                selectTab(tab)
              }
            >

              {tab}

            </button>

          ))}

        </div>


        {/* ERROR */}

        {error && (

          <div className="error-message">
            ⚠️ {error}
          </div>

        )}


        {/* CONTENT */}

        {activeTab === "Website"
          ? renderWebsite()
          : activeTab === "Claim"
          ? renderClaim()
          : renderMedia()
        }


        {renderResults()}

        {renderHistory()}

      </main>


      {/* FOOTER */}

      <footer>

        <strong>
          TruthGuard AI
        </strong>

        <span>
          AI-powered digital trust & verification
        </span>

      </footer>

    </div>

  );

}


export default App;
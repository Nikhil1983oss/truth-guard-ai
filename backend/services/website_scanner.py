import ipaddress
import socket
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0 Safari/537.36 TruthGuardAI/1.0"
)

TIMEOUT = 15
MAX_RESPONSE_SIZE = 5 * 1024 * 1024
MAX_PAGES = 5


# ============================================================
# URL VALIDATION
# ============================================================

def normalize_url(url: str) -> str:

    url = url.strip()

    if not url:
        raise ValueError("Website URL is required.")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP and HTTPS URLs are supported.")

    if not parsed.hostname:
        raise ValueError("Invalid website URL.")

    return url


def is_private_hostname(hostname: str) -> bool:

    hostname = hostname.lower().strip(".")

    if hostname in (
        "localhost",
        "localhost.localdomain",
    ):
        return True

    try:

        addresses = socket.getaddrinfo(
            hostname,
            None
        )

        for address in addresses:

            ip_text = address[4][0]

            ip = ipaddress.ip_address(ip_text)

            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
                or ip.is_multicast
            ):
                return True

    except socket.gaierror:

        return False

    return False


# ============================================================
# DOMAIN
# ============================================================

def get_domain(url):

    return (
        urlparse(url)
        .hostname
        or ""
    ).lower()


# ============================================================
# SAME DOMAIN
# ============================================================

def same_domain(url1, url2):

    domain1 = get_domain(url1)
    domain2 = get_domain(url2)

    return (
        domain1 == domain2
        or domain1.endswith("." + domain2)
        or domain2.endswith("." + domain1)
    )


# ============================================================
# SUSPICIOUS KEYWORDS
# ============================================================

SUSPICIOUS_KEYWORDS = [

    "verify your account",
    "verify account",
    "login",
    "sign in",
    "password",
    "confirm identity",
    "confirm your identity",
    "bank account",
    "credit card",
    "debit card",
    "otp",
    "one time password",
    "security alert",
    "urgent",
    "suspended",
    "account suspended",
    "claim reward",
    "free prize",
    "winner",
    "download now",
    "install now",
    "remote access",
    "payment required",
]


def find_suspicious_keywords(text):

    text_lower = text.lower()

    found = []

    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in text_lower:

            found.append(keyword)

    return found


# ============================================================
# MAIN SCANNER
# ============================================================

def scan_website(url: str):

    original_url = normalize_url(url)

    parsed_original = urlparse(
        original_url
    )

    hostname = (
        parsed_original.hostname
    )

    if is_private_hostname(hostname):

        raise ValueError(
            "Scanning localhost or private network addresses is blocked."
        )


    session = requests.Session()

    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml"
    })


    response = session.get(
        original_url,
        timeout=TIMEOUT,
        allow_redirects=True,
        stream=True,
    )


    # ========================================================
    # RESPONSE SIZE PROTECTION
    # ========================================================

    content_length = response.headers.get(
        "Content-Length"
    )

    if content_length:

        try:

            if int(content_length) > MAX_RESPONSE_SIZE:

                raise ValueError(
                    "Website response is larger than the allowed scan size."
                )

        except ValueError:

            pass


    content_type = (
        response.headers.get(
            "Content-Type",
            ""
        )
        .lower()
    )


    if (
        "text/html" not in content_type
        and "application/xhtml+xml" not in content_type
    ):

        return {
            "success": False,
            "url": original_url,
            "error": (
                "The URL did not return an HTML webpage."
            ),
            "scanner": "TruthGuard Full Web Scanner"
        }


    # ========================================================
    # READ RESPONSE
    # ========================================================

    content = b""

    for chunk in response.iter_content(
        chunk_size=65536
    ):

        if not chunk:
            continue

        content += chunk

        if len(content) > MAX_RESPONSE_SIZE:

            raise ValueError(
                "Website response exceeded the 5 MB scan limit."
            )


    html = content.decode(
        response.encoding
        or "utf-8",
        errors="replace"
    )


    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    final_url = response.url

    final_domain = get_domain(
        final_url
    )


    # ========================================================
    # TITLE
    # ========================================================

    title = ""

    if soup.title:

        title = soup.title.get_text(
            " ",
            strip=True
        )


    # ========================================================
    # PAGE TEXT
    # ========================================================

    for tag in soup([
        "script",
        "style",
        "noscript"
    ]):

        tag.extract()


    page_text = soup.get_text(
        " ",
        strip=True
    )

    page_text = " ".join(
        page_text.split()
    )


    # ========================================================
    # KEYWORDS
    # ========================================================

    suspicious_keywords = (
        find_suspicious_keywords(
            page_text
        )
    )


    # ========================================================
    # FORMS
    # ========================================================

    forms = soup.find_all("form")

    password_forms = 0
    external_actions = 0

    form_details = []


    for form in forms:

        action = (
            form.get("action")
            or ""
        )

        action_url = urljoin(
            final_url,
            action
        )

        form_domain = get_domain(
            action_url
        )

        is_external = (
            form_domain
            and not same_domain(
                final_url,
                action_url
            )
        )

        inputs = form.find_all(
            "input"
        )

        has_password = any(
            (
                inp.get("type", "")
                .lower()
                == "password"
            )
            for inp in inputs
        )

        if has_password:

            password_forms += 1

        if is_external:

            external_actions += 1

        form_details.append({
            "action": action_url,
            "method": (
                form.get(
                    "method",
                    "GET"
                ).upper()
            ),
            "password": has_password,
            "external_action": bool(
                is_external
            )
        })


    # ========================================================
    # LINKS
    # ========================================================

    anchors = soup.find_all("a")

    internal_links = 0
    external_links = 0
    download_links = 0

    external_domains = set()

    download_extensions = (
        ".exe",
        ".msi",
        ".apk",
        ".dmg",
        ".zip",
        ".rar",
        ".7z",
        ".bat",
        ".cmd",
        ".scr",
        ".js",
        ".jar",
        ".iso",
    )


    for anchor in anchors:

        href = (
            anchor.get("href")
            or ""
        ).strip()

        if not href:
            continue

        if href.startswith(
            (
                "#",
                "mailto:",
                "tel:",
                "javascript:"
            )
        ):

            continue

        link_url = urljoin(
            final_url,
            href
        )

        link_domain = get_domain(
            link_url
        )

        if same_domain(
            final_url,
            link_url
        ):

            internal_links += 1

        else:

            external_links += 1

            if link_domain:

                external_domains.add(
                    link_domain
                )


        if any(
            link_url.lower().split("?")[0].endswith(ext)
            for ext in download_extensions
        ):

            download_links += 1


    # ========================================================
    # SCRIPTS
    # ========================================================

    scripts = soup.find_all("script")

    inline_scripts = 0
    external_scripts = 0

    suspicious_javascript = False

    suspicious_js_patterns = [

        "eval(",
        "atob(",
        "document.write",
        "window.location",
        "location.href",
        "location.replace",
        "fromcharcode",
        "unescape(",
    ]


    for script in scripts:

        src = script.get("src")

        if src:

            external_scripts += 1

        else:

            inline_scripts += 1

            script_text = (
                script.get_text(
                    " ",
                    strip=True
                )
                .lower()
            )

            for pattern in suspicious_js_patterns:

                if pattern.lower() in script_text:

                    suspicious_javascript = True

                    break


    # ========================================================
    # IFRAMES
    # ========================================================

    iframe_tags = soup.find_all(
        "iframe"
    )

    external_iframes = 0

    for iframe in iframe_tags:

        src = (
            iframe.get("src")
            or ""
        )

        iframe_url = urljoin(
            final_url,
            src
        )

        if (
            get_domain(iframe_url)
            and not same_domain(
                final_url,
                iframe_url
            )
        ):

            external_iframes += 1


    # ========================================================
    # IMAGES
    # ========================================================

    image_tags = soup.find_all(
        "img"
    )

    missing_alt = 0

    for image in image_tags:

        if not image.get("alt"):

            missing_alt += 1


    # ========================================================
    # SECURITY HEADERS
    # ========================================================

    headers = response.headers

    security_headers = {

        "Content-Security-Policy":
            bool(
                headers.get(
                    "Content-Security-Policy"
                )
            ),

        "Strict-Transport-Security":
            bool(
                headers.get(
                    "Strict-Transport-Security"
                )
            ),

        "X-Content-Type-Options":
            bool(
                headers.get(
                    "X-Content-Type-Options"
                )
            ),

        "X-Frame-Options":
            bool(
                headers.get(
                    "X-Frame-Options"
                )
            ),

        "Referrer-Policy":
            bool(
                headers.get(
                    "Referrer-Policy"
                )
            ),
    }


    # ========================================================
    # REDIRECTS
    # ========================================================

    redirect_count = len(
        response.history
    )

    cross_domain_redirect = False

    redirect_chain = []

    for redirect in response.history:

        redirect_url = redirect.url

        redirect_chain.append(
            redirect_url
        )

        if not same_domain(
            original_url,
            redirect_url
        ):

            cross_domain_redirect = True


    redirect_chain.append(
        final_url
    )


    # ========================================================
    # RISK ENGINE
    # ========================================================

    risk_score = 0

    findings = []


    # HTTP

    if parsed_original.scheme != "https":

        risk_score += 15

        findings.append(
            "Website is not using HTTPS."
        )


    # PASSWORD FORMS

    if password_forms > 0:

        risk_score += 20

        findings.append(
            "Password/login form detected."
        )


    # EXTERNAL FORM

    if external_actions > 0:

        risk_score += 25

        findings.append(
            "Form submits data to an external domain."
        )


    # SUSPICIOUS KEYWORDS

    if len(suspicious_keywords) >= 5:

        risk_score += 20

        findings.append(
            "Multiple suspicious/phishing-related keywords detected."
        )

    elif len(suspicious_keywords) >= 2:

        risk_score += 10

        findings.append(
            "Suspicious security/payment/account language detected."
        )


    # REDIRECT

    if cross_domain_redirect:

        risk_score += 20

        findings.append(
            "Cross-domain redirect detected."
        )


    # EXTERNAL LINKS

    if external_links >= 20:

        risk_score += 10

        findings.append(
            "Large number of external links detected."
        )


    # DOWNLOADS

    if download_links > 0:

        risk_score += 15

        findings.append(
            "Potential downloadable files detected."
        )


    # JAVASCRIPT

    if suspicious_javascript:

        risk_score += 15

        findings.append(
            "Potentially suspicious JavaScript patterns detected."
        )


    # IFRAMES

    if external_iframes > 0:

        risk_score += 5

        findings.append(
            "External iframe content detected."
        )


    # SECURITY HEADERS

    missing_headers = sum(
        1
        for value in security_headers.values()
        if not value
    )

    if missing_headers >= 4:

        risk_score += 10

        findings.append(
            "Several recommended security headers are missing."
        )


    risk_score = min(
        risk_score,
        100
    )


    # ========================================================
    # RISK LEVEL
    # ========================================================

    if risk_score >= 65:

        risk_level = "HIGH"
        verdict = "HIGH RISK WEBSITE"

    elif risk_score >= 30:

        risk_level = "MEDIUM"
        verdict = "SUSPICIOUS WEBSITE"

    else:

        risk_level = "LOW"
        verdict = "LOW RISK WEBSITE"


    # ========================================================
    # PAGE STRUCTURE
    # ========================================================

    page_structure = {

        "forms":
            len(forms),

        "password_forms":
            password_forms,

        "links":
            len(anchors),

        "internal_links":
            internal_links,

        "external_links":
            external_links,

        "download_links":
            download_links,

        "scripts":
            len(scripts),

        "iframes":
            len(iframe_tags),

        "images":
            len(image_tags),

    }


    # ========================================================
    # RESULT
    # ========================================================

    return {

        "success": True,

        "scanner":
            "TruthGuard Full Web Scanner",

        "url":
            original_url,

        "final_url":
            final_url,

        "domain":
            final_domain,

        "title":
            title or "Untitled Website",

        "status_code":
            response.status_code,

        "https":
            final_url.lower().startswith(
                "https://"
            ),

        "page_size":
            len(content),

        "content_chars":
            len(page_text),

        "pages_scanned":
            1,

        "page_limit":
            MAX_PAGES,

        "risk_score":
            risk_score,

        "risk_level":
            risk_level,

        "verdict":
            verdict,

        "page_structure":
            page_structure,

        "forms": {

            "total":
                len(forms),

            "password_forms":
                password_forms,

            "external_actions":
                external_actions,

            "details":
                form_details,
        },

        "links": {

            "total":
                len(anchors),

            "internal":
                internal_links,

            "external":
                external_links,

            "downloads":
                download_links,
        },

        "scripts": {

            "total_scripts":
                len(scripts),

            "inline_scripts":
                inline_scripts,

            "external_scripts":
                external_scripts,

            "suspicious_javascript":
                suspicious_javascript,
        },

        "iframes": {

            "total":
                len(iframe_tags),

            "external":
                external_iframes,
        },

        "images": {

            "total":
                len(image_tags),

            "missing_alt":
                missing_alt,
        },

        "network": {

            "total_requests":
                1,

            "external_request_count":
                external_links,

            "external_domains":
                sorted(
                    external_domains
                ),
        },

        "security_headers":
            security_headers,

        "redirects": {

            "count":
                redirect_count,

            "cross_domain":
                cross_domain_redirect,

            "chain":
                redirect_chain,
        },

        "external_domains":
            sorted(
                external_domains
            ),

        "suspicious_keywords":
            suspicious_keywords,

        "findings":
            findings,

        "disclaimer":
            (
                "TruthGuard Full Web Scanner analyzes "
                "server-returned webpage signals. It does "
                "not execute the website like a full browser "
                "sandbox and cannot guarantee that a website "
                "is safe or malicious."
            ),
    }
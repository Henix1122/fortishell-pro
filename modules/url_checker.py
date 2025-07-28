import re
from urllib.parse import urlparse
import asyncio
import aiohttp
from datetime import datetime
import socket

PHISH_KEYWORDS = [
    "login", "verify", "secure", "banking", "update", "account", "signin",
    "password", "confirmation", "paypal", "appleid", "amazon", "unlock",
    "support", "helpdesk", "reset", "invoice", "payment", "alert", "urgent"
]

SUSPICIOUS_TLDS = [
    "xyz", "top", "club", "online", "info", "buzz", "work", "support"
]

BRAND_IMPERSONATION = [
    "paypa1", "amaz0n", "micros0ft", "faceb00k", "g00gle", "app1eid"
]

MALICIOUS_PATTERNS = [
    r"(xn--)",  # punycode (IDN homograph attacks)
    r"(\/\/[a-zA-Z0-9\-\.]*@)",  # @ in URL (obfuscation)
    r"(\\u[0-9a-fA-F]{4})",  # Unicode escapes
    r"(0x[a-fA-F0-9]+)",  # Hex IPs
    r"(base64,)",  # Embedded base64 data
    r"(data:text/html)",  # Data URLs
]

SUSPICIOUS_PATHS = [
    "wp-login", "admin", "dashboard", "cpanel", "config", "setup", "install"
]

THREAT_FEEDS = [
    # Example threat feed URLs (replace with real feeds or APIs)
    "https://otx.alienvault.com/api/v1/indicators/domain/{domain}/general",
    # Add more feeds as needed
]

def is_ip_address(domain):
    return re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", domain) is not None

def has_suspicious_tld(domain):
    tld = domain.split('.')[-1]
    return tld in SUSPICIOUS_TLDS

def has_brand_impersonation(domain):
    for fake in BRAND_IMPERSONATION:
        if fake in domain:
            return True
    return False

def has_homoglyphs(domain):
    return bool(re.search(r"[0O1lI]", domain))

def matches_malicious_patterns(url):
    for pattern in MALICIOUS_PATTERNS:
        if re.search(pattern, url):
            return True
    return False

def has_suspicious_path(path):
    for suspicious in SUSPICIOUS_PATHS:
        if suspicious in path:
            return True
    return False

def is_short_lived_domain(domain):
    try:
        import whois
        w = whois.whois(domain)
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]
        if creation:
            age_days = (datetime.utcnow() - creation).days
            return age_days < 30
    except Exception:
        pass
    return False

async def check_domain_reputation(domain):
    VT_API_KEY = "YOUR_API_KEY"
    vt_url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {"x-apikey": VT_API_KEY}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(vt_url, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("malicious", 0) > 0:
                        return True
        except Exception:
            pass
        # Check additional threat feeds
        for feed in THREAT_FEEDS:
            url = feed.format(domain=domain)
            try:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if "pulse_info" in data and data["pulse_info"].get("count", 0) > 0:
                            return True
            except Exception:
                continue
    return False

async def check_redirects(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, allow_redirects=True, timeout=10) as resp:
                if len(resp.history) > 2:
                    return True
    except Exception:
        pass
    return False

def is_suspicious_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    full_url = url.lower()

    issues = []

    if not parsed.scheme or not parsed.netloc:
        issues.append("Missing scheme or domain ❌")

    if is_ip_address(domain):
        issues.append("URL uses IP address 📛")

    if any(keyword in full_url for keyword in PHISH_KEYWORDS):
        issues.append("Contains phishing keyword 🔎")

    if domain.count(".") > 2:
        issues.append("Too many subdomains 🧨")

    if re.search(r"[^a-zA-Z0-9.-]", domain):
        issues.append("Unusual characters in domain 🧬")

    if has_suspicious_tld(domain):
        issues.append(f"Suspicious TLD: .{domain.split('.')[-1]} 🚩")

    if has_brand_impersonation(domain):
        issues.append("Possible brand impersonation 🕵️")

    if has_homoglyphs(domain):
        issues.append("Homoglyphs detected in domain 🧐")

    if len(url) > 100 or len(path) > 60:
        issues.append("Unusually long URL/path 🧵")

    if domain.count('-') > 2 or domain.count('.') > 3:
        issues.append("Excessive hyphens/dots in domain ⚠️")

    if matches_malicious_patterns(url):
        issues.append("Malicious pattern detected 🦠")

    if has_suspicious_path(path):
        issues.append("Suspicious path detected 🗂️")

    if is_short_lived_domain(domain):
        issues.append("Domain is very new ⏳")

    return {
        "URL": url,
        "Domain": domain,
        "Suspicious": bool(issues),
        "Issues Found": issues if issues else ["None 🎉"]
    }

async def check_phishing_url(url):
    result = is_suspicious_url(url)
    domain = result["Domain"]
    reputation_flag = await check_domain_reputation(domain)
    if reputation_flag:
        result["Issues Found"].append("Domain flagged by threat intelligence 🛑")
        result["Suspicious"] = True
    redirects_flag = await check_redirects(url)
    if redirects_flag:
        result["Issues Found"].append("Excessive redirects detected 🔄")
        result["Suspicious"] = True
    if result["Suspicious"]:
        log_suspicious(url, result["Issues Found"])
        return f"Potential phishing detected!\nIssues: {', '.join(result['Issues Found'])}"
    return "URL appears safe."

def log_suspicious(url, issues):
    timestamp = datetime.utcnow().isoformat()
    with open("suspicious_urls.log", "a") as f:
        f.write(f"{timestamp} | {url} | {issues}\n")

def safe_resolve_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

def validate_url(url):
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return False
    if not safe_resolve_domain(parsed.netloc):
        return False
    return True

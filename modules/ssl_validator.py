import ssl
import socket
from datetime import datetime
from typing import Dict, Any, Union

def check_ssl_cert(domain: str) -> Union[Dict[str, Any], str]:
    """
    Advanced SSL certificate validator for a domain.
    Returns detailed certificate info or error message.
    """
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(socket.socket(), server_hostname=domain) as sock:
            sock.settimeout(5)
            sock.connect((domain, 443))
            cert = sock.getpeercert()

            # Parse subject and issuer
            subject = {k: v for x in cert.get("subject", []) for k, v in x}
            issuer = {k: v for x in cert.get("issuer", []) for k, v in x}

            # Dates
            valid_from = cert.get("notBefore", "N/A")
            valid_until = cert.get("notAfter", "N/A")
            try:
                expiry = datetime.strptime(valid_until, "%b %d %H:%M:%S %Y %Z")
                status = "Valid ✅" if expiry > datetime.utcnow() else "Expired 🔴"
                days_left = (expiry - datetime.utcnow()).days
            except Exception:
                status = "Invalid date format"
                days_left = "N/A"

            # Serial number
            serial = cert.get("serialNumber", "N/A")

            # SANs (Subject Alternative Names)
            san = []
            for ext in cert.get("subjectAltName", []):
                if ext[0] == "DNS":
                    san.append(ext[1])

            # Signature algorithm (if available)
            sig_alg = cert.get("signatureAlgorithm", "N/A")

            # Version
            version = cert.get("version", "N/A")

            return {
                "Domain": domain,
                "Subject CN": subject.get("commonName", "N/A"),
                "Issuer CN": issuer.get("commonName", "N/A"),
                "Valid From": valid_from,
                "Valid Until": valid_until,
                "Days Until Expiry": days_left,
                "Status": status,
                "Serial Number": serial,
                "SANs": san,
                "Signature Algorithm": sig_alg,
                "Version": version,
            }

    except ssl.SSLCertVerificationError as e:
        return f"Certificate verification failed: {e}"
    except socket.timeout:
        return "Connection timed out."
    except Exception as e:
        return f"Certificate check failed: {e}"

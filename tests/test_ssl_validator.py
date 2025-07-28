import pytest
from modules.ssl_validator import check_ssl_cert

@pytest.mark.parametrize("domain,expected_in_output", [
    ("example.com", "SSL certificate is valid"),
    ("expired.badssl.com", "SSL certificate has expired"),
    ("wrong.host.badssl.com", "SSL certificate hostname mismatch"),
    ("self-signed.badssl.com", "SSL certificate is self-signed"),
    ("invalid-domain", "Error"),
])
def test_check_ssl_cert_pro(domain, expected_in_output):
    result = check_ssl_cert(domain)
    assert isinstance(result, str)
    assert expected_in_output in result
    assert len(result) > 0

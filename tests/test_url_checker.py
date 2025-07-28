import pytest
from modules.url_checker import check_phishing_url

@pytest.mark.parametrize("url,expected_type", [
    ('http://example.com', str),
    ('https://secure-site.org', str),
    ('ftp://invalid-protocol.com', str),
    ('', str),
    ('http://phishing-site.com', str),
])
def test_check_phishing_url_various(url, expected_type):
    result = check_phishing_url(url)
    assert isinstance(result, expected_type)
    assert len(result) > 0
    # Optionally, check for specific keywords in result
    assert any(keyword in result.lower() for keyword in ['safe', 'phishing', 'warning', 'invalid', 'error'])

def test_check_phishing_url_handles_exceptions():
    # Simulate a malformed URL or unexpected input
    result = check_phishing_url(None)
    assert isinstance(result, str)
    assert 'error' in result.lower() or 'invalid' in result.lower()

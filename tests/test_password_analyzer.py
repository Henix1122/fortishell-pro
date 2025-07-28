import pytest
from modules.password_analyzer import analyze_password

def test_analyze_password_valid():
    result = analyze_password('G@naStrong2025!')
    assert isinstance(result, dict)
    assert 'Password' in result
    assert result['Strength'] in ['Weak', 'Moderate', 'Strong']
    assert result['Length'] == len('G@naStrong2025!')
    assert result['HasUppercase'] is True
    assert result['HasLowercase'] is True
    assert result['HasDigit'] is True
    assert result['HasSpecialChar'] is True

@pytest.mark.parametrize("password,expected_strength", [
    ("123456", "Weak"),
    ("abcdefgH", "Moderate"),
    ("AbcdefgH1!", "Strong"),
    ("", "Weak"),
])
def test_analyze_password_various(password, expected_strength):
    result = analyze_password(password)
    assert result['Strength'] == expected_strength

def test_analyze_password_edge_cases():
    result = analyze_password('A1!')
    assert result['Length'] == 3
    assert result['HasUppercase'] is True
    assert result['HasLowercase'] is False
    assert result['HasDigit'] is True
    assert result['HasSpecialChar'] is True

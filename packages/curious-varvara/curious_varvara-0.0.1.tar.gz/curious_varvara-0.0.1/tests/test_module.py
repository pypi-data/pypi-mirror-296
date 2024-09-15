from curious_varvara import is_live, body_md5
from unittest.mock import MagicMock, patch

def test_is_live_success():
    mock_response = MagicMock()
    mock_response.status = 200

    with patch('urllib3.PoolManager.request', return_value=mock_response):
      is_url_available = is_live("http://www.google.com")

      assert is_url_available

def test_is_live_success():
    mock_response = MagicMock()
    mock_response.status = 404

    with patch('urllib3.PoolManager.request', return_value=mock_response):
      is_url_available = is_live("http://www.google.com")

      assert not is_url_available

def test_body_md5():
    mock_response = MagicMock()
    mock_response.data = b"Hello, world!"

    with patch('urllib3.PoolManager.request', return_value=mock_response):
      md5_hash = body_md5("http://www.google.com")

      assert md5_hash == "6cd3556deb0da54bca060b4c39479839"

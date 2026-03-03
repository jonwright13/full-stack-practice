from main import handler
from typing import Any


def test_handler(mock_event: dict[str, list[dict[str, Any]]]):
    result = handler(mock_event, {})
    assert result["statusCode"] == 200
    assert result["body"]["bucket"] == "my-bucket"
    assert result["body"]["key"] == "my file.txt"

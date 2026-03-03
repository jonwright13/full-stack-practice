from pytest import fixture
from typing import Any


@fixture
def mock_event() -> dict[str, list[dict[str, Any]]]:

    return {
        "Records": [
            {
                "eventTime": "2024-01-01T00:00:00.000Z",
                "s3": {
                    "bucket": {"name": "my-bucket"},
                    "object": {"key": "my+file.txt", "size": 1024},
                },
            }
        ]
    }

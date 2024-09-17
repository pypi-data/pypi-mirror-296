"""Helper utilities."""

import pathlib

from .const import BASE_API_URL


def create_mock(mock_aio, url, filename, status=200, repeat=False):
    """Create a mock."""

    mock_aio.get(
        f"{BASE_API_URL}{url}",
        status=status,
        body=load_json_txt(f"../data/{filename}"),
        repeat=repeat,
    )


def create_update_mock(mock_aio, method, url, filename, status=200, repeat=False):
    """Create a mock."""

    if method == "put":
        mock_aio.put(
            f"{BASE_API_URL}{url}",
            status=status,
            body=load_json_txt(f"../data/{filename}"),
            repeat=repeat,
        )
    else:
        mock_aio.delete(
            f"{BASE_API_URL}{url}",
            status=status,
            body=load_json_txt(f"../data/{filename}"),
            repeat=repeat,
        )


def load_json_txt(filename):
    """Load a json file as string."""
    return pathlib.Path(__file__).parent.joinpath(filename).read_text(encoding="utf8")

import json
from urllib.request import urlopen


def extract_api(url: str):
    with urlopen(url, timeout=5) as response:
        if response.status != 200:
            raise RuntimeError(f"API returned HTTP {response.status}")
        return json.loads(response.read().decode("utf-8"))

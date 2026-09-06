#!/usr/bin/env python3
"""Materialize the exact public source tree from the verified UNS Vercel deployment."""
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import json
import shutil
import tempfile

BASE = "https://uns-website-1.vercel.app"
FILES = {
    "index.html": "/",
    "about/index.html": "/about/",
    "academics/index.html": "/academics/",
    "admissions/index.html": "/admissions/",
    "learning-options/index.html": "/learning-options/",
    "research/index.html": "/research/",
    "career-development/index.html": "/career-development/",
    "news-events/index.html": "/news-events/",
    "contact/index.html": "/contact/",
    "assets/styles.css": "/assets/styles.css",
    "assets/site.js": "/assets/site.js",
    "assets/uns-logo.jpg": "/assets/uns-logo.jpg",
    "assets/uns-map.png": "/assets/uns-map.png",
    "robots.txt": "/robots.txt",
    "sitemap.xml": "/sitemap.xml",
}

def download(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "UNS-source-sync/1.0"})
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}: {url}")
        data = response.read()
    if not data:
        raise RuntimeError(f"Empty response: {url}")
    return data

def main() -> None:
    root = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="uns-sync-") as temp:
        stage = Path(temp)
        manifest = {}
        for relative, route in FILES.items():
            data = download(BASE + route)
            destination = stage / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            manifest[relative] = {
                "source": BASE + route,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
            print(f"verified {relative} ({len(data)} bytes)")
        for relative in FILES:
            source = stage / relative
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        (root / "production-manifest.json").write_text(
            json.dumps({"source": BASE, "files": manifest}, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"Synchronized {len(FILES)} verified production files from {BASE}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the UNS static site from the verified production deployment and apply current integrations."""
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import json
import shutil

BASE = "https://uns-website-1.vercel.app"
FORM = "https://form.jotform.com/262473510150043"
OUT = Path("dist")
LEADERSHIP = '''<section class="section neutral" id="leadership"><div class="container"><div class="section-heading"><p class="eyebrow">University leadership</p><h2>Leadership team</h2><p>The officers serving the University of Northeastern Somalia.</p></div><div class="opportunity-grid"><article class="simple-card"><p class="eyebrow">President</p><h3>Prof. Abdiqani Ashkir</h3></article><article class="simple-card"><p class="eyebrow">Academic Director</p><h3>Abdulahi Mohamed Said</h3></article><article class="simple-card"><p class="eyebrow">Academic Advisor</p><h3>Abdulahi A. Hasan</h3></article><article class="simple-card"><p class="eyebrow">Operations Director</p><h3>Ahmed A. Osman</h3></article><article class="simple-card"><p class="eyebrow">Students Affairs Administrator</p><h3>Sakarie Abdulahi Said</h3></article></div></div></section>'''
FILES = {
    "index.html": "/", "about/index.html": "/about/", "academics/index.html": "/academics/",
    "admissions/index.html": "/admissions/", "learning-options/index.html": "/learning-options/",
    "research/index.html": "/research/", "career-development/index.html": "/career-development/",
    "news-events/index.html": "/news-events/", "contact/index.html": "/contact/",
    "assets/styles.css": "/assets/styles.css", "assets/site.js": "/assets/site.js",
    "assets/uns-logo.jpg": "/assets/uns-logo.jpg", "assets/uns-map.png": "/assets/uns-map.png",
    "robots.txt": "/robots.txt", "sitemap.xml": "/sitemap.xml",
}

def fetch(route: str) -> bytes:
    request = Request(BASE + route, headers={"User-Agent": "UNS-Vercel-build/1.0"})
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}: {BASE + route}")
        data = response.read()
    if not data:
        raise RuntimeError(f"Empty response: {BASE + route}")
    return data

def update_html(data: bytes, relative: str) -> bytes:
    text = data.decode("utf-8")
    text = text.replace('href="/admissions/#apply"', f'href="{FORM}"')
    if relative == "about/index.html" and 'id="leadership"' not in text:
        text = text.replace("</main>", LEADERSHIP + "</main>")
    if relative == "admissions/index.html":
        text = text.replace(
            "Contact the Admissions team to begin your application and confirm current requirements.",
            "Complete the official UNS online application form to begin your application.",
        )
        text = text.replace(
            '<a class="btn btn-gold" href="tel:0905265390">Call 0905265390</a><a class="btn btn-outline-light" href="mailto:info@uns.edu.so?subject=Undergraduate%20Application">Email Admissions</a>',
            f'<a class="btn btn-gold" href="{FORM}">Open Application Form</a><a class="btn btn-outline-light" href="tel:0905265390">Call 0905265390</a>',
        )
    return text.encode("utf-8")

def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    manifest = {}
    form_links = 0
    for relative, route in FILES.items():
        data = fetch(route)
        if relative.endswith(".html"):
            data = update_html(data, relative)
            text = data.decode("utf-8")
            if '/admissions/#apply' in text or 'Undergraduate%20Application' in text:
                raise RuntimeError(f"Legacy application link remains in {relative}")
            form_links += text.count(FORM)
        destination = OUT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        manifest[relative] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    if form_links != 56:
        raise RuntimeError(f"Expected 56 application form links, found {form_links}")
    about = (OUT / "about/index.html").read_text()
    leadership_names = ["Prof. Abdiqani Ashkir", "Abdulahi Mohamed Said", "Abdulahi A. Hasan", "Ahmed A. Osman", "Sakarie Abdulahi Said"]
    if about.count('id="leadership"') != 1 or any(about.count(name) != 1 for name in leadership_names):
        raise RuntimeError("Leadership section validation failed")
    (OUT / "production-manifest.json").write_text(
        json.dumps({"source": BASE, "applicationForm": FORM, "formLinks": form_links, "files": manifest}, indent=2) + "\n"
    )
    print(f"Built {len(FILES)} files with {form_links} application-form links and 5 leadership profiles")

if __name__ == "__main__":
    main()

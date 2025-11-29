import requests
import json
from pathlib import Path
from typing import List, Tuple


def download_wikipedia_page(title: str, lang: str, save_dir: Path) -> bool:
    """
    Download a clean plaintext version of a Wikipedia article.

    Args:
        title: Page title (e.g. "Paella", "España", "대한민국")
        lang:  Language code (es, he, ja, ko)
        save_dir: Folder where .txt and .meta.json will be saved

    Returns:
        True if download succeeded, False otherwise.
    """

    api_url = f"https://{lang}.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "titles": title,
        "format": "json",
    }

    headers = {
        # MediaWiki requires a valid User-Agent for automated scripts
        "User-Agent": "anote-benchmark-bot/0.1 (student project; youremail@example.com)"
    }

    print(f"[{lang}] Requesting: {title}")

    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=15)
    except Exception as e:
        print(f"   ❌ Network error: {e}")
        return False

    if response.status_code != 200:
        print(f"   ❌ HTTP {response.status_code}")
        print(f"   {response.text[:200]}")
        return False

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("   ❌ Response was not valid JSON. First 200 chars:")
        print("   " + response.text[:200].replace("\n", " ") + " ...")
        return False

    if "query" not in data or "pages" not in data["query"]:
        print("   ❌ Wikipedia JSON missing expected fields.")
        return False

    pages = data["query"]["pages"]
    page = next(iter(pages.values()))

    if "missing" in page or "extract" not in page:
        print(f"   ❌ Article not found: {title}")
        return False

    text = page["extract"].strip()

    if not text:
        print("   ❌ Article text empty.")
        return False

    # Make folder
    save_dir.mkdir(parents=True, exist_ok=True)

    safe_title = title.replace(" ", "_")
    txt_path = save_dir / f"{safe_title}.txt"
    meta_path = save_dir / f"{safe_title}.meta.json"

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    metadata = {
        "title": title,
        "url": f"https://{lang}.wikipedia.org/wiki/{safe_title}",
        "section": "Full Article",
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"   ✅ Saved text: {txt_path}")
    print(f"   ✅ Saved metadata: {meta_path}")

    return True


def batch_download_for_language(lang: str, titles: List[str], base_dir: Path):
    """
    Download multiple Wikipedia pages for a single language.
    Automatically saves to data/raw/benchmark/<lang>/
    """
    save_dir = base_dir / lang
    print(f"\n=== Downloading {lang} pages ===")

    success = 0
    for title in titles:
        ok = download_wikipedia_page(title, lang, save_dir)
        if ok:
            success += 1

    print(f"[{lang}] Finished: {success}/{len(titles)} downloaded.\n")


def main():
    """
    Modify the list of article titles here.
    These are demo lists you can replace with your own.
    """

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    input_base = project_root / "data" / "raw" / "benchmark"

    # Example titles (customize as needed)
    es_titles = ["Paella", "España", "Inteligencia_artificial"]
    ja_titles = ["日本", "東京", "機械学習"]
    ko_titles = ["대한민국", "서울", "인공지능"]
    he_titles = ["ישראל", "ירושלים", "בינה מלאכותית"]

    input_base.mkdir(parents=True, exist_ok=True)

    batch_download_for_language("es", es_titles, input_base)
    batch_download_for_language("ja", ja_titles, input_base)
    batch_download_for_language("ko", ko_titles, input_base)
    batch_download_for_language("he", he_titles, input_base)

    print("All downloads attempted.")


if __name__ == "__main__":
    main()

import requests
import json
from pathlib import Path
from typing import List


MIN_CHARS = 500  # skip tiny pages


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
        "redirects": True,   # follow redirects like 서울 → 서울특별시
        "format": "json",
    }

    headers = {
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
        print("   ❌ Response not valid JSON:")
        print("   " + response.text[:200].replace("\n", " ") + " ...")
        return False

    if "query" not in data or "pages" not in data["query"]:
        print("   ❌ JSON missing 'query/pages'")
        return False

    pages = data["query"]["pages"]
    page = next(iter(pages.values()))

    if "missing" in page or "extract" not in page:
        print(f"   ❌ Article missing or has no extract")
        return False

    text = page["extract"].strip()
    if not text:
        print("   ❌ Article text empty.")
        return False

    if len(text) < MIN_CHARS:
        print(f"   ⚠ Skipping: too short ({len(text)} chars)")
        return False

    save_dir.mkdir(parents=True, exist_ok=True)

    safe_title = title.replace(" ", "_")
    txt_path = save_dir / f"{safe_title}.txt"
    meta_path = save_dir / f"{safe_title}.meta.json"

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    final_title = page.get("title", title)  # resolved canonical title

    metadata = {
        "title": final_title,
        "url": f"https://{lang}.wikipedia.org/wiki/{safe_title}",
        "section": "Full Article",
        "original_query_title": title,
        "char_length": len(text),
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"   ✅ Saved text ({len(text)} chars)")
    print(f"   ✅ {txt_path.name}")
    return True


def batch_download_for_language(lang: str, titles: List[str], base_dir: Path):
    """
    Download multiple Wikipedia pages for a single language.
    Saves to data/raw/benchmark/<lang>/
    """

    save_dir = base_dir / lang
    print(f"\n=== Downloading {lang} pages ===")
    print(f"Target folder: {save_dir}\n")

    success = 0
    for title in titles:
        ok = download_wikipedia_page(title, lang, save_dir)
        if ok:
            success += 1

    print(f"[{lang}] Finished: {success}/{len(titles)} downloaded.\n")


def get_es_titles() -> List[str]:
    return [
        "España",
        "Madrid",
        "Barcelona",
        "América_Latina",
        "Inteligencia_artificial",
        "Aprendizaje_automático",
        "Red_neuronal_artificial",
        "Cambio_climático",
        "Energía_renovable",
        "Revolución_industrial",
        "Guerra_Civil_Española",
        "Miguel_de_Cervantes",
        "Gabriel_García_Márquez",
        "Internet",
        "Computadora",
        "Lengua_española",
        "Cultura_de_México",
        "Literatura_española",
        "Economía_de_España",
        "Derechos_humanos",
        "COVID-19",
        "Sistema_solar",
        "Teoría_de_la_relatividad",
        "Psicología",
        "Democracia",
    ]


def get_ja_titles() -> List[str]:
    return [
        "日本",
        "東京",
        "大阪市",
        "京都市",
        "日本語",
        "日本文化",
        "日本の歴史",
        "第二次世界大戦",
        "人工知能",
        "機械学習",
        "ニューラルネットワーク",
        "インターネット",
        "コンピュータ",
        "気候変動",
        "再生可能エネルギー",
        "経済学",
        "心理学",
        "相対性理論",
        "宇宙",
        "太陽系",
        "茶道",
        "寿司",
        "アニメ",
        "マンガ",
        "日本文学",
    ]


def get_ko_titles() -> List[str]:
    return [
        "대한민국",
        "서울특별시",
        "부산광역시",
        "한국어",
        "한국의_문화",
        "한국사",
        "조선_왕조",
        "일제강점기",
        "인공지능",
        "기계_학습",
        "신경망",
        "인터넷",
        "컴퓨터",
        "기후_변화",
        "재생_에너지",
        "경제학",
        "심리학",
        "상대성이론",
        "태양계",
        "우주",
        "한식",
        "김치",
        "케이팝",
        "한국_문학",
        "민주주의",
    ]


def get_he_titles() -> List[str]:
    return [
        "ישראל",
        "ירושלים",
        "תל_אביב-יפו",
        "העברית",
        "תרבות_ישראל",
        "היסטוריה_של_ישראל",
        "השואה",
        "מלחמת_יום_הכיפורים",
        "בינה_מלאכותית",
        "למידה_ממוחשבת",
        "רשת_עצבית",
        "האינטרנט",
        "מחשב",
        "שינוי_אקלימי",
        "אנרגיה_מתחדשת",
        "כלכלה",
        "פסיכולוגיה",
        "תורת_היחסות",
        "מערכת_השמש",
        "היקום",
        "היהדות",
        "תנ\"ך",
        "ספרות_עברית",
        "דמוקרטיה",
        "זכויות_האדם",
    ]


def main():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    input_base = project_root / "data" / "raw" / "benchmark"
    input_base.mkdir(parents=True, exist_ok=True)

    es_titles = get_es_titles()
    ja_titles = get_ja_titles()
    ko_titles = get_ko_titles()
    he_titles = get_he_titles()

    batch_download_for_language("es", es_titles, input_base)
    batch_download_for_language("ja", ja_titles, input_base)
    batch_download_for_language("ko", ko_titles, input_base)
    batch_download_for_language("he", he_titles, input_base)

    print("All batch downloads attempted.")


if __name__ == "__main__":
    main()

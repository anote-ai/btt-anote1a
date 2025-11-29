"""
Multilingual Benchmark Dataset Creation (Step 2)

This script:
- Loads raw benchmark text files for Spanish, Hebrew, Japanese, Korean
- Cleans web/HTML junk
- Splits text into overlapping paragraph/sentence chunks
- Adds citation metadata (title, section, URL)
- Outputs one JSONL file per language for downstream QA generation
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple



# Text cleaning

class TextCleaner:
    """
    Web text cleaner.

    Removes:
    - URLs
    - HTML tags
    - simple nav/boilerplate phrases
    - HTML entities (&amp; etc.)
    - very short lines
    """

    def __init__(self) -> None:
        self.web_junk_patterns = {
            "urls": re.compile(r"https?://[^\s<>" r"{}|\\^`\[\]]+"),
            "email": re.compile(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
            ),
            "html_tags": re.compile(r"<[^>]+>"),
            "extra_spaces": re.compile(r"\s+"),
            "extra_newlines": re.compile(r"\n\s*\n\s*\n+"),
            "nav_junk": re.compile(
                r"(Sign up|Sign in|Follow|Listen|Share|Write|Search|Cookie Policy|"
                r"Privacy Policy|Terms of Service)",
                re.IGNORECASE,
            ),
        }

    def clean_text(self, raw_text: str) -> str:
        if not raw_text or not raw_text.strip():
            return ""

        text = raw_text

        # Remove URLs and HTML tags
        text = self.web_junk_patterns["urls"].sub(" ", text)
        text = self.web_junk_patterns["html_tags"].sub(" ", text)

        # Remove generic navigation / boilerplate junk
        text = self.web_junk_patterns["nav_junk"].sub(" ", text)

        # Drop HTML entities like &amp;
        text = re.sub(r"&[a-zA-Z0-9#]+;", " ", text)

        # Remove escaped characters like \n \t \r if present literally
        text = re.sub(r"\\[rnt]", " ", text)

        # Drop common boilerplate phrases
        junk_phrases = [
            r".*sitemap.*",
            r".*cookie policy.*",
            r".*privacy policy.*",
            r".*terms of service.*",
            r".*all rights reserved.*",
            r".*copyright.*",
            r".*subscribe.*newsletter.*",
            r".*follow us on.*",
        ]
        for pattern in junk_phrases:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        # Normalize whitespace
        text = self.web_junk_patterns["extra_spaces"].sub(" ", text)
        text = self.web_junk_patterns["extra_newlines"].sub("\n\n", text)

        # Filter out extremely short / punctuation-only lines
        lines = text.split("\n")
        clean_lines: List[str] = []
        for line in lines:
            line = line.strip()
            if len(line) > 10 and not re.match(r"^[^\w]*$", line):
                clean_lines.append(line)

        text = "\n".join(clean_lines)
        return text.strip()

# Chunking

class TextChunker:
    """
    Split text into overlapping chunks.

    """

    def __init__(self, chunk_size: int = 500, overlap: int = 150) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_into_chunks(self, text: str) -> List[str]:
        if len(text) < 50:
            return []

        # Split on blank-line paragraphs
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        if not paragraphs:
            return self._split_by_sentences(text)

        chunks: List[str] = []
        current_chunk = ""

        for paragraph in paragraphs:
            # Very large paragraph: handle via sentence splitting
            if len(paragraph) > self.chunk_size:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                big_chunks = self._split_by_sentences(paragraph)
                chunks.extend(big_chunks)
                continue

            # Would this paragraph overflow the chunk?
            if len(current_chunk + paragraph) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                overlap_text = self._get_overlap(current_chunk)
                current_chunk = overlap_text + paragraph + "\n\n"
            else:
                current_chunk += paragraph + "\n\n"

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # Filter trivially short chunks
        good_chunks = [c for c in chunks if len(c.strip()) > 50]
        return good_chunks

    def _split_by_sentences(self, text: str) -> List[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks: List[str] = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk + sentence) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                overlap_text = self._get_overlap(current_chunk)
                current_chunk = overlap_text + sentence + " "
            else:
                current_chunk += sentence + " "

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _get_overlap(self, text: str) -> str:
        if len(text) <= self.overlap:
            return text + " "
        return text[-self.overlap :] + " "


# Benchmark-specific processing

class BenchmarkDataProcessing:
    """
    Pipeline for one language:

    - Read all .txt files in input_folder
    - Clean text
    - Chunk text
    - Attach citation metadata (title/section/url)
    - Write JSONL with one record per chunk
    """

    def __init__(self, input_folder: Path, output_file: Path, lang: str) -> None:
        self.input_folder = input_folder
        self.output_file = output_file
        self.lang = lang
        self.cleaner = TextCleaner()
        self.chunker = TextChunker()

        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        print(f"[{lang}] Input folder:  {self.input_folder}")
        print(f"[{lang}] Output file:   {self.output_file}")

    # Top-level runner 
    def run_pipeline(self) -> Dict[str, int]:
        stats: Dict[str, int] = {
            "files_found": 0,
            "files_processed": 0,
            "total_chunks": 0,
            "files_skipped": 0,
            "errors": 0,
        }

        txt_files = list(self.input_folder.glob("**/*.txt"))
        stats["files_found"] = len(txt_files)

        if not txt_files:
            print(f"[{self.lang}] No .txt files found.")
            return stats

        print(f"[{self.lang}] Found {len(txt_files)} .txt files.\n")

        with open(self.output_file, "w", encoding="utf-8") as out_f:
            for i, file_path in enumerate(txt_files, 1):
                print(f"[{self.lang}] {i}/{len(txt_files)}: {file_path.name}")
                try:
                    chunks = self._process_single_file(file_path)
                    if chunks:
                        for chunk in chunks:
                            out_f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                        stats["files_processed"] += 1
                        stats["total_chunks"] += len(chunks)
                        print(f"    -> {len(chunks)} chunks written")
                    else:
                        stats["files_skipped"] += 1
                        print("    -> skipped (no useful content)")
                except Exception as e:
                    stats["errors"] += 1
                    print(f"    -> ERROR: {e}")
                print()

        return stats

    # Per-file processing 
    def _process_single_file(self, file_path: Path) -> List[Dict]:
        # 1) Read file (try several encodings)
        file_content: Optional[str] = None
        encodings_to_try = ["utf-8", "utf-8-sig", "latin1", "cp1252"]

        for enc in encodings_to_try:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    file_content = f.read()
                break
            except UnicodeDecodeError:
                continue

        if file_content is None:
            raise Exception("Could not read file (encoding issue)")

        if not file_content.strip():
            return []

        # 2) Clean
        clean_text = self.cleaner.clean_text(file_content)
        if len(clean_text.strip()) < 50:
            return []

        # 3) Chunk
        chunks = self.chunker.split_into_chunks(clean_text)
        if not chunks:
            return []

        # 4) Metadata (title/section/url)
        meta_title, meta_section, meta_url = self._load_metadata_for_file(file_path)

        title = meta_title or file_path.stem
        base_section = meta_section  # may be None
        doc_id = self._make_doc_id(title)
        source_rel = str(file_path.as_posix())

        chunk_objects: List[Dict] = []
        for idx, chunk_text in enumerate(chunks):
            chunk_id = f"{self.lang}_{doc_id}_{idx:04d}"

            chunk_obj: Dict = {
                "id": chunk_id,
                "lang": self.lang,
                "doc_id": doc_id,
                "chunk_index": idx,
                "text": chunk_text,
                "source": source_rel,
                "citation": {
                    "title": title,
                    # You can later replace this with real section names
                    "section": base_section or f"chunk_{idx}",
                    "url": meta_url,
                },
            }
            chunk_objects.append(chunk_obj)

        return chunk_objects

    # Helper: load .meta.json sidecar if present 
    def _load_metadata_for_file(
        self, file_path: Path
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        If a sidecar metadata file exists, e.g.:

            article1.txt
            article1.meta.json

        with JSON like:
            {
              "title": "Wikipedia: Something",
              "url": "https://es.wikipedia.org/...",
              "section": "History"
            }

        we will use these values in the citation block.
        """
        meta_path = file_path.with_suffix(".meta.json")
        if meta_path.exists():
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                title = meta.get("title")
                section = meta.get("section")
                url = meta.get("url")
                return title, section, url
            except Exception:
                # If anything goes wrong, just fall back to defaults
                pass
        return None, None, None

    # Helper: normalize a doc_id from title 
    @staticmethod
    def _make_doc_id(title: str) -> str:
        doc_id = re.sub(r"[^A-Za-z0-9]+", "-", title).strip("-").lower()
        return doc_id or "doc"



# Main for all four languages

def main() -> None:
    # Infer project root (folder that contains src/ and data/)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    # Where raw benchmark data lives
    input_base = project_root / "data" / "raw" / "benchmark"
    # Where processed chunks will be saved
    output_base = project_root / "data" / "processed" / "benchmark_chunks"

    languages = ["es", "he", "ja", "ko"]

    print(f"Project root: {project_root}")
    print(f"Input base:   {input_base}")
    print(f"Output base:  {output_base}\n")

    for lang in languages:
        lang_input = input_base / lang
        lang_output = output_base / f"benchmark_{lang}.jsonl"

        if not lang_input.exists():
            print(f"[{lang}] WARNING: {lang_input} does not exist, skipping.\n")
            continue

        processor = BenchmarkDataProcessing(lang_input, lang_output, lang)
        stats = processor.run_pipeline()

        print(f"[{lang}] Summary:")
        print(f"   Files found:      {stats['files_found']}")
        print(f"   Files processed:  {stats['files_processed']}")
        print(f"   Total chunks:     {stats['total_chunks']}")
        print(f"   Files skipped:    {stats['files_skipped']}")
        print(f"   Errors:           {stats['errors']}")
        print("-" * 50 + "\n")

    print("All languages processed (where input folders existed).")


if __name__ == "__main__":
    main()

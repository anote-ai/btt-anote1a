import os
import re
import json
import hashlib
from pathlib import Path
from typing import List, Dict

# Cleaner class
class TextCleaner:

    def __init__(self):

        # Regex patterns commonly found in "web junk" and specifically for Medium Articles
        self.web_junk_patterns = {
            'urls': re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+'),
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'html_tags': re.compile(r'<[^>]+>'),
            'extra_spaces': re.compile(r'\s+'),
            'extra_newlines': re.compile(r'\n\s*\n\s*\n+'),
            'medium_artifacts': re.compile(r'(Sign up|Sign in|Follow|Listen|Share|Write|Search|Medium Logo)', re.IGNORECASE)
        }

    def clean_text(self, raw_text: str) -> str:

        # Clean text func
        if not raw_text or not raw_text.strip():
            return ""

        text = raw_text

        # Remove web junk
        print("Removing web junk...")
        text = self.web_junk_patterns['urls'].sub(' ', text)
        text = self.web_junk_patterns['html_tags'].sub(' ', text)

        # Remove Medium navigation junk
        text = self.web_junk_patterns['medium_artifacts'].sub('', text)

        # Clean common entities
        text = re.sub(r'&[a-zA-Z0-9#]+;', ' ', text)  # HTML entities like &amp;
        text = re.sub(r'\\[rnt]', ' ', text)  # Escaped characters

        # Clean irrelevant content
        junk_phrases = [
            r'.*sitemap.*',
            r'.*open in app.*',
            r'.*cookie policy.*',
            r'.*privacy policy.*',
            r'.*terms of service.*',
            r'.*all rights reserved.*',
            r'.*copyright.*',
            r'.*subscribe.*newsletter.*',
            r'.*follow us on.*',
        ]

        for pattern in junk_phrases:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        # Clean up whitespace
        text = self.web_junk_patterns['extra_spaces'].sub(' ', text)
        text = self.web_junk_patterns['extra_newlines'].sub('\n\n', text)

        # Clean short/meaningless lines
        lines = text.split('\n')
        clean_lines = []
        for line in lines:
            line = line.strip()
            if len(line) > 10 and not re.match(r'^[^\w]*$', line):  # Skip lines with just punctuation
                clean_lines.append(line)

        text = '\n'.join(clean_lines)

        return text.strip()

# Chunk maker class
class TextChunker:

    def __init__(self, chunk_size=500, overlap=150):

        self.chunk_size = chunk_size    # How long each chunk should be
        self.overlap = overlap          # How much chunks should overlap

    def split_into_chunks(self, text: str) -> List[str]:

        if len(text) < 50:  # Skip tiny texts
            return []

        # Split paragraphs first
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        # Otherwise split via sentences
        if not paragraphs:
            return self._split_by_sentences(text)

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:

            # If this paragraph is bigger than chunk size, split it up
            if len(paragraph) > self.chunk_size:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                    current_chunk = ""

                big_chunks = self._split_by_sentences(paragraph)
                chunks.extend(big_chunks)
                continue

            # If adding paragraph would make chunk too large for RAG...
            if len(current_chunk + paragraph) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())

                # Then we start new chunk w overlap from previous
                overlap_text = self._get_overlap(current_chunk)
                current_chunk = overlap_text + paragraph + "\n\n"
            else:
                current_chunk += paragraph + "\n\n"

        # Final chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # Filtering out chunks that would be bad for RAG
        good_chunks = [chunk for chunk in chunks if len(chunk.strip()) > 50]

        # Returning the good chunks we want to use for our embeddings
        return good_chunks

    def _split_by_sentences(self, text: str) -> List[str]:

        # When splitting via paragraph does not work, split via sentence
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
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

        # Overlap chunks
        if len(text) <= self.overlap:
            return text + " "
        return text[-self.overlap:] + " "

# Driver class for cleaning and chunking pipeline
class DataProcessing:

    def __init__(self, input_folder: str, output_file: str):
        self.input_folder = Path(input_folder)
        self.output_file = Path(output_file)
        self.cleaner = TextCleaner()
        self.chunker = TextChunker()

        # Make sure output folder exists
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        print(f"For files in: {self.input_folder}")
        print(f"Save results to: {self.output_file}")

    # Cleaning pipeline
    def run_pipeline(self) -> Dict[str, int]:

        # To provide more info on the data processing during execution to confirm it works
        stats = {
            "files_found": 0,
            "files_processed": 0,
            "total_chunks": 0,
            "files_skipped": 0,
            "errors": 0
        }

        # Get all .txt files
        txt_files = list(self.input_folder.glob("**/*.txt"))
        stats["files_found"] = len(txt_files)

        if not txt_files:
            print("No .txt files found, check the input folder path.")
            return stats

        # Helper messages
        print(f"Found {len(txt_files)} .txt files to process!")
        print("Starting the cleaning process...\n")

        # Process each file
        with open(self.output_file, 'w', encoding='utf-8') as output:
            for i, file_path in enumerate(txt_files, 1):

                print(f"Processing file {i}/{len(txt_files)}: {file_path.name}")
                try:
                    chunks = self._process_single_file(file_path)
                    if chunks:

                        # Write each chunk to the output file
                        for chunk in chunks:
                            output.write(json.dumps(chunk, ensure_ascii=False) + '\n')

                        # Increment stats
                        stats["files_processed"] += 1
                        stats["total_chunks"] += len(chunks)
                        print(f"Successfully created {len(chunks)} chunks")
                    else:
                        stats["files_skipped"] += 1
                        print(f"Skipped (no useful content)")

                except Exception as e:
                    stats["errors"] += 1
                    print(f"Error: {str(e)}")
                print()

        # Return stats to see how the cleaner did (and verify any errors)
        return stats

    def _process_single_file(self, file_path: Path) -> List[Dict[str, str]]:

        # Step 1: Read the file (DEBUG: trying diff encodings)
        print("Reading file...")
        encodings_to_try = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
        file_content = None

        for encoding in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    file_content = f.read()
                print(f"Successfully read with {encoding} encoding")    # DEBUG:
                break
            except UnicodeDecodeError:
                continue

        if file_content is None:                                        # DEBUG:
            raise Exception("Could not read file: encoding")

        # Empty file
        if not file_content.strip():
            return []

        # Clean the text in the file
        print("Cleaning text...")
        clean_text = self.cleaner.clean_text(file_content)

        # Too short to be useful for RAG
        if len(clean_text.strip()) < 50:
            return []

        # Split into chunks
        print("Splitting into chunks...")
        chunks = self.chunker.split_into_chunks(clean_text)

        # Step 4: Create the final chunk objects for JSONL output
        print("Creating chunk objects...")
        chunk_objects = []

        for i, chunk_text in enumerate(chunks):

            # Derive metadata for chunk obj
            title = file_path.stem
            doc_id = re.sub(r"[^A-Za-z0-9]+", "-", title).strip("-").lower() or "doc"
            source_rel = str(file_path.as_posix())

            chunk_object = {
                "doc_id": doc_id,
                "source": source_rel,
                "chunk_index": i,
                "title": title,
                "text": chunk_text,
            }
            chunk_objects.append(chunk_object)

        return chunk_objects

    def _create_chunk_id(self, filename: str, chunk_number: int, text: str) -> str:

        # Use first 8 characters of text hash to make ID unique
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]
        return f"{filename}_chunk_{chunk_number:03d}_{text_hash}"

# Main program
# EDIT PATH CONFIG HERE !!!!!!!!!!!
def main():

    # Config (EDIT FOR UR OWN ABSOLUTE PATHS IF RUNNING SCRIPT LOCALLY!)
    INPUT_FOLDER = r"C:\Users\Bella\btt-anote1a\data\raw"
    OUTPUT_FILE =  r"C:\Users\Bella\btt-anote1a\data\processed\clean_chunks.jsonl"

    # Create the processor obj and run it
    processor = DataProcessing(INPUT_FOLDER, OUTPUT_FILE)
    results = processor.run_pipeline()

    # Show results
    print("Processing complete!")
    print(f"Files found: {results['files_found']}")
    print(f"Files successfully processed: {results['files_processed']}")
    print(f"Total chunks created: {results['total_chunks']}")
    print(f"Files skipped: {results['files_skipped']}")
    print(f"Errors encountered: {results['errors']}")

    if results['total_chunks'] > 0:
        avg_chunks = results['total_chunks'] / max(results['files_processed'], 1)
        print(f"Average chunks per file: {avg_chunks:.1f}")
        print()
        print(f"Cleaned data ready for RAG embeddings availible at: {OUTPUT_FILE}")
    else:
        print("No chunks could be created, check input folder.")

if __name__ == "__main__":
    main()
# Translation Testing Dataset Card

## Dataset Description
A multilingual translation evaluation benchmark with 400 QA pairs across Spanish, Hebrew, Japanese, and Korean.

## Languages
- Spanish (es): 100 items
- Hebrew (he): 100 items
- Japanese (ja): 100 items
- Korean (ko): 100 items

## Dataset Structure
Each item contains:
- `question`: Natural language question
- `answer`: Expected answer
- `cite_from`: "source" or "target"
- `citation_text`: Exact text span
- `difficulty`: "easy" | "medium" | "hard"
- `question_type`: "factual" | "reasoning" | "ambiguous"
- `register`: "formal" | "informal"
- `model`: Generation model (chatgpt/claude/gemini)

## Intended Use
- Evaluating LLM translation understanding
- Benchmarking multilingual reasoning
- Translation quality assessment

## Limitations
- Generated from synthetic translation pairs
- Limited to 4 languages
- Model-generated ground truth

## Citation
[Your team/project citation info]
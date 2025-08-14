# Anote - Break Through Tech 1A

## Languages Learning Resources
**Videos:**
- [Personalized Chatbots for Languages and Companies – Arya Sinha](https://www.youtube.com/watch?v=1BU1_Ii4SVQ)
- [Evaluating Multilingual LLM Performance – Angela Bai](https://www.youtube.com/watch?v=FisQu6RqyEI)
- [Fine Tuning LLMs for Languages – Rebecca Frey](https://www.youtube.com/watch?v=Mk3opMRlWcU)
- [Found in Translation Project – Arya, Angela & Rebecca](https://www.youtube.com/watch?v=w9f9LZhzFuw&t=490s)

**Anote Website:**
[https://anote.ai/languages](https://anote.ai/languages)


**Example working product:**
[https://dashboard.privatechatbot.ai/languages/spanish](https://dashboard.privatechatbot.ai/languages/spanish)


**Codebase with existing working code:**
[https://github.com/nv78/Autonomous-Intelligence](https://github.com/nv78/Autonomous-Intelligence)


# Project: Language Model Evaluation and Build Your Own Fine Tuned Chatbot Enhancement

## **Overview**
This project focuses on **exploring and improving AI language and translation models** through:

- **Synthetic evaluation dataset creation**
- **Benchmark development**
- **Integration into customized chatbots**
The aim is to **assess and compare** language and translation models (e.g., ChatGPT, Claude, Llama) and deploy the **best-performing models** into user-facing applications.
Special focus will be on **language-specific optimization** for **Chinese, Korean, Japanese, and Hebrew** to meet potential client needs.
---

## **Project Concept**
- Users can choose between a **"language"** model (chat experience) or a **"translation"** model.
- Models will be embedded into a **chatbot** or API.
- Synthetic evaluation datasets will be generated (similar to the [Anote Model Leaderboard](https://anote.ai/leaderboard) or [Scale’s SEAL leaderboard](https://scale.com/leaderboard)).
- Model performance will be evaluated on these datasets, and the **best model** will be routed into the chatbot.

---

## **Goals**
By the end of the project, we aim to:
1. **Create synthetic datasets** for evaluation.
2. **Build language-specific and/or universal benchmarks** for conversation and translation quality.
3. **Fine-tune chatbots** for different languages, integrating Anote’s document analysis capabilities.
4. **Integrate evaluation datasets** into the **model leaderboard**.
5. Deliver:
   - A **fine-tuned chatbot** for specific languages or translation tasks.
   - Corresponding benchmark datasets posted to the leaderboard.
   - **Writeup** and **final presentation**.

---

## **Step 1 (Week 1): Fine-Tune Chatbot on Anote Data**

### **1. Data Collection**
Sources:
- [https://anote.ai/](https://anote.ai/)
- [https://docs.anote.ai/](https://docs.anote.ai/)
- [Google Drive Folder](https://drive.google.com/drive/folders/1RonBrEWV4sxVr7Cdd2uYc6xK6UZfQIMK)
- [Medium Article](https://anote-ai.medium.com/anotes-ai-platform-excels-in-rigorous-nist-and-humane-intelligence-red-team-evaluation-c74e2b112d5a)

### **2. Preprocessing**
- Remove HTML boilerplate, ads, irrelevant content.
- Clean formatting in HTML/PDF/Markdown.
- Structure into Q&A pairs or contextual sections.

### **3. Model Fine-Tuning or RAG Setup**
- Choose between **fine-tuning** or **Retrieval-Augmented Generation (RAG)**.
- Prepare training data in JSONL format.
- Train or configure chatbot at:
  [http://chat.anote.ai/organizations/anote](http://chat.anote.ai/organizations/anote)

**Evaluation metrics:** [Example](https://docs.anote.ai/api-prompting/example8.html)

**Example URL after deployment:**
- `chat.anote.ai/organizations/anote`
- Future: `chat.anote.ai/language/japanese`

### **4. Output**
- A fine-tuned Anote chatbot accessible via a custom URL.

---

## **Next Steps After Initial PR (06/23/25)**

### **1. Languages Tab**
- Route: `/languages/:language`
- Show chatbot for that language.

### **2. Companies Tab**
- Route: `/organizations/:company`
- Show company-specific chatbot.

### **3. Models Tab**
- List fine-tuned models with download buttons and setup instructions.

### **4. Evaluations Tab**
- Show synthetic evaluation datasets.
- Display leaderboard with performance scores.

### **5. Backend & Database**
- Update `db.py` and schema to support languages, companies, models.

### **6. Code Cleanup**
- Create a clean branch (remove `.env`, temp files, etc.).

---

## **Step 2 (Week 2): Multilingual Benchmark Dataset Creation**

**Languages:** Spanish, Korean, Japanese, Hebrew

### **1. Data Curation Sources**
- Wikipedia (per language)
- Open-access books/reports
- AIHub (Korean)
- Kyoto Corpus (Japanese)
- Open-licensed news sites

### **2. Preprocessing**
- Clean text, remove ads/tags.
- Break into chunks by paragraph or section.
- Add citation metadata (title, section, URL).

### **3. Testing Dataset Creation**
- Use multilingual LLM to create **QA-citation pairs**.
- Include:
  - Factual
  - Reasoning-based
  - Ambiguous/challenging questions

**Reference:** Lutra.ai Benchmark Creator

---

## **Step 3: Translation Task Dataset Creation**
- Repeat the dataset creation process for **translation tasks**.
- Include varied difficulty and formal/informal registers.

---

## **Step 4: Integration into Anote Codebase**
- Reference:
  - [GTM Chatbot Folder] within Anote Product Repo
  - [Backend SDK Docs](https://docs.anote.ai/api-overview/chat.html)
  - Example repo with starter code: [Autonomous Intelligence GitHub](https://github.com/nv78/Autonomous-Intelligence)


## **Key Questions**
- **RAG vs. Unsupervised Fine-Tuning** — Evaluate tradeoffs.
- **Uploading Websites vs. Documents** — Determine ingestion best practices.

# Social Support AI Workflow

AI-powered workflow for assessing social support eligibility and providing economic enablement suggestions. This system
streamlines the assessment process, automates eligibility checks, and provides actionable recommendations for
applicants.

---

## Requirements

- Python 3.10+
- [Ollama LLM](https://ollama.com/) (e.g., `gemma3:4b` model)
- Docker (optional, for containerized deployment)

---

## Installation & Run

### Direct App Run

```bash
cd social_support_ai_app
pip install -r requirements.txt
ollama run gemma3:4b
streamlit run ui/chat_app.py
```

### Docker App Run

```bash
cd social_support_ai_app
ollama run gemma3:4b
docker build -t social-support-ai:latest .
docker run -it -p 8501:8501 -e OLLAMA_BASE=http://host.docker.internal:11434 social-support-ai:latest
```

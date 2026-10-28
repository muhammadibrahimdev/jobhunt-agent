# AI Job Matcher

## What it does

AI Job Matcher compares your CV with a job description using an LLM and produces a match score out of 100, matched skills, missing skills, strengths, and a short explanation. You can analyze one job at a time or process multiple job-description text files in a batch and export the results to a CSV file. The goal is to help you assess how closely your current CV aligns with a role and identify skills or experience to improve.

## How to run it

### 1. Requirements

- Python 3.10 or newer
- A Groq API key
- Job descriptions saved as `.txt` files

### 2. Install dependencies

Create and activate a virtual environment if you want to isolate the project dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install the packages used by your project. For example, if `llm.py` uses the OpenAI-compatible Groq API and `python-dotenv`:

```bash
pip install openai python-dotenv
```

If your project has a `requirements.txt`, install from it instead:

```bash
pip install -r requirements.txt
```

### 3. Configure `.env`

Create a file named `.env` in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Load the key in your code with `python-dotenv`, and make sure `llm.py` uses the Groq API and the model `openai/gpt-oss-20b`.

**Security:** Never commit `.env` or your API key to GitHub. Add `.env` to `.gitignore`.

### 4. Add your CV and job descriptions

Keep your CV in the file expected by `read_cv()` (for example, `cv.txt`). Save the job description you want to analyze as `job.txt`.

For batch processing, put your job-description files in a `jobs/` folder, for example:

```text
jobs/
├── job1.txt
├── job2.txt
└── job3.txt
```

### 5. Run a single job match

```bash
python day5.py job.txt
```

This compares your CV with `job.txt` and prints a match report in the terminal.

### 6. Run batch matching

```bash
python batch.py
```

This processes the `.txt` files in `jobs/` and exports the results to `results.csv`. Make sure your batch script uses the same folder and CSV filename.

## Tech used

- **Python** — application logic and file processing
- **Groq API** — LLM inference
- **`openai/gpt-oss-20b`** — model used to evaluate CV-to-job alignment
- **CSV** — export batch matching results

## Roadmap

- [ ] Generate tailored CVs for individual job descriptions
- [ ] Generate role-specific cover letters
- [ ] Collect job listings from Gmail with user authorization
- [ ] Add LangGraph agents to coordinate multi-step job-search workflows
- [ ] Build a dashboard to review scores, matched skills, and missing skills

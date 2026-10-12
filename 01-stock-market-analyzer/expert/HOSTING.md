# Host your company chatbot (free, from GitHub)

You built `stock_chatbot.py`. Now put it online, so you can show it in an interview or
send the link to a friend. This guide gives you two free ways, both starting from your
GitHub repo:

| Way | What you get | Good for | Cost |
| --- | ------------ | -------- | ---- |
| **A. GitHub Codespaces** | Your repo opens in VS Code in the browser; you run the chatbot there | Running and demoing it from any PC, even without Python installed | Free: 120 core-hours a month (60 hours on the basic machine); verified students get 180 |
| **B. Streamlit Community Cloud** | A real **web chatbot** with its own link, like `https://your-name-chatbot.streamlit.app` | Sharing a link on your resume or LinkedIn | Free for public apps |

> **Why not GitHub Pages?** GitHub Pages only hosts static web pages. It cannot run
> Python, and a chatbot page would have to put your Gemini key inside the page, where
> anyone can copy it. Codespaces and Streamlit Cloud keep the key **secret** on the server.

Time: about **30 minutes**. You need a working chatbot (the [expert README](README.md))
and your free Gemini key.

---

## Step 0 — Put your project on GitHub (both ways need this)

1. In your project folder you need these files: `stock_trend.py`, `stock_chatbot.py`, and
   (for way B) `streamlit_app.py` and `requirements.txt`.
2. Make sure your key can **never** be uploaded. Ask Copilot (Agent mode):

   ```text
   Create a .gitignore that ignores .env, .streamlit/secrets.toml, *_trend.json,
   *_report.md and __pycache__/. Then create requirements.txt with: streamlit, yfinance,
   requests, beautifulsoup4, feedparser, openai, python-dotenv.
   ```
3. VS Code → **Source Control** panel → **Publish to GitHub** → choose **public** (Streamlit
   Cloud's free plan is for public repos).
4. **Before you confirm, check the file list: `.env` must NOT be in it.** If a key was ever
   pushed, delete that key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
   and make a new one. Deleting the file is not enough: it stays in the history.

---

## Way A — Run it in GitHub Codespaces

A Codespace is a computer in the cloud with your repo, VS Code and Python already set up.

1. **Save your key as a Codespaces secret** (so it is never in a file):
   GitHub → your profile picture → **Settings → Codespaces → Secrets → New secret**.
   Name: `GEMINI_API_KEY`, value: your key, **Repository access**: your chatbot repo.
   Add `LLM_PROVIDER` with value `gemini` the same way.
2. Open your repo on GitHub → green **Code** button → **Codespaces** tab →
   **Create codespace on main**. VS Code opens in the browser (the first time takes a
   minute or two).
3. In its terminal:

   ```bash
   pip install -r requirements.txt
   python stock_chatbot.py "Infosys"
   ```

   The secrets arrive as environment variables, and the script reads them just like it
   reads `.env`.
4. **The web version works here too:** run `streamlit run streamlit_app.py`. Codespaces
   shows a pop-up, **Open in Browser**, with a private link to your web chatbot.
5. **Stop the Codespace when you finish** (Code → Codespaces → ⋯ → **Stop codespace**):
   the free hours only count while it runs.

---

## Way B — A web chatbot on Streamlit Community Cloud

### B1. Make the web version

Streamlit turns a Python script into a web page. The web app **reuses** your
`stock_chatbot.py`, so the data, the news and the rules stay the same. Ask Copilot:

```text
Create streamlit_app.py: a web version of my company chatbot that imports and reuses
stock_chatbot.py (gather, system_prompt, make_client, chat_once, explain, PROVIDERS,
REPORT_REQUEST, MAX_TURNS). Requirements:
1. At the top, copy LLM_PROVIDER, GEMINI_API_KEY, GROQ_API_KEY, LLM_MODEL and
   APP_PASSWORD from st.secrets into os.environ (ignore errors if there are no secrets),
   BEFORE importing stock_chatbot.
2. If APP_PASSWORD is set, show a password box and stop until the right password is typed.
3. If the provider's key is missing, show a clear error and stop.
4. A form with a "Company name" box and a "Load company" button. Cache gather() with
   st.cache_data(ttl=900). Show the company name, three st.metric boxes (price with
   today's change, 1-year change, number of headlines), and the headlines in an expander.
5. A chat with st.chat_input and st.chat_message, the history in st.session_state; send
   the system prompt + the last MAX_TURNS questions and answers + the new question.
6. A "Write a 5-section report" button that sends REPORT_REQUEST.
7. Limit each visitor to 15 questions per session, with a friendly message.
8. A caption: "A learning project, not financial advice."
Then run it with: streamlit run streamlit_app.py
```

Reference solution: [`streamlit_app.py`](streamlit_app.py). Packages: [`requirements.txt`](requirements.txt).

### B2. Test it on your laptop first

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Your browser opens `http://localhost:8501`. It reads the key from your `.env`. Load
**Infosys**, ask *"What does this company do?"*, and try **Write a 5-section report**.

### B3. Deploy it

1. Push the new files to GitHub (Source Control → **Commit** → **Sync**).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and **sign in with GitHub**.
   Allow Streamlit to see your repos.
3. **Create app** → **Deploy a public app from GitHub**:
   - Repository: your chatbot repo · Branch: `main`
   - Main file path: `streamlit_app.py` (in this workshop repo it is
     `01-stock-market-analyzer/expert/streamlit_app.py`)
   - App URL: pick a name, for example `yourname-company-chatbot`
4. Open **Advanced settings → Secrets** and paste (TOML format, with quotes):

   ```toml
   LLM_PROVIDER = "gemini"
   GEMINI_API_KEY = "paste-your-key-here"
   APP_PASSWORD = "choose-a-password"
   ```
5. Click **Deploy**. After a few minutes your chatbot is live at
   `https://yourname-company-chatbot.streamlit.app`.

Every time you push a change to GitHub, the app updates by itself.

### B4. Protect your free key (read this)

Anyone with the link uses **your** Gemini key, and the free tier has a daily limit.

- Keep `APP_PASSWORD` set, and share the password only with people you choose
  (interviewers, friends). Without it, strangers could use up your limit.
- The app allows **15 questions per visitor session**. Lower `MAX_QUESTIONS` in
  `streamlit_app.py` if you need to.
- The key lives **only** in Streamlit's Secrets box, never in GitHub. To change the key:
  app → **⋮ → Settings → Secrets**.
- Free Streamlit apps **go to sleep** when nobody uses them for a while. The next visitor
  sees a "wake up" button; it starts again in under a minute.

---

## Done when

- Way A: `python stock_chatbot.py "Infosys"` answers you inside a Codespace, and the key is
  not in any file.
- Way B: your `*.streamlit.app` link asks for the password, loads Infosys and answers a
  question. Your repo on GitHub has **no** `.env` and **no** `secrets.toml`.
- Your GitHub README has the link and a screenshot: that is your portfolio piece.

## Common errors and fixes

| You see | Fix |
| ------- | --- |
| `GEMINI_API_KEY is not set` (Streamlit Cloud) | Add it under the app's **Settings → Secrets**, with quotes, then **Reboot app**. |
| `GEMINI_API_KEY is not set` (Codespaces) | The secret was added after the Codespace started, or not given access to this repo. Fix the secret, then stop and restart the Codespace. |
| `ModuleNotFoundError: No module named 'stock_trend'` | `stock_trend.py` and `stock_chatbot.py` must be in the same folder as `streamlit_app.py` in your repo. |
| `ModuleNotFoundError` for a package on Streamlit Cloud | Add it to `requirements.txt` in the **same folder** as the main file (or the repo root), push, and the app reinstalls. |
| The app is "in the oven" for a long time | The first deploy installs all packages; wait 3–5 minutes. Check **Manage app → logs** for errors. |
| News or prices are empty on the hosted app | Some sites limit requests from cloud servers. The bot still answers from the rest of the data; try again later. |
| `429` / free limit reached | Too many questions today, or by too many visitors. Wait, use Groq as a backup (`LLM_PROVIDER = "groq"` + `GROQ_API_KEY`), or set a password. |
| You pushed `.env` by mistake | Delete that key at aistudio.google.com/apikey **now** and create a new one. |

> Free plans and limits change. These were checked in October 2026: GitHub Codespaces
> [billing docs](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces)
> and [Streamlit Community Cloud](https://share.streamlit.io/). This is a learning project,
> not financial advice.

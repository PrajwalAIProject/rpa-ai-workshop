"""Project 1 - Expert: the company chatbot as a web app (Streamlit).

Reference solution for HOSTING.md. It reuses stock_chatbot.py, so the data, the news and
the rules are exactly the same as the command-line chatbot; only the screen is new.

Run on your laptop:
    pip install streamlit
    streamlit run streamlit_app.py
Host it for free: see HOSTING.md (Streamlit Community Cloud, deployed from GitHub).

Settings come from a .env file on your laptop, or from the app's Secrets on Streamlit
Community Cloud: LLM_PROVIDER, GEMINI_API_KEY (or GROQ_API_KEY), optional LLM_MODEL,
and optional APP_PASSWORD (recommended for a public link: only people with the password
can chat, so strangers can't use up your free key).
"""

import os

import streamlit as st

# Streamlit Cloud keeps keys in "Secrets". Copy them into the environment so that
# stock_chatbot.py reads them exactly like it reads a .env file.
try:
    for name in ("LLM_PROVIDER", "GEMINI_API_KEY", "GROQ_API_KEY", "LLM_MODEL", "APP_PASSWORD"):
        if name in st.secrets and not os.getenv(name):
            os.environ[name] = str(st.secrets[name])
except Exception:
    pass  # no secrets file on this laptop: the .env file is used instead

import stock_chatbot as bot  # noqa: E402  (after the secrets are in the environment)

MAX_QUESTIONS = 15  # per visitor session: keeps one visitor from using up the free AI limit

st.set_page_config(page_title="Company chatbot", page_icon="📈", layout="centered")
st.title("📈 Company chatbot")
st.caption("Ask about one company. The AI answers only from live market data, screener.in "
           "fundamentals and the latest news. A learning project, not financial advice.")

# ---------------------------------------------------------------- optional password
password = os.getenv("APP_PASSWORD", "")
if password and not st.session_state.get("unlocked"):
    typed = st.text_input("Password", type="password")
    if typed and typed == password:
        st.session_state.unlocked = True
        st.rerun()
    elif typed:
        st.error("Wrong password.")
    st.stop()

# ---------------------------------------------------------------- AI settings
provider = os.getenv("LLM_PROVIDER", "gemini").strip().lower()
if provider not in bot.PROVIDERS:
    st.error(f"LLM_PROVIDER must be one of {', '.join(bot.PROVIDERS)} (got '{provider}').")
    st.stop()
key_name = bot.PROVIDERS[provider][1]
if not os.getenv(key_name):
    st.error(f"{key_name} is not set. On your laptop put it in .env; on Streamlit Cloud add it "
             "under the app's Settings → Secrets (see HOSTING.md).")
    st.stop()


@st.cache_data(ttl=900, show_spinner=False)  # reuse the same company's data for 15 minutes
def load(company):
    return bot.gather(company)


# ---------------------------------------------------------------- pick a company
with st.form("pick_company"):
    company = st.text_input("Company name", value=st.session_state.get("company", "Infosys"))
    if st.form_submit_button("Load company") and company.strip():
        with st.spinner(f"Collecting data and news for {company}..."):
            try:
                st.session_state.data, st.session_state.news = load(company.strip())
            except Exception as error:
                st.error(f"Could not collect data: {error}")
                st.stop()
        st.session_state.company, st.session_state.history = company.strip(), []

if "data" not in st.session_state:
    st.info("Type a company name (for example Infosys, TCS or Tata Motors) and press Load company.")
    st.stop()

data, news = st.session_state.data, st.session_state.news
today, trend = data.get("today", {}), data.get("price_trend", {})
st.subheader(f"{data['company']} ({data['symbol']})")
c1, c2, c3 = st.columns(3)
c1.metric("Price", f"{today.get('currency', '')} {today.get('price') or trend.get('last_close')}",
          f"{today.get('day_change_pct')}% today" if today.get("day_change_pct") is not None else None)
c2.metric("1 year", f"{trend.get('change_1_year_pct')}%")
c3.metric("News headlines", len(news))
with st.expander("Latest news the bot is using"):
    if not news:
        st.write(data.get("news_error", "No headlines found."))
    for n in news:
        st.markdown(f"- [{n['title']}]({n['link']}) · {n['source']}, {n['date']}")

# ---------------------------------------------------------------- chat
history = st.session_state.setdefault("history", [])
for message in history:
    st.chat_message(message["role"]).markdown(message["content"])

asked = sum(1 for m in history if m["role"] == "user")
question = st.chat_input("Ask about this company…", disabled=asked >= MAX_QUESTIONS)
if st.button("Write a 5-section report", disabled=asked >= MAX_QUESTIONS):
    question = bot.REPORT_REQUEST
if asked >= MAX_QUESTIONS:
    st.warning(f"You've asked {MAX_QUESTIONS} questions in this session (free-tier limit). "
               "Refresh the page to start again.")

if question:
    shown = "Write a 5-section report." if question == bot.REPORT_REQUEST else question
    st.chat_message("user").markdown(shown)
    messages = ([{"role": "system", "content": bot.system_prompt(data, news)}]
                + history[-2 * bot.MAX_TURNS:] + [{"role": "user", "content": question}])
    with st.chat_message("assistant"), st.spinner("Thinking..."):
        try:
            client = bot.make_client(provider)
            model = os.getenv("LLM_MODEL") or bot.PROVIDERS[provider][2]
            answer, _ = bot.chat_once(client, provider, model, messages)
        except Exception as error:
            answer = bot.explain(error) if hasattr(error, "status_code") or "Connection" in type(error).__name__ \
                else f"Something went wrong: {error}"
        st.markdown(answer)
    history.extend([{"role": "user", "content": shown}, {"role": "assistant", "content": answer}])

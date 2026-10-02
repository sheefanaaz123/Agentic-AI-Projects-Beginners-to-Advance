"""Streamlit UI:  streamlit run app.py"""
import os

import streamlit as st
from dotenv import load_dotenv
from pydantic import ValidationError

from router import InputRejected, RoutingError, handle_query

load_dotenv()  

st.set_page_config(page_title="Financial Calculator Agent", page_icon="💹")
st.title("💹 Automated Financial Calculator Agent")
st.caption("The LLM only routes the request. Every number is computed by deterministic Python tools.")


DEFAULT_MODEL = {
    "google_genai": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
}
KEY_ENV = {"google_genai": "GOOGLE_API_KEY"}
PROVIDER_LABEL = {"google_genai": "Google Gemini"}


@st.cache_resource(show_spinner=False)
def get_llm(provider: str, model: str, api_key: str):
    from langchain.chat_models import init_chat_model
    return init_chat_model(model, model_provider=provider, temperature=0, api_key=api_key)


with st.sidebar:
    st.header("Router")
    mode = st.radio("Mode", ["Rule-based (offline)", "LLM router"])
    llm = None
    if mode == "LLM router":
        provider = st.selectbox("Provider", list(DEFAULT_MODEL), format_func=PROVIDER_LABEL.get)
        model = st.text_input("Model", DEFAULT_MODEL[provider])
        key  = os.getenv(KEY_ENV[provider], "")
        if key:
            llm = get_llm(provider, model, key)
        else:
            st.warning("No key set; falling back to rules.")
    st.markdown("**Examples**\n- EMI for 500000 at 8.5% for 20 years\n- SIP 10000 at 12% for 15 years\n"
                "- CAGR from 100000 to 250000 in 6 years\n- IRR of -1000, 300, 400, 500\n- (1200*1.08)^3")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.chat_input("Ask a financial question…")
if query:
    try:
        st.session_state.history.append((query, handle_query(query, llm), None))
    except (InputRejected, RoutingError, ValidationError, ValueError) as exc:
        st.session_state.history.append((query, None, str(exc)))

for q, res, err in st.session_state.history:
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        if err:
            st.error(err)
            continue
        st.markdown(f"**Tool:** `{res['tool']}` · routed by *{res['router']}*")
        data = {k: v for k, v in res["result"].items() if k != "formula"}
        cols = st.columns(len(data))
        for col, (k, v) in zip(cols, data.items()):
            col.metric(k.replace("_", " ").title(), f"{v:,}")
        st.caption(f"Formula: {res['result']['formula']}")
        with st.expander("Audit trail (validated inputs)"):
            st.json(res["inputs"])
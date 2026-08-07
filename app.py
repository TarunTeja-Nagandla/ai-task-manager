from agent import call_agent
from database import init_db
import streamlit as st

st.set_page_config(
    page_title="AI Task Manager",
    page_icon="🤖",
    layout="wide"
)

init_db()

st.subheader("🤖 AI-Powered Task Manager")
st.caption("Manage your tasks using natural language powered by LangChain, Groq & SQLAlchemy 2.0")

with st.sidebar:
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

query = st.chat_input("Ask Me Anything About Your Tasks...")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.chat_message("user").markdown(query)
    with st.chat_message("ai"):
        with st.spinner("Processing Your Request..."):
            try:
                res = call_agent(query)
                st.markdown(res)
                st.session_state.messages.append({"role": "ai", "content": res})
            except Exception as e:
                error_msg = f"⚠️ An error occurred: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "ai", "content": error_msg})
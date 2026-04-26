import streamlit as st
import google.generativeai as genai

# 1. Setup & Team Branding
st.set_page_config(page_title="FinBot", page_icon="💰")
st.title("🤖 FinBot")
st.caption("AI-Powered Financial Education Platform")

# Sidebar - Project Information
st.sidebar.header("📋 Project Info")
st.sidebar.write("**Team Members:**")
st.sidebar.write("- John Lagao  ")

# 2. Key Configuration
# Note: Using 'gemini-1.5-flash' as it is the most stable version for 2026 free API keys
genai.configure(api_key="AIzaSyB8ypHUuFP2WlidMDalK7nc3t5Xb_NkVJs")

# Define the AI personality (System Instruction)
instruction = "You are FinBot, a friendly financial advisor. Use simple, jargon-free English. Keep responses concise."
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=instruction
)

# 3. Sidebar Topics (Educational Branches)
FINANCIAL_TOPICS = {
    "Budgeting": "Learn the 50/30/20 Rule and how to track expenses.",
    "Investing": "Understanding Compound Interest, ETFs, and Index Funds.",
    "Debt Management": "Using the Snowball or Avalanche methods to pay off debt.",
    "Retirement": "Planning with 401(k), IRAs, and the 4% rule."
}

st.sidebar.markdown("---")
st.sidebar.header("Explore Topics")
selection = st.sidebar.selectbox("Choose a branch:", ["Home"] + list(FINANCIAL_TOPICS.keys()))

if selection != "Home":
    st.sidebar.info(f"**Quick Guide:** {FINANCIAL_TOPICS[selection]}")

# 4. Chat logic (Session Management)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm FinBot. Ask me anything about budgeting, investing, or saving for the future!"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input & AI Response
if prompt := st.chat_input("Ask FinBot a question (e.g., 'Explain the 50/30/20 rule')"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        try:
            # We use the existing chat history to give the AI context
            chat = model.start_chat(history=[
                {"role": m["role"] if m["role"] != "assistant" else "model", "parts": [m["content"]]} 
                for m in st.session_state.messages[:-1]
            ])
            
            response = chat.send_message(prompt)
            bot_response = response.text
            
            st.markdown(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            
        except Exception as e:
            st.error(f"FinBot is having trouble: {e}")
            st.info("Check if your API Key is active or if the model name needs updating.")
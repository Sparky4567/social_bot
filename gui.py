import streamlit as st
from modules.speak_module.Speak_Module import Speak_Module
from modules.llm_module.LLM_Module import LLM_module
from modules.memory_module.Memory_Module import MemoryDB
from modules.speech_to_text.Speech_To_Text_Module import VoskRecognizer
from settings.settings import SPEECH_TO_TEXT


def main():
    st.set_page_config(page_title="🧠 AI Assistant", layout="centered")
    st.title("🧠 Conversational Assistant")
    st.caption("Powered by your custom modules + Vosk speech recognition")

    # --- Initialize modules only once ---
    if "speak" not in st.session_state:
        st.session_state.speak = Speak_Module()
    if "llm" not in st.session_state:
        st.session_state.llm = LLM_module()
    if "memory" not in st.session_state:
        st.session_state.memory = MemoryDB()
    if SPEECH_TO_TEXT and "asr" not in st.session_state:
        st.session_state.asr = VoskRecognizer()

    # --- Initialize conversation history ---
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --- Input section ---
    st.subheader("🎤 Your Input")

    user_input = ""
    if SPEECH_TO_TEXT:
        if st.button("▶️ Start Listening"):
            asr = st.session_state.asr
            if asr.is_ready:
                with st.spinner("Listening... say 'stop' to finish"):
                    user_input = asr.listen_until_stop().strip()
    else:
        user_input = st.text_area("💬 Type your message here:", "", height=100)
        if st.button("Submit"):
            user_input = user_input.strip()

    # --- Processing ---
    if user_input:
        if user_input.lower() in ["exit", "quit", "q"]:
            st.warning("👋 Quitting… (just stop the app)")
            return

        llm = st.session_state.llm
        memory = st.session_state.memory

        with st.spinner("🤖 Thinking..."):
            response = llm.get_response_from_llm(user_input)

        bot_response = "No response"
        if "<think>" in response:
            bot_response = str(response).split("</think>")[1].strip()
        else:
            bot_response = str(response).strip()

        # Save conversation in session + memory
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Assistant", bot_response))
        memory._create_table()
        memory.add_memory(user_input, bot_response)

        # Speak response
        st.session_state.speak.speak(bot_response)

    # --- Display conversation history ---
    st.subheader("💬 Conversation History")
    for speaker, text in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"**🧑 {speaker}:** {text}")
        else:
            st.markdown(f"**🤖 {speaker}:** {text}")


if __name__ == "__main__":
    main()

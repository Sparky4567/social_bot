from modules.speak_module.Speak_Module import Speak_Module
from modules.llm_module.LLM_Module import LLM_module
from modules.memory_module.Memory_Module import MemoryDB
from modules.speech_to_text.Speech_To_Text_Module import VoskRecognizer
from settings.settings import SPEECH_TO_TEXT
def main():
    speakback = Speak_Module()
    llm = LLM_module()
    memory = MemoryDB()
    if SPEECH_TO_TEXT:
        asr = VoskRecognizer()
    try:
        if SPEECH_TO_TEXT and asr.is_ready:
            print("\n\nListening for your input...\n\n")
            user_input = asr.listen_until_stop().strip()
            print("You said: {}".format(user_input))
        else:
            user_input = str(input("\n\nYour input:\n\n")).strip()
        response = llm.get_response_from_llm(user_input)
        memory._create_table()
        if "<think>" in response:
            bot_response = str(response).split("</think>")[1].strip()
            print("===\n\n",bot_response,"\n\n===\n\n")
        else:
            bot_response = response
            print("===\n\n",bot_response,"\n\n===\n\n")
        print("\n\nStoring in memory... User-input: {} Bot-response: {}\n\n".format(user_input, bot_response))
        memory.add_memory(user_input, bot_response)
        speakback.speak(bot_response)
        main()
    except Exception as e:
        print(str("Exception: {}".format(e)))
    except KeyboardInterrupt:
        print("Quiting...")
        quit()

if __name__ == "__main__":
    main()

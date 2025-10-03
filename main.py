from modules.speak_module.Speak_Module import Speak_Module
from modules.llm_module.LLM_Module import LLM_module
from modules.memory_module.Memory_Module import MemoryDB
from modules.speech_to_text.Speech_To_Text_Module import VoskRecognizer
from modules.agentic_module.Agentic_Module import Agentic_Module
from modules.logo_module.Logo_Module import Logo_Module
from settings.settings import SPEECH_TO_TEXT
from settings.settings import AGENTIC

def main():
    speakback = Speak_Module()
    llm = LLM_module()
    memory = MemoryDB()
    agentic = Agentic_Module()
    logo = Logo_Module()
    try:
        logo.print_logo()
        if SPEECH_TO_TEXT:
            asr = VoskRecognizer()
            if asr.is_ready:
                print("\n\nListening for your input...\n\n")
                user_input = asr.listen_until_stop().strip()
                print("You said: {}".format(user_input))
        else:
            user_input = str(input("\n\nYour input:\n\n")).strip()
        match user_input.lower():
            case "exit" | "quit" | "q":
                print("Quiting...")
                quit()
            case _:
                print("\nProcessing your input...\n")
                if AGENTIC:
                    response = agentic.select_tool(str(user_input).lower())
                    if (response[0] is True and response[1] is not None):
                        response = response[1]
                    elif (response[0] is False and response[1] is None):
                        response = llm.get_response_from_llm(user_input)
                else:
                    response = llm.get_response_from_llm(user_input)
                memory._create_table()
                bot_response = "No response"
                if "<think>" in response:
                    bot_response = str(response).split("</think>")[1].strip()
                    print("===\n\n",bot_response,"\n\n===\n\n")
                else:
                    bot_response = str(response).strip()
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

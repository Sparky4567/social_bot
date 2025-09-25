from modules.speak_module.Speak_Module import Speak_Module
from modules.llm_module.LLM_Module import LLM_module

def main():
    speakback = Speak_Module()
    llm = LLM_module()
    try:
        user_input = str(input("\n\nYour input:\n\n")).strip()
        response = llm.get_response_from_llm(user_input)
        if "<think>" in response:
            bot_response = str(response).split("</think>")[1].strip()
            print("===\n\n",bot_response,"\n\n===\n\n")
            speakback.speak(bot_response)
        main()
    except Exception as e:
        print(str("Exception: {}".format(e)))
    except KeyboardInterrupt:
        print("Quiting...")
        quit()

if __name__ == "__main__":
    main()

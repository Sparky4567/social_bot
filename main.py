from modules.speak_module.Speak_Module import Speak_Module
from modules.llm_module.LLM_Module import LLM_module
from modules.memory_module.Memory_Module import MemoryDB

def main():
    speakback = Speak_Module()
    llm = LLM_module()
    memory = MemoryDB()

    try:
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

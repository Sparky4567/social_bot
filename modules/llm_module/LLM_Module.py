from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from settings.settings import (LOCAL_LLM, special_directives_loader, directives_loader, BOT_NAME)
from random import randint
from modules.memory_module.Memory_Module import MemoryDB

class LLM_module:
    def __init__(self):
        self.llm = OllamaLLM(model=LOCAL_LLM)
    def mood_choose(self):
        rand=randint(1,100)
        return str(rand)
    # Define a function to format the prompt
    def format_prompt(self, passed_prompt):
        try:
            # Define a prompt template
            SPECIAL_DIRECTIVES = special_directives_loader()
            #print(SPECIAL_DIRECTIVES)
            DIRECTIVES = directives_loader(BOT_NAME)
            #print(DIRECTIVES)
            MOOD = self.mood_choose()
            #print(MOOD)
            print("\n\nLoading directives...\n\n")
            memory_db = MemoryDB()
            memory_db._create_table()
            MEMORIES = memory_db.fetch_all()
            if not MEMORIES:
                MEMORIES = "No memories found."
            else:
                MEMORIES = "\n".join([f"User: {mem[1]} | Bot: {mem[2]}" for mem in MEMORIES])
            print("\n\nMemories have been loaded.\n\n")
            new_prompt = PromptTemplate(
                    input_variables=["question"],
                    template="Those are your possible moods:{moods}.\n,You chose mood:{chosen_mood}.\nThose are your instructions:{directives} to follow while giving the answers.\nThe following The following is a record of past conversations:{memories}\nQ: {question}\n"
            )
            formatted_prompt = new_prompt.format(moods=SPECIAL_DIRECTIVES,chosen_mood=MOOD,directives=DIRECTIVES,memories=MEMORIES,question=passed_prompt)
            return formatted_prompt
        except Exception as e:
            print(f"Error formatting prompt: {e}")
            return None

    def get_response_from_llm(self, passed_prompt):
        try:
            text=""
            if passed_prompt and passed_prompt is not None:
                prompt = self.format_prompt(passed_prompt)
                for chunk in self.llm.stream(prompt, stop=["Q:", "User:"]):
                    print(chunk, end='', flush=True)
                    text+=chunk
                print("\n\n")
                text+="\n\n"
                return text
            else:
                return None
        except Exception as e:
            print(f"LLM Error: {e}")
            self.get_response_from_llm(passed_prompt)

    
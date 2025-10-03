import webbrowser
class Agentic_Module:
    
    def __init__(self):
        self.default_browser_address = "https://www.google.com/"
        self.default_web_url = "https://www.google.com"
        self.youtube_url = "https://www.youtube.com/"
        self.google_url = "https://www.google.com/"
        self.gpt_url = "https://chat.openai.com/"
        self.giphy_url = "https://giphy.com/"
        self.default_status = None

    def message_handler(self, message_to_return):
        return message_to_return
    
    def return_status(self, status):
        self.default_status = status
        return self.default_status
    
    def open_browser (self):
        webbrowser.open_new(self.default_browser_address)

    # Youtube Search
    # words: list of words to identify the command
    # sentence: full user input
    # passed_url: base url to use for the search
    # Example: words = ["search","youtube","for"], sentence = "search youtube for cute cats", passed_url = "https://www.youtube.com/"
    # Look at the example above, if all words in the list are found in the sentence, the function will extract the search terms (cute cats) and open a new tab with the search results on YouTube.
    # The function constructs the search URL by appending the search terms to the base URL.
    # The search terms are joined with '+' to form a valid query string.
    # Finally, it opens a new browser tab with the constructed URL.
    # This function can be adapted for other search engines by changing the base URL and the command words.
    # Example for Google: words = ["search","google","for"], passed_url = "https://www.google.com/"
    # Look at init functions below for usage examples.
    def search_youtube(self,words,sentence,passed_url):
        if all(x in str(sentence).lower().split() and x is not None for x in words ):
            new_sentence = str(sentence)
            for x in words:
                new_sentence=str(new_sentence).replace(x,"").strip()
            query_words = new_sentence.split()
            youtube_url="{}results?search_query=".format(passed_url)
            for word_index, word in enumerate(query_words):
                if(word_index==0):
                    youtube_url = "{}{}".format(youtube_url,word)
                else:
                    youtube_url = "{}+{}".format(youtube_url,word)
            webbrowser.open_new_tab(youtube_url)
           
    
    def search_google(self,words,sentence,passed_url):
        if all(x in str(sentence).lower().split() and x is not None for x in words):
            new_sentence = str(sentence)
            for x in words:
                new_sentence=str(new_sentence).replace(x,"").strip()
            query_words = new_sentence.split()
            google_url="{}search?q=".format(passed_url)
            for word_index, word in enumerate(query_words):
                if(word_index==0):
                    google_url = "{}{}".format(google_url,word)
                else:
                    google_url = "{}+{}".format(google_url,word)
            webbrowser.open_new_tab(google_url)
            
    def search_giphy(self,words,sentence,passed_url):
        if all(x in str(sentence).lower().split() and x is not None for x in words):
            new_sentence = sentence
            for x in words:
                new_sentence=str(new_sentence).replace(x,"").strip()
            query_words = new_sentence.split()
            giphy_url="{}search/".format(passed_url)
            for word_index, word in enumerate(query_words):
                if(word_index==0):
                    giphy_url = "{}{}".format(giphy_url,word)
                else:
                    giphy_url = "{}-{}".format(giphy_url,word)
            webbrowser.open_new_tab(giphy_url)

    def search_youtube_ini(self,passed_phrase):
        self.search_youtube(["search","youtube","for"],passed_phrase,self.youtube_url)

    # Google Search
    # words: list of words to identify the command
    # sentence: full user input
    # passed_url: base url to use for the search
    # Example: words = ["search","google","for"], sentence = "search google for cute cats", passed_url = "https://www.google.com/"
    # Look at the example above, if all words in the list are found in the sentence, the function will extract the search terms (cute cats) and open a new tab with the search results on Google.
    # Search google method is being called in the init function below.
    def search_google_ini(self,passed_phrase):
        self.search_google(["search","google","for"],passed_phrase,self.google_url)
    
    def search_giphy_ini(self,passed_phrase):
        self.search_giphy(["search","giphy","for"],passed_phrase,self.giphy_url)

    def select_tool(self, user_input):
        match user_input:
            case "open browser":
                self.open_browser()
                return [self.return_status(True),self.message_handler("Opening web browser !")]
            case _ if all(x in str(user_input).lower().split() and x is not None for x in ["search","youtube","for"]):
                self.search_youtube_ini(user_input)
                return [self.return_status(True),self.message_handler("Searching Youtube for {}!".format(str(user_input).replace("search youtube for","").strip()))]
            case _ if all(x in str(user_input).lower().split() and x is not None for x in ["search","google","for"]):
                self.search_google_ini(user_input)
                return [self.return_status(True),self.message_handler("Searching Google for {}!".format(str(user_input).replace("search google for","").strip()))]
            case _ if all(x in str(user_input).lower().split() and x is not None for x in ["search","giphy","for"]):
                self.search_giphy_ini(user_input)
                return [self.return_status(True),self.message_handler("Searching Giphy for {}!".format(str(user_input).replace("search giphy for","").strip()))]
            case _:
                return [self.return_status(False),self.message_handler(None)]
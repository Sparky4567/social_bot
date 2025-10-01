import webbrowser
class Agentic_Module:
    
    def __init__(self):
        self.default_browser_address = "https://www.google.com/"
        self.default_status = None

    def message_handler(self, message_to_return):
        return message_to_return
    
    def return_status(self, status):
        self.default_status = status
        return self.default_status
    
    def open_browser (self):
        webbrowser.open_new(self.default_browser_address)

    def select_tool(self, user_input):
        match user_input:
            case "open browser":
                self.open_browser()
                return [self.return_status(True),self.message_handler("Opening web browser !")]
            case _:
                return [self.return_status(False),self.message_handler(None)]
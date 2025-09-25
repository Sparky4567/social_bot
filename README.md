# Social Local LLM Bot

A local social bot powered by your chosen LLM (Large Language Model). This project enables you to run a conversational bot on your machine, ensuring privacy and control.

(Ollama service should be running on your local machine, you can pick another ollama supported model in settings.py [llama, llama3.1 or llama3.2 - whatever you prefer - ollama pull model first])

## Features

- Local inference with an LLM
- Social interaction capabilities (if you add any)
- Easy setup and launch

## Requirements

- Python 3.8+
- [Astral's U Manager](https://github.com/astral-sh/uv)


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/social_bot.git
    cd social_bot
    ```
    
## Launch Instructions

To start the bot, use Astral's U Manager:

```bash
uv run main.py

```

## Configuration

Edit `settings.py` to set your model path and parameters.

## License

MIT
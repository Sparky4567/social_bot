# KEY DIFFERENCES FROM PREVIOUS VERSION

- Text inputs only (for now)
- No extra components (unnecessary packages were removed to keep the project as small as possible)
- Piper tts support (it speaks back the same way as previous version did - a minimal model is being used instead of a medium one)

# PLANNED UPDATES

- Memory storage/retrieval module - Solved / Marked as done
- Text to speech support - Solved / Marked as done
- Speech to text support - Solved / Marked as done
- Agentic module - Solved / Marked as done (you can code your own desired behavior based on static commands "open browser, etc.")
- Some sort of a GUI to let you interact with the chatbot, remove/review/add memories - Planning stage

# RECENT CHANGES

- Memory storage/retrieval module (Yes, the LLM is able to use and store memories by using a local database solution)
- Vosk local model speech to text convertion until "stop" word is spoken
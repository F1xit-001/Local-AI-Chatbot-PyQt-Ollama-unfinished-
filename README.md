# Local AI Chatbot (PyQt + Ollama)

A simple, **Unfinished** local chatbot built with Python and PyQt5. Supports customizable personas, editable bot profile, chat history, and easy local LLM chatting using **Ollama**.

---

## ✨ Features

- 🪄  Nice looking simple PyQt interface
- 👤 Create and switch between custom personas (with icons and descriptions)
- 🤖 Easily edit the bot’s name, appearance, and lore
- 💬 Chat history (auto-trimmed, stored in JSON)
- 📄 All chat messages displayed in a scrollable feed with user and bot avatars
- 🧠 Persona memory summary passed in prompt
- 🔧 Supports any model installed via [Ollama](https://ollama.com)

---

## 🚀 Requirements

- Python 3.10+ (tested and working on 3.9 too)
- Ollama installed and running
- A supported LLM (e.g. `llama3`, `mistral`, etc.)
- Run from **main.py**
---

| File/Folders          | Description                                |
| --------------------- | ------------------------------------------ |
| `main.py`             | App entry point                            |
| `chatbot_ui.py`       | Main chat window (PyQt logic)              |
| `conversation.py`     | Message formatting and bot handling        |
| `persona_selector.py` | Persona browser + active persona selection |
| `edit_persona.py`     | Create/edit/delete persona UI              |
| `edit_bot.py`         | Edit bot profile window                    |
| `memory.py`           | Handles memory file loading                |
| `styles.py`           | Stylesheet + layout setup                  |
| `config/`             | Holds JSON files: personas, memory, active |
| `Icons/`              | App icons                                  |

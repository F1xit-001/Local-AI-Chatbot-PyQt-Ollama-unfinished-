from PyQt5.QtWidgets import QApplication
import os
import json
import sys
import ollama
from llama_cpp import Llama
from chatbot_ui import ChatBotUI

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
Chat_History = os.path.join(CONFIG_DIR, "chat_history.json")


def load_json(filename):
    file_path = os.path.join(CONFIG_DIR, filename)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


bot_data = load_json("bot.json")
bot_name = bot_data.get("bot_name", "Assistant")
bot_description = bot_data.get("bot_personality", "An AI assistant.")


def load_chat_json():
    if os.path.exists(Chat_History):
        try:
            with open(Chat_History, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"messages": []}
    return {"messages": []}


def save_chat_json(data):
    with open(Chat_History, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_history():
    """Retrieves the last 30 messages from the chat history."""
    history = load_chat_json().get("messages", [])
    return history[-30:]


def save_history(history):
    """Saves the chat history, keeping only the last 30 messages."""
    save_chat_json({"messages": history})


def generate_reply(user_input):
    active_data = load_json("active.json")
    active_persona_key = active_data.get("active_persona", "")

    persona_data = load_json("persona.json").get("personas", {})
    active_persona = persona_data.get(active_persona_key, {})

    user_name = active_persona.get("name", "User")
    user_description = active_persona.get("description", "A mysterious person.")
    memory = load_json("memory.json").get("memory", "")

    chat_data = load_json(Chat_History)
    chat_history = chat_data.get("messages", [])

    chat_history = [msg for msg in chat_history if msg["role"] in ["user", "assistant"]][-30:]

    system_prompt = f"""
    [INST]
    - Your name is {bot_name}.  
    - Your Appearance, Backstory, and General Lore are: {bot_description}.  
    - You are talking to {user_name}. Their Description is: {user_description}.  
    - Summary of past events (provided by user): {memory}.    
    [/INST]
    """

    print("Loaded Chat History:", json.dumps(chat_history, indent=4))

    messages = [{"role": "system", "content": system_prompt}] + chat_history
    messages.append({"role": "user", "content": user_input})

    j = ollama.chat(model="llama3.1:8b", messages=messages, stream=True)
    # Generate AI response, you can change the model to whatever model you like here
    response_text = ""
    for chunk in j:
        response_text += chunk["message"]["content"]

    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response_text})

    print("Updated Chat History:", json.dumps(chat_history, indent=4))

    save_history(chat_history[-30:])

    return response_text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatBotUI()
    window.show()
    sys.exit(app.exec_())

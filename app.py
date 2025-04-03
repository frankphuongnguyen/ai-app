import gradio as gr
import ollama
import sqlite3

MODEL_NAME = 'llama3.2:latest'

DB_PATH = "chat_log.db"


def setup_db():
    """Create db if not exists"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAP
        )
    """)
    conn.commit()
    conn.close()


def chat_with_model(prompt):
    response = ollama.chat(model=MODEL_NAME, messages=[{'role': 'user', 'content': prompt}])["message"]["content"]

    # Log to db
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (prompt, response) VALUES (?, ?)", (prompt, response))
    conn.commit()
    conn.close()

    return response

iface = gr.Interface(
    fn=chat_with_model,
    inputs=gr.Textbox(lines=2, placeholder="Type your message here..."),
    outputs="text",
    title=f"Chat with {MODEL_NAME}",
    description="Enter a message and get a response from the Ollama 3.2 model.",
)

if __name__ == """__main__""":
    setup_db()
    iface.launch()


import tkinter as tk
from tkinter import scrolledtext
from integration import generate_text

def create_gui(model, tokenizer, device, config):
    def on_send_message():
        user_message = user_input.get().strip()
        if user_message:
            chat_log.insert(tk.END, f"You ? {user_message}\n")
            response = generate_text(user_message, model, tokenizer, device, config)
            chat_log.insert(tk.END, f"Bot ? {response}\n\n")
            chat_log.see(tk.END)
            user_input.delete(0, tk.END)

    root = tk.Tk()
    root.title("RuGPT3Small Chatbot")
    root.resizable(True, True)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    chat_frame = tk.Frame(root)
    chat_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    chat_frame.grid_rowconfigure(0, weight=1)
    chat_frame.grid_columnconfigure(0, weight=1)

    chat_log = scrolledtext.ScrolledText(
        chat_frame, 
        wrap=tk.WORD, 
        state="normal", 
        bg="black", 
        fg="white"
    )
    chat_log.grid(row=0, column=0, sticky="nsew")

    input_frame = tk.Frame(root)
    input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
    input_frame.grid_columnconfigure(0, weight=1)

    user_input = tk.Entry(input_frame)
    user_input.grid(row=0, column=0, sticky="ew", padx=(0, 5))

    send_button = tk.Button(input_frame, text="Send", command=on_send_message)
    send_button.grid(row=0, column=1)

    root.mainloop()
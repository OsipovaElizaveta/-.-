# -*- coding: cp1251 -*-
import tkinter as tk
from tkinter import ttk
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# �������� ���������� ��������� �� ����� .env
load_dotenv()

# ��������� API-����� �� ���������� ���������
api_key = os.getenv("HF_API_KEY")

# ��������� API �������� Hugging Face
client = InferenceClient(api_key=api_key)

# �������� ��������� ����
root = tk.Tk()
root.title("��������� � API")
root.geometry("800x500")  # ������ �������� ����

# ===========================
# ������� ��� ��������� ��������
def send_to_qwen_coder():
    """��������� ��������� ��� Qwen2.5-Coder (����� ����� ����)"""
    user_input = entry_left.get().strip()
    if user_input:
        try:
            messages = [{"role": "user", "content": user_input}]
            completion = client.chat.completions.create(
                model="Qwen/Qwen2.5-Coder-32B-Instruct",  # ������ ��� ����� �������
                messages=messages,
                max_tokens=500
            )
            response = completion.choices[0].message["content"]
        except Exception as e:
            response = f"Error communicating with Qwen2.5-Coder: {str(e)}"
        # ����������� ������
        text_display_left.insert(tk.END, f"�� -> {user_input}\nQwen2.5-Coder -> {response}\n\n")
        entry_left.delete(0, tk.END)

def send_to_qwq():
    """��������� ��������� ��� QwQ-32B-Preview (������ ����� ����)"""
    user_input = entry_right.get().strip()
    if user_input:
        try:
            messages = [{"role": "user", "content": user_input}]
            completion = client.chat.completions.create(
                model="Qwen/QwQ-32B-Preview",  # ������ ��� ������ �������
                messages=messages,
                max_tokens=500
            )
            response = completion.choices[0].message["content"]
        except Exception as e:
            response = f"Error communicating with QwQ-32B-Preview: {str(e)}"
        # ����������� ������
        text_display_right.insert(tk.END, f"�� -> {user_input}\nQwQ-32B-Preview -> {response}\n\n")
        entry_right.delete(0, tk.END)

# ===========================
# �������� ����������
# �������� �������� ������
frame_main = ttk.Frame(root)
frame_main.pack(fill="both", expand=True)

# ����� �������
frame_left = ttk.Frame(frame_main, padding=5)
frame_left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

label_left = ttk.Label(frame_left, text="Qwen2.5-Coder API", anchor="center", background="black", foreground="white")
label_left.pack(fill="x")

text_display_left = tk.Text(frame_left, wrap="word", bg="black", fg="white", state="normal", height=15, width=30)
text_display_left.pack(fill="both", expand=True)

frame_left_input = ttk.Frame(frame_left)
frame_left_input.pack(fill="x", pady=5)

entry_left = tk.Entry(frame_left_input, width=40)
entry_left.pack(side="left", fill="x", expand=True, padx=5)

button_left_send = ttk.Button(frame_left_input, text="���������", command=send_to_qwen_coder)
button_left_send.pack(side="right")

# ������ �������
frame_right = ttk.Frame(frame_main, padding=5)
frame_right.pack(side="right", fill="both", expand=True, padx=5, pady=5)

label_right = ttk.Label(frame_right, text="QwQ-32B-Preview API", anchor="center", background="black", foreground="white")
label_right.pack(fill="x")

text_display_right = tk.Text(frame_right, wrap="word", bg="black", fg="white", state="normal", height=15, width=30)
text_display_right.pack(fill="both", expand=True)

frame_right_input = ttk.Frame(frame_right)
frame_right_input.pack(fill="x", pady=5)

entry_right = tk.Entry(frame_right_input, width=40)
entry_right.pack(side="left", fill="x", expand=True, padx=5)

button_right_send = ttk.Button(frame_right_input, text="���������", command=send_to_qwq)
button_right_send.pack(side="right")


# ������ ��������� ����� ���������
root.mainloop()
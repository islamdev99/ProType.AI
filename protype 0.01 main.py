import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from serpapi import GoogleSearch

# Function to load data from JSON file
def load_data(file_path='bot_data.json'):
    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}
    except json.JSONDecodeError:
        print("Error: Corrupted JSON file. Starting fresh.")
        return {}
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}

# Function to save data to JSON file
def save_data(data, file_path='bot_data.json'):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

# Function to perform Google search using SerpAPI
def perform_search(query):
    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": "f41082ce8546f83f717679baf1318d649d123ba213a92067de9dfdee2ea5accb"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        if organic_results:
            return organic_results[0].get("snippet", "No snippet available")
        return "Sorry, I couldn’t find anything relevant."
    except Exception as e:
        return f"Oops! Search failed: {e}"

# Analyze question for deep thinking
def analyze_question(question):
    question = question.lower().strip()
    if question.startswith("what is") or question.startswith("ما هو"):
        return "definition"
    elif question.startswith("how") or question.startswith("كيف"):
        return "process"
    elif question.startswith("why") or question.startswith("لماذا"):
        return "reason"
    else:
        return "general"

# GUI Application
class ProtypeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Protype 0.01 - Made by Islam Ibrahim")
        self.root.geometry("800x600")
        self.root.configure(bg="#e8f1f5")

        self.data = load_data()

        # Style Configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Arial", 10, "bold"), padding=8, background="#4CAF50", foreground="white")
        style.map("TButton", background=[("active", "#45a049")])
        style.configure("TLabel", font=("Arial", 12), background="#e8f1f5", foreground="#333333")
        style.configure("TNotebook", background="#e8f1f5", tabmargins=[5, 5, 5, 0])
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[10, 5])

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=15, padx=15, fill="both", expand=True)

        # Teach Tab
        self.teach_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.teach_frame, text="Teach Protype")
        self.setup_teach_tab()

        # Search Tab
        self.search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_frame, text="Search & Learn")
        self.setup_search_tab()

        # Chat Tab
        self.chat_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.chat_frame, text="Chat with Protype")
        self.setup_chat_tab()

    def setup_teach_tab(self):
        ttk.Label(self.teach_frame, text="Teach Protype Something New!", font=("Arial", 16, "bold"), foreground="#0288d1").pack(pady=10)

        ttk.Label(self.teach_frame, text="What’s your question?").pack(pady=5)
        self.teach_question = ttk.Entry(self.teach_frame, width=70, font=("Arial", 11))
        self.teach_question.pack()

        ttk.Label(self.teach_frame, text="What’s the answer?").pack(pady=5)
        self.teach_answer = ttk.Entry(self.teach_frame, width=70, font=("Arial", 11))
        self.teach_answer.pack()

        self.teach_output = tk.Text(self.teach_frame, height=12, width=80, bg="#ffffff", fg="#333333", font=("Arial", 10), relief="flat", borderwidth=2)
        self.teach_output.pack(pady=15)
        self.teach_output.insert(tk.END, "Hey there! Teach me something cool by entering a question and answer!\n")

        btn_frame = ttk.Frame(self.teach_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Teach Me", command=self.process_teach_input).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Clear", command=lambda: self.teach_output.delete(1.0, tk.END), style="TButton").grid(row=0, column=1, padx=5)
        ttk.Style().configure("TButton", background="#ff7043")

    def setup_search_tab(self):
        ttk.Label(self.search_frame, text="Search & Learn with Protype!", font=("Arial", 16, "bold"), foreground="#0288d1").pack(pady=10)

        ttk.Label(self.search_frame, text="What do you want to search for?").pack(pady=5)
        self.search_query = ttk.Entry(self.search_frame, width=70, font=("Arial", 11))
        self.search_query.pack()

        self.search_output = tk.Text(self.search_frame, height=12, width=80, bg="#ffffff", fg="#333333", font=("Arial", 10), relief="flat", borderwidth=2)
        self.search_output.pack(pady=15)
        self.search_output.insert(tk.END, "Enter a search query, and I’ll fetch something useful!\n")

        btn_frame = ttk.Frame(self.search_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Search", command=self.process_search_input).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Clear", command=lambda: self.search_output.delete(1.0, tk.END), style="TButton").grid(row=0, column=1, padx=5)
        ttk.Style().configure("TButton", background="#ff7043")

    def setup_chat_tab(self):
        ttk.Label(self.chat_frame, text="Chat with Protype!", font=("Arial", 16, "bold"), foreground="#0288d1").pack(pady=10)

        self.chat_output = tk.Text(self.chat_frame, height=15, width=80, bg="#ffffff", fg="#333333", font=("Arial", 10), relief="flat", borderwidth=2)
        self.chat_output.pack(pady=15)
        self.chat_output.insert(tk.END, "Hello! I’m Protype 0.01, created by Islam Ibrahim. Ask me anything, and I’ll think deeply to help you!\n")

        ttk.Label(self.chat_frame, text="Ask me something:").pack()
        self.chat_question = ttk.Entry(self.chat_frame, width=70, font=("Arial", 11))
        self.chat_question.pack(pady=5)

        btn_frame = ttk.Frame(self.chat_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Ask Me", command=self.process_chat_input).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Clear Chat", command=lambda: self.chat_output.delete(1.0, tk.END), style="TButton").grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Exit", command=self.exit_app, style="TButton").grid(row=0, column=2, padx=5)

    def process_teach_input(self):
        question = self.teach_question.get().strip()
        answer = self.teach_answer.get().strip()

        if not question or not answer:
            messagebox.showwarning("Oops!", "Please fill in both the question and answer!")
            return

        self.teach_output.delete(1.0, tk.END)
        if question not in self.data:
            self.data[question] = []
        self.data[question].append({"answer": answer, "weight": 0.5})

        if save_data(self.data):
            self.teach_output.insert(tk.END, f"Thanks! I’ve learned: '{question}' -> '{answer}'\nSaved successfully!\n")
        else:
            self.teach_output.insert(tk.END, "Uh-oh! Something went wrong while saving. Try again?\n")

        self.teach_question.delete(0, tk.END)
        self.teach_answer.delete(0, tk.END)

    def process_search_input(self):
        query = self.search_query.get().strip()
        if not query:
            messagebox.showwarning("Oops!", "Please enter something to search for!")
            return

        self.search_output.delete(1.0, tk.END)
        self.search_output.insert(tk.END, f"Searching for '{query}'...\n")
        result = perform_search(query)
        self.search_output.insert(tk.END, f"Here’s what I found: {result}\n")

        search_question = f"search: {query}"
        if search_question not in self.data:
            self.data[search_question] = []
        self.data[search_question].append({"answer": result, "weight": 0.5})

        if save_data(self.data):
            self.search_output.insert(tk.END, "Knowledge saved successfully!\n")
        else:
            self.search_output.insert(tk.END, "Failed to save the knowledge. Please try again!\n")

        self.search_query.delete(0, tk.END)

    def process_chat_input(self):
        question = self.chat_question.get().strip()
        if not question:
            messagebox.showwarning("Oops!", "Please ask me something!")
            return

        self.chat_output.insert(tk.END, f"You asked: {question}\n")
        question_type = analyze_question(question)

        if question in self.data and self.data[question]:
            # Choose the highest-weighted answer
            answers = sorted(self.data[question], key=lambda x: x["weight"], reverse=True)
            answer = answers[0]["answer"]
            prefix = {
                "definition": "Here’s the definition: ",
                "process": "Let me explain how it works: ",
                "reason": "Here’s why: ",
                "general": "Here’s what I know: "
            }
            self.chat_output.insert(tk.END, f"Protype: {prefix[question_type]}{answer}\n")
        else:
            # Deep thinking: Suggest similar or search
            similar_found = False
            for stored_q in self.data:
                if question.lower() in stored_q.lower() or stored_q.lower() in question.lower():
                    answer = self.data[stored_q][0]["answer"]
                    self.chat_output.insert(tk.END, f"Protype: I don’t know '{question}' exactly, but about '{stored_q}': {answer}\n")
                    similar_found = True
                    break

            if not similar_found:
                self.chat_output.insert(tk.END, f"Protype: Hmm, I don’t have an answer for that yet! Should I search for '{question}' in the Search tab?\n")

        self.chat_question.delete(0, tk.END)

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to leave Protype 0.01?"):
            self.root.quit()

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ProtypeApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
import json
import os

tasks = []

def add_task():
    description = task_desc_entry.get()
    deadline = deadline_entry.get()
if description and deadline:
        task = {"description": description, "deadline": deadline, "done": False}
        tasks.append(task)
        update_task_combobox()
    else:
        messagebox.showwarning("Attention", "Veuillez entrer une description et une date d'échéance.")

def update_task_combobox():
    task_combobox['values'] = [task["description"] + " - Date limite: " + task["deadline"] for task in tasks]
    task_combobox.set("")  # Sélection vide par défaut

def mark_as_done():
    selected_index = task_combobox.current()
    if selected_index >= 0:
        tasks[selected_index]["done"] = True
        update_task_combobox()

def delete_task():
    selected_index = task_combobox.current()
    if selected_index >= 0:
        del tasks[selected_index]
        update_task_combobox()

def save_tasks():
    file_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", ".json")])
    if file_name:
        with open(file_name, "w") as file:
            json.dump(tasks, file)
        messagebox.showinfo("Sauvegarde", "Les tâches ont été enregistrées avec succès.")

def load_tasks():
    file_name = filedialog.askopenfilename(filetypes=[("JSON files", ".json")])
    if file_name and os.path.exists(file_name):
        with open(file_name, "r") as file:
            global tasks
            tasks = json.load(file)
        messagebox.showinfo("Chargement", "Les tâches ont été chargées avec succès.")
        update_task_combobox()

root = tk.Tk()
root.title("Gestion avancée de tâches")

task_desc_label = tk.Label(root, text="Description de la tâche:")
task_desc_label.pack()

task_desc_entry = tk.Entry(root, width=50)
task_desc_entry.pack()

deadline_label = tk.Label(root, text="Date d'échéance (JJ/MM/AAAA):")
deadline_label.pack()

deadline_entry = tk.Entry(root, width=20)
deadline_entry.pack()

add_button = tk.Button(root, text="Ajouter la tâche", command=add_task)
add_button.pack()
task_combobox = Combobox(root, width=70)
task_combobox.pack()

mark_done_button = tk.Button(root, text="Marquer comme terminée", command=mark_as_done)
mark_done_button.pack()

delete_button = tk.Button(root, text="Supprimer", command=delete_task)
delete_button.pack()

save_button = tk.Button(root, text="Enregistrer", command=save_tasks)
save_button.pack()

load_button = tk.Button(root, text="Charger", command=load_tasks)
load_button.pack()

root.mainloop()
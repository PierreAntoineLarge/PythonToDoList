import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
import json
import os
from datetime import datetime

# Liste des tâches
tasks = []

# Fonction pour ajouter une tâche
def add_task():
    task_name = task_desc_entry.get()
    detail_name = detail_desc_entry.get()
    deadline = deadline_entry.get()

    name_valid = bool(task_name)
    date_valid = validate_date(deadline)

    if name_valid and date_valid:
        # Création d'un dictionnaire représentant la tâche
        task = {"task_name": task_name,"detail": detail_name, "deadline": deadline, "done": False}
        # Ajout de la tâche à la liste
        tasks.append(task)
        # Mise à jour de la liste des tâches affichée
        update_task_combobox()
    elif not name_valid:
        messagebox.showwarning("Attention", "Veuillez entrer un nom de tâche valide.")
    elif not date_valid:
        messagebox.showwarning("Attention", "Veuillez entrer une date valide au format JJ/MM/AAAA.")

# Fonction pour valider la date
def validate_date(date_string):
    try:
        day, month, year = map(int, date_string.split('/'))
        current_date = datetime.now().date()
        input_date = datetime(year, month, day).date()

        if input_date >= current_date:
            return True
        else:
            return False
    except ValueError:
        return False

# Fonction pour mettre à jour la liste des tâches affichée
def update_task_combobox():
  def display_state(state):
    if state == True:
        return "Terminée"
    elif state == False:
        return "A faire"
  sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x["deadline"], "%d/%m/%Y"))
  task_combobox['values'] = [task["task_name"] + " - Date limite : " + task["deadline"] + " - Etat : " + display_state(task["done"]) for task in sorted_tasks]
  task_combobox.set("")  # Sélection vide par défaut

# Fonction pour mettre à jour les détails de la tâche sélectionnée
def update_selected_task_detail(event=None):
    selected_index = task_combobox.current()
    if selected_index >= 0:
        if len(tasks[selected_index]["detail"]) > 0:
          selected_task_detail.set("Détail : " + tasks[selected_index]["detail"])
        else:          
          selected_task_detail.set("Aucun détail")
    else:
        selected_task_detail.set("Aucune tâche sélectionnée")

# Fonction pour marquer une tâche comme terminée ou à faire
def mark_as_done(state):
    selected_index = task_combobox.current()
    if selected_index >= 0:
        if state == True:
          tasks[selected_index]["done"] = True
          update_task_combobox()
          update_selected_task_detail()
        elif state == False:
          tasks[selected_index]["done"] = False
          update_task_combobox()
          update_selected_task_detail()

# Fonction pour supprimer une tâche
def delete_task():
    selected_index = task_combobox.current()
    if selected_index >= 0:
        del tasks[selected_index]
        update_task_combobox()
        update_selected_task_detail()

# Fonction pour enregistrer les tâches dans un fichier JSON
def save_tasks():
    file_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", ".json")])
    if file_name:
        with open(file_name, "w") as file:
            json.dump(tasks, file)
        messagebox.showinfo("Sauvegarde", "Les tâches ont été enregistrées avec succès.")

# Fonction pour charger les tâches depuis un fichier JSON
def load_tasks():
    file_name = filedialog.askopenfilename(filetypes=[("JSON files", ".json")])
    if file_name and os.path.exists(file_name):
        with open(file_name, "r") as file:
            global tasks
            tasks = json.load(file)
        messagebox.showinfo("Chargement", "Les tâches ont été chargées avec succès.")
        update_task_combobox()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Gestion avancée de tâches")

# Variable Tkinter pour stocker les détails de la tâche sélectionnée
selected_task_detail = tk.StringVar()

# Libellé et champ pour le nom de la tâche
task_name_label = tk.Label(root, text="Nom de la tâche:")
task_name_label.pack()

task_desc_entry = tk.Entry(root, width=50)
task_desc_entry.pack()

# Libellé et champ pour les détails de la tâche
detail_name_label = tk.Label(root, text="Détails liés à la tâche:")
detail_name_label.pack()

detail_desc_entry = tk.Entry(root, width=50)
detail_desc_entry.pack()

# Libellé et champ pour la date d'échéance
deadline_label = tk.Label(root, text="Date d'échéance (JJ/MM/AAAA):")
deadline_label.pack()

deadline_entry = tk.Entry(root, width=20)
deadline_entry.pack()

# Bouton pour ajouter une tâche
add_button = tk.Button(root, text="Ajouter la tâche", command=add_task)
add_button.pack()

# Liste déroulante pour afficher les tâches
task_combobox = Combobox(root, width=70)
task_combobox.pack()

# Écouter l'événement de sélection dans la ComboBox pour mettre à jour les détails de la tâche
task_combobox.bind("<<ComboboxSelected>>", update_selected_task_detail)

# Appel initial de la fonction pour afficher "Aucune tâche sélectionnée" au démarrage
update_selected_task_detail()

# Libellé pour afficher les détails de la tâche sélectionnée
selected_task_label = tk.Label(root, textvariable=selected_task_detail, bg="white")
selected_task_label.pack()

# Bouton pour marquer une tâche comme terminée
mark_done_button = tk.Button(root, text="Marquer comme terminée", command=lambda: mark_as_done(True))
mark_done_button.pack()

# Bouton pour marquer une tâche comme à faire
mark_done_button = tk.Button(root, text="Marquer comme à faire", command=lambda: mark_as_done(False))
mark_done_button.pack()

# Bouton pour supprimer une tâche
delete_button = tk.Button(root, text="Supprimer", command=delete_task)
delete_button.pack()

# Bouton pour enregistrer les tâches
save_button = tk.Button(root, text="Enregistrer", command=save_tasks)
save_button.pack()

# Bouton pour charger les tâches
load_button = tk.Button(root, text="Charger", command=load_tasks)
load_button.pack()

# Lancement de la boucle principale de l'application
root.mainloop()

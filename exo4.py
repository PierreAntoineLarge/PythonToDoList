# Projet : Gestion avancée de tâches avec interface graphique et stockage de données

# Contexte : Vous souhaitez créer une application de gestion de tâches plus avancée qui permet aux utilisateurs de gérer leurs tâches, d'enregistrer leurs listes de tâches et de charger ces listes ultérieurement.

# Objectif : Créer une application en Python avec Tkinter qui permet à l'utilisateur d'ajouter, afficher, marquer comme terminées, supprimer des tâches, enregistrer des listes de tâches et les charger.

# Description :

# Interface utilisateur : Créez une fenêtre avec des zones de texte pour entrer la description de la tâche et la date d'échéance, un bouton "Ajouter" pour ajouter une tâche, une liste pour afficher les tâches, des boutons pour marquer les tâches comme terminées et les supprimer. Ajoutez également des boutons pour enregistrer et charger des listes de tâches.

# Ajout de tâches : Lorsque l'utilisateur entre une description et une date d'échéance et clique sur "Ajouter", la tâche doit être ajoutée à la liste.

# Affichage des tâches : Les tâches ajoutées doivent s'afficher dans la liste avec des cases à cocher pour indiquer si elles sont terminées.

# Marquer une tâche comme terminée : L'utilisateur doit pouvoir cocher une case pour marquer une tâche comme terminée. Le texte de la tâche doit changer de couleur pour indiquer qu'elle est terminée.

# Suppression de tâches : L'utilisateur doit pouvoir supprimer une tâche en cliquant sur un bouton "Supprimer" à côté de la tâche.

# Enregistrement et chargement de listes : L'utilisateur doit être capable d'enregistrer sa liste de tâches dans un fichier local et de la charger ultérieurement. Le programme doit gérer plusieurs listes de tâches enregistrées.

# Consignes supplémentaires :

# Utilisez la bibliothèque Tkinter pour créer l'interface utilisateur.
# Implémentez un système de stockage de données en utilisant un format de fichier simple (par exemple, CSV ou JSON) pour enregistrer et charger les listes de tâches.
# Créez une interface utilisateur pour gérer les listes sauvegardées, permettant de charger, renommer et supprimer des listes.
# Ajoutez une fonction de tri pour trier les tâches par date d'échéance.
# Offrez la possibilité d'ajouter des notes ou des descriptions plus détaillées pour chaque tâche.


import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
import json
import os
from datetime import datetime

tasks = []

def add_task():
    task_name = task_desc_entry.get()
    deadline = deadline_entry.get()
    description = description_entry.get()

    if task_name and validate_date(deadline) and description :
        task = {"task_name": task_name, "deadline": deadline,"description": description, "done": False}
        tasks.append(task)
        update_task_combobox()
        messagebox.showinfo("Sauvegarde", "La tâche ont été ajoutés avec succès.")
        
        
    else:
        messagebox.showwarning("Attention", "Veuillez entrer un nom de tâche valide et une date d'échéance au format JJ/MM/AAAA.")

def validate_date(date_string):
    try:
        day, month, year = map(int, date_string.split('/'))
        if 1 <= day <= 31 and 1 <= month <= 12 and year >= 2023:
            return True
        else:
            messagebox.showwarning("Erreur de date", "Veuillez entrer un jour entre 1 et 31, un mois entre 1 et 12, et une année supérieure ou égale à 2023.")
            return False
    except ValueError:
        messagebox.showwarning("Erreur de date", "Veuillez entrer une date valide au format JJ/MM/AAAA.")
        return False

def update_task_combobox():
    sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x["deadline"], "%d/%m/%Y"))
    task_combobox['values'] = [task["task_name"] + " - Date limite: " + task["deadline"] for task in sorted_tasks]
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

fenetre = tk.Tk()
fenetre.title("Gestion avancée de tâches")
fenetre.geometry("1900x1500")

title_label = tk.Label(fenetre, text="Gestionnaire de tâche",font=35)
title_label.pack()

add_label = tk.Label(fenetre, text="Ajoutez une tâche",font=35)
add_label.place(x=1500,y=75)

task_name_label = tk.Label(fenetre, text="Nom de la tâche:", font=35)
task_name_label.place(x=1310,y=150)

task_desc_entry = tk.Entry(fenetre, width=60)
task_desc_entry.place(x=1450,y=152)

deadline_label = tk.Label(fenetre, text="Date d'échéance (JJ/MM/AAAA):", font=35)
deadline_label.place(x=1310,y=230)

deadline_entry = tk.Entry(fenetre, width=30 )
deadline_entry.place(x=1550,y=232)

description_label = tk.Label(fenetre, text="Description de la tâche : ", font=35)
description_label.place(x=1310,y=300)

description_entry = tk.Entry(fenetre, width=55,font=35)
description_entry.place(x=1310,y=330)

add_button = tk.Button(fenetre, text="Ajouter la tâche", command=add_task, font=35)
add_button.place(x=1500,y=450)

task_combobox = Combobox(fenetre, width=150)
task_combobox.place(x=50,y=70)

mark_done_button = tk.Button(fenetre, text="Marquer comme terminée", command=mark_as_done, font=35)
mark_done_button.place(x=150,y=100)

delete_button = tk.Button(fenetre, text="Supprimer", command=delete_task, font=35)
delete_button.place(x=550,y=100)

save_button = tk.Button(fenetre, text="Enregistrer la liste de tâche dans un ficher", command=save_tasks, font=35)
save_button.place(x=50,y=900)

load_button = tk.Button(fenetre, text="Charger une liste de tâche déjà existante depuis un fichier", command=load_tasks, font=35)
load_button.place(x=1350,y=900)

fenetre.mainloop()
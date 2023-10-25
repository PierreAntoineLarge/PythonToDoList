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

# Liste des tâches
tasks = []

# Fonction pour ajouter une tâche
def add_task():
    task_name = task_desc_entry.get()
    deadline = deadline_entry.get()
    detail_name = detail_desc_entry.get()

    name_valid = bool(task_name)
    date_valid = validate_date(deadline)

    if name_valid and date_valid :
         # Création d'un dictionnaire représentant la tâche
        task = {"task_name": task_name, "deadline": deadline,"description": detail_name, "done": False}
         # Ajout de la tâche à la liste
        tasks.append(task)
        # Mise à jour de la liste des tâches affichée
        update_task_combobox()
        # Message Pop up Réussit
        messagebox.showinfo("Sauvegarde", "La tâche ont été ajoutés avec succès.")
        
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
        messagebox.showwarning("Erreur de date", "Veuillez entrer une date valide au format JJ/MM/AAAA.")
        return False

# Fonction pour mettre à jour la liste des tâches affichée
def update_task_combobox():
  def display_state(state):
    if state == True:
        return "Fait"
    elif state == False:
        return "A faire"
  sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x["deadline"], "%d/%m/%Y"))
  task_combobox['values'] = [task["task_name"] + " - Date limite: " + task["deadline"] + " - Etat : " + display_state(task["done"]) for task in sorted_tasks]
  task_combobox.set("")  # Sélection vide par défaut

# Fonction pour mettre à jour les détails de la tâche sélectionnée
def update_selected_task_detail(event=None):
    selected_index = task_combobox.current()
    if selected_index >= 0:
        if len(tasks[selected_index]["detail"]) > 0:
          selected_task_detail.set("Détails : " + tasks[selected_index]["detail"])
        else:          
          selected_task_detail.set("Aucun détails")
    else:
        selected_task_detail.set("Aucune tâches séléctionnée")


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
fenetre = tk.Tk()
fenetre.title("Gestion avancée de tâches")
fenetre.geometry("1900x1500")

# Variable Tkinter pour stocker les détails de la tâche sélectionnée
selected_task_detail = tk.StringVar()

title_label = tk.Label(fenetre, text="Gestionnaire de tâche",font=35)
title_label.pack()

add_label = tk.Label(fenetre, text="Ajoutez une tâche",font=35)
add_label.place(x=1500,y=75)

# Libellé et champ pour le nom de la tâche
task_name_label = tk.Label(fenetre, text="Nom de la tâche:", font=35)
task_name_label.place(x=1310,y=150)

task_desc_entry = tk.Entry(fenetre, width=60)
task_desc_entry.place(x=1450,y=152)

# Libellé et champ pour les détails de la tâche
detail_name_label = tk.Label(fenetre, text="Détails liés à la tâche:", font=35)
detail_name_label.place(x=1310,y=300)

detail_desc_entry = tk.Entry(fenetre, width=55, font=35)
detail_desc_entry.place(x=1310,y=330)

# Libellé et champ pour la date d'échéance
deadline_label = tk.Label(fenetre, text="Date d'échéance (JJ/MM/AAAA):", font=35)
deadline_label.place(x=1310,y=230)

deadline_entry = tk.Entry(fenetre, width=30 )
deadline_entry.place(x=1550,y=232)


# Bouton pour ajouter une tâche
add_button = tk.Button(fenetre, text="Ajouter la tâche", command=add_task, font=35)
add_button.place(x=1500,y=450)

# Liste déroulante pour afficher les tâches
task_combobox = Combobox(fenetre, width=150)
task_combobox.place(x=50,y=70)

# Écouter l'événement de sélection dans la ComboBox pour mettre à jour les détails de la tâche
task_combobox.bind("<<ComboboxSelected>>", update_selected_task_detail)

# Appel initial de la fonction pour afficher "Aucune tâche sélectionnée" au démarrage
update_selected_task_detail()

# Libellé pour afficher les détails de la tâche sélectionnée
selected_task_label = tk.Label(fenetre, textvariable=selected_task_detail, bg="white")
selected_task_label.pack()

# Bouton pour marquer une tâche comme terminée
mark_done_button = tk.Button(fenetre, text="Marquer comme terminée", command=lambda: mark_as_done(True), font=35)
mark_done_button.place(x=150,y=100)

# Bouton pour marquer une tâche comme à faire
mark_done_button = tk.Button(fenetre, text="Marquer comme à faire", command=lambda: mark_as_done(False), font=35)
mark_done_button.place(x=750,y=100)

# Bouton pour supprimer une tâche
delete_button = tk.Button(fenetre, text="Supprimer", command=delete_task, font=35)
delete_button.place(x=550,y=100)

# Bouton pour enregistrer les tâches
save_button = tk.Button(fenetre, text="Enregistrer la liste de tâche dans un ficher", command=save_tasks, font=35)
save_button.place(x=50,y=900)

# Bouton pour charger les tâches
load_button = tk.Button(fenetre, text="Charger une liste de tâche déjà existante depuis un fichier", command=load_tasks, font=35)
load_button.place(x=1350,y=900)

# Lancement de la boucle principale de l'application
fenetre.mainloop()
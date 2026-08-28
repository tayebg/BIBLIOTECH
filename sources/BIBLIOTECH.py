# -*- coding: utf-8 -*-
"""
=============================================================================
 BIBLIOTECH - Contactless Library Management System (Desktop Version)
 
 Author: Tayeb Bekkouche (@tayebg)
 Repository: https://github.com/tayebg/BIBLIOTECH
 Contact: tayebekk2004@gmail.com
 
 Description:
 A modern, contactless library management application built with Python, 
 CustomTkinter, Database Layer (PostgreSQL & SQLite), and bibliographic lookup (isbnlib).
=============================================================================
"""

import os
import sys
from datetime import date, timedelta
from tkinter import Tk
from customtkinter import (
    CTkButton,
    CTkEntry,
    CTkImage,
    CTkLabel,
    CTkProgressBar,
    CTkToplevel,
)
from PIL import Image
from isbnlib import meta

# --- Path & Resource Resolution ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from db import get_db

ANNEXE_DIR = os.path.join(BASE_DIR, "Annexe")
ICONES_DIR = os.path.join(ANNEXE_DIR, "icones")

# --- Application Initialization ---
root = Tk()
root.geometry("1080x890")
root.title("BIBLIOTECH - Library Management")
root.configure(bg="#0A1437")
root.resizable(False, False)

# Typography
Outfit = ("Outfit", 10)
OutfitPlus = ("Outfit", 15)
OutfitBold = ("Outfit", 15, "bold")
OutfitTitle = ("Outfit", 30, "bold")

# Database Connection (PostgreSQL with SQLite fallback)
db = get_db()

# State Variables
today_date = date.today()
td = timedelta(days=30)

Liste_Adherent = []
Liste_Livre = []
Liste_Emprunt = []
Liste_Affiche = []
num_liste_affiche = 1
num_liste_max = 1
page = "livre"
root_annexe = None

# Entry References
EntryNom = None
EntryPrenom = None
EntryMail = None
EntryTelephone = None
EntryRechercheAdherent = None

EntryScanLivre = None
EntryCategorie = None
EntryRechercheLivre = None

EntryScanEmprunt = None
EntryAdherentCarte = None
EntryRechercheEmprunt = None

# Popup References
EntryISBN_Pop = None
EntryTitre_Pop = None
EntryAuteur_Pop = None
EntryEditeur_Pop = None
EntryCategorie_Pop = None

EntryNom_Pop = None
EntryPrenom_Pop = None
EntryMail_Pop = None
EntryTel_Pop = None

# --- Assets Loading ---
Image_Poubelle = CTkImage(Image.open(os.path.join(ICONES_DIR, "Delete.png")), size=(15, 15))
Image_Next_Page = CTkImage(Image.open(os.path.join(ICONES_DIR, "circle_right.png")), size=(15, 15))
Image_Previous_Page = CTkImage(Image.open(os.path.join(ICONES_DIR, "circle_left.png")), size=(15, 15))
Image_Retard = CTkImage(Image.open(os.path.join(ICONES_DIR, "Retard.png")), size=(15, 15))

# --- UI Helpers ---
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()
    for i in range(25):
        CTkLabel(root, text="", corner_radius=10, height=10, width=10, font=Outfit, fg_color="#0A1437").grid(row=i, column=i)

def Lim(texte, nbmaxi):
    if texte is None:
        return ""
    dico_car_max = {1: 65, 2: 30, 3: 30, 4: 20}
    nb_car_max = dico_car_max.get(nbmaxi, 30)
    str_txt = str(texte)
    return str_txt[:nb_car_max] + "..." if len(str_txt) > nb_car_max else str_txt

def Edit_Nb_Auteur(string):
    if not string:
        return ""
    if string.count("'") >= 4:
        n1 = string.find("'")
        n2 = string.find("'", n1 + 1)
        n3 = string.find("'", n2 + 1)
        n4 = string.find("'", n3 + 1)
        if n4 != -1:
            return string[:n4]
    return string

# --- Navigation Menu ---
def affichage_menu():
    CTkLabel(root, text="", corner_radius=10, height=10, width=20, font=Outfit, text_color="#1C1C1E", fg_color="#0A1437").grid(row=0, column=0)
    CTkLabel(root, text="BIBLIOTECH", corner_radius=10, height=19, width=120, font=OutfitTitle, text_color="white", fg_color="#0A1437").grid(row=2, column=1)
    CTkLabel(root, text="", corner_radius=10, height=10, width=216, font=Outfit, text_color="#1C1C1E", fg_color="#0A1437").grid(row=2, column=2)
    
    CTkLabel(root, text="", corner_radius=33, height=55, width=285, font=Outfit, text_color="white", fg_color="white").grid(row=1, rowspan=3, column=3, columnspan=3)
    
    adh_color = "#BAC8EB" if page == "adherent" else "white"
    livre_color = "#BAC8EB" if page == "livre" else "white"
    emp_color = "#BAC8EB" if page in ("emprunt", "retard") else "white"

    CTkButton(root, text="ADHERENT", corner_radius=20, height=35, width=92, font=Outfit, text_color="#1C1C1E", fg_color=adh_color, bg_color="white", hover=False, command=ChangementAdherent).grid(row=2, column=3, sticky="e")
    CTkButton(root, text="LIVRE", corner_radius=20, height=35, width=61, font=Outfit, text_color="#1C1C1E", fg_color=livre_color, bg_color="white", hover=False, command=ChangementLivre).grid(row=2, column=4)
    CTkButton(root, text="EMPRUNT", corner_radius=20, height=35, width=79, font=Outfit, text_color="#1C1C1E", fg_color=emp_color, bg_color="white", hover=False, command=ChangementEmprunts).grid(row=2, column=5, sticky="w")
    
    CTkLabel(root, text="", corner_radius=10, height=10, width=230, font=Outfit, text_color="#1C1C1E", fg_color="#0A1437").grid(row=1, column=6, columnspan=2)
    CTkButton(root, text="QUITTER", corner_radius=20, height=50, width=87, font=Outfit, text_color="#1C1C1E", fg_color="#BAC8EB", hover=False, command=Quitter).grid(row=1, rowspan=3, column=8, columnspan=2)

# --- Tab View: Adherents ---
def affichage_liste_adherent():
    global EntryNom, EntryPrenom, EntryMail, EntryTelephone, EntryRechercheAdherent
    
    CTkLabel(root, text="", corner_radius=10, height=30, font=Outfit, fg_color="#0A1437").grid(row=4, column=0)
    CTkLabel(root, text="", corner_radius=15, height=70, width=1025, font=Outfit, text_color="white", fg_color="white").grid(row=5, rowspan=3, column=1, columnspan=10)
    
    EntryNom = CTkEntry(root, placeholder_text="Nom", placeholder_text_color="#7882A5", width=180, corner_radius=10, height=50, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryNom.grid(row=6, column=1, padx=(20, 0))
    EntryPrenom = CTkEntry(root, placeholder_text="Prenom", placeholder_text_color="#7882A5", corner_radius=10, height=50, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", width=180, border_width=0)
    EntryPrenom.grid(row=6, column=2)
    EntryMail = CTkEntry(root, placeholder_text="Mail", placeholder_text_color="#7882A5", corner_radius=10, height=50, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", width=180, border_width=0)
    EntryMail.grid(row=6, column=3, columnspan=2)
    EntryTelephone = CTkEntry(root, placeholder_text="Telephone", placeholder_text_color="#7882A5", corner_radius=10, height=50, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", width=180, border_width=0)
    EntryTelephone.grid(row=6, column=5, columnspan=2, padx=(20, 0))
    CTkButton(root, text="AJOUTER", corner_radius=20, height=50, width=87, font=Outfit, text_color="#1C1C1E", fg_color="#BAC8EB", bg_color="white", hover=False, command=Ajouter_Adherent).grid(row=6, column=8, columnspan=2)
    
    CTkLabel(root, text="", corner_radius=15, height=70, width=600, font=Outfit, text_color="white", fg_color="white").grid(row=9, rowspan=3, column=1, columnspan=4)
    EntryRechercheAdherent = CTkEntry(root, placeholder_text="Rechercher un Adherent", placeholder_text_color="#7882A5", corner_radius=10, height=50, width=380, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryRechercheAdherent.grid(row=10, column=1, columnspan=2)
    CTkButton(root, text="RECHERCHER", corner_radius=20, height=50, width=87, font=Outfit, text_color="#1C1C1E", fg_color="#BAC8EB", bg_color="white", hover=False, command=RechercherAdherent).grid(row=10, column=3, columnspan=2, sticky="e", padx=(0, 20))
    
    display_count = len(Liste_Affiche)
    hauteur_deca = 50 + 55 * display_count if display_count > 0 else 100
    CTkLabel(root, text="", corner_radius=15, height=hauteur_deca, width=1025, font=Outfit, text_color="white", fg_color="white").grid(row=13, rowspan=22, column=1, columnspan=10, sticky="n")
    
    CTkButton(root, text="Nom >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("nomAdherent", "adherent")).grid(row=13, column=1, pady=10, sticky="w", padx=(25, 0))
    CTkButton(root, text="Prenom >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("prenomAdherent", "adherent")).grid(row=13, column=2, pady=10, sticky="w", padx=(10, 0))
    CTkButton(root, text="Mail >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("Mail", "adherent")).grid(row=13, column=3, columnspan=2, pady=10, sticky="w", padx=(10, 0))
    CTkButton(root, text="Telephone >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("telephone", "adherent")).grid(row=13, column=5, columnspan=2, pady=10, sticky="w", padx=(10, 0))
    CTkButton(root, text="Identifiant >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("identifiant", "adherent")).grid(row=13, column=7, columnspan=2, pady=10, sticky="w", padx=(10, 0))
    CTkProgressBar(root, height=1, width=1040, fg_color="#E6E6E6", progress_color="#E6E6E6", border_width=0).grid(row=14, column=1, columnspan=10)
    
    for i, item in enumerate(Liste_Affiche):
        CTkLabel(root, wraplength=180, text=Lim(item[1], 2), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=1, sticky="w", padx=(25, 0))
        CTkLabel(root, wraplength=180, text=Lim(item[2], 2), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=2, sticky="w", padx=(10, 0))
        CTkLabel(root, wraplength=180, text=Lim(item[3], 2), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=3, columnspan=2, sticky="w", padx=(10, 0))
        CTkLabel(root, wraplength=180, text=Lim(item[4], 3), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=5, columnspan=2, sticky="w", padx=(10, 0))
        CTkLabel(root, wraplength=180, text=Lim(str(item[0]), 4), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=7, columnspan=2, sticky="w", padx=(10, 0))
        CTkButton(root, bg_color="white", fg_color="white", hover_color="red", text="", image=Image_Poubelle, width=15, height=15, command=lambda row=i, p=num_liste_affiche: delete(row, p)).grid(row=15 + 2 * i, column=7, columnspan=3, sticky="e", padx=(0, 20))
        if i != display_count - 1:
            CTkProgressBar(root, height=1, width=1040, fg_color="#E6E6E6", progress_color="#E6E6E6", border_width=0).grid(row=16 + 2 * i, column=1, columnspan=10)
    
    if num_liste_affiche > 1:
        CTkButton(root, bg_color="white", fg_color="white", text="", image=Image_Previous_Page, width=15, height=15, hover_color="#BAC8EB", command=Previous_Page).grid(row=13, column=8)
    if num_liste_affiche < num_liste_max:
        CTkButton(root, bg_color="white", fg_color="white", text="", image=Image_Next_Page, width=15, height=15, hover_color="#BAC8EB", command=Next_Page).grid(row=13, column=9, sticky="w")

# --- Tab View: Livres ---
def affichage_liste_livre():
    global EntryScanLivre, EntryCategorie, EntryRechercheLivre
    
    CTkLabel(root, text="", corner_radius=10, height=30, font=Outfit, fg_color="#0A1437").grid(row=4, column=0)
    CTkLabel(root, text="", corner_radius=15, height=70, width=715, font=Outfit, text_color="white", fg_color="white").grid(row=5, rowspan=3, column=1, columnspan=5, sticky="w")
    
    EntryScanLivre = CTkEntry(root, placeholder_text="ISBN du livre", placeholder_text_color="#7882A5", width=400, corner_radius=10, height=50, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryScanLivre.grid(row=6, column=1, columnspan=2, sticky="w", padx=(10, 0))
    EntryCategorie = CTkEntry(root, placeholder_text="Categorie", placeholder_text_color="#7882A5", corner_radius=10, height=50, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", width=180, border_width=0)
    EntryCategorie.grid(row=6, column=2, columnspan=3, padx=(0, 15), sticky="e")
    CTkButton(root, text="AJOUTER", corner_radius=20, height=50, width=87, font=Outfit, text_color="#1C1C1E", fg_color="#BAC8EB", bg_color="white", hover=False, command=Ajouter_Livre).grid(row=6, column=5, padx=(0, 25), sticky="w")
    
    CTkLabel(root, text="", corner_radius=15, height=70, width=600, font=Outfit, text_color="white", fg_color="white").grid(row=9, rowspan=3, column=1, columnspan=4, padx=(0, 20))
    EntryRechercheLivre = CTkEntry(root, placeholder_text="Rechercher un livre", placeholder_text_color="#7882A5", corner_radius=10, height=50, width=380, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryRechercheLivre.grid(row=10, column=1, columnspan=2, sticky="w", padx=(10, 0))
    CTkButton(root, text="RECHERCHER", corner_radius=20, height=50, width=87, font=Outfit, text_color="#1C1C1E", fg_color="#BAC8EB", bg_color="white", hover=False, command=RechercherLivre).grid(row=10, column=3, columnspan=2, sticky="e", padx=(0, 30))
    
    display_count = len(Liste_Affiche)
    hauteur_deca = 50 + 55 * display_count if display_count > 0 else 100
    CTkLabel(root, text="", corner_radius=15, height=hauteur_deca, width=1035, font=Outfit, text_color="white", fg_color="white").grid(row=13, rowspan=22, column=1, columnspan=10, sticky="n", padx=(0, 25))
    
    CTkButton(root, text="ISBN >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("isbn", "livre")).grid(row=13, column=1, pady=10, sticky="w", padx=(5, 0))
    CTkButton(root, text="Titre >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("titre", "livre")).grid(row=13, column=1, columnspan=2, padx=(100, 0), sticky="w")
    CTkButton(root, text="Auteur >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("auteur", "livre")).grid(row=13, column=3, columnspan=2, pady=10, sticky="w", padx=(10, 0))
    CTkButton(root, text="Editeur >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("editeur", "livre")).grid(row=13, column=5, columnspan=2, pady=10, sticky="w", padx=(10, 0))
    CTkButton(root, text="Categorie >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("categorie", "livre")).grid(row=13, column=7, columnspan=2, pady=10, sticky="w", padx=(0, 0))
    CTkProgressBar(root, height=1, width=1060, fg_color="#E6E6E6", progress_color="#E6E6E6", border_width=0).grid(row=14, column=1, columnspan=10)
    
    for i, item in enumerate(Liste_Affiche):
        CTkLabel(root, text=Lim(item[0], 4), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=1, sticky="w", padx=(15, 0))
        CTkLabel(root, text=Lim(item[1], 1), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=1, columnspan=2, padx=(100, 0), sticky="w")
        CTkLabel(root, text=Lim(item[2], 2), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=3, columnspan=2, sticky="w", padx=(10, 0))
        CTkLabel(root, text=Lim(item[3], 3), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=5, columnspan=2, sticky="w", padx=(10, 0))
        cat_val = item[6] if len(item) > 6 else ""
        CTkLabel(root, text=Lim(cat_val, 4), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=7, columnspan=2, sticky="w", padx=(10, 0))
        CTkButton(root, bg_color="white", fg_color="white", hover_color="red", text="", image=Image_Poubelle, width=15, height=15, command=lambda row=i, p=num_liste_affiche: delete(row, p)).grid(row=15 + 2 * i, column=7, columnspan=3, sticky="e", padx=(0, 20))
        if i != display_count - 1:
            CTkProgressBar(root, height=1, width=1060, fg_color="#E6E6E6", progress_color="#E6E6E6", border_width=0).grid(row=16 + 2 * i, column=1, columnspan=10)
    
    if num_liste_affiche > 1:
        CTkButton(root, bg_color="white", fg_color="white", text="", image=Image_Previous_Page, width=15, height=15, hover_color="#BAC8EB", command=Previous_Page).grid(row=13, column=8, columnspan=2, sticky="w")
    if num_liste_affiche < num_liste_max:
        CTkButton(root, bg_color="white", fg_color="white", text="", image=Image_Next_Page, width=15, height=15, hover_color="#BAC8EB", command=Next_Page).grid(row=13, column=8, columnspan=2)

# --- Tab View: Emprunts ---
def affichage_liste_emprunts():
    global EntryScanEmprunt, EntryAdherentCarte, EntryRechercheEmprunt
    
    CTkLabel(root, text="", corner_radius=10, height=30, font=Outfit, fg_color="#0A1437").grid(row=4, column=0)
    CTkLabel(root, text="", corner_radius=15, height=70, width=1025, font=Outfit, text_color="white", fg_color="white").grid(row=5, rowspan=3, column=1, columnspan=10, sticky="w")
    
    EntryScanEmprunt = CTkEntry(root, placeholder_text="ISBN du livre", placeholder_text_color="#7882A5", width=370, corner_radius=10, height=50, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryScanEmprunt.grid(row=6, column=1, columnspan=3, padx=(10, 0), sticky="w")
    EntryAdherentCarte = CTkEntry(root, placeholder_text="Identifiant de l'adherent", placeholder_text_color="#7882A5", corner_radius=10, height=50, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", width=370, border_width=0)
    EntryAdherentCarte.grid(row=6, column=2, columnspan=6, sticky="w", padx=(190, 0))
    CTkButton(root, text="RETOUR", corner_radius=20, height=50, width=110, font=Outfit, text_color="#1C1C1E", fg_color="#BAC8EB", bg_color="white", hover=False, command=Retour).grid(row=6, column=6, columnspan=4, padx=(0, 130), sticky="e")
    CTkButton(root, text="AJOUTER", corner_radius=20, height=50, width=110, font=Outfit, text_color="#1C1C1E", fg_color="#BAC8EB", bg_color="white", hover=False, command=Emprunt).grid(row=6, column=7, columnspan=3, padx=(0, 10), sticky="e")
    
    CTkLabel(root, text="", corner_radius=15, height=70, width=600, font=Outfit, text_color="white", fg_color="white").grid(row=9, rowspan=3, column=1, columnspan=4, padx=(0, 10))
    EntryRechercheEmprunt = CTkEntry(root, placeholder_text="Rechercher un Emprunt", placeholder_text_color="#7882A5", corner_radius=10, height=50, width=380, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryRechercheEmprunt.grid(row=10, column=1, columnspan=2, padx=(0, 10))
    CTkButton(root, text="RECHERCHER", corner_radius=20, height=50, width=87, font=Outfit, text_color="#1C1C1E", fg_color="#BAC8EB", bg_color="white", hover=False, command=RechercherEmprunt).grid(row=10, column=3, columnspan=2, sticky="e", padx=(0, 20))
    
    btn_retard_text = "Tous les emprunts" if page == "retard" else "Livres en retard"
    CTkButton(root, text=btn_retard_text, corner_radius=15, height=30, width=125, font=Outfit, text_color="#1C1C1E", fg_color="white", hover=False, command=Retard).grid(row=9, rowspan=3, column=7, columnspan=3, padx=(90, 0))
    
    display_count = len(Liste_Affiche)
    hauteur_deca = 50 + 55 * display_count if display_count > 0 else 100
    CTkLabel(root, text="", corner_radius=15, height=hauteur_deca, width=1025, font=Outfit, text_color="white", fg_color="white").grid(row=13, rowspan=22, column=1, columnspan=10, sticky="wn")
    
    table_name = page
    CTkButton(root, text="Livre >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("NomLivre", table_name)).grid(row=13, column=1, pady=10, sticky="w", padx=(25, 0))
    CTkButton(root, text="Auteur >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("Auteur", table_name)).grid(row=13, column=2, pady=10, sticky="w", padx=(10, 0))
    CTkButton(root, text="Nom Adherent >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("NomAdherent", table_name)).grid(row=13, column=3, columnspan=2, pady=10, sticky="w", padx=(10, 0))
    CTkButton(root, text="Prenom >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("PrenomAdherent", table_name)).grid(row=13, column=5, columnspan=2, pady=10, sticky="w", padx=(10, 0))
    CTkButton(root, text="Retour >", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, hover=False, command=lambda: sortby("DateRetour", table_name)).grid(row=13, column=7, columnspan=2, pady=10, sticky="w", padx=(10, 0))
    CTkProgressBar(root, height=1, width=1040, fg_color="#E6E6E6", progress_color="#E6E6E6", border_width=0).grid(row=14, column=1, columnspan=10)
    
    for i, item in enumerate(Liste_Affiche):
        CTkLabel(root, wraplength=180, text=Lim(item[1], 1), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=1, sticky="nw", padx=(25, 0))
        CTkLabel(root, wraplength=180, text=Lim(item[7], 2), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=2, sticky="nw", padx=(10, 0))
        CTkLabel(root, wraplength=180, text=Lim(item[6], 2), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=3, columnspan=2, sticky="nw", padx=(10, 0))
        CTkLabel(root, wraplength=180, text=Lim(item[8], 2), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=5, columnspan=2, sticky="nw", padx=(10, 0))
        date_retour_str = str(item[3])
        CTkLabel(root, wraplength=180, text=Lim(date_retour_str, 4), text_color="#1C1C1E", fg_color="white", bg_color="white", height=40, font=Outfit).grid(row=15 + 2 * i, column=7, columnspan=2, sticky="nw", padx=(10, 0))
        
        if date_retour_str <= str(today_date):
            CTkButton(root, bg_color="white", fg_color="white", hover_color="red", text="", image=Image_Retard, width=15, height=15, command=lambda row=i, p=num_liste_affiche: delete(row, p)).grid(row=15 + 2 * i, column=7, columnspan=3, sticky="e", padx=(0, 20))
        if i != display_count - 1:
            CTkProgressBar(root, height=1, width=1040, fg_color="#E6E6E6", progress_color="#E6E6E6", border_width=0).grid(row=16 + 2 * i, column=1, columnspan=10)
    
    if num_liste_affiche > 1:
        CTkButton(root, bg_color="white", fg_color="white", text="", image=Image_Previous_Page, width=15, height=15, hover_color="#BAC8EB", command=Previous_Page).grid(row=13, column=8)
    if num_liste_affiche < num_liste_max:
        CTkButton(root, bg_color="white", fg_color="white", text="", image=Image_Next_Page, width=15, height=15, hover_color="#BAC8EB", command=Next_Page).grid(row=13, column=9, sticky="w")

# --- Pagination Controller ---
def update_page_view(items, render_func):
    global Liste_Affiche, num_liste_affiche, num_liste_max
    num_liste_max = max(1, (len(items) + 9) // 10)
    if num_liste_affiche < 1:
        num_liste_affiche = 1
    elif num_liste_affiche > num_liste_max:
        num_liste_affiche = num_liste_max
    
    start_idx = (num_liste_affiche - 1) * 10
    end_idx = min(start_idx + 10, len(items))
    Liste_Affiche = items[start_idx:end_idx]
    
    clear_frame()
    affichage_menu()
    render_func()

def Previous_Page():
    global num_liste_affiche
    if num_liste_affiche > 1:
        num_liste_affiche -= 1
        refresh_current_tab()

def Next_Page():
    global num_liste_affiche, num_liste_max
    if num_liste_affiche < num_liste_max:
        num_liste_affiche += 1
        refresh_current_tab()

def refresh_current_tab():
    if page == "adherent":
        update_page_view(Liste_Adherent, affichage_liste_adherent)
    elif page == "livre":
        update_page_view(Liste_Livre, affichage_liste_livre)
    elif page in ("emprunt", "retard"):
        update_page_view(Liste_Emprunt, affichage_liste_emprunts)

# --- Tab Switchers ---
def ChangementAdherent():
    global page, Liste_Adherent, num_liste_affiche
    page = "adherent"
    Liste_Adherent = db.fetchall("SELECT * FROM adherent")
    num_liste_affiche = 1
    update_page_view(Liste_Adherent, affichage_liste_adherent)

def ChangementLivre():
    global page, Liste_Livre, num_liste_affiche
    page = "livre"
    Liste_Livre = db.fetchall("SELECT * FROM livre")
    num_liste_affiche = 1
    update_page_view(Liste_Livre, affichage_liste_livre)

def ChangementEmprunts():
    global page, Liste_Emprunt, num_liste_affiche
    page = "emprunt"
    Liste_Emprunt = db.fetchall("SELECT * FROM emprunt")
    num_liste_affiche = 1
    update_page_view(Liste_Emprunt, affichage_liste_emprunts)

# --- Data Actions ---
def delete(row, page_affiche):
    global num_liste_affiche, Liste_Adherent, Liste_Livre, Liste_Emprunt
    idx = (page_affiche - 1) * 10 + row
    if page == "adherent" and idx < len(Liste_Adherent):
        identifiant = Liste_Adherent[idx][0]
        db.execute("DELETE FROM adherent WHERE identifiant=?", (identifiant,))
        db.commit()
        Liste_Adherent.pop(idx)
        update_page_view(Liste_Adherent, affichage_liste_adherent)
    elif page == "livre" and idx < len(Liste_Livre):
        idlivre = Liste_Livre[idx][4]
        db.execute("DELETE FROM livre WHERE idlivre=?", (idlivre,))
        db.commit()
        Liste_Livre.pop(idx)
        update_page_view(Liste_Livre, affichage_liste_livre)
    elif page in ("emprunt", "retard") and idx < len(Liste_Emprunt):
        num_livre = Liste_Emprunt[idx][0]
        identifiant = Liste_Emprunt[idx][5]
        db.execute("DELETE FROM emprunt WHERE NumLivre=? AND Identifiant=?", (num_livre, identifiant))
        db.commit()
        Liste_Emprunt.pop(idx)
        update_page_view(Liste_Emprunt, affichage_liste_emprunts)

def sortby(column, table):
    global Liste_Livre, Liste_Adherent, Liste_Emprunt, num_liste_affiche
    num_liste_affiche = 1
    if table == "livre":
        Liste_Livre = db.fetchall(f"SELECT * FROM livre ORDER BY {column} COLLATE NOCASE ASC")
        update_page_view(Liste_Livre, affichage_liste_livre)
    elif table == "adherent":
        Liste_Adherent = db.fetchall(f"SELECT * FROM adherent ORDER BY {column} COLLATE NOCASE ASC")
        update_page_view(Liste_Adherent, affichage_liste_adherent)
    elif table == "retard":
        Liste_Emprunt = db.fetchall(f"SELECT * FROM emprunt WHERE DATE(DateRetour) < CURRENT_DATE ORDER BY {column} COLLATE NOCASE ASC")
        update_page_view(Liste_Emprunt, affichage_liste_emprunts)
    else:
        Liste_Emprunt = db.fetchall(f"SELECT * FROM emprunt ORDER BY {column} COLLATE NOCASE ASC")
        update_page_view(Liste_Emprunt, affichage_liste_emprunts)

def Ajouter_Livre():
    categorie = EntryCategorie.get().strip() if EntryCategorie else ""
    isbn = EntryScanLivre.get().strip() if EntryScanLivre else ""
    try:
        book = meta(isbn) if isbn else None
    except Exception:
        book = None
    
    if book:
        authors = book.get("Authors", [])
        auteur = Edit_Nb_Auteur(str(authors)[2:-2]) if authors else ""
        titre = str(book.get("Title", ""))
        editeur = Edit_Nb_Auteur(str(book.get("Publisher", "")))
    else:
        auteur = ""
        titre = ""
        editeur = ""
    affichage_confirmation_livre(titre, auteur, categorie, editeur, isbn)

def Ajouter_Adherent():
    nom = EntryNom.get().strip() if EntryNom else ""
    prenom = EntryPrenom.get().strip() if EntryPrenom else ""
    mail = EntryMail.get().strip() if EntryMail else ""
    telephone = EntryTelephone.get().strip() if EntryTelephone else ""
    affichage_confirmation_adherent(nom, prenom, mail, telephone)

def Emprunt():
    global Liste_Emprunt
    id_livre_input = EntryScanEmprunt.get().strip() if EntryScanEmprunt else ""
    id_adh_input = EntryAdherentCarte.get().strip() if EntryAdherentCarte else ""
    if not id_livre_input or not id_adh_input:
        return
    
    data_livre = db.fetchone("SELECT * FROM livre WHERE isbn=? OR CAST(idlivre AS TEXT)=?", (id_livre_input, id_livre_input))
    data_adherent = db.fetchone("SELECT * FROM adherent WHERE CAST(identifiant AS TEXT)=?", (id_adh_input,))
    
    if not data_livre or not data_adherent:
        return
    
    num_livre = str(data_livre[4])
    nom_livre = str(data_livre[1])
    date_emp = str(today_date)
    date_ret = str(today_date + td)
    id_adh = data_adherent[0]
    nom_adh = str(data_adherent[1])
    prenom_adh = str(data_adherent[2])
    auteurs = str(data_livre[2])
    
    try:
        db.execute("INSERT INTO emprunt(NumLivre, NomLivre, DateEmprunt, DateRetour, Identifiant, NomAdherent, PrenomAdherent, Auteur) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (num_livre, nom_livre, date_emp, date_ret, id_adh, nom_adh, prenom_adh, auteurs))
        db.commit()
    except Exception as e:
        print(f"Erreur lors de l'emprunt: {e}")
    
    Liste_Emprunt = db.fetchall("SELECT * FROM emprunt")
    update_page_view(Liste_Emprunt, affichage_liste_emprunts)

def Retour():
    global Liste_Emprunt
    id_livre_input = EntryScanEmprunt.get().strip() if EntryScanEmprunt else ""
    id_adh_input = EntryAdherentCarte.get().strip() if EntryAdherentCarte else ""
    if not id_livre_input or not id_adh_input:
        return
    
    data_livre = db.fetchone("SELECT * FROM livre WHERE isbn=? OR CAST(idlivre AS TEXT)=?", (id_livre_input, id_livre_input))
    if not data_livre:
        return
    
    num_livre = str(data_livre[4])
    db.execute("DELETE FROM emprunt WHERE NumLivre=? AND CAST(Identifiant AS TEXT)=?", (num_livre, id_adh_input))
    db.commit()
    
    Liste_Emprunt = db.fetchall("SELECT * FROM emprunt")
    update_page_view(Liste_Emprunt, affichage_liste_emprunts)

def RechercherAdherent():
    global Liste_Adherent
    term = EntryRechercheAdherent.get().strip() if EntryRechercheAdherent else ""
    param = f"%{term}%"
    res = db.fetchall("SELECT * FROM adherent WHERE nomAdherent LIKE ? OR prenomAdherent LIKE ? OR Mail LIKE ? OR telephone LIKE ? OR CAST(identifiant AS TEXT) LIKE ?",
                      (param, param, param, param, param))
    Liste_Adherent = res if res else []
    update_page_view(Liste_Adherent, affichage_liste_adherent)

def RechercherLivre():
    global Liste_Livre
    term = EntryRechercheLivre.get().strip() if EntryRechercheLivre else ""
    param = f"%{term}%"
    res = db.fetchall("SELECT * FROM livre WHERE isbn LIKE ? OR titre LIKE ? OR auteur LIKE ? OR CAST(idlivre AS TEXT) LIKE ? OR editeur LIKE ? OR categorie LIKE ?",
                      (param, param, param, param, param, param))
    Liste_Livre = res if res else []
    update_page_view(Liste_Livre, affichage_liste_livre)

def RechercherEmprunt():
    global Liste_Emprunt
    term = EntryRechercheEmprunt.get().strip() if EntryRechercheEmprunt else ""
    param = f"%{term}%"
    if page == "retard":
        res = db.fetchall("SELECT * FROM emprunt WHERE DATE(DateRetour) < CURRENT_DATE AND (NomLivre LIKE ? OR Auteur LIKE ? OR NomAdherent LIKE ? OR PrenomAdherent LIKE ? OR DateRetour LIKE ?)",
                          (param, param, param, param, param))
    else:
        res = db.fetchall("SELECT * FROM emprunt WHERE NomLivre LIKE ? OR Auteur LIKE ? OR NomAdherent LIKE ? OR PrenomAdherent LIKE ? OR DateRetour LIKE ?",
                          (param, param, param, param, param))
    Liste_Emprunt = res if res else []
    update_page_view(Liste_Emprunt, affichage_liste_emprunts)

def Retard():
    global page, Liste_Emprunt
    if page == "emprunt":
        page = "retard"
        Liste_Emprunt = db.fetchall("SELECT * FROM emprunt WHERE DATE(DateRetour) < CURRENT_DATE")
    else:
        page = "emprunt"
        Liste_Emprunt = db.fetchall("SELECT * FROM emprunt")
    update_page_view(Liste_Emprunt, affichage_liste_emprunts)

def annuler():
    global root_annexe
    if root_annexe:
        root_annexe.destroy()
        root_annexe = None

def addlivre(isbn, titre, auteur, editeur, categorie):
    global root_annexe
    if EntryISBN_Pop and EntryISBN_Pop.get().strip():
        isbn = EntryISBN_Pop.get().strip()
    if EntryTitre_Pop and EntryTitre_Pop.get().strip():
        titre = EntryTitre_Pop.get().strip()
    if EntryAuteur_Pop and EntryAuteur_Pop.get().strip():
        auteur = EntryAuteur_Pop.get().strip()
    if EntryEditeur_Pop and EntryEditeur_Pop.get().strip():
        editeur = EntryEditeur_Pop.get().strip()
    if EntryCategorie_Pop and EntryCategorie_Pop.get().strip():
        categorie = EntryCategorie_Pop.get().strip()
    
    db.execute("INSERT INTO livre(isbn, titre, auteur, editeur, categorie) VALUES (?, ?, ?, ?, ?)",
               (str(isbn), str(titre), str(auteur), str(editeur), str(categorie)))
    db.commit()
    annuler()
    ChangementLivre()

def addadherent(nom, prenom, mail, telephone):
    global root_annexe
    if EntryNom_Pop and EntryNom_Pop.get().strip():
        nom = EntryNom_Pop.get().strip()
    if EntryPrenom_Pop and EntryPrenom_Pop.get().strip():
        prenom = EntryPrenom_Pop.get().strip()
    if EntryMail_Pop and EntryMail_Pop.get().strip():
        mail = EntryMail_Pop.get().strip()
    if EntryTel_Pop and EntryTel_Pop.get().strip():
        telephone = EntryTel_Pop.get().strip()
    
    db.execute("INSERT INTO adherent(nomAdherent, prenomAdherent, Mail, telephone) VALUES (?, ?, ?, ?)",
               (str(nom), str(prenom), str(mail), str(telephone)))
    db.commit()
    annuler()
    ChangementAdherent()

# --- Modal Dialogs ---
def affichage_confirmation_livre(titre, auteur, categorie, editeur, isbn):
    global root_annexe, EntryISBN_Pop, EntryTitre_Pop, EntryAuteur_Pop, EntryEditeur_Pop, EntryCategorie_Pop
    annuler()
    
    root_annexe = CTkToplevel(root)
    root_annexe.geometry("440x500")
    root_annexe.title("Confirmation d'ajout - Livre")
    root_annexe.configure(fg_color="#0A1437")
    root_annexe.resizable(False, False)
    root_annexe.attributes("-topmost", True)
    
    CTkLabel(root_annexe, text="", corner_radius=10, height=20, width=10, font=Outfit, fg_color="#0A1437").grid(row=0, column=0)
    CTkLabel(root_annexe, text="", corner_radius=10, height=450, width=400, font=Outfit, text_color="#1C1C1E", fg_color="white").grid(row=1, rowspan=15, column=1, columnspan=4, sticky="n")
    CTkLabel(root_annexe, text="Confirmation d'ajout", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold).grid(row=1, column=1, sticky="sw", padx=(20, 0), pady=(10, 20))
    
    CTkLabel(root_annexe, text="Titre", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, height=20).grid(row=2, column=1, sticky="sw", padx=(20, 0))
    EntryTitre_Pop = CTkEntry(root_annexe, placeholder_text="Titre", placeholder_text_color="#7882A5", width=350, corner_radius=10, height=40, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryTitre_Pop.grid(row=3, column=1, sticky="nw", padx=(20, 0))
    if titre:
        EntryTitre_Pop.insert(0, titre)
    
    CTkLabel(root_annexe, text="Auteur", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, height=20).grid(row=4, column=1, sticky="sw", padx=(20, 0))
    EntryAuteur_Pop = CTkEntry(root_annexe, placeholder_text="Auteur", placeholder_text_color="#7882A5", width=350, corner_radius=10, height=40, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryAuteur_Pop.grid(row=5, column=1, sticky="nw", padx=(20, 0))
    if auteur:
        EntryAuteur_Pop.insert(0, auteur)
    
    CTkLabel(root_annexe, text="Categorie", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, height=20).grid(row=6, column=1, sticky="sw", padx=(20, 0))
    EntryCategorie_Pop = CTkEntry(root_annexe, placeholder_text="Categorie", placeholder_text_color="#7882A5", width=350, corner_radius=10, height=40, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryCategorie_Pop.grid(row=7, column=1, sticky="nw", padx=(20, 0))
    if categorie:
        EntryCategorie_Pop.insert(0, categorie)
    
    CTkLabel(root_annexe, text="Editeur", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, height=20).grid(row=8, column=1, sticky="sw", padx=(20, 0))
    EntryEditeur_Pop = CTkEntry(root_annexe, placeholder_text="Editeur", placeholder_text_color="#7882A5", width=350, corner_radius=10, height=40, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryEditeur_Pop.grid(row=9, column=1, sticky="nw", padx=(20, 0))
    if editeur:
        EntryEditeur_Pop.insert(0, editeur)
    
    CTkLabel(root_annexe, text="ISBN", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, height=20).grid(row=10, column=1, sticky="sw", padx=(20, 0))
    EntryISBN_Pop = CTkEntry(root_annexe, placeholder_text="ISBN", placeholder_text_color="#7882A5", width=350, corner_radius=10, height=40, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryISBN_Pop.grid(row=11, column=1, sticky="nw", padx=(20, 0))
    if isbn:
        EntryISBN_Pop.insert(0, isbn)
    
    CTkLabel(root_annexe, text="", text_color="#1C1C1E", fg_color="#1C1C1E", bg_color="#1C1C1E").grid(row=12, column=0)
    CTkButton(root_annexe, text="ANNULER", corner_radius=20, height=50, width=87, font=Outfit, text_color="#1C1C1E", fg_color="#BAC8EB", bg_color="white", hover=False, command=annuler).grid(row=14, column=1, columnspan=2, sticky="w", padx=(10, 0), pady=(0, 10))
    CTkButton(root_annexe, text="AJOUTER", corner_radius=20, height=50, width=87, font=Outfit, text_color="#1C1C1E", fg_color="#BAC8EB", bg_color="white", hover=False, command=lambda: addlivre(isbn, titre, auteur, editeur, categorie)).grid(row=14, column=1, columnspan=4, sticky="e", padx=(0, 10), pady=(0, 10))

def affichage_confirmation_adherent(nom, prenom, mail, telephone):
    global root_annexe, EntryNom_Pop, EntryPrenom_Pop, EntryMail_Pop, EntryTel_Pop
    annuler()
    
    root_annexe = CTkToplevel(root)
    root_annexe.geometry("440x500")
    root_annexe.title("Confirmation d'ajout - Adherent")
    root_annexe.configure(fg_color="#0A1437")
    root_annexe.resizable(False, False)
    root_annexe.attributes("-topmost", True)
    
    CTkLabel(root_annexe, text="", corner_radius=10, height=20, width=10, font=Outfit, fg_color="#0A1437").grid(row=0, column=0)
    CTkLabel(root_annexe, text="", corner_radius=10, height=450, width=400, font=Outfit, text_color="#1C1C1E", fg_color="white").grid(row=1, rowspan=15, column=1, columnspan=4, sticky="n")
    CTkLabel(root_annexe, text="Confirmation d'ajout", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold).grid(row=1, column=1, sticky="sw", padx=(20, 0), pady=(10, 20))
    
    CTkLabel(root_annexe, text="Nom", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, height=20).grid(row=2, column=1, sticky="sw", padx=(20, 0))
    EntryNom_Pop = CTkEntry(root_annexe, placeholder_text="Nom", placeholder_text_color="#7882A5", width=350, corner_radius=10, height=40, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryNom_Pop.grid(row=3, column=1, sticky="nw", padx=(20, 0))
    if nom:
        EntryNom_Pop.insert(0, nom)
    
    CTkLabel(root_annexe, text="Prenom", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, height=20).grid(row=4, column=1, sticky="sw", padx=(20, 0))
    EntryPrenom_Pop = CTkEntry(root_annexe, placeholder_text="Prenom", placeholder_text_color="#7882A5", width=350, corner_radius=10, height=40, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryPrenom_Pop.grid(row=5, column=1, sticky="nw", padx=(20, 0))
    if prenom:
        EntryPrenom_Pop.insert(0, prenom)
    
    CTkLabel(root_annexe, text="Mail", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, height=20).grid(row=6, column=1, sticky="sw", padx=(20, 0))
    EntryMail_Pop = CTkEntry(root_annexe, placeholder_text="Mail", placeholder_text_color="#7882A5", width=350, corner_radius=10, height=40, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryMail_Pop.grid(row=7, column=1, sticky="nw", padx=(20, 0))
    if mail:
        EntryMail_Pop.insert(0, mail)
    
    CTkLabel(root_annexe, text="Telephone", text_color="#1C1C1E", fg_color="white", bg_color="white", font=OutfitBold, height=20).grid(row=8, column=1, sticky="sw", padx=(20, 0))
    EntryTel_Pop = CTkEntry(root_annexe, placeholder_text="Telephone", placeholder_text_color="#7882A5", width=350, corner_radius=10, height=40, font=Outfit, text_color="#1C1C1E", fg_color="#E5EAF8", bg_color="white", border_width=0)
    EntryTel_Pop.grid(row=9, column=1, sticky="nw", padx=(20, 0))
    if telephone:
        EntryTel_Pop.insert(0, telephone)
    
    CTkLabel(root_annexe, text="", text_color="#1C1C1E", fg_color="#1C1C1E", bg_color="#1C1C1E").grid(row=12, column=0)
    CTkButton(root_annexe, text="ANNULER", corner_radius=20, height=40, width=87, font=Outfit, text_color="#1C1C1E", fg_color="#BAC8EB", bg_color="white", hover=False, command=annuler).grid(row=14, column=1, columnspan=2, sticky="w", padx=(20, 0), pady=(0, 10))
    CTkButton(root_annexe, text="AJOUTER", corner_radius=20, height=40, width=87, font=Outfit, text_color="#1C1C1E", fg_color="#BAC8EB", bg_color="white", hover=False, command=lambda: addadherent(nom, prenom, mail, telephone)).grid(row=14, column=1, columnspan=4, sticky="e", padx=(0, 10), pady=(0, 10))

def Quitter():
    db.close()
    root.destroy()
    sys.exit(0)

if __name__ == "__main__":
    ChangementLivre()
    root.mainloop()

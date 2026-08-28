# 📚 BIBLIOTECH

<p align="center">
  <img src="img_readme/fond.PNG" alt="Bannière BIBLIOTECH" width="800"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3"/>
  <img src="https://img.shields.io/badge/Interface-CustomTkinter-blue?style=for-the-badge" alt="CustomTkinter"/>
  <img src="https://img.shields.io/badge/Base_de_Données-SQLite3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite3"/>
  <img src="https://img.shields.io/badge/Matériel-NFC%20%2F%20RFID-4C8BF5?style=for-the-badge" alt="NFC"/>
  <img src="https://img.shields.io/badge/Auteur-Tayeb%20Bekkouche-orange?style=for-the-badge" alt="Auteur"/>
</p>

<p align="center">
  <b>Logiciel Moderne de Gestion de Bibliothèque Sans Contact & Desktop</b><br/>
  (Read in <a href="README.md">English 🇬🇧</a>)
</p>

---

## 📌 Sommaire
1. [Présentation Générale](#-présentation-générale)
2. [Fonctionnalités Clés](#-fonctionnalités-clés)
3. [Interface Utilisateur](#-interface-utilisateur)
4. [Technologies Utilisées](#-technologies-utilisées)
5. [Installation & Lancement](#-installation--lancement)
6. [Guide d'Utilisation](#-guide-dutilisation)
7. [Architecture du Projet](#-architecture-du-projet)
8. [Auteur & Crédits](#-auteur--crédits)

---

## 🌟 Présentation Générale

**BIBLIOTECH** est un logiciel complet et ergonomique de gestion de bibliothèque. Il modernise et simplifie le travail des bibliothécaires et documentalistes en combinant la recherche bibliographique automatisée par ISBN et la technologie sans contact (NFC/RFID) pour l'identification rapide des adhérents et le suivi des ouvrages.

---

## ✨ Fonctionnalités Clés

- 📖 **Gestion du Catalogue de Livres** : Ajout, recherche multicritère, tri dynamique et suppression de livres avec récupération automatique des métadonnées (titre, auteur, éditeur, catégorie) par code ISBN.
- 👤 **Répertoire des Adhérents** : Gestion complète des adhérents (nom, prénom, courriel, téléphone, identifiant unique).
- 🔄 **Gestion des Emprunts & Retours** : Enregistrement simplifié des prêts avec calcul automatique de la date d'échéance (30 jours).
- ⏰ **Suivi des Retards** : Onglet dédié mettant en évidence les prêts en retard avec alertes visuelles.
- 🏷️ **Technologie NFC / RFID** : Prise en charge des lecteurs de cartes et badges NFC pour une identification instantanée.
- 🎨 **Interface Graphique Moderne** : Développée avec CustomTkinter, thématique sombre élégante, pagination fluide et filtres en direct.

---

## 🖥️ Interface Utilisateur

### Menu Principal (Catalogue des Livres)
<p align="center">
  <img src="img_readme/menu_livre.PNG" alt="Menu Livres" width="750"/>
</p>

### Fenêtres Modales de Confirmation
<p align="center">
  <img src="img_readme/Capture.PNG" alt="Confirmation Adhérent" width="450"/>
  &nbsp;&nbsp;
  <img src="img_readme/Capture2.PNG" alt="Confirmation Livre" width="450"/>
</p>

---

## 🛠️ Technologies Utilisées

| Technologie | Rôle |
| :--- | :--- |
| **[Python 3](https://www.python.org/)** | Langage principal de développement |
| **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** | Framework d'interface graphique moderne |
| **[SQLite3](https://docs.python.org/3/library/sqlite3.html)** | Moteur de base de données relationnelle embarquée |
| **[isbnlib](https://pypi.org/project/isbnlib/)** | Récupération automatisée des données bibliographiques par ISBN |
| **[Pillow (PIL)](https://pillow.readthedocs.io/)** | Traitement et affichage des icônes et images |
| **[nfcpy](https://nfcpy.readthedocs.io/) / smartcard** | Gestion de la technologie sans contact NFC / RFID |

---

## 🚀 Installation & Lancement

### Prérequis
- Python 3.9 ou version ultérieure.

### 1. Cloner le dépôt
```bash
git clone https://github.com/tayebg/BIBLIOTECH.git
cd BIBLIOTECH
```

### 2. Créer et activer l'environnement virtuel
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r sources/Annexe/requirements.txt
```

### 4. Démarrer l'application

#### Version Standard (Sans matériel NFC requis)
```bash
cd sources
python BIBLIOTECH.py
```

#### Version avec Matériel NFC
```bash
cd sources
python BIBLIOTECH_nfc.py
```

---

## 📖 Guide d'Utilisation

1. **Ajouter un livre** : Dans l'onglet **LIVRE**, scannez ou saisissez l'ISBN, renseignez la catégorie, puis cliquez sur **AJOUTER**. Les informations du livre sont automatiquement importées.
2. **Ajouter un adhérent** : Dans l'onglet **ADHERENT**, entrez les coordonnées de l'adhérent puis cliquez sur **AJOUTER**.
3. **Emprunter un livre** : Dans l'onglet **EMPRUNT**, entrez l'ISBN du livre et l'identifiant adhérent, puis cliquez sur **AJOUTER**.
4. **Retourner un livre** : Dans l'onglet **EMPRUNT**, entrez l'ISBN et l'identifiant, puis cliquez sur **RETOUR**.
5. **Consulter les retards** : Cliquez sur le bouton **Livres en retard** pour filtrer instantanément les emprunts échus.

---

## 📁 Architecture du Projet

```
BIBLIOTECH/
├── img_readme/              # Captures d'écran et illustrations
├── sources/
│   ├── Annexe/
│   │   ├── font/            # Polices d'écriture (Outfit)
│   │   ├── icones/          # Icônes de l'interface
│   │   └── requirements.txt # Dépendances Python
│   ├── nfc/                 # Pilotes et modules pour le matériel NFC
│   ├── BIBLIOTECH.py        # Application principale (desktop standard)
│   ├── BIBLIOTECH_nfc.py    # Application avec support matériel NFC
│   ├── bibliotheque.db      # Base de données SQLite (standard)
│   └── bibliotheque_nfc.db  # Base de données SQLite (NFC)
├── .gitignore
├── README.md                # Documentation en anglais
└── README_fr.md             # Documentation en français
```

---

## ✍️ Auteur & Crédits

- **Auteur & Développeur** : [Tayeb Bekkouche (@tayebg)](https://github.com/tayebg)  
- **Courriel** : [tayebekk2004@gmail.com](mailto:tayebekk2004@gmail.com)  
- **Dépôt GitHub** : [https://github.com/tayebg/BIBLIOTECH](https://github.com/tayebg/BIBLIOTECH)

> *Projet modernisé, optimisé et maintenu par Tayeb Bekkouche.*

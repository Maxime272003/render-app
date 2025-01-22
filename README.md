# Automatisation de Rendus avec Maya et Arnold

Cette application permet de faciliter et d'automatiser les rendus avec Maya et Arnold. Elle offre une interface graphique pour configurer des rendus, les ajouter à une file d'attente, et exécuter plusieurs rendus en séquence.

---

## 📥 Télécharger l'exécutable
**Téléchargez la dernière version ici** :  
[📥 Télécharger maintenant](https://github.com/Maxime272003/render-app/releases/latest/download/render-app.exe)

---

## Fonctionnalités principales
- **Rendu unique** : Lancez un rendu unique en sélectionnant une scène et des paramètres de rendu.
- **File d'attente** : Ajoutez plusieurs configurations de rendu à une file d'attente et exécutez-les en séquence.
- **Types de rendu** :
  - `Rendu complet` : Rendu de toutes les images d'une plage définie.
  - `Rendu rapide (FML)` : Rendu de trois images : la première, celle du milieu et la dernière.
- **Paramètres dynamiques** : Configurez les chemins pour Maya et les plugins Qt selon votre environnement.

---

## Prérequis
### Logiciels nécessaires
- **Maya** : Assurez-vous que Maya est installé sur votre système.
- **Arnold** : Le moteur de rendu Arnold doit être activé dans Maya.

### Dépendances Python
- **PyQt5** : Installez avec la commande :
  ```bash
  pip install PyQt5
  ```

---

## Installation et utilisation
### Étapes d'installation
#### Option 1 : Utilisation du fichier exécutable
1. Téléchargez le fichier `.exe` généré dans le dossier `dist/` (disponible après le build).
2. Exécutez le fichier `.exe` directement pour lancer l'application.

#### Option 2 : Construire l'application vous-même
1. Clonez ou téléchargez ce projet dans un répertoire local :
   ```bash
   git clone https://github.com/Maxime272003/render-app.git
   cd render-app
   ```
2. Installez les dépendances nécessaires :
   ```bash
   pip install PyQt5
   ```
3. Générez un fichier exécutable avec PyInstaller :
   ```bash
   pyinstaller --onefile ./render-app.py
   ```
4. Le fichier exécutable sera généré dans le dossier `dist/`.
5. Lancez le fichier `.exe` généré pour utiliser l'application.

---

## Configuration des paramètres
### Chemins requis
Avant de lancer l'application, configurez les chemins pour Maya et les plugins Qt :
1. Cliquez sur le bouton **Paramètres** dans l'application.
2. Configurez les chemins suivants :
   - **Chemin Maya (bin)** : Le dossier `bin` de votre installation Maya (par exemple : `C:\Program Files\Autodesk\Maya2024\bin`).
   - **Chemin Qt Plugins** : Le dossier contenant les plugins Qt de Maya (par exemple : `C:\Program Files\Autodesk\Maya2024\plugins`).
3. Sauvegardez les paramètres.

### Chargement automatique
Les chemins configurés sont sauvegardés dans un fichier `config.ini` et rechargés automatiquement à chaque lancement de l'application.

---

## Utilisation de l'application
### Rendu unique
1. Remplissez les champs nécessaires :
   - Chemin de la scène Maya (`*.ma` ou `*.mb`).
   - Frame de début et de fin.
   - Répertoire de sortie.
   - Résolution en pourcentage (facultatif).
2. Sélectionnez le type de rendu (`Rendu complet` ou `Rendu rapide (FML)`).
3. Cliquez sur **Lancer**.

### File d'attente
1. Configurez un rendu en suivant les étapes du rendu unique.
2. Cliquez sur **Ajouter à la file d'attente**.
3. Répétez pour ajouter plusieurs rendus.
4. Cliquez sur **Lancer** pour exécuter tous les rendus de la file d'attente.

### Gestion de la file d'attente
- Pour supprimer un rendu, sélectionnez-le dans la liste et cliquez sur **Supprimer le rendu sélectionné**.

---

## Logs et diagnostics
Les messages relatifs aux rendus (commandes, succès, erreurs) sont affichés dans la section des logs de l'application. Utilisez ces informations pour diagnostiquer les problèmes si nécessaire.

---

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à soumettre des pull requests ou à signaler des problèmes.

---

## Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

# ng20-lda

**Sandeep-Singh NIRMAL – Manel LOUNISSI – Brice SAILLARD**  
Projet de **Packaging Python – M2**

Package Python permettant :
- l’export de documents du dataset **20 Newsgroups**,
- l’entraînement d’un modèle **LDA**,
- la description de documents par topics,
- le comptage du nombre de lignes d’un fichier,
- l’exposition des fonctionnalités via **CLI** et **API HTTP (FastAPI)**,
- la génération de documentation avec **Sphinx**.

---

## Fonctionnalités

### CLI (ligne de commande)
Un exécutable unique `ng20` avec sous-commandes :
- `export` : export de documents 20 Newsgroups
- `train-lda` : entraînement d’un modèle LDA
- `describe` : description d’un document par topics
- `count-lines` : comptage du nombre de lignes
- `serve` : lancement de l’API HTTP

### API HTTP (FastAPI)
- `/health`
- `/count-lines`
- `/export`
- `/describe`

Documentation interactive Swagger disponible à :  
👉 **http://127.0.0.1:8000/docs**

### Qualité logicielle
- Tests unitaires avec **pytest**
- Tests basés sur des propriétés avec **hypothesis**
- Logging avec le module `logging`
- Docstrings au format **Google**
- Documentation générée avec **Sphinx**

---

## Installation

### 1. Cloner le projet
```bash
git clone https://github.com/singh-24-01/Packaging.git
cd Packaging
```

### 2. Créer et activer un environnement virtuel
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer le package
```bash
pip install --upgrade pip
pip install .
```

## Utilisation – CLI
Export de documents 20 Newsgroups
```bash
ng20 export sci.space 10 ./output
```
→ Crée output/sci.space/ contenant les fichiers i.txt


## Entraîner un modèle LDA
```bash
ng20 train-lda ./output ./model
```
→ Enregistre le modèle entraîné (pickle)


## Décrire un document
```bash
ng20 describe ./output/sci.space/0.txt ./model
```
→ Affiche les 3 premiers topics avec leurs 5 mots principaux.

## Compter le nombre de lignes
```bash
ng20 count-lines ./output/sci.space/0.txt
```

## Lancer l’API HTTP

Démarrage du serveur
```bash
ng20 serve
```
Le serveur est accessible à :

→ API : http://127.0.0.1:8000

→ Documentation Swagger : http://127.0.0.1:8000/docs

⚠️ Important :
Le serveur doit être lancé dans un terminal dédié et laissé actif pendant l’utilisation de l’API.


## Tests
Lancer tous les tests
```bash
pytest
```
## Les tests couvrent :

→ les fonctions de comptage de lignes,

→ les tests classiques (pytest),

→ les tests de propriétés (hypothesis).


## Documentation Sphinx

La documentation HTML est générée avec Sphinx et inclut :

→ les modules,

→ les fonctions,

→ les docstrings

Elle est disponible dans :
```bash
doc/build/html/index.html
```

### Structure du projet

Packaging/
├── src/ng20_lda/        # Code source du package
├── tests/               # Tests unitaires
├── doc/                 # Documentation Sphinx
├── README.md
├── pyproject.toml
├── setup.cfg
└── setup.py

## Licence

Projet académique - usage pédagogique


















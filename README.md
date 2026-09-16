# NWIMFull

NWIM est une application de bureau pour la modélisation hydrologique pluie-débit. Elle permet de calibrer et valider des modèles conceptuels de transformation pluie-débit à partir de séries temporelles observées (pluie, débit, données climatiques), avec calage manuel ou automatique (optimisation), calcul d'évapotranspiration, et régression par apprentissage automatique.

L'application est construite avec PySide6 (Qt for Python) : la logique métier est écrite en Python, l'interface utilisateur en QML.

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Architecture du projet](#architecture-du-projet)
- [Modèles disponibles](#modèles-disponibles)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Lancement](#lancement)
- [Génération d'un exécutable](#génération-dun-exécutable)
- [Structure des fichiers](#structure-des-fichiers)

## Fonctionnalités

- **Chargement de données** : import de séries temporelles (pluie, débit, données climatiques) au format tabulaire.
- **Calcul d'évapotranspiration (ETP)** à partir de données climatiques.
- **Calage manuel** des paramètres du modèle pluie-débit avec visualisation immédiate des résultats simulés vs observés.
- **Calage automatique (optimisation)** des paramètres par algorithmes métaheuristiques (recherche sur grille, algorithme génétique, évolution différentielle, hypercube latin).
- **Comblement de lacunes / régression** par des modèles d'apprentissage automatique (KNN, forêt aléatoire, ridge, SVM, XGBoost) pour reconstituer des séries incomplètes.
- **Séparation d'hydrogramme (débit de base)** selon plusieurs méthodes de récession classiques.
- **Évaluation des performances** du modèle via des critères statistiques usuels (NSE, KGE, RMSE, MAE, MAPE, R²).
- **Export** des paramètres calés (JSON), des séries simulées (texte) et des graphiques.

## Architecture du projet

Le projet suit une séparation en trois couches :

| Couche | Rôle |
|---|---|
| `backend/` | Cœur scientifique : modèles hydrologiques (production, pertes, routage, débit de base), optimisation, régression, calcul d'ETP. Pur Python, indépendant de l'interface. |
| `api/` | Couche d'exposition des objets Python vers QML (`QObject`, signaux/slots exposés via `Property`/`Slot`), gestion des fichiers et modèles de données tabulaires. |
| `frontend/` (+ `io/qml/`) | Interface utilisateur QML : pages, composants graphiques, formulaires de paramètres. |

Le point d'entrée `main.py` instancie les objets métier (calibration manuelle/automatique, gestion de fichiers, ETP, régression, etc.), les expose au moteur QML via `setContextProperty`, puis charge `main.qml`.

Les modèles hydrologiques sont créés dynamiquement via des **fabriques** (pattern *Factory*), ce qui permet d'ajouter facilement une nouvelle méthode sans modifier le code appelant :

- `ProductionFactory` — méthodes de production de pluie nette
- `InitialLossFactory` — méthodes de pertes initiales
- `RecessionFactory` — méthodes de séparation d'écoulement / débit de base
- `RoutingFactory` — méthodes de routage / transfert
- `OptimizationFactory` — algorithmes d'optimisation pour le calage automatique
- `MLFactory` — modèles de régression pour le comblement de lacunes

Le module `backend/simulation/Simulation.py` orchestre l'ensemble de la chaîne de calcul : production → pertes initiales → routage → débit de base, puis calcule les métriques de performance en calage et en validation.

## Modèles disponibles

**Production de pluie nette**
- SCS
- WMin
- Horton modifié
- Philip

**Séparation d'écoulement / débit de base**
- Chapman
- Furey-Gupta
- Récession quadratique
- Récession exponentielle
- Eckhardt
- Boughton

**Routage / transfert**
- HUN
- Nash
- Muskingum
- PLA

**Optimisation (calage automatique)**
- Hypercube latin (Latin Hypercube)
- Algorithme génétique
- Évolution différentielle

**Régression (comblement de lacunes)**
- KNN
- Forêt aléatoire (Random Forest)
- Ridge
- SVM
- XGBoost

## Prérequis

- Python 3.10 ou supérieur
- pip

## Installation

1. Cloner ou récupérer le projet, puis se placer à la racine :

   ```bash
   cd NWIMFull-main
   ```

2. Créer un environnement virtuel (recommandé) :

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   venv\Scripts\activate         # Windows
   ```

3. Installer les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

   > Le fichier `requirements.txt` liste les dépendances principales (`PySide6`, `numpy`, `matplotlib`, `pandas`). Le module `backend/simulation/Simulation.py` utilise également le package `permetrics` pour le calcul des métriques de performance ; s'il n'est pas installé automatiquement, ajoutez-le manuellement :
   >
   > ```bash
   > pip install permetrics
   > ```
   >
   > De même, si les modèles de régression sont utilisés, assurez-vous que `scikit-learn` et `xgboost` sont disponibles dans l'environnement.

## Lancement

Depuis la racine du projet :

```bash
python main.py
```

L'application s'ouvre dans une fenêtre Qt. Le menu principal donne accès aux différentes fonctionnalités : chargement de données, calcul d'ETP, calage manuel (page d'accueil), optimisation, grille de paramètres, régression et débit de base.

> **Note (rendu graphique) :** `main.py` force par défaut le backend de rendu Qt sur OpenGL (`QSG_RHI_BACKEND=opengl`) pour plus de stabilité sur certaines cartes graphiques. Si l'application ne se lance pas correctement, essayez de forcer un rendu logiciel en modifiant cette variable dans `main.py` (`QSG_RHI_BACKEND=software`).

## Génération d'un exécutable

Un fichier de configuration `pysidedeploy.spec` est fourni pour générer un exécutable autonome avec `pyside6-deploy` (basé sur Nuitka). Ce fichier contient des chemins spécifiques à l'environnement Windows d'origine ; adaptez les champs `project_dir`, `input_file`, `exec_directory`, `icon` et `python_path` à votre propre environnement avant de lancer :

```bash
pyside6-deploy -c pysidedeploy.spec
```

## Structure des fichiers

```
NWIMFull-main/
├── main.py                    # Point d'entrée de l'application
├── main.qml                   # Fenêtre principale et navigation QML
├── requirements.txt           # Dépendances Python
├── pysidedeploy.spec          # Configuration de packaging (pyside6-deploy)
│
├── api/                       # Pont entre le backend Python et l'interface QML
│   ├── FactoryManager.py
│   ├── GridParametersQML.py
│   ├── InitialLossQML.py
│   ├── OptimizationQML.py
│   ├── ParametersQML.py
│   ├── ProductionQML.py
│   ├── RangeParametersQML.py
│   ├── RecessionQML.py
│   ├── RoutingQML.py
│   ├── TestQML.py
│   ├── load_data/             # Gestion des fichiers, modèles de tables (PandasModel, TableModel...)
│   └── simulation/            # Contrôleurs de simulation exposés à QML (calage manuel/auto, grille)
│
├── backend/                   # Cœur scientifique (indépendant de l'UI)
│   ├── baseFlow/              # Méthodes de séparation d'écoulement (Chapman, Eckhardt, Boughton...)
│   ├── contracts/             # Types de données partagés (TypedDict) entre modules
│   ├── factory/                # Fabriques de création des modèles
│   ├── grid/                  # Recherche par grille de paramètres
│   ├── initialLoss/           # Méthodes de pertes initiales
│   ├── optimization/          # Algorithmes d'optimisation (LHC, algo génétique, évolution différentielle)
│   ├── production/            # Méthodes de production de pluie nette (SCS, WMin, Horton, Philip)
│   ├── pte/                   # Calcul de l'évapotranspiration
│   ├── ptq/                   # Gestion des séries pluie-température-débit (PTQ)
│   ├── regressor/              # Modèles de régression / apprentissage automatique
│   ├── results/                # Export des résultats de simulation
│   ├── routing/                # Méthodes de routage / transfert (HUN, Nash, Muskingum, PLA)
│   ├── simulation/             # Orchestration de la chaîne de calcul complète
│   ├── smooth/                 # Lissage de séries
│   └── workers/                # Threads d'exécution en arrière-plan
│
├── frontend/                   # Interface utilisateur QML
│   ├── components/
│   │   ├── chartsComponents/   # Composants graphiques (courbes, hydrogrammes)
│   │   ├── customComponents/   # Composants réutilisables (boutons, dialogues de fichiers, menus...)
│   │   ├── datasetComponents/  # Composants de visualisation/édition de jeux de données
│   │   ├── pages/               # Pages principales (HomePage, LoadData, Optimization, Regression, BaseFlow, ETPComputing, GridParametersDialog)
│   │   └── parameters/          # Formulaires de saisie des paramètres de modèle
│   └── icons/                   # Ressources graphiques
│
└── io/qml/                     # Types QML enregistrés côté Python (métadonnées Qt générées)
```

## Licence

Aucune licence n'est actuellement définie pour ce projet.

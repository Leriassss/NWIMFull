class KNNModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode KNN.
    """

    Metrics = {
        0: 'euclidean',
        1: 'manhattan',
        2: 'minkowski'
    }
    Weights = {
        0: 'uniform',
        1: 'distance'
    }

    def __init__(self, n_neighbors, weights, metric):
        """
        Initialise et valide les données pour la méthode KNN.
        :param n_neighbors: Nombre de voisins (int > 0)
        :param weights: Type de pondération (0=uniform, 1=distance)
        :param metric: Type de métrique (0=euclidean, 1=manhattan, 2=minkowski)
        """
        self.n_neighbors = int(float(n_neighbors))
        self.weights = int(float(weights))
        self.metric = int(float(metric))
        self.validate()

    def validate(self):
        """Valide les paramètres."""
        if self.n_neighbors <= 0:
            raise ValueError("Le paramètre 'n_neighbors' doit être un entier strictement positif.")
        if self.weights not in (0,1):
            raise ValueError("Only 0 (uniform) 1 (distance) accepted")
        if self.metric not in [0, 1, 2]:
            raise ValueError("Only 0 (euclidean) 1 (manhattan) 2 (minkowski) accepted")

    def to_dict(self):
        """Retourne les paramètres sous forme de dictionnaire."""
        return {
            'n_neighbors': self.n_neighbors,
            'weights': self.Weights[self.weights],
            'metric': self.Metrics[self.metric]
        }

    @staticmethod
    def get_parameter_names():
        """Retourne un mapping clé → nom lisible."""
        return {
            "n_neighbors": "Nombre de voisins",
            "weights": "Pondération",
            "metric": "Métrique"
        }

    @staticmethod
    def get_default_ranges():
        """Retourne les plages de valeurs par défaut."""
        return {
            "n_neighbors": [1, 100],
            "weights": [0, 1],
            "metric": [0, 2]
        }

    @staticmethod
    def get_default_values():
        """Retourne les valeurs par défaut."""
        return {
            "n_neighbors": 5,
            "weights": 0,
            "metric": 0
        }

    @staticmethod
    def validate_parameter(key, value):
        """
        Vérifie dynamiquement la validité d'un paramètre spécifique.
        :param key: Nom du paramètre à vérifier.
        :param value: Valeur du paramètre.
        :return: True si valide, sinon message d'erreur.
        """
        try:
            value = int(float(value))
            if key == "n_neighbors" and value <= 0:
                raise ValueError("Le paramètre 'n_neighbors' doit être un entier strictement positif.")
            elif key == "weights" and value not in [0, 1]:
                raise ValueError("Only 0 (uniform) 1 (distance) accepted")
            elif key == "metric" and value not in [0, 1, 2]:
                raise ValueError("Only 0 (euclidean) 1 (manhattan) 2 (minkowski) accepted")
            return True
        except Exception as e:
            return str(e)

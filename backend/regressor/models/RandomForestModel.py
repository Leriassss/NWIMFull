class RandomForestModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode Random Forest.
    """

    def __init__(self, n_estimators, max_depth, min_samples_split):
        """
        Initialise et valide les données pour la méthode Random Forest.
        :param n_estimators: Nombre d'arbres dans la forêt (int > 0)
        :param max_depth: Profondeur maximale des arbres (int > 0 ou None)
        :param min_samples_split: Nombre minimum d'échantillons pour diviser un nœud (int >= 2)
        """
        self.n_estimators = int(float(n_estimators))
        self.max_depth =  int(float(max_depth))
        self.min_samples_split = int(float(min_samples_split))
        self.validate()

    def validate(self):
        """Valide les paramètres."""
        if self.n_estimators <= 0:
            raise ValueError("Le paramètre 'n_estimators' doit être un entier strictement positif.")
        if  self.max_depth <0:
            raise ValueError("Le paramètre 'max_depth' doit être un entier strictement positif ou  0 (None).")
        if self.min_samples_split < 2:
            raise ValueError("Le paramètre 'min_samples_split' doit être un entier supérieur ou égal à 2.")

    def to_dict(self):
        """Retourne les paramètres sous forme de dictionnaire."""
        return {
            'n_estimators': self.n_estimators,
            'max_depth': self.max_depth if self.max_depth>0 else None,
            'min_samples_split': self.min_samples_split
        }

    @staticmethod
    def get_parameter_names():
        """Retourne un mapping clé → nom lisible."""
        return {
            "n_estimators": "Nombre d'arbres",
            "max_depth": "Profondeur maximale",
            "min_samples_split": "Échantillons min. pour division"
        }

    @staticmethod
    def get_default_ranges():
        """Retourne les plages de valeurs par défaut."""
        return {
            "n_estimators": [10, 500],
            "max_depth": [1, 50],  # None est aussi accepté
            "min_samples_split": [2, 20]
        }

    @staticmethod
    def get_default_values():
        """Retourne les valeurs par défaut."""
        return {
            "n_estimators": 100,
            "max_depth": 1,
            "min_samples_split": 2
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
            if key == "max_depth" and value <= 0:
                return True
            if key == "n_estimators" and value <= 0:
                raise ValueError("Le paramètre 'n_estimators' doit être un entier strictement positif.")
            elif key == "max_depth" and value < 0:
                raise ValueError("Le paramètre 'max_depth' doit être un entier strictement positif ou 0 (None) .")
            elif key == "min_samples_split" and value < 2:
                raise ValueError("Le paramètre 'min_samples_split' doit être >= 2.")
            return True
        except Exception as e:
            return str(e)

class SVMModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode SVM.
    """

    Kernels ={
        0 : 'linear',
        1: 'rbf',
        2 : 'sigmoid',
        3 : 'poly'
    } 

    def __init__(self, kernel, C, gamma, epsilon):
        """
        Initialise et valide les données pour la méthode SVM.
        :param kernel: Type de noyau ('linear' ou 'rbf')
        :param C: Paramètre de régularisation (int > 0)
        :param gamma: Coefficient gamma (float dans Gamma_values)
        :param epsilon: Paramètre epsilon (float dans Epsilon_values)
        """
        self.kernel = int(float(kernel))
        self.C = float(C)
        self.gamma = float(gamma)
        self.epsilon = float(epsilon)
        self.validate()

    def validate(self):
        """Valide les paramètres."""
        if self.kernel not in [0,1,2,3]:
            raise ValueError(f"Le paramètre 'kernel' doit être parmi {SVMModel.Kernels}.")
        if self.C  < 0 :
            raise ValueError(f"Le paramètre 'C' doit être positif")
        if self.gamma < 0 :
            raise ValueError(f"Le paramètre 'gamma' doit être doit être positif.")
        if self.epsilon < 0 :
            raise ValueError(f"Le paramètre 'epsilon' doit être doit être positif.")

    def to_dict(self):
        """Retourne les paramètres sous forme de dictionnaire."""
        return {
            'kernel': self.Kernels[self.kernel],
            'C': self.C,
            'gamma': self.gamma,
            'epsilon': self.epsilon
        }

    @staticmethod
    def get_parameter_names():
        """Retourne un mapping clé → nom lisible."""
        return {
            "kernel": "Type de noyau",
            "C": "Régularisation C",
            "gamma": "Gamma",
            "epsilon": "Epsilon"
        }

    @staticmethod
    def get_default_ranges():
        """Retourne les plages de valeurs par défaut."""
        return {
            "kernel":  [None, None],
            "C": [None, None],
            "gamma":  [None, None],
            "epsilon":  [None, None]
        }

    @staticmethod
    def get_default_values():
        """Retourne les valeurs par défaut."""
        return {
            "kernel": 0,
            "C": 1,
            "gamma": 0.1,
            "epsilon": 0.1
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
            value = float(value)
            if key == "kernel":
                if int(value) not in [0,1,2,3]:
                    raise ValueError(f"Le paramètre 'kernel' doit être parmi {SVMModel.Kernels}.")
            elif key == "C":
                if value < 0 :
                    raise ValueError(f"Le paramètre 'C' doit être positif.")
            elif key == "gamma":
                if value < 0 :
                    raise ValueError(f"Le paramètre 'gamma' doit être positif")
            elif key == "epsilon":
                if value < 0 :
                    raise ValueError(f"Le paramètre 'epsilon' doit être positif")
            return True
        except Exception as e:
            return str(e)

class DEModel:
    def __init__(self, maxiter=1000, popsize=15, tol=0.01, mutation=0.5, recombination=0.7):
        self.maxiter = maxiter
        self.popsize = popsize
        self.tol = tol
        self.mutation = mutation
        self.recombination = recombination

        self.validate()

    def validate(self):
        """ Vérifie tous les paramètres à l'initialisation. """
        for key, value in self.to_dict().items():
            validation = self.validate_parameter(key, value)
            if validation is not True:
                raise ValueError(validation)

    def to_dict(self):
        """ Retourne les paramètres sous forme de dictionnaire. """
        return {
            'maxiter': self.maxiter,
            'popsize': self.popsize,
            'tol': self.tol,
            'mutation': (self.mutation,1),
            'recombination': self.recombination
        }

    @staticmethod
    def get_parameter_names():
        """ Retourne les noms des paramètres avec leurs descriptions. """
        return {
            'maxiter': "Nombre maximal d'itérations",
            'popsize': "Taille de la population",
            'tol': "Tolérance d'arrêt",
            'mutation': "Probabilité de mutation",
            'recombination': "Taux de recombinaison"
        }

    @staticmethod
    def validate_parameter(key, value):
        """
        Vérifie dynamiquement la validité d'un paramètre spécifique.

        :param key: Nom du paramètre à vérifier.
        :param value: Valeur du paramètre à valider.
        :return: True si valide, sinon un message d'erreur.
        """
        try:
            if key == "maxiter":
                if not isinstance(value, int) or value <= 0:
                    raise ValueError("maxiter doit être un entier positif.")
            elif key == "popsize":
                if not isinstance(value, int) or value <= 0:
                    raise ValueError("popsize doit être un entier positif.")
            elif key == "tol":
                value = float(value)
                if not (0 < value <= 1):
                    raise ValueError("tol doit être un float strictement compris entre 0 et 1.")
            elif key == "mutation":
                value = float(value)
                if not (0 < value < 1):
                    raise ValueError("mutation doit être compris entre 0 et 1.")
            elif key == "recombination":
                value = float(value)
                if not (0 <= value <= 1):
                    raise ValueError("recombination doit être un float entre 0 et 1.")
            else:
                raise ValueError("Paramètre inconnu : {key}")
            return True
        except Exception as e:
            return str(e)


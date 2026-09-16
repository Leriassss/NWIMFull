class HortonModifiedModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode Horton.
    """

    def __init__(self, init_storage, smax, k):
        """
        Initialise et valide les données pour la méthode Horton.

        :param prec: Série pandas contenant les précipitations (en mm).
        :param f_0: Taux d'infiltration initial (en mm/h).
        :param f_t: Taux d'infiltration final (en mm/h).
        :param k: Constante de décroissance exponentielle (en 1/h).
        """
        self.init_storage = float(init_storage)
        self.smax = float(smax)
        self.k = float(k)
        self.validate()

    def validate(self):
        try:
            if self.init_storage  < 0 or self.init_storage > 1:
                raise ValueError("Le paramètre doit être compris entre 0 et 1.")
            if self.smax < 0 : 
                raise ValueError("Le paramètre doit être strictement positif.")
            if self.k  < 0 or self.k > 1:
                raise ValueError("Le paramètre doit être compris entre 0 et 1.")
            return True  # Si aucune erreur, le paramètre est valide

        except Exception as e:
            return str(e)  # Retourne le message d'erreur



    def to_dict(self):
        return {
                'init_storage': self.init_storage,
                'smax': self.smax,
                'k': self.k
            }

    @staticmethod
    def get_parameter_names():
        return {
            "init_storage" : "intial capacity",
            "smax" : "storage capacity",
            "k" : "k"
    }

    @staticmethod
    def get_default_ranges():
        return {
                "init_storage" : [0,1],
                "smax" : [1,20],
                "k" : [0,1]
        }
    @staticmethod
    def get_default_values():
        return {
                "init_storage" : 0.5,
                "smax" : 10,
                "k" : 0.1
            }

    @staticmethod
    def validate_parameter(key, value):
        try:
            value = float(value)  # S'assure que la valeur est un nombre

            if key == "init_storage" and (value < 0 or value > 1):
                raise ValueError("Le paramètre doit être compris entre 0 et 1.")
            elif key == "smax" and value <= 0:
                raise ValueError("Le paramètre doit être strictement positif.")
            elif key == "k" and (value < 0 or value > 1):
                raise ValueError("Le paramètre doit être compris entre 0 et 1.")
            return True  # Si aucune erreur, le paramètre est valide

        except Exception as e:
            return str(e)  # Retourne le message d'erreur


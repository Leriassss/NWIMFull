class HortonModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode Horton.
    """

    def __init__(self, f_0, f_t, k):
        """
        Initialise et valide les données pour la méthode Horton.

        :param prec: Série pandas contenant les précipitations (en mm).
        :param f_0: Taux d'infiltration initial (en mm/h).
        :param f_t: Taux d'infiltration final (en mm/h).
        :param k: Constante de décroissance exponentielle (en 1/h).
        """
        self.f_0 = float(f_0)
        self.f_t = float(f_t)
        self.k = float(k)
        self.validate()

    def validate(self):
        if any(param <= 0 for param in [self.f_0, self.f_t, self.k]):
            raise ValueError("Les paramètres doivent être strictement positifs.")


    def to_dict(self):
        return {
                'f_0': self.f_0,
                'f_t': self.f_t,
                'k': self.k
            }

    @staticmethod
    def get_parameter_names():
        return {
            "f_0" : "f_0",
            "f_t" : "f_t",
            "k" : "k"
    }

    @staticmethod
    def get_default_ranges():
        return {
                "f_0" : [1,10],
                "f_t" : [1,1.5],
                "k" : [1,1.5]
        }
    @staticmethod
    def get_default_values():
        return {
                "f_0" : 10,
                "f_t" : 1.5,
                "k" : 1
            }

    @staticmethod
    def validate_parameter(key, value):
        try:
            value = float(value)  # S'assure que la valeur est un nombre

            if key == "f_0" and value <= 0:
                raise ValueError("Le paramètre doit être strictement positif.")
            elif key == "f_t" and value <= 0:
                raise ValueError("Le paramètre doit être strictement positif.")
            elif key == "k" and value <= 0:
                raise ValueError("Le paramètre doit être strictement positif.")
            return True  # Si aucune erreur, le paramètre est valide

        except Exception as e:
            return str(e)  # Retourne le message d'erreur


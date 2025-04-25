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
        self.f_0 = f_0
        self.f_t = f_t
        self.k = k
        self.validate()

    def validate(self):
        try:
            value = float(value)  # S'assure que la valeur est un nombre
            if key == "curve_number" and not (0 <= value <= 100):
                raise ValueError("Le paramètre 'curve_number' doit être compris entre 0 et 100.")
            elif key == "i_a" and not (0 < value <= 1):
                raise ValueError("Le paramètre 'i_a' doit être compris entre 0 et 1.")
            return True
        except Exception as e:
            return str(e)

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
    def validate_parameter(key, value):
        """
        Vérifie dynamiquement la validité d'un paramètre spécifique.

        :param key: Nom du paramètre à vérifier.
        :param value: Valeur du paramètre à valider.
        :return: True si valide, sinon un message d'erreur est retourné.
        """
        try:
            value = float(value)  # S'assure que la valeur est un nombre
            if key == "curve_number" and not (0 <= value <= 100):
                raise ValueError("Le paramètre 'curve_number' doit être compris entre 0 et 100.")
            elif key == "i_a" and not (0 < value <= 1):
                raise ValueError("Le paramètre 'i_a' doit être compris entre 0 et 1.")
            return True
        except Exception as e:
            return str(e)


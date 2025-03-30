class PhilipModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode Philip.
    """

    def __init__(self, S: float, K: float):
        """
        Initialise et valide les données pour la méthode Philip.

        :param prec: Série pandas contenant les précipitations (en mm).
        :param S: Paramètre d'absorption (positif).
        :param K: Conductivité hydraulique (positif).
        """
        self.S = S
        self.K = K
        self.validate()

    def validate(self):
        """
        Valide les paramètres du modèle.
        """
        if self.S <= 0 or self.K <= 0:
            raise ValueError("Les paramètres 'S' et 'K' doivent être positifs.")


    def to_dict(self):
        return {
                'S': self.S,
                "K" : self.K
            }

    @staticmethod
    def get_parameter_names():
            return {
                'S': "S",
                "K" : "K"
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
            if key == "S" and value <= 0:
                raise ValueError("Le paramètre 'S' doit être strictement positif.")
            elif key == "K" and value <= 0:
                raise ValueError("Le paramètre 'K' doit être strictement positif.")
            return True  # Si aucune erreur, le paramètre est valide
        except Exception as e:
            return str(e)  # Retourne le message d'erreur

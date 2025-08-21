class PhilipModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode Philip.
    """

    def __init__(self, K: float):
        """
        Initialise et valide les données pour la méthode Philip.

        :param prec: Série pandas contenant les précipitations (en mm).
        :param S: Paramètre d'absorption (positif).
        :param K: Conductivité hydraulique (positif).
        """
        self.K = float(K)
        self.validate()

    def validate(self):
        """
        Valide les paramètres du modèle.
        """
        try:
            if self.K <= 0:
                raise ValueError("Le paramètre 'K' doit être strictement positif.")
            return True  # Si aucune erreur, le paramètre est valide
        except Exception as e:
            return str(e)  # Retourne le message d'erreur

    def to_dict(self):
        return {
                "K" : self.K
            }

    @staticmethod
    def get_parameter_names():
            return {
                "K" : "K"
        }

    @staticmethod
    def get_default_ranges():
        return {
                "K" : [1,10]
        }
    
    @staticmethod
    def get_default_values():
        return {
                "K" : 10
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
            if key == "K" and value <= 0:
                raise ValueError("Le paramètre 'K' doit être strictement positif.")
            return True  # Si aucune erreur, le paramètre est valide
        except Exception as e:
            return str(e)  # Retourne le message d'erreur

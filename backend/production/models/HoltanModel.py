class HoltanModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode Holtan.
    """

    def __init__(self,f_0, f_t, k, storage_capacity):
        """
        Initialise et valide les données pour la méthode Holtan.
        :param f_0: Taux d'infiltration initial (en mm/h).
        :param f_t: Taux d'infiltration final (en mm/h).
        :param k: Exposant empirique du modèle.
        :param storage_capacity: Capacité de stockage du sol (en mm).
        """
        self.f_0 = float(f_0)
        self.f_t = float(f_t)
        self.k = float(k)
        self.storage_capacity = float(storage_capacity)
        self.validate()

    def validate(self):
        """
        Valide les paramètres du modèle.
        """
        if any(param <= 0 for param in [self.f_0, self.f_t, self.k, self.storage_capacity]):
            raise ValueError("Les paramètres 'f_0', 'f_t', 'k' et 'storage_capacity' doivent être strictement positifs.")


    def to_dict(self):
        return {
                    'f_0': self.f_0,
                    'f_t': self.f_t,
                    'k': self.k,
                    'storage_capacity' : self.storage_capacity
            }

    @staticmethod
    def get_parameter_names():
        return {
                "f_0" : "f_0",
                "f_t" : "f_t",
                "k" : "k",
                "storage_capacity" : "sc"
        }
    
    @staticmethod
    def get_default_ranges():
        return {
                "f_0" : [1,10],
                "f_t" : [1,1.5],
                "k" : [1,1.5],
                "storage_capacity" : [1,20]
        }

    @staticmethod
    def get_default_values():
        return {
                "f_0" : 10,
                "f_t" : 1.5,
                "k" : 1,
                "storage_capacity" : 20
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

            if key == "f_0" and value <= 0:
                raise ValueError("Le paramètre doit être strictement positif.")
            elif key == "f_t" and value <= 0:
                raise ValueError("Le paramètre doit être strictement positif.")
            elif key == "k" and value <= 0:
                raise ValueError("Le paramètre doit être strictement positif.")
            elif key == "storage_capacity" and value <= 0:
                raise ValueError("Le paramètre doit être strictement positif.")

            return True  # Si aucune erreur, le paramètre est valide

        except Exception as e:
            return str(e)  # Retourne le message d'erreur

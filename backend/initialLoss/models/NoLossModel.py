class NoLossModel:
    """
    Modèle représentant l'absence de pertes (aucun paramètre nécessaire).
    """

    def __init__(self, args):
        """
        Initialise un modèle sans pertes. Aucun paramètre n'est requis.
        """
        pass  # Aucune initialisation nécessaire

    def validate(self):
        """
        Méthode de validation vide, car aucun paramètre n'a besoin d'être validé.
        """
        pass

    def to_dict(self):
        """
        Retourne un dictionnaire vide, car il n'y a pas de paramètres à stocker.
        """
        return {}

    @staticmethod
    def get_parameter_names():
        """
        Retourne un dictionnaire vide, car ce modèle ne nécessite aucun paramètre.
        """
        return {}

    @staticmethod
    def validate_parameter(key, value):
        """
        Fonction de validation toujours valide (aucun paramètre à vérifier).

        :return: Toujours True.
        """
        return True

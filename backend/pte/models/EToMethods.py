class EToMethods:
    """
    Classe statique listant les méthodes disponibles pour le calcul de l'évapotranspiration potentielle (ETP).
    """
    
    # Liste des méthodes disponibles
    AVAILABLE_METHODS = {
        "Penman": "Température Moy., Humidité relative de l'air, Radiation Net, Vitesse moy., Latitude, Elevation",
        "Penman-Monteith": "Température Moy., Humidité relative de l'air, Radiation Net, Vitesse moy., Latitude, Elevation",
        "Hamon": "Température Moy., Latitude",
        "Turc": "Température Moy., Humidité relative de l'air, Radiation solaire, Vitesse moy.",
        "Hargreaves": "Température Moy., Température Min., Température Max.,  Latitude",
        "Oudin": "Température Moy., Latitude",
        "FAO-56" : "Température Moy., Humidité relative de l'air, Radiation solaire, Vitesse moy., Latitude, Elevation",
    }

    AVAILABLE_PARAMETERS  = ["Température Moy.", "Humidité relative de l'air",
                                "Radiation solaire", "Vitesse moy.", "Latitude", "Elevation"]
    
    @staticmethod
    def list_methods():
        """
        Retourne la liste des méthodes d'ETP disponibles sous forme de dictionnaire.
        """
        return list(EToMethods.AVAILABLE_METHODS.keys())

    @staticmethod
    def list_parameters():
        """
        Retourne la liste des méthodes d'ETP disponibles sous forme de dictionnaire.
        """
        return list(EToMethods.AVAILABLE_METHODS.keys())
    
    @staticmethod
    def required_params() :
        return list(EToMethods.AVAILABLE_METHODS.values())

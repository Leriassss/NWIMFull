class EToMethods:
    """
    Classe statique listant les méthodes disponibles pour le calcul de l'évapotranspiration potentielle (ETP).
    """
    
    # Liste des méthodes disponibles
    AVAILABLE_METHODS = {
        "Penman": "T, RH, R, u2, Lat, El",
        "Penman-Monteith": "T, RH, R, u2, Lat, El",
        "Hamon": "T, Lat",
        "Turc": "T, RH, R",
        "Hargreaves": "T, Tmin, Tmax, Lat",
        "Oudin": "T, Lat",
        "FAO-56" : "T, RH, R, u2, Lat, El"
    }
    
    @staticmethod
    def list_methods():
        """
        Retourne la liste des méthodes d'ETP disponibles sous forme de dictionnaire.
        """
        return list(EToMethods.AVAILABLE_METHODS.keys())
    
    @staticmethod
    def required_params() :
        return EToMethods.AVAILABLE_METHODS.values()

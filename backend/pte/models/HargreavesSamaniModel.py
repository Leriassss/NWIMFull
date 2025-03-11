import pandas as pd 

class HargreavesSamaniModel:
    """
    Classe pour valider les données et les constantes utilisées dans le modèle Hargreaves-Samani.
    """

    def __init__(self, data: pd.DataFrame, constants: dict):
        """
        Initialise et valide les données pour la méthode Phi.

        :param prec: Série pandas contenant les précipitations (en mm).
        :param c_r: Coefficient de ruissellement (entre 0 et 1).
        """
        self._data = data
        self._constants = constants
        self.validate()
    
    def validate(self):
        """
        Valide les données et les constantes.

        :param data: DataFrame contenant les colonnes nécessaires ('Tmax', 'Tmin', 'J', 'Date').
        :param constants: Dictionnaire contenant les constantes nécessaires ('Elev', 'lat_rad', 'lambda', 'Gsc').
        """
        required_columns = ['Tmax', 'Tmin', 'J', 'Date']
        for column in required_columns:
            if column not in self._data.columns:
                raise ValueError(f"La colonne '{column}' est requise dans les données.")
        
        required_constants = ['Elev', 'lat_rad', 'lambda', 'Gsc']
        for key in required_constants:
            if key not in self._constants:
                raise ValueError(f"La constante '{key}' est requise.")


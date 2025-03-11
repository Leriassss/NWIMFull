import pandas as pd

class PenmanMonteithModel:
    """
    Classe pour valider les données et les constantes utilisées dans le modèle Penman-Monteith.
    """
    def __init__(self, data: pd.DataFrame, constants: dict):
        """
        Initialise et valide les données pour la méthode Penman-Monteith.

        :param data: DataFrame contenant les colonnes nécessaires ['Tmax', 'Tmin', 'RH', 'Rn', 'u2', 'Date'].
        :param constants: Dictionnaire contenant les constantes nécessaires ['lambda', 'gamma', 'Cp'].
        """
        self._data = data
        self._constants = constants
        self.validate()

    def validate(self):
        """
        Valide les données et les constantes.

        :param data: DataFrame contenant les colonnes nécessaires ['Tmax', 'Tmin', 'RH', 'Rn', 'u2', 'Date'].
        :param constants: Dictionnaire contenant les constantes nécessaires ['lambda', 'gamma', 'Cp'].
        """
        required_columns = ['Tmax', 'Tmin', 'RH', 'Rn', 'u2', 'Date']
        for column in required_columns:
            if column not in self._data.columns:
                raise ValueError(f"La colonne '{column}' est requise.")
        
        required_constants = ['lambda', 'gamma', 'Cp']
        for key in required_constants:
            if key not in self._constants:
                raise ValueError(f"La constante '{key}' est requise.")


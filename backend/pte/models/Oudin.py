import pandas as pd

class OudinModel:
    """
    Classe pour valider les données et les constantes utilisées dans la méthode de Oudin.
    """
    def __init__(self, data: pd.DataFrame, constants: dict):
        """
        Initialise et valide les données pour la méthode Oudin.

        :param data: DataFrame contenant les colonnes nécessaires ['JulianDay', 'Temperature'].
        :param constants: Dictionnaire contenant les constantes nécessaires ['Latitude', 'LatUnit'].
        """
        self._data = data
        self._constants = constants
        self.validate_arguments()

    def validate_arguments(self):
        """
        Valide les données et les constantes.

        :param data: DataFrame contenant les colonnes nécessaires ['JulianDay', 'Temperature'].
        :param constants: Dictionnaire contenant les constantes nécessaires ['Latitude', 'LatUnit'].
        """
        required_columns = ['JulianDay', 'Temperature']
        for column in required_columns:
            if column not in self._data.columns:
                raise ValueError(f"La colonne '{column}' est requise.")
        
        if 'Latitude' not in self._constants:
            raise ValueError("La constante 'Latitude' est requise.")
        
        if 'LatUnit' in self._constants and self._constants['LatUnit'] not in ['deg', 'rad']:
            raise ValueError("'LatUnit' doit être 'deg' ou 'rad'.")


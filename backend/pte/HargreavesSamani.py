# evapotranspiration_hargreaves_samani.py
import numpy as np
import pandas as pd 
from pte import Evapotranspiration
from pte.models.HargreavesSamaniModel import HargreavesSamaniModel

class HargreavesSamani(Evapotranspiration):
    """
    Classe implémentant la méthode d'évapotranspiration Hargreaves-Samani.
    """
    def __init__(self, data_model: HargreavesSamaniModel):
        self._data_model = data_model

    def calculate(self) -> pd.DataFrame:
        """
        Calcule l'évapotranspiration annuelle en utilisant la méthode de Hargreaves-Samani.

        :param data: DataFrame contenant les colonnes nécessaires ('Tmax', 'Tmin', 'J', 'Date').
        :param constants: Dictionnaire contenant les constantes nécessaires ('Elev', 'lat_rad', 'lambda', 'Gsc').

        :return: DataFrame avec les résultats d'évapotranspiration annuelle.
        """
        # Validation des arguments
        data = self._data_model._data
        constants = self._data_model._constants

        # Calcul de la température moyenne
        data['Ta'] = (data['Tmax'] + data['Tmin']) / 2

        # Paramètres solaires
        data['d_r2'] = 1 + 0.033 * np.cos(2 * np.pi / 365 * data['J'])
        data['delta2'] = 0.409 * np.sin(2 * np.pi / 365 * data['J'] - 1.39)
        data['w_s'] = np.arccos(-np.tan(constants['lat_rad']) * np.tan(data['delta2']))
        data['R_a'] = (1440 / np.pi) * data['d_r2'] * constants['Gsc'] * (
            data['w_s'] * np.sin(constants['lat_rad']) * np.sin(data['delta2']) +
            np.cos(constants['lat_rad']) * np.cos(data['delta2']) * np.sin(data['w_s'])
        )

        # Coefficient de Hargreaves-Samani
        data['C_HS'] = 0.00185 * (data['Tmax'] - data['Tmin']) ** 2 - \
                        0.0433 * (data['Tmax'] - data['Tmin']) + 0.4023

        # Évapotranspiration journalière
        data['ET_HS_Daily'] = 0.0135 * data['C_HS'] * data['R_a'] / constants['lambda'] * \
                              (data['Tmax'] - data['Tmin']) ** 0.5 * (data['Ta'] + 17.8)

        # Agrégation annuelle
        data['Year'] = pd.to_datetime(data['Date']).dt.year
        et_annual = data.groupby('Year')['ET_HS_Daily'].sum()

        return et_annual

    @classmethod
    def help(cls):
        """
        Fournit une description de la classe HargreavesSamani et son utilisation.
        """
        description = """
        Classe HargreavesSamani :
        Cette classe calcule l'évapotranspiration annuelle en utilisant la méthode de Hargreaves-Samani.

        Méthodes principales :
        - validate_arguments(data: pd.DataFrame, constants: dict) : Valide les données et les constantes.
        - calculate(data: pd.DataFrame, constants: dict) : Calcule l'évapotranspiration annuelle.

        Arguments requis pour `calculate` :
        - data : DataFrame contenant les colonnes suivantes :
            - 'Tmax' : Température maximale (°C)
            - 'Tmin' : Température minimale (°C)
            - 'J' : Jour julien
            - 'Date' : Date au format YYYY-MM-DD
        - constants : Dictionnaire contenant :
            - 'Elev' : Altitude (m)
            - 'lat_rad' : Latitude en radians
            - 'lambda' : Chaleur latente de vaporisation (MJ/kg)
            - 'Gsc' : Constante solaire (MJ/m²/min)

        Exemple d'utilisation :
        ```python
        from evapotranspiration_hargreaves_samani import HargreavesSamani
        constants = {'Elev': 100, 'lat_rad': 0.7854, 'lambda': 2.45, 'Gsc': 0.0820}
        data = pd.DataFrame({
            'Tmax': [30, 32, 31],
            'Tmin': [20, 21, 19],
            'J': [1, 2, 3],
            'Date': ['2025-01-01', '2025-01-02', '2025-01-03']
        })
        hs = HargreavesSamani()
        result = hs.calculate(data, constants)
        print(result)
        ```
        """
        print(description)

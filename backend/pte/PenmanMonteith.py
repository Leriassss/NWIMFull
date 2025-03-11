
import numpy as np
import pandas as pd 
from pte import Evapotranspiration
from pte.models.PenmanMonteithModel import PenmanMonteithModel

class PenmanMonteith(Evapotranspiration):
    """
    Classe implémentant la méthode d'évapotranspiration Penman-Monteith.
    """
    def __init__(self, data_model: PenmanMonteithModel):
        """
        Initialise le modèle Penman-Monteith avec la classe de validation des arguments.
        """
        self._data_model = data_model

    def calculate(self) -> pd.DataFrame:
        """
        Calcule l'évapotranspiration annuelle en utilisant la méthode Penman-Monteith.

        :return: DataFrame avec les résultats d'évapotranspiration annuelle.
        """
        data = self._data_model._data
        constants = self._data_model._constants

        # Température moyenne
        data['Ta'] = (data['Tmax'] + data['Tmin']) / 2

        # Calcul de delta (slope de la courbe de pression de vapeur)
        data['delta'] = 4098 * (0.6108 * np.exp((17.27 * data['Ta']) / (data['Ta'] + 237.3))) / (data['Ta'] + 237.3) ** 2

        # Calcul de l'évapotranspiration journalière
        data['ET_PM_Daily'] = (
            (0.408 * data['delta'] * data['Rn'] +
             constants['gamma'] * (900 / (data['Ta'] + 273)) * data['u2'] * (data['RH'])) /
            (data['delta'] + constants['gamma'] * (1 + 0.34 * data['u2']))
        )

        # Agrégation annuelle
        data['Year'] = pd.to_datetime(data['Date']).dt.year
        et_annual = data.groupby('Year')['ET_PM_Daily'].sum()

        return et_annual

    @classmethod
    def help(cls):
        """
        Fournit une description de la classe PenmanMonteith et son utilisation.
        """
        description = """
        Classe PenmanMonteith :
        Cette classe calcule l'évapotranspiration annuelle en utilisant la méthode de Penman-Monteith.

        Méthodes principales :
        - validate_arguments() : Valide les données et les constantes.
        - calculate() : Calcule l'évapotranspiration annuelle.

        Arguments requis pour `calculate` :
        - data : DataFrame contenant les colonnes suivantes :
            - 'Tmax' : Température maximale (°C)
            - 'Tmin' : Température minimale (°C)
            - 'RH' : Humidité relative (%)
            - 'Rn' : Radiation nette (MJ/m²/jour)
            - 'u2' : Vitesse du vent à 2 m (m/s)
            - 'Date' : Date au format YYYY-MM-DD
        - constants : Dictionnaire contenant :
            - 'lambda' : Chaleur latente de vaporisation (MJ/kg)
            - 'gamma' : Constante psychrométrique (kPa/°C)
            - 'Cp' : Capacité thermique de l'air (MJ/kg°C)

        Exemple d'utilisation :
        ```python
        from evapotranspiration_penman_monteith import PenmanMonteith
        constants = {'lambda': 2.45, 'gamma': 0.067, 'Cp': 1.013}
        data = pd.DataFrame({
            'Tmax': [30, 32, 31],
            'Tmin': [20, 21, 19],
            'RH': [60, 65, 70],
            'Rn': [15, 17, 16],
            'u2': [3.5, 4.0, 3.2],
            'Date': ['2025-01-01', '2025-01-02', '2025-01-03']
        })
        pm_model = PenmanMonteithModel(data, constants)
        pm = PenmanMonteith(pm_model)
        result = pm.calculate()
        print(result)
        ```
        """
        print(description)

import numpy as np
import pandas as pd 
from pte import Evapotranspiration
from pte.models.Oudin import OudinModel


class Oudin(Evapotranspiration):
    """
    Classe implémentant la méthode d'évapotranspiration annuelle de Oudin.
    """
    def __init__(self, data_model: OudinModel):
        """
        Initialise la méthode de calcul avec la classe de validation des arguments.
        """
        self._data_model = data_model

    def calculate(self) -> pd.DataFrame:
        """
        Calcule l'évapotranspiration annuelle en utilisant la méthode Oudin.

        :return: DataFrame avec les résultats d'évapotranspiration annuelle.
        """
        data = self._data_model._data
        constants = self._data_model._constants

        julian_days = data['JulianDay'].values
        temperatures = data['Temperature'].values
        latitude = constants['Latitude']
        lat_unit = constants.get('LatUnit', 'deg')

        # Conversion de la latitude en radians si nécessaire
        if lat_unit == "deg":
            latitude = np.radians(latitude)

        # Constantes
        evapotranspiration_annual = 0
        cos_lat = np.cos(latitude)

        # Calcul pour chaque jour
        for jd, temp in zip(julian_days, temperatures):
            if temp is None or np.isnan(temp):  # Ignorer les valeurs manquantes
                continue

            # Calcul de l'angle solaire
            theta = 0.4093 * np.sin(jd / 58.1 - 1.405)  # Inclinaison de la Terre
            cos_theta = np.cos(theta)
            cos_gz = max(0.001, np.cos(latitude - theta))  # Assure que cos_gz est positif
            gz = np.arccos(cos_gz)

            cos_omega = 1 - cos_gz / (cos_lat * cos_theta)
            cos_omega = np.clip(cos_omega, -1, 1)  # Limiter la valeur pour éviter des erreurs

            omega = np.arccos(cos_omega)
            eta = 1 + np.cos(jd / 58.1) / 30  # Facteur d'excentricité orbitale

            # Calcul de GE (énergie solaire)
            ge = 446 * omega * (cos_gz + cos_lat * cos_theta * (np.sin(omega) / omega - 1)) * eta
            ge = max(ge, 0.001)  # Empêcher les valeurs négatives

            # Calcul de l'évapotranspiration journalière
            if temp >= -5:
                et_daily = ge * (temp + 5) / (100 * 28.5)
            else:
                et_daily = 0

            # Accumulation de l'évapotranspiration annuelle
            evapotranspiration_annual += et_daily

        return pd.DataFrame({
            'Evapotranspiration_Annual': [evapotranspiration_annual]
        })

    @classmethod
    def help(cls):
        """
        Fournit une description de la classe Oudin et son utilisation.
        """
        description = """
        Classe Oudin :
        Cette classe calcule l'évapotranspiration annuelle en utilisant la méthode de Oudin.

        Méthodes principales :
        - validate_arguments() : Valide les données et les constantes.
        - calculate() : Calcule l'évapotranspiration annuelle.

        Arguments requis pour `calculate` :
        - data : DataFrame contenant les colonnes suivantes :
            - 'JulianDay' : Jour julien
            - 'Temperature' : Température en °C
        - constants : Dictionnaire contenant :
            - 'Latitude' : Latitude de la localisation (en degrés ou radians)
            - 'LatUnit' : Unité de latitude ("deg" pour degrés ou "rad" pour radians), facultatif, par défaut "deg"

        Exemple d'utilisation :
        ```python
        from evapotranspiration_oudin import Oudin
        constants = {'Latitude': 45.0, 'LatUnit': 'deg'}
        data = pd.DataFrame({
            'JulianDay': [100, 150, 200],
            'Temperature': [20, 22, 24]
        })
        oud_model = OudinModel(data, constants)
        oud = Oudin(oud_model)
        result = oud.calculate()
        print(result)
        ```
        """
        print(description)

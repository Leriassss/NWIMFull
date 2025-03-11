# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd

class PTE:
    def hargreaves_samani_annual(data, constants):
        """
        Calcul de l'évapotranspiration annuelle avec la méthode Hargreaves-Samani.

        Arguments :
        - data : DataFrame contenant 'Tmax', 'Tmin', 'J' (jour julien) et 'Date'.
        - constants : Dictionnaire avec 'Elev', 'lat_rad', 'lambda', et 'Gsc'.

        Retour :
        - DataFrame contenant les valeurs annuelles d'évapotranspiration.
        """
        # Vérification des colonnes nécessaires
        if 'Tmax' not in data.columns or 'Tmin' not in data.columns or 'J' not in data.columns:
            raise ValueError("Les colonnes 'Tmax', 'Tmin', et 'J' sont requises dans les données.")

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


    def penman_monteith(data, constants, solar="sunshine hours", wind="yes", crop="short", verbose=True):
        """
        Implémentation du modèle Penman-Monteith pour le calcul de l'évapotranspiration annuelle.

        Paramètres :
            - data : DataFrame Pandas contenant les colonnes : 'Tmax', 'Tmin', 'RHmax', 'RHmin', 'u2' (ou 'uz'), 'Date'.
            - constants : dictionnaire contenant les constantes : 'Elev' (altitude en mètres) et 'lambda' (chaleur latente).
            - solar : méthode d'entrée du rayonnement solaire (par défaut "sunshine hours").
            - wind : indique si les données de vent sont utilisées ("yes" ou "no").
            - crop : type de culture, "short" (par défaut) ou "tall".
            - verbose : afficher des messages d'information.

        Retour :
            - DataFrame Pandas contenant l'évapotranspiration annuelle.
        """
        # Vérification des données requises
        required_cols = ['Tmax', 'Tmin', 'RHmax', 'RHmin', 'Date']
        if wind == "yes":
            required_cols.append('u2')
        for col in required_cols:
            if col not in data.columns:
                raise ValueError(f"Donnée requise manquante : '{col}'")

        # Calcul des variables intermédiaires
        data['Ta'] = (data['Tmax'] + data['Tmin']) / 2

        # Calcul de la pression de vapeur saturante (vas) et réelle (vabar)
        data['vs_Tmax'] = 0.6108 * np.exp(17.27 * data['Tmax'] / (data['Tmax'] + 237.3))
        data['vs_Tmin'] = 0.6108 * np.exp(17.27 * data['Tmin'] / (data['Tmin'] + 237.3))
        data['vas'] = (data['vs_Tmax'] + data['vs_Tmin']) / 2
        data['vabar'] = (data['vs_Tmin'] * data['RHmax'] / 100 + data['vs_Tmax'] * data['RHmin'] / 100) / 2

        # Calcul de la pression atmosphérique (P)
        elev = constants['Elev']
        data['P'] = 101.3 * ((293 - 0.0065 * elev) / 293) ** 5.26

        # Calcul des paramètres delta et gamma
        data['delta'] = 4098 * (0.6108 * np.exp(17.27 * data['Ta'] / (data['Ta'] + 237.3))) / ((data['Ta'] + 237.3) ** 2)
        data['gamma'] = 0.00163 * data['P'] / constants['lambda']

        # Calcul de l'évapotranspiration journalière
        if wind == "yes":
            if 'u2' not in data.columns:
                data['u2'] = data['uz'] * 4.87 / np.log(67.8 * constants['z'] - 5.42)
            data['ET_daily'] = (
                (0.408 * data['delta'] * (data['vas'] - data['vabar']) +
                data['gamma'] * 900 * data['u2'] * (data['vas'] - data['vabar']) / (data['Ta'] + 273)) /
                (data['delta'] + data['gamma'] * (1 + 0.34 * data['u2']))
            )
        else:
            raise NotImplementedError("Calcul sans données de vent non implémenté.")

        # Agrégation annuelle
        data['Year'] = pd.to_datetime(data['Date']).dt.year
        annual_et = data.groupby('Year')['ET_daily'].sum().reset_index()
        annual_et.rename(columns={'ET_daily': 'ET_Annual'}, inplace=True)

        if verbose:
            print("Méthode : Penman-Monteith")
            print("Valeurs annuelles d'évapotranspiration calculées avec succès.")

        return annual_et




    def annual_evapotranspiration_oudin(julian_days, temperatures, latitude, lat_unit="deg"):
        """
        Calcule l'évapotranspiration annuelle basée sur la formule de Oudin.
        
        :param julian_days: Liste ou tableau des jours julian (1 à 366).
        :param temperatures: Liste ou tableau des températures journalières correspondantes (°C).
        :param latitude: Latitude de la localisation (en degrés ou radians).
        :param lat_unit: Unité de latitude, "deg" pour degrés ou "rad" pour radians. Défaut "deg".
        :return: Évapotranspiration annuelle en mm.
        """
        # Vérifications des entrées
        if not isinstance(julian_days, (list, np.ndarray)) or not isinstance(temperatures, (list, np.ndarray)):
            raise ValueError("Les 'julian_days' et 'temperatures' doivent être des listes ou des tableaux NumPy.")
        if len(julian_days) != len(temperatures):
            raise ValueError("'julian_days' et 'temperatures' doivent avoir la même longueur.")
        if lat_unit not in ["deg", "rad"]:
            raise ValueError("'lat_unit' doit être 'deg' ou 'rad'.")
        
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
        
        return evapotranspiration_annual

import numpy as np
import pandas as pd
from typing import Union

class EToModel:
    def __init__(self, T, Tmin = None, Tmax = None, RH=None, R=None, u2=None, Lat: Union[int, float] = None, El: Union[int, float] = None):
        self.T = np.array(T, dtype=np.float64) if T is not None else None
        self.Tmin = np.array(Tmin, dtype=np.float64) if Tmin is not None else None
        self.Tmax = np.array(Tmax, dtype=np.float64) if Tmax is not None else None
        self.RH = np.array(RH, dtype=np.float64) if RH is not None else None
        self.R = np.array(R, dtype=np.float64) if R is not None else None
        self.u2 = np.array(u2, dtype=np.float64) if u2 is not None else None
        self.lat = Lat  if Lat is not None else None
        self.el = El  if El is not None else None
        self.validate()

    def validate(self):
        errors = []

        # Vérification que T est un tableau non vide
        if self.T.size == 0:
            errors.append("T ne peut pas être vide.")

        # Vérification des autres variables par rapport à T uniquement si elles sont fournies
        if self.RH is not None:
            if self.RH.size != self.T.size:
                errors.append("RH doit avoir la même longueur que T.")
            if not np.all((0 <= self.RH) & (self.RH <= 100)):
                errors.append("RH doit être compris entre 0 et 100.")

        if self.R is not None:
            if self.R.size != self.T.size:
                errors.append("R doit avoir la même longueur que T.")
            if not np.all(self.R >= 0):
                errors.append("R doit être un nombre positif.")

        if self.u2 is not None:
            if self.u2.size != self.T.size:
                errors.append("u2 doit avoir la même longueur que T.")
            if not np.all(self.u2 >= 0):
                errors.append("u2 doit être un nombre positif.")

        # Vérification que la latitude est un nombre réel (en radians)
        if self.lat is not None and not isinstance(self.lat, (int, float)):
            errors.append("Lat doit être un nombre réel en radians.")

        # Vérification que l'altitude est un nombre positif
        if self.el is not None and (not isinstance(self.el, (int, float)) or self.el < 0):
            errors.append("El doit être un nombre positif.")

        if errors:
            raise ValueError("Erreurs de validation : " + "; ".join(errors))
        return True

    def eto_datas(self):
        return {
            "tmean" : pd.Series(self.T),
            "tmin" : pd.Series(self.Tmin),
            "tmax" : pd.Series(self.Tmax),
            "rh" : pd.Series(self.RH),
            "rn" : pd.Series(self.R),
            "wind" : pd.Series(self.u2),
            "elevation" : self.el,
            "lat" : self.lat
        }


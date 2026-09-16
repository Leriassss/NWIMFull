import numpy as np
import pandas as pd
from dateutil import parser
class EToModel:
    def __init__(self, dates, tmean, tmin = None, tmax = None, rh=None, rn=None, wind=None, lat = None, elevation = None):
        self.dates = np.array(dates, dtype=str)
        self.tmean = np.array(tmean, dtype=np.float64) if tmean is not None else None
        self.tmin = np.array(tmin, dtype=np.float64) if tmin is not None else None
        self.tmax = np.array(tmax, dtype=np.float64) if tmax is not None else None
        self.rh = np.array(rh, dtype=np.float64) if rh is not None else None
        self.rn= np.array(rn, dtype=np.float64) if rn is not None else None
        self.wind = np.array(wind, dtype=np.float64) if wind is not None else None
        self.lat = lat  if lat is not None else None
        self.elevation = elevation  if elevation is not None else None
        self._errors = []
        self.validate()


    def validate(self):
        errors = []

        if len(self.dates) !=  self.tmean.size :
            errors.append("Dates, la longueur ne correspond pas")

        if len(self.dates) == 0:
            errors.append("Dates ne peut pas être vide")

        # Vérification que T est un tableau non vide
        if self.tmean.size == 0:
            errors.append("tmean ne peut pas être vide")

        # Vérification des autres variables par rapport à T uniquement si elles sont fournies
        if self.rh is not None:
            if self.rh.size != self.tmean.size:
                errors.append("rh doit avoir la même longueur que tmean")
            if not np.all((0 <= self.rh) & (self.rh <= 100)):
                errors.append("rh doit être compris entre 0 et 100")

        if self.tmin is not None:
            if self.tmin.size != self.tmean.size:
                errors.append("tmin doit avoir la même longueur que tmean")

        if self.tmax is not None:
            if self.tmax.size != self.tmean.size:
                errors.append("tmax doit avoir la même longueur que tmean")

        if self.rn is not None:
            if self.rn.size != self.tmean.size:
                errors.append("rn doit avoir la même longueur que tmean")
            if not np.all(self.rn>= 0):
                errors.append("rn doit être un nombre positif")

        if self.wind is not None:
            if self.wind.size != self.tmean.size:
                errors.append("wind doit avoir la même longueur que tmean")
            if not np.all(self.wind >= 0):
                errors.append("wind doit être un nombre positif")

        if self.lat != "" :
            try:
                lat_value = float(self.lat)
            except (ValueError, TypeError):
                errors.append("lat doit être un nombre réel en radians")

        if self.elevation != "" :
            try:
                elevation_value = float(self.elevation)
            except (ValueError, TypeError):
                errors.append("Elevation doit être un nombre réel")
        try:
            self.dates = [d.strftime("%Y-%m-%d") for d in np.vectorize(parser.parse)(self.dates)]

        except ValueError:
            errors.append("Format de dates non reconnues")

        self._errors = errors


    def eto_datas(self):
        if len(self._errors) == 0 :
            return {
                "Dates" : self.dates,
                "tmean" : pd.Series(self.tmean),
                "tmin" : pd.Series(self.tmin),
                "tmax" : pd.Series(self.tmax),
                "rh" : pd.Series(self.rh),
                "rn" : pd.Series(self.rn),
                "wind" : pd.Series(self.wind),
                "elevation" : float(self.elevation) if self.elevation != "" else None,
                "lat" : float(self.lat) if self.lat != "" else None
            }
        else :
            return None


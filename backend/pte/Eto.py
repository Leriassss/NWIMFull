import pyet
from backend.pte.models.EToModel import EToModel
from backend.pte.Evapotranspiration import Evapotranspiration


class ETo(Evapotranspiration):
    """
    Classe implémentant la méthode d'évapotranspiration Penman-Monteith.
    """
    def __init__(self, data : EToModel):
        self._data = data

    def calculate(self, method):
        params = self._data.eto_datas()
        if method == "Penman":
            eto_calulated = pyet.penman(
                tmean=params["tmean"],wind=params["wind"],rn=params["rn"],rh=params["rh"],
                elevation=params["elevation"],lat=params["lat"])
        elif method == "Penman-Monteith":
            eto_calulated = pyet.pm(
                tmean=params["tmean"],wind=params["wind"],rn=params["rn"],rh=params["rh"],
                elevation=params["elevation"],lat=params["lat"])
        elif method == "Hamon":
            eto_calulated = pyet.hamon(
                tmean=params["tmean"],lat=params["lat"])
        elif method == "Turc":
            eto_calulated = pyet.turc(
                tmean=params["tmean"],rs=params["rn"],rh=params["rh"])
        elif method == "Hargreaves":
            eto_calulated = pyet.hargreaves(
                tmean=params["tmean"],tmin=params["tmin"],tmax=params["tax"],lat=params["lat"])
        elif method == "Oudin":
            eto_calulated = pyet.oudin(
                tmean=params["tmean"],lat=params["lat"])
        elif method == "FAO-56":
            eto_calulated = pyet.pm_fao56(
                tmean=params["tmean"],wind=params["wind"],rn=params["rn"],rh=params["rh"],
                elevation=params["elevation"],lat=params["lat"])
        else:
            raise NotImplementedError("Méthode non reconnue")
        return eto_calulated
        
    @classmethod
    def help(cls):
        """
        Fournit une description
        """
        description = """
        Classe Eto :
        Cette classe calcule l'évapotranspiration journalière
        """
        print(description)

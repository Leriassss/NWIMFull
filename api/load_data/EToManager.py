import pandas as pd
import numpy as np
import datetime
from dateutil import parser
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement
from itertools import zip_longest
from backend.results.ResultsFileManager import ResultsFileManager
from backend.pte.models.EToMethods import EToMethods
from backend.pte.models.EToModel import EToModel
from backend.pte.Eto import ETo

class EToManager(QObject):
    def __init__(self):
        super().__init__()
        self._headers = []
        self._data = []
        self._data_dict = {}
        self._errors = []
        self._parameters = ""
        self._method = ""
        self._etoModel = None
        self._etp_computation = {"Dates": [], "ETP" : []}

    headersChanged = Signal(list)
    dataChanged = Signal(list)
    dataDictChanged = Signal()
    errorsChanged = Signal()
    methodChanged = Signal()
    computationChanged=Signal()

    @Property(list, notify=errorsChanged)
    def errors(self):
        return self._errors

    # Propriété pour les en-têtes
    @Property(list, notify=headersChanged)
    def headers(self):
        return self._headers

    # Propriété pour les données
    @Property(dict, notify=dataChanged)
    def data(self):
        return self._data

    @Property(dict, notify=dataDictChanged)
    def dataDict(self):
        return self._data_dict



    @Slot(str)
    def readFile(self, filePath):
        try:
            if filePath.endswith('.csv'):
                df = pd.read_csv(filePath)
            elif filePath.endswith('.xlsx'):
                df = pd.read_excel(filePath, engine='openpyxl')
            else:
                print("Format de fichier non supporté")
                return

            # Extraire les en-têtes et les données
            hd = df.columns.tolist()
            hd.append("Non défini")
            self._headers =hd

            self._data = df.to_dict(orient="list")

            self.headersChanged.emit(self._headers)
            self.dataChanged.emit(self._data)

        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")


    @Slot(dict)
    def setDictValues(self, data_dict):
        user_values = {
            key: None if value == "Non défini" else self._data[value]
            for key, value in data_dict.items()
            if key not in {"elevation", "lat"}
        }
        user_values["elevation"] = data_dict["elevation"]
        user_values["lat"] = data_dict["lat"]
        print(user_values)
        self._etoModel = EToModel(**user_values)

        if(len(self._etoModel._errors) !=0):
            self._errors = self._etoModel._errors
            self.errorsChanged.emit()
            return
        self._data_dict = self._etoModel.eto_datas()
        print("SETDICTVALUES ---------------2")
        print(self._data_dict)
        self.dataDictChanged.emit()

    @Property("QVariant", constant = True)
    def availableMethods(self):
        return EToMethods.list_methods()

    @Slot(str)
    def setMethod(self, index):
        self._method = index
        self._parameters = EToMethods.AVAILABLE_METHODS[index] if index in EToMethods.list_methods() else None
        self.methodChanged.emit()

    @Property(str, notify=methodChanged)
    def methodParameters(self):
        return self._parameters

    @Slot()
    def computeETo(self):
        self._etp_computation["ETP"] = (ETo(self._etoModel).calculate(self._method).round(3)).tolist()
        self._etp_computation["Dates"] = self._data_dict["Dates"]
        self.computationChanged.emit()
        print(" ------------------------- EToManager --- computation -------------------")
        print(self._etp_computation)

    @Property(dict, notify = computationChanged)
    def etpComputed(self):
        return self._etp_computation


    @Slot(str)
    def savePet(self, path):
        if len(self._etp_computation["Dates"]) == 0:
            self._errors.append("No data found. Please compute a PET method before")
            self.errorsChanged.emit()
            return
        df = pd.DataFrame(self._etp_computation)
        ResultsFileManager.saveData(df, path)



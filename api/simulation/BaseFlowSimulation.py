# This Python file uses the following encoding: utf-8

import pandas as pd
import numpy as np
import datetime

from backend.results.ResultsFileManager import ResultsFileManager
from backend.factory.RecessionFactory import RecessionFactory
from dateutil import parser
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement
from itertools import zip_longest

class BaseFlowSimulation(QObject):
    def __init__(self):
        super().__init__()
        self._headers = []
        self._data = []
        self._data_dict = {}
        self._errors = []
        self._baseflow = {"Dates": None, "Baseflow" : None}
        self._activated = False

    headersChanged = Signal(list)
    dataChanged = Signal(list)
    dataDictChanged = Signal()
    baseflowChanged = Signal()
    errorsChanged = Signal()
    activationChanged = Signal()

    @Property(list, notify=errorsChanged)
    def errors(self):
        return self._errors

    @Property(bool, notify=activationChanged)
    def activated(self):
        return self._activated

    @Property(dict, notify=baseflowChanged)
    def baseflowData(self):
        return self._baseflow

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
        self._errors = []
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
            self._headers =hd
            self._data = df.to_dict(orient="list")
            # Émettre les signaux pour mettre à jour QML
            self.headersChanged.emit(self._headers)
            self.dataChanged.emit(self._data)

        except Exception as e:
            self._errors = e.args[0].split(";")
            return



    @Slot(dict)
    def setDictValues(self, columnMapping):
        self._errors = []
        self._activated = False
        data_dict_values = { key: self._data[value] for key, value in columnMapping.items() }
        if not self.check_keys_match(data_dict_values, ["Dates","Q"]):
            self._errors.append("Des Colonnes de données sont manquantes!")
            self.errorsChanged.emit()
            return
        try:
            parsed_dates = np.vectorize(self.check_and_convert_date)(data_dict_values["Dates"])
            data_dict_values["Dates"] = np.array([d.strftime("%Y-%m-%d") for d in parsed_dates]).tolist()
        except Exception as e:
            self._errors = e.args[0].split(";")
            return

        self._data_dict = dict(data_dict_values)
        self._baseflow["Dates"] = data_dict_values["Dates"]
        self._activated = True
        self.dataDictChanged.emit()
        self.activationChanged.emit()

    @Slot(dict)
    def computeBaseflow(self,params_dict):
        self._errors = []
        if not self._activated:
            self._errors.append("No data found! Import data before compute")
            self.errorsChanged.emit()
            return
        prametersValues =  params_dict['parameterValues']
        currentMethod = params_dict["currentMethod"]

        self._baseflow["Baseflow"] = RecessionFactory.createInstance(currentMethod,*prametersValues).compute(np.array(self._data_dict["Q"])).tolist()
        self.baseflowChanged.emit()

    @Slot(str)
    def saveBaseFlow(self, path):
        df = pd.DataFrame(self._baseflow)
        ResultsFileManager.saveData(df, path)

    def check_keys_match(self, d, keys_list):
        dict_keys = set(d.keys())
        list_keys = set(keys_list)
        return dict_keys == list_keys

    def check_and_convert_date(self, date):
        return parser.parse(str(date))

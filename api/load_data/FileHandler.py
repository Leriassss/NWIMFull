import pandas as pd
import numpy as np
import datetime
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement

class FileHandler(QObject):
    def __init__(self):
        super().__init__()
        self._headers = []
        self._data = []
        self._data_dict = {}
        self._date_format = {
            "YYYYMMDD" : "%Y%m%d",
            "yyyy-MM-dd" : "%Y-%m-%d" ,
            "yyyy/MM/dd" : "%Y/%m/%d"
        }
        self._user_format = "yyyy-MM-dd"
        self._qInfos = {}
        self._pInfos = {}
        self._tempInfos = {}
        self._etpInfos = {}
        self._datesInfos = {}


    headersChanged = Signal(list)
    dataChanged = Signal(list)
    dataDictChanged = Signal()
    userFormatChanged = Signal()

    qInfosChanged = Signal()
    pInfosChanged = Signal()
    etpInfosChanged = Signal()
    tempInfosChanged = Signal()
    datesInfosChanged = Signal()


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

    @Slot()
    def updateQInfos(self):
        if "Q" in self._data_dict and self._data_dict["Q"]:
            qobs = np.array(self._data_dict["Q"])
            self._qInfos = {
                "data": qobs.tolist(),
                "min": qobs.min().tolist(),
                "max": qobs.max().tolist(),
                "mean": qobs.mean().tolist(),
                "std": qobs.std().tolist(),
                "count" : len(qobs)
            }
        else:
            self._qInfos = {
                "data": [],
                "min": None,
                "max": None,
                "mean": None,
                "std": None,
                "count" : None
            }
        self.qInfosChanged.emit()

    @Property(dict, notify=qInfosChanged)
    def qInfos(self):
        return self._qInfos

    @Slot()
    def updatePInfos(self):
        if "P" in self._data_dict and self._data_dict["P"]:
            rainfall = np.array(self._data_dict["P"])
            self._pInfos = {
                "data": rainfall.tolist(),
                "min": rainfall.min().tolist(),
                "max": rainfall.max().tolist(),
                "sum": rainfall.sum().tolist(),
                "std": rainfall.std().tolist()
            }
        else:
            self._pInfos = {
                "data": [],
                "min": None,
                "max": None,
                "sum": None,
                "std": None
            }
        self.pInfosChanged.emit()

    @Property(dict, notify=pInfosChanged)
    def pInfos(self):
        print(" ----------------- Dates 1")
        print(self._pInfos)
        return self._pInfos

    @Slot()
    def updateTempInfos(self):
        if "T" in self._data_dict and self._data_dict["T"]:
            temp = np.array(self._data_dict["T"])
            self._tempInfos = {
                "data": temp.tolist(),
                "min": temp.min().tolist(),
                "max": temp.max().tolist(),
                "mean": temp.mean().tolist(),
                "std": temp.std().tolist(),
                "count": len(temp)
            }
        else:
            self._tempInfos = {
                "data": [],
                "min": None,
                "max": None,
                "mean": None,
                "std": None,
                "count": 0
                }
        self.tempInfosChanged.emit()

    @Property(dict, notify=tempInfosChanged)
    def tempInfos(self):
        return self._tempInfos


    @Slot()
    def updateETPInfos(self):
        if "ETP" in self._data_dict and self._data_dict["ETP"]:
            etp = np.array(self._data_dict["ETP"])
            self._etpInfos = {
            "data": etp.tolist(),
            "min": etp.min().tolist(),
            "max": etp.max().tolist(),
            "mean": etp.mean().tolist(),
            "std": etp.std().tolist(),
            "count": len(etp)
            }
        else:
            self._etpInfos = {
                "data": [],
                "min": None,
                "max": None,
                "mean": None,
                "std": None,
                "count": 0
            }
        self.etpInfosChanged.emit()

    @Property(dict, notify=etpInfosChanged)
    def etpInfos(self):
        return self._etpInfos


    @Slot()
    def updateDatesInfos(self):
        if "Dates" in self._data_dict and self._data_dict["Dates"]:
            date_series = self._data_dict["Dates"]
            date_format = self._date_format[self._user_format]

            def convert_date(date):
                if isinstance(date, int) or (isinstance(date, str) and date.isdigit()):
                    return datetime.datetime.strptime(str(date), "%Y%m%d")
                elif isinstance(date, str):
                    return datetime.datetime.strptime(date, date_format)
                raise ValueError(f"Format de date non reconnu : {date}")

            # Conversion des dates
            parsed_dates = [convert_date(date) for date in date_series]

            self._datesInfos = {
                "data": [d.strftime("%Y-%m-%d") for d in parsed_dates],
                "min": parsed_dates[0].strftime("%Y-%m-%d"),
                "max": parsed_dates[-1].strftime("%Y-%m-%d"),
                "count": len(parsed_dates)
            }
        else:
            self._datesInfos = {
                "data": [],
                "min": None,
                "max": None,
                "count": 0,
            }

        self.datesInfosChanged.emit()


    @Property(dict, notify=datesInfosChanged)
    def datesInfos(self):
        return self._datesInfos

    @Property(list, constant = True)
    def dateFormat(self):
        return self._date_format.keys()

    @Property(str, notify=userFormatChanged)
    def userFormat(self):
        return self._user_format

    @Slot(str)
    def getDateFormat(self, index):
        self._user_format =  index
        self.userFormatChanged.emit()



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
            hd.append("Aucun")
            self._headers =hd
            self._data = df.to_dict(orient="list")
            # Émettre les signaux pour mettre à jour QML
            self.headersChanged.emit(self._headers)
            self.dataChanged.emit(self._data)

        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")


    @Slot(dict)
    def setDictValues(self, data_dict):
        self._data_dict = { key: [] if value == "Aucun" else self._data[value] for key, value in data_dict.items() }

        self.dataDictChanged.emit()
        self.updateDatesInfos()
        self.updateETPInfos()
        self.updatePInfos()
        self.updateQInfos()
        self.updateTempInfos()







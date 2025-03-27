import pandas as pd
import numpy as np
import datetime
from dateutil import parser
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement
from itertools import zip_longest

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

        self._errors = []
        self._display_data = []
        self._calage_index = 20


    headersChanged = Signal(list)
    dataChanged = Signal(list)
    dataDictChanged = Signal()
    userFormatChanged = Signal()

    qInfosChanged = Signal()
    pInfosChanged = Signal()
    etpInfosChanged = Signal()
    tempInfosChanged = Signal()
    datesInfosChanged = Signal()
    displayDataChanged = Signal()

    errorsChanged = Signal()

    @Property(list, notify=errorsChanged)
    def errors(self):
        return self._errors


    def check_numeric_and_length(self, key):
        if key in self._data_dict and key != "Dates":
            data = self._data_dict[key]
            try:
                series =  np.array(data, dtype=np.float64)
            except Exception as e:
                self._errors.append(f"Les données de la série {key} contiennent des valeurs non numériques")
                return False
            if len(data) != len(self._data_dict.get("Dates", [])):
                self._errors.append(f"Les longueurs des dates et de la série {key} ne correspondent pas")
                return False
        return True

    def check_and_convert_date(self, date):
        try:
            return parser.parse(str(date))
        except ValueError:
            self._errors.append("Format de dates non reconnues")
            self.errorsChanged.emit()
            return []

    def updateDatas(self, key):
        if self._data_dict[key]  and self._datesInfos and self.check_numeric_and_length(key):
            dataset = np.array(self._data_dict[key])
            sum_ann_cal , mean_ann_cal, std_ann_cal = self.annual_statistics(dataset[:self._calage_index], self._datesInfos["data"][:self._calage_index])
            sum_ann_val , mean_ann_val, std_ann_val = self.annual_statistics(dataset[self._calage_index:], self._datesInfos["data"][self._calage_index:])
            sum_ann , mean_ann, std_ann = self.annual_statistics(dataset, self._datesInfos["data"])
            return {
                "data": dataset.tolist(),
                "data_cal" : dataset[:self._calage_index].tolist(),
                "data_val" : dataset[self._calage_index:].tolist(),
                "min": dataset.min().tolist(),
                "max": dataset.max().tolist(),
                "min_cal" : dataset[:self._calage_index].min().tolist(),
                "max_cal" : dataset[:self._calage_index].max().tolist(),
                "min_val" : dataset[self._calage_index:].min().tolist(),
                "max_val" : dataset[self._calage_index:].max().tolist(),
                "sum_val" : sum_ann_val.tolist(),
                "sum_cal" : sum_ann_cal.tolist(),
                "sum": sum_ann.tolist(),
                "mean_cal" : mean_ann_cal.tolist(),
                "mean_val" : mean_ann_val.tolist(),
                "mean" : mean_ann.tolist(),
                "std_cal" : std_ann_cal.tolist(),
                "std_val" : std_ann_val.tolist(),
                "std": std_ann.tolist(),
                "count" : len(dataset)
            }
        else:
            self.errorsChanged.emit()
            return {
                "data": [],
                "data_cal" : None,
                "data_val" : None,
                "min": None,
                "max": None,
                "min_val" : None,
                "max_val" : None,
                "min_cal" : None,
                "max_cal" : None,
                "sum_val" : None,
                "sum_cal" : None,
                "sum": None,
                "mean_ann_cal" : None,
                "mean_ann_val" : None,
                "mean" : None,
                "std_ann_cal" :None,
                "std_ann_val" : None,
                "std": None,
                "count" : None
            }

    def annual_statistics(self, data, dates):
        df = pd.DataFrame({"date": pd.to_datetime(dates), "value": data})
        df["year"] = df["date"].dt.year
        grouped = df.groupby("year")["value"]
        return grouped.sum().mean(), grouped.mean().mean(), grouped.std().mean()

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
        self._qInfos = self.updateDatas("Q")
        self._data_dict["Q"] = self._qInfos["data"]
        self.qInfosChanged.emit()
        self.dataDictChanged.emit()

    @Property(dict, notify=qInfosChanged)
    def qInfos(self):
        return self._qInfos

    @Slot()
    def updatePInfos(self):
        self._pInfos = self.updateDatas("P")
        self._data_dict["P"] = self._pInfos["data"]
        self.pInfosChanged.emit()
        self.dataDictChanged.emit()

    @Property(dict, notify=pInfosChanged)
    def pInfos(self):
        return self._pInfos

    @Slot()
    def updateTempInfos(self):
        self._tempInfos = self.updateDatas("T")
        self._data_dict["T"] = self._tempInfos["data"]
        self.tempInfosChanged.emit()
        self.dataDictChanged.emit()

    @Property(dict, notify=tempInfosChanged)
    def tempInfos(self):
        return self._tempInfos

    @Slot()
    def updateETPInfos(self):
        self._etpInfos = self.updateDatas("ETP")

        self._data_dict["ETP"] = self._etpInfos["data"]
        self.etpInfosChanged.emit()
        self.dataDictChanged.emit()

    @Property(dict, notify=etpInfosChanged)
    def etpInfos(self):
        return self._etpInfos

    @Slot()
    def transform_data(self):
        keys = ["Dates", "P", "T", "Q", "ETP"]

            # Utilisation de zip pour combiner les listes
        transformed = [
            dict(zip(keys, row))
            for row in zip(*[self._data_dict[key] for key in keys])
        ]
        self._display_data = transformed
        self.displayDataChanged.emit()


    @Property("QVariant", notify=displayDataChanged)
    def displayData(self):
        print("----------------------------")
        print(self._display_data[0:200])
        return self._display_data

    @Slot()
    def updateDatesInfos(self):
        if self._data_dict["Dates"]:
            date_series = self._data_dict["Dates"]
            date_format = self._date_format[self._user_format]

            # Conversion des dates
            parsed_dates = np.vectorize(self.check_and_convert_date)(date_series)
            dataset = [d.strftime(date_format) for d in parsed_dates]
            self._datesInfos = {
                "data": dataset,
                "data_cal": dataset[:self._calage_index],
                "data_val": dataset[self._calage_index:],
                "min": parsed_dates[0].strftime(date_format),
                "max": parsed_dates[-1].strftime(date_format),
                "count": len(parsed_dates)
            }

            self._data_dict["Dates"] = self._datesInfos["data"]

        self.datesInfosChanged.emit()
        self.dataDictChanged.emit()


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
            hd.append("Non défini")
            self._headers =hd
            self._data = df.to_dict(orient="list")
            # Émettre les signaux pour mettre à jour QML
            self.headersChanged.emit(self._headers)
            self.dataChanged.emit(self._data)

        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")


    @Slot(dict)
    def setDictValues(self, data_dict):
        self._data_dict = { key: [] if value == "Non défini" else self._data[value] for key, value in data_dict.items() }
        self.updateDatesInfos()
        self.updateETPInfos()
        self.updatePInfos()
        self.updateQInfos()
        self.updateTempInfos()
        #self.transform_data()

    #POUR LE CALCUL DE L'ETP DANS L'OPTION ETP
    @Slot(dict)
    def setEToValues(self, etp_list):
        self._data_dict["ETP"] = etp_list["ETP"]
        self._data_dict["Dates"] = etp_list["Dates"]
        self.updateDatesInfos()
        self.updateETPInfos()
        print("etp_list 1---------------------")
        print(etp_list)
        print(self._data_dict)


    @Slot(str)
    def initDatesValues(self, key):
        self._data_dict["Dates"] =  [] if key == "Non défini" else self._data[key]
        self.updateDatesInfos()


    @Slot(str)
    def initETPValues(self, key):
        self._data_dict["ETP"] =  [] if key == "Non défini" else self._data[key]
        self.updateETPInfos()

    @Slot(str)
    def initPValues(self, key):
        self._data_dict["P"] =  [] if key == "Non défini" else self._data[key]
        self.updatePInfos()


    @Slot(str)
    def initTempValues(self, key):
        self._data_dict["T"] =  [] if key == "Non défini" else self._data[key]
        self.updateTempInfos()

    @Slot(str)
    def initQValues(self, key):
        self._data_dict["Q"] =  [] if key == "Non défini" else self._data[key]
        self.updateQInfos()

import pandas as pd
import numpy as np
import datetime

from api.load_data.DataManager import DataManager
from dateutil import parser
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement
from itertools import zip_longest

class FileHandler(QObject):
    def __init__(self):
        super().__init__()

        self._data_manager = None
        self._headers = []
        self._data = []

        self._data_dict = {}
        self._calibration_time = {}
        self._date_format = {
            "YYYYMMDD" : "%Y%m%d",
            "yyyy-MM-dd" : "%Y-%m-%d" ,
            "yyyy/MM/dd" : "%Y/%m/%d"
        }
        self._user_format = "yyyy-MM-dd"
        self._qInfos = {}
        self._pInfos = {}
        self._etpInfos = {}
        self._datesInfos = {}

        self._errors = []
        self._display_data = []
        self._calage_index = 20

        self._calibration_date = ""
        self._validation_date = ""

        self._calibration_length = []
        self._validation_length = []

        self._activate = False

        self._ptq ={}
        self._data_parameters = {}

    headersChanged = Signal(list)
    dataChanged = Signal(list)
    dataDictChanged = Signal()
    userFormatChanged = Signal()
    calibrationTimeChanged= Signal()

    qInfosChanged = Signal()
    pInfosChanged = Signal()
    etpInfosChanged = Signal()
    datesInfosChanged = Signal()
    displayDataChanged = Signal()

    calibrationDateChanged = Signal()
    validationDateChanged = Signal()

    ptqChanged = Signal()

    errorsChanged = Signal()
    activateChanged = Signal()


    @Property(bool, notify=activateChanged)
    def activate(self):
        return self._activate

    @Property(list, notify=errorsChanged)
    def errors(self):
        return self._errors

    @Property(dict, notify=ptqChanged)
    def ptq(self):
        return self._ptq

    @Slot()
    def calibrationTime(self):
        dates = self._data_dict["Dates"]
        self._calibration_time = self._data_manager.getDatasDatesCalendar(dates)
        self.calibrationTimeChanged.emit()

    def setPeriodsDates(self, user_dates):
        if user_dates["calibration"] and user_dates["validation"]:
            c_start = pd.to_datetime(user_dates["calibration"][0])
            c_end = pd.to_datetime(user_dates["calibration"][1])
            v_start = pd.to_datetime(user_dates["validation"][0])
            v_end = pd.to_datetime(user_dates["validation"][1])
            if c_start >= c_end or v_start >= v_end or c_start == v_start or c_end == v_end or  c_start == v_end or v_start == v_end:
                raise Exception("Dates non-corrects")
            if c_end - c_start <pd.Timedelta(days=365):
                raise Exception("Non-suffisant values")
            if c_start >= v_start and v_end >= c_start:
                raise Exception("Crossing dates")
            dates = self._data_dict["Dates"]
            df = pd.DataFrame({"date": pd.to_datetime(dates)})
            calib_dates = df[(df["date"] >= c_start) & (df["date"] <= c_end)]
            valid_dates = df[(df["date"] >= v_start) & (df["date"] <= v_end)]
            return calib_dates, valid_dates
        else :
            raise Exception("Define calibration and validation dates")


    @Property(dict, notify=calibrationTimeChanged)
    def calendar_dates(self):
        return self._calibration_time

    @Property(str, notify=calibrationDateChanged)
    def calibrationDate(self):
        return self._calibration_date

    @Property(str, notify=validationDateChanged)
    def validationDate(self):
        return self._validation_date

    @Slot(dict)
    def updateCalibrationAndValibationDates(self, dates):
        self._errors = []
        self._activate = False

        try : 
            dates_list = self.setPeriodsDates(dates)
            self._calibration_length = dates_list[0].index
            self._validation_length = dates_list[1].index
            self._calibration_date = dates_list[0].iloc[0].dt.strftime("%Y-%m-%d").iloc[0] +" to " + dates_list[0].iloc[-1].dt.strftime("%Y-%m-%d").iloc[0]
            self._validation_date = dates_list[1].iloc[0].dt.strftime("%Y-%m-%d").iloc[0] +" to "+ dates_list[1].iloc[-1].dt.strftime("%Y-%m-%d").iloc[0]
            self.calibrationDateChanged.emit()
            self.validationDateChanged.emit()
            self.updateFields()
            self._ptq = self._data_manager._ptq

            self._activate = True

            self.qInfosChanged.emit()
            self.pInfosChanged.emit()
            self.etpInfosChanged.emit()
            self.datesInfosChanged.emit()
            self.ptqChanged.emit()
            self.activateChanged.emit()

        except Exception as e:
            self._errors = e.args[0].split(";")
            self.errorsChanged.emit()



    @Slot()
    def updateFields(self):
        self._qInfos = self._data_manager.updateDatas("Q", self._calibration_length, self._validation_length)
        self._pInfos = self._data_manager.updateDatas("P", self._calibration_length, self._validation_length)
        self._etpInfos = self._data_manager.updateDatas("ETP", self._calibration_length, self._validation_length)
        self._datesInfos = self._data_manager.updateDatesInfos(self._data_dict["Dates"], self._calibration_length, self._validation_length)


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

    @Property(dict, notify=qInfosChanged)
    def qInfos(self):
        return self._qInfos

    @Property(dict, notify=pInfosChanged)
    def pInfos(self):
        return self._pInfos


    @Property(dict, notify=etpInfosChanged)
    def etpInfos(self):
        return self._etpInfos


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
            self._headers =hd
            self._data = df.to_dict(orient="list")
            # Émettre les signaux pour mettre à jour QML
            self.headersChanged.emit(self._headers)
            self.dataChanged.emit(self._data)

        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")



    @Slot(dict)
    def setDictValues(self, data_dict):
        self._errors = []
        try :
            self._data_manager = DataManager(self._data, data_dict)
            self._data_dict = self._data_manager._data_dict
            self.dataDictChanged.emit()
        except Exception as e :
            self._errors = e.args[0].split(";")
            self.errorsChanged.emit()





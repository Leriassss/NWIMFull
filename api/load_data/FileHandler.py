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
        self._tempInfos = {}
        self._etpInfos = {}
        self._datesInfos = {}

        self._errors = []
        self._display_data = []
        self._calage_index = 20

        self._calibration_date = ""
        self._validation_date = ""

        self._calibration_length = []
        self._validation_length = []

        self._ptq ={}

    headersChanged = Signal(list)
    dataChanged = Signal(list)
    dataDictChanged = Signal()
    userFormatChanged = Signal()
    calibrationTimeChanged= Signal()

    qInfosChanged = Signal()
    pInfosChanged = Signal()
    etpInfosChanged = Signal()
    tempInfosChanged = Signal()
    datesInfosChanged = Signal()
    displayDataChanged = Signal()

    calibrationDateChanged = Signal()
    validationDateChanged = Signal()

    ptqChanged = Signal()

    errorsChanged = Signal()


    @Property(list, notify=errorsChanged)
    def errors(self):
        return self._errors

    @Property(dict, notify=ptqChanged)
    def ptq(self):
        return self._ptq

    @Slot()
    def calibrationTime(self):
        print("------------------- CT")
        print(self._data_dict)
        dates = self._data_dict["Dates"]
        self._calibration_time = self._data_manager.getDatasDatesCalendar(dates)
        print("APPEL------------- 2")
        print(self._calibration_time)
        self.calibrationTimeChanged.emit()

    @Property(dict, notify=calibrationTimeChanged)
    def calendar_dates(self):
        print("CALENDAR-------------")
        print(self._calibration_time)
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
        try : 
            dates_list = self._data_manager.updateCalibrationAndValibationDates(dates)
            self._calibration_length = dates_list[0]
            self._validation_length = dates_list[1]
            self._calibration_date =dates_list[2]
            self._validation_date = dates_list[3]
            self.calibrationDateChanged.emit()
            self.validationDateChanged.emit()
            print("---------- uCAVD (fh)-----------")
            print(dates)
            print(self._calibration_date, self._validation_date)
            print(" --------- EMISSION --------------")
            self.updateFields()
            self._ptq = self._data_manager._ptq

            print(self._ptq)

            self.qInfosChanged.emit()
            self.pInfosChanged.emit()
            self.tempInfosChanged.emit()
            self.etpInfosChanged.emit()
            self.datesInfosChanged.emit()
            self.ptqChanged.emit()

        except Exception as e:
            print('EXECEPTION LEVEE ------------------------------')
            print(e)
            self._errors = e.args[0].split(";")
            self.errorsChanged.emit()



    @Slot()
    def updateFields(self):
        self._qInfos = self._data_manager.updateDatas("Q", self._calibration_length, self._validation_length)
        self._pInfos = self._data_manager.updateDatas("P", self._calibration_length, self._validation_length)
        self._tempInfos = self._data_manager.updateDatas("T", self._calibration_length, self._validation_length)
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

    @Property(dict, notify=tempInfosChanged)
    def tempInfos(self):
        return self._tempInfos


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
            self._calibration_date =self._data_dict["Dates"][0]
            self._validation_date = self._data_dict["Dates"][0]
            self.calibrationDateChanged.emit()
            self.validationDateChanged.emit()
        except Exception as e :
            self._errors = e.args[0].split(";")
            self.errorsChanged.emit()





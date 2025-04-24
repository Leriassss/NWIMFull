# This Python file uses the following encoding: utf-8
import pandas as pd
import numpy as np
import datetime
from dateutil import parser
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement
from itertools import zip_longest


class DataManager:
        def __init__(self, data, columnMapping):
            self._errors = []
            self._data_dict = self.setDictValues(data, columnMapping)
            self._ptq = {
              "CALIBRATION" : {"Dates" : None, "P" : None, "T" : None, "Q" : None},
              "VALIDATION" : {"Dates" : None, "P" : None, "T" : None, "Q" : None}
            }

        def check_keys_match(self, d, keys_list):
            dict_keys = set(d.keys())
            list_keys = set(keys_list)

            return dict_keys == list_keys

        def setDictValues(self, data, columnMapping):
            data_dict_values = { key: data[value] for key, value in columnMapping.items() }
            if not self.check_keys_match(data_dict_values, ["Dates","T", "ETP", "Q", "P"]):
                raise Exception("Des Colonnes de données sont manquantes!")

            self._errors = []
            for key in columnMapping.keys():
                self.check_numeric_and_length(data_dict_values, key,self._errors)

            date_format = "%Y-%m-%d"
            try :
                parsed_dates = np.vectorize(self.check_and_convert_date)(data_dict_values["Dates"])
                data_dict_values["Dates"] = np.array([d.strftime(date_format) for d in parsed_dates]).tolist()
            except Exception :
                errors.append("Format de dates non reconnues")

            if len(self._errors) != 0:
                raise Exception(";".join(self._errors))
            else:
                return data_dict_values


        def check_numeric_and_length(self,obj, key, errors):
            if key in obj.keys() and key != "Dates":
                data = obj[key]
                try:
                    series =  np.array(data, dtype=np.float64)
                except Exception as e:
                    errors.append(f"Les données de la série {key} contiennent des valeurs non numériques")
                if len(data) != len(obj.get("Dates", [])):
                    errors.append(f"Les longueurs des dates et de la série {key} ne correspondent pas")



        def check_and_convert_date(self, date):
            return parser.parse(str(date))

        def updateDatas(self, key, c_length, v_length):
            dataset = np.array(self._data_dict[key])
            dates_infos = np.array(self._data_dict["Dates"])
            sum_ann_cal , mean_ann_cal, std_ann_cal = self.annual_statistics(dataset[c_length], dates_infos[c_length])
            sum_ann_val , mean_ann_val, std_ann_val = self.annual_statistics(dataset[v_length], dates_infos[v_length])
            sum_ann , mean_ann, std_ann = self.annual_statistics(dataset, self._data_dict["Dates"])
            self._ptq["CALIBRATION"][key] = dataset[c_length].tolist()
            self._ptq["VALIDATION"][key] = dataset[v_length].tolist()
            return {
                    "data": dataset.tolist(),
                    "data_cal" : dataset[c_length].tolist(),
                    "data_val" : dataset[v_length].tolist(),
                    "min": dataset.min().tolist(),
                    "max": dataset.max().tolist(),
                    "min_cal" : dataset[c_length].min().tolist(),
                    "max_cal" : dataset[c_length].max().tolist(),
                    "min_val" : dataset[v_length].min().tolist(),
                    "max_val" : dataset[v_length].max().tolist(),
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


        def annual_statistics(self, data, dates):
            df = pd.DataFrame({"date": pd.to_datetime(dates), "value": data})
            df["year"] = df["date"].dt.year
            grouped = df.groupby("year")["value"]
            return grouped.sum().mean(), grouped.mean().mean(), grouped.std().mean()

        def getDatasDatesCalendar(self, dates):
            df = pd.DataFrame({"date": pd.to_datetime(dates)})

            # Extraction de l'année, du mois et du jour
            df["year"] = df["date"].dt.year.astype(str)
            df["month"] = df["date"].dt.month.astype(str)
            df["day"] = df["date"].dt.day

            # Construction du dictionnaire imbriqué
            result = {}
            for _, row in df.iterrows():
                year, month, day = row["year"], row["month"], row["day"]

                if year not in result:
                    result[year] = {}

                if month not in result[year]:
                    result[year][month] = []

                result[year][month].append(day)

            return result

        def updateCalibrationAndValibationDates(self, dates):
            calibration_date = parser.parse(str(dates['calibration']))
            validation_date = parser.parse(str(dates['validation']))
            if abs((calibration_date-validation_date).days) < 10 :
                raise Exception("L'écart Calage-Validation est insuffisant")
            df = pd.DataFrame(self._data_dict)
            df['Dates'] = pd.to_datetime(df['Dates'])

            if(calibration_date<=validation_date):
                calibration_length = df[(df['Dates'] >= calibration_date) & (df['Dates'] < validation_date)].index
                validation_length = df[(df['Dates'] >= validation_date)].index
            else:
                validation_length = df[(df['Dates'] >= validation_date) & (df['Dates'] < calibration_date)].index.tolist()
                calibration_length= df[(df['Dates'] >= calibration_date)].index
            return [calibration_length, validation_length , calibration_date.strftime("%Y-%m-%d"), validation_date.strftime("%Y-%m-%d")]


        def updateDatesInfos(self, date_series, c_length, v_length):
            date_format = "%Y-%m-%d"
            # Conversion des dates
            try :
                parsed_dates = np.vectorize(self.check_and_convert_date)(date_series)
            except Exception :
                self._errors.append("Format de dates non reconnues")
                parsed_dates = []

            dataset = np.array([d.strftime(date_format) for d in parsed_dates])
            print("-------- updateDatesInfos (DATAMANAGER)---------------")
            print(dataset)
            print(c_length)
            print(v_length)
            print({
                "data": dataset.tolist(),
                "data_cal": dataset[c_length].tolist(),
                "data_val": dataset[v_length].tolist(),
                "min": parsed_dates[0].strftime(date_format),
                "max": parsed_dates[-1].strftime(date_format),
                "count": len(parsed_dates)
            })
            self._ptq["CALIBRATION"]["Dates"] = dataset[c_length].tolist()
            self._ptq["VALIDATION"]["Dates"] = dataset[v_length].tolist()
            return  {
                    "data": dataset.tolist(),
                    "data_cal": dataset[c_length].tolist(),
                    "data_val": dataset[v_length].tolist(),
                    "min": parsed_dates[0].strftime(date_format),
                    "max": parsed_dates[-1].strftime(date_format),
                    "count": len(parsed_dates)
                }







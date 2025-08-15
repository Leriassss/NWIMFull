import json
from pathlib import Path

import pandas as pd

from backend.simulation.models.SimulationModel import SimulationModel

class ResultsFileManager:     

    regressionFileIds = ["datalist", "regressor"]
    modelFileIds = ["pn", "qb", "loss", "sim"]
    @staticmethod
    def serialize_params(simulation_model):
        return {
            "params" : {key: value.tolist() for key, value in simulation_model.items()}
            }
    @staticmethod
    def deserialize_params(data):
        try:
            if "params" not in data:
                raise ValueError(f"Donnée manquante dans le fichier JSON ")               
            return data["params"]
        
        except ValueError as e:
            print(f"Erreur de validation des données : {e}")
            return None
        except Exception as e:
            print(f"Une erreur inattendue s'est produite lors de la création de l'objet : {e}")
            return None
        
    @staticmethod
    def saveData(datas : pd.DataFrame, file_path)-> None:
        try:
            datas.to_csv(file_path, sep= '\t', index=False)
        except IOError as e:
            raise RuntimeError(f"Failed to save results: {str(e)}")

    @staticmethod
    def save_optim_range_params(params, file_path) -> None:
        file_path = file_path +".json"
        try:
            with open(file_path, 'w') as f:
                json.dump(params, f, indent=2)
        except IOError as e:
            raise RuntimeError(f"Failed to save results: {str(e)}")

    @staticmethod
    def save_calibration_results(data, path) -> None:
        file_path = Path(path)
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            raise RuntimeError(f"Failed to save results: {str(e)}")

    @staticmethod
    def save_regression_results(data, path) -> None:
        file_path = Path(path)
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            raise RuntimeError(f"Failed to save results: {str(e)}")

    def load_optim_range_params(self, filename):
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                return data
            except FileNotFoundError:
                print(f"Erreur : Le fichier {filename} n'existe pas.")
                return None
            except json.JSONDecodeError:
                print(f"Erreur : Le fichier {filename} n'est pas un JSON valide.")
                return None
            except IOError as e:
                print(f"Erreur lors de la lecture du fichier {filename}: {e}")
                return None
            except Exception as e:
                print(f"Une erreur inattendue s'est produite lors de la lecture : {e}")
                return None

    @staticmethod
    def load_calibration_results(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

        except FileNotFoundError:
            raise Exception(f"Erreur : Le fichier {filename} n'existe pas.")
        except json.JSONDecodeError:
            raise Exception(f"Erreur : Le fichier {filename} n'est pas un JSON valide.")
        except IOError as e:
            raise Exception(f"Erreur lors de la lecture du fichier {filename}: {e}")
        except Exception as e:
            raise Exception(f"Une erreur inattendue s'est produite lors de la lecture : {e}")

        print("data ----------------- ", data)
        if set(data.keys()) != set(ResultsFileManager.modelFileIds):
            raise ValueError("Le fichier n'est pas un fichier de modèle valide")

        return data

    @staticmethod
    def load_regression_results(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise Exception(f"Le fichier n'existe pas.")
        except json.JSONDecodeError:
            raise Exception(f"Le fichier n'est pas un JSON valide.")
        except IOError as e:
            raise Exception(f"Erreur lors de la lecture du fichier")
        except Exception as e:
            raise Exception(f"Une erreur inattendue s'est produite lors de la lecture")

        if set(data.keys()) != set(ResultsFileManager.regressionFileIds):
            raise ValueError("Le fichier n'est pas un fichier de chargement valide")

        return data




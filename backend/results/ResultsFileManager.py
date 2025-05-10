import json
from pathlib import Path

import pandas as pd

from backend.simulation.models.SimulationModel import SimulationModel

class ResultsFileManager:     

    @staticmethod
    def serialize_params(simulation_model: SimulationModel):
        return {
            "params" : {key: value.tolist() for key, value in simulation_model.params.items()}
            }
    @staticmethod
    def deserialize_params(data):
        try:
            if "params" not in data:
                raise ValueError(f"Donnée manquante dans le fichier JSON : {key}")               
            return data["params"]
        
        except ValueError as e:
            print(f"Erreur de validation des données : {e}")
            return None
        except Exception as e:
            print(f"Une erreur inattendue s'est produite lors de la création de l'objet : {e}")
            return None
        
            
    def save_optim_range_params(self, params, file_path) -> None:
        file_path = file_path +".json"
        try:
            with open(file_path, 'w') as f:
                json.dump(params, f, indent=2)
        except IOError as e:
            raise RuntimeError(f"Failed to save results: {str(e)}")


    def save_calibration_results(self, data: SimulationModel, path) -> None:
        file_path = Path(path) +".json"
        try:
            with open(file_path, 'w') as f:
                json.dump(ResultsFileManager.serialize_params(data), f, indent=2)
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

        
    def load_calibration_results(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            return ResultsFileManager.deserialize_params(data)
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

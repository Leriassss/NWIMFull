import json
from pathlib import Path

import pandas as pd

from simulation.models.SimulationModel import SimulationModel

class CalibrationResults:
    def __init__(self):
        self.results_dir = Path("C:/Users/HP/Documents/p/results")       

    @staticmethod
    def _to_dict(simulation_model: SimulationModel):
        data_serializable = {key: value.tolist() for key, value in simulation_model.params.items()}
        return {
            "calibration_sim": simulation_model.calibration_sim.to_json(),
            "validation_sim": simulation_model.validation_sim.to_json(),
            "params": data_serializable,
            "calibration_metric": simulation_model.calibration_metric,
            "validation_metric": simulation_model.validation_metric
        }
    
    def save_calibration(self, data: SimulationModel, result_type: str) -> None:
        file_path = self.results_dir / f"{result_type}.json"
        try:
            self.results_dir.mkdir(exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(CalibrationResults._to_dict(data), f, indent=2)
        except IOError as e:
            raise RuntimeError(f"Failed to save results: {str(e)}")

    def save_regression(self, data: list[SimulationModel], automatic_params, grid_params, regression_params) -> None:
        """Save regression results with parameter ranges and merge existing data"""
        file_path = self.results_dir / "regression_results.json"
        try:
            self.results_dir.mkdir(exist_ok=True)
            
            # Load existing data
            existing_data = []
            if file_path.exists():
                with open(file_path, 'r') as f:
                    existing_data = json.load(f)
            
            # Create new entry with parameters and models
            new_entry = {
                "AutomaticParams": automatic_params,
                "GridParams": grid_params,
                "RegressionParams": regression_params,
                "models": [CalibrationResults._to_dict(model) for model in data]
            }
            
            # Merge and save
            existing_data.append(new_entry)
            with open(file_path, 'w') as f:
                json.dump(existing_data, f, indent=2)
                
        except IOError as e:
            raise RuntimeError(f"Failed to save results: {str(e)}")

    def load_regression(self) -> list:
        """Load merged regression results with parameters"""
        file_path = self.results_dir / "regression_results.json"
        if not file_path.exists():
            return []
            
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            results = []
            for entry in data:
                models = [CalibrationResults._from_dict(model_dict)
                         for model_dict in entry.get("models", [])]
                results.append({
                    "automatic_params": entry.get("AutomaticParams"),
                    "grid_params": entry.get("GridParams"),
                    "regression_params": entry.get("RegressionParams"),
                    "models": [m for m in models if m is not None]
                })
                
            return results
            
        except Exception as e:
            print(f"Error loading regression data: {e}")
            return []
        
    @staticmethod
    def _from_dict(data):
        try:
            # Validation des données requises
            required_keys = ["calibration_sim", "validation_sim", "params", "calibration_metric", "validation_metric"]
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Donnée manquante dans le fichier JSON : {key}")

            return SimulationModel(
                calibration_sim=pd.Series(json.loads(data["calibration_sim"])),
                validation_sim=pd.Series(json.loads(data["validation_sim"])),
                params=data["params"],
                calibration_metric=float(data["calibration_metric"]),
                validation_metric=float(data["validation_metric"])
            )
        except ValueError as e:
            print(f"Erreur de validation des données : {e}")
            return None
        except Exception as e:
            print(f"Une erreur inattendue s'est produite lors de la création de l'objet : {e}")
            return None
        
    def load_calibration(self, file):
        filename = self.results_dir / f"{file}.json"
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            return CalibrationResults._from_dict(data)
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
        
    def display(self) -> None:
        """Display results (to be implemented by subclasses)"""
        raise NotImplementedError("Display method must be implemented in subclass")
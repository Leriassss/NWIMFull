
class SimulationModel:
    def __init__(self,calibration_sim, validation_sim, params, calibration_metric, validation_metric):
        self.calibration_sim = calibration_sim
        self.validation_sim = validation_sim
        self.params = params
        self.calibration_metric = calibration_metric
        self.validation_metric = validation_metric
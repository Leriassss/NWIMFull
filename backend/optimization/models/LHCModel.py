class LHCModel:
    def __init__(self,n_samples):
        self.n_samples = n_samples
        self.validate_params()

    def validate_params(self):
        if not isinstance(self.n_samples, int) or self.n_samples <= 0:
            raise ValueError("max_num_iteration doit être un entier positif.")



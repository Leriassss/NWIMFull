class GridParams:
    def __init__(self):
        self.production = {
            "WMin": {"w": [0.1, 0.9]},
            "Horton": {"f_0": [1, 20], "f_t": [1, 3], "k": [1, 3]},
            "SCS": {"cn": [10, 90], "i_a": [0.1, 0.5]},
            "Holtan": {"f_0": [1, 20], "f_t": [1, 3], "k": [1, 3], "sc": [1, 20]},
            "Philip": {"S": [1, 20], "K": [1, 20]}
        }
        
        self.recession = {
            "FureyGupta": {"gamma": [0.08, 0.1], "cs_over_c": [0.5, 2]},
            "Chapman": {"alpha": [0.7, 1]},
            "Quadratic": {"lambda": [0.1, 0.7]},
            "Exponential": {"lambda": [0.1, 0.7]}
        }
        
        self.routing = {
            "PLA": {"mu": [1,5], "landa": [1,20], "t_x": [0.1, 0.9], "s_f": [0.01, 0.09]},
            "Nash": {"nash_k": [1, 50], "nash_n": [1, 50], "time_base": [1, 20]},
            "HUN": {"dt": [1, 1.1], "time_base": [1, 25]},
            "Muskingum": {"k": [1,50], "x": [0.2,0.5], "dt": [1,50]}
        }
        
        self.loss = {
            "ia_loss": {"s": [0, 50], "alpha": [0, 1], "loss_days": [0, 100]},
            "eto_loss": {"alpha": [0.1, 0.5]},
            "s_loss": {"s": [0, 50], "loss_days": [0, 10]},
            "p_loss": {"p": [0.2, 0.5]},
            "no_loss": {"no": [0, 1]}
        }
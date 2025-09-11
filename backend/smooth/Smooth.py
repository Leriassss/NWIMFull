import pandas as pd
import numpy as np

class Smooth:
    def laminage(self, o_l, qsim, index):
        c = qsim.copy()
        excess = c[index] - o_l
        c[index] = o_l
        i = index
        while excess > 0 and i < len(c):
            a = c[i]
            c[i] = np.minimum(o_l, a + excess)
            excess = np.fmax(0,a + excess - o_l)
            i += 1
        return c
    
    def compute_laminage(self, qsim, output_limit):
        limit_reach = True
        c = np.array(qsim)
        while limit_reach :
            indexes = np.where(c > output_limit)[0]
            if len(indexes) > 0 :
                index = indexes[0]
                c = self.laminage(output_limit, c, index)
            else :
                limit_reach = False
        return c
    
    def compute_lissage(self, qsim, window):
        return pd.Series(qsim).rolling(window=window, center=True, min_periods=1).mean()
    
    def compute(self, method, args):
        return self.methods()[method](args)

    def methods(self):
        return {
        "rolling" : self.compute_laminage,
        "smoothing" : self.compute_lissage

    }
    @staticmethod
    def methodsList():
        return [
        "rolling",
        "smoothing"
    ]

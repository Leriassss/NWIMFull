import numpy as np
import pandas as pd


class Adapter:
    """
        def __init__(self, prod_function, prod_args):
        return self.adapter(prod_function, prod_args)
    """


    def adapter(self, prod_function,args):
        non_null_groups = args.prec.groupby((np.round(args.prec,2) == 0.0).cumsum())
        sequences = pd.Series([group.values for key, group in non_null_groups])
        r_h = list()
        for element in sequences :
            args.prec = pd.Series(element)
            r_h.append(prod_function(args).compute())
        return np.concatenate(r_h).tolist()
    
    def daily_seq_adapter(self, prod_fonction, args):
        r_h = list(map(lambda x : prod_fonction(x).compute(),args.prec))
        return r_h
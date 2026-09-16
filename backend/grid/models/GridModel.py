from itertools import product
from backend.contracts.Bundle import RoutingData

class GridModel:
    def __init__(self, productionBundle,recessionBundle,routingBundle,lossBundle):
        self.combinations = []
        self.combinations_names = []
        cartesian_product = product(productionBundle.items(), recessionBundle.items(), lossBundle.items(), routingBundle.items())
        for prod, rec, loss, rout in cartesian_product:
            comb_dict : RoutingData = {
                "pn": prod[1], 
                "qb": rec[1],
                "loss": loss[1], 
                "sim": rout[1],
            }
            self.combinations_names.append((prod[0],rec[0],rout[0],loss[0]))
            self.combinations.append(comb_dict)

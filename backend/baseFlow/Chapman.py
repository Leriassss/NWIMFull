from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.models.ChapmanModel import ChapmanModel
from backend.ptq.PTQ import PTQ


class Chapman(BaseFlow):
    """
    Classe pour implémenter la méthode de récession Chapman.
    """
    def __init__(self,ptq : PTQ, chapmanModel : ChapmanModel):
        self.flow_series = ptq.q
        self.alpha = chapmanModel.alpha

    def compute(self):
        """
        Implémente la méthode de séparation des écoulements selon la méthode de Chapman.
        
        Args:
            flow_series : Série temporelle des débits de rivières (Yk).
            alpha (float) : Coefficient alpha (par défaut 0.925).
            
        Returns:
            np.array : Série des débits de base (Qk).
        """
        Q_base = self.flow_series.copy()
        factor1 = (3 * self.alpha - 1) / (3 - self.alpha)
        factor2 = (1 - self.alpha) / (3 - self.alpha)
        
        for k in range(1, len(self.flow_series)):
            Q_base[k] = (
                factor1 * Q_base[k - 1]
                + factor2 * (self.flow_series[k] + self.flow_series[k - 1])
            )
        
        return Q_base

    @staticmethod
    def help():
        """
        Fournit une description des méthodes disponibles dans la classe Recession.
        """
        description = """
        Implémente le filtre de récession de Furey-Gupta.


        Arguments pour `furey_gupta`:
        - flow_series : Série temporelle des débits [mm/jour] (pd.Series ou np.ndarray).
        - gamma : Coefficient de récession (par défaut 0.03).
        - cs_over_c : Ratio des coefficients (par défaut 1.1).
        """
        print(description)

class GreenAmptModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode Green-Ampt.
    """

    def __init__(self, prec, succion, d_theta, ks, H0):
        self.prec = prec
        self.succion = succion
        self.d_theta = d_theta
        self.ks = ks
        self.H0 = H0
        self.validate()

    def validate(self):
        """
        Valide les paramètres du modèle.
        """
        if not isinstance(self.prec, pd.Series):
            raise TypeError("La variable 'prec' doit être une série pandas.")
        if any(param <= 0 for param in [self.succion, self.d_theta, self.ks, self.H0]):
            raise ValueError("Les paramètres 'succion', 'd_theta', 'ks' et 'H0' doivent être strictement positifs.")
        if self.prec.isnull().any():
            raise ValueError("La série 'prec' ne doit pas contenir de valeurs manquantes.")

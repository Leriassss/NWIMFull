class SCSModel:
    """
    Modèle de données pour valider les paramètres nécessaires à la méthode SCS.
    """

    def __init__(self, curve_number: float, i_a = 0.2):
        """
        Initialise et valide les données pour la méthode SCS.

        :param prec: Série pandas contenant les précipitations (en mm).
        :param curve_number: Curve Number, doit être compris entre 0 et 100.
        """
        self.curve_number = float(curve_number)
        self.i_a = float(i_a)
        self.validate()

    def validate(self):  
        try:
            if (self.curve_number < 0 or self.curve_number > 100):
                raise ValueError("Le Curve Number doit être compris entre 0 et 100.")
            if (self.i_a < 0 or self.i_a > 1):
                raise ValueError("Les pertes initiales doivent être compris entre 0 et 1.")
            return True
        except Exception as e:
            return str(e)

    def to_dict(self):
        return {
            "curve_number": self.curve_number,
            "i_a" : self.i_a
        }

    @staticmethod
    def get_parameter_names():
        return {
            "curve_number": "CN",
            "i_a" : "ia"
            }

    @staticmethod
    def get_default_ranges():
        return {
            "curve_number": [0,100],
            "i_a" : [0,1]
            }
    
    @staticmethod
    def get_default_values():
        return {
            "curve_number": 25,
            "i_a" : 0.2
        }

    @staticmethod
    def validate_parameter(key, value):
        try:
            value = float(value)  # S'assure que la valeur est un nombre
            if key == "curve_number" and (value < 0 or value > 100):
                raise ValueError("Le Curve Number doit être compris entre 0 et 100.")
            elif key == "i_a" and (value < 0 or value > 1):
                raise ValueError("Les pertes initiales doivent être compris entre 0 et 1.")
            return True
        except Exception as e:
            return str(e)

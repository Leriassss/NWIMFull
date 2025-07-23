class GAModel:
    def __init__(self, max_num_iteration=3000, population_size=100, mutation_probability=0.1,
                 elit_ratio=0.01, crossover_probability=0.5, parents_portion=0.3
                 ):

        self.max_num_iteration = max_num_iteration
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.elit_ratio = elit_ratio
        self.crossover_probability = crossover_probability
        self.parents_portion = parents_portion
        self.crossover_type = 'uniform'
        self.max_iteration_without_improv = None

        self.validate()

    def validate(self):
        """ Vérifie tous les paramètres à l'initialisation. """
        for key, value in self.to_dict().items():
            validation = self.validate_parameter(key, value)
            if validation is not True:
                raise ValueError(validation)

    def get_default_values():
        """ Retourne les paramètres sous forme de dictionnaire. """
        return {
            'max_num_iteration': 3000,
            'population_size': 100,
            'mutation_probability': 0.1,
            'elit_ratio': 0.01,
            'crossover_probability': 0.5,
            'parents_portion': 0.3,
            'crossover_type':'uniform',
            'max_iteration_without_improv' : None
        }
    
    def to_dict(self):
        return {
                'max_num_iteration': int(self.max_num_iteration),
                'population_size': int(self.population_size),
                'mutation_probability': float(self.mutation_probability),
                'elit_ratio': float(self.elit_ratio),
                'crossover_probability': float(self.crossover_probability),
                'parents_portion': float(self.parents_portion),
                'crossover_type':self.crossover_type,
                'max_iteration_without_improv' : self.max_iteration_without_improv
        }

    @staticmethod
    def get_parameter_names():
        """ Retourne les noms des paramètres avec leurs descriptions. """
        return {
            'max_num_iteration': "Nombre max d'itérations",
            'population_size': "Taille de la population",
            'mutation_probability': "Probabilité de mutation",
            'elit_ratio': "Ratio d'élitisme",
            'crossover_probability': "Probabilité de croisement",
            'parents_portion': "Proportion de parents",
        }

    @staticmethod
    def validate_parameter(key, value):
        """
        Vérifie dynamiquement la validité d'un paramètre spécifique.

        :param key: Nom du paramètre à vérifier.
        :param value: Valeur du paramètre à valider.
        :return: True si valide, sinon un message d'erreur.
        """
        try:
            if key == "max_num_iteration":
                if int(value) <= 0:
                    raise ValueError("max_num_iteration doit être un entier positif.")
            elif key == "population_size":
                if  int(value) <= 0:
                    raise ValueError("population_size doit être un entier positif.")
            elif key == "mutation_probability":
                value = float(value)
                if not (0 <= value <= 1):
                    raise ValueError("mutation_probability doit être un float entre 0 et 1.")
            elif key == "elit_ratio":
                value = float(value)
                if not (0 <= value <= 1):
                    raise ValueError("elit_ratio doit être un float entre 0 et 1.")
            elif key == "crossover_probability":
                value = float(value)
                if not (0 <= value <= 1):
                    raise ValueError("crossover_probability doit être un float entre 0 et 1.")
            elif key == "parents_portion":
                value = float(value)
                if not (0 <= value <= 1):
                    raise ValueError("parents_portion doit être un float entre 0 et 1.")
            elif key == "crossover_type" :
                pass
            elif key == "max_iteration_without_improv":
                pass
            else:
                 raise ValueError(f"Paramètre inconnu : {key}")
            return True
        except Exception as e:
            return str(e)


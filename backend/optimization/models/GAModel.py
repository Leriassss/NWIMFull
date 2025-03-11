class GAModel:
    def __init__(self, max_num_iteration=3000, population_size=100, mutation_probability=0.1,
                 elit_ratio=0.01, crossover_probability=0.5, parents_portion=0.3,
                 crossover_type='uniform', max_iteration_without_improv=None):

        self.max_num_iteration = max_num_iteration
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.elit_ratio = elit_ratio
        self.crossover_probability = crossover_probability
        self.parents_portion = parents_portion
        self.crossover_type = crossover_type
        self.max_iteration_without_improv = max_iteration_without_improv
        self.validate_params()

        self.parameter_names = {
                    'max_num_iteration': "Nombre max d'itérations",
                    'population_size': "Taille de la population",
                    'mutation_probability': "Probabilité de mutation",
                    'elit_ratio': "Ratio d'élitisme",
                    'crossover_probability': "Probabilité de croisement",
                    'parents_portion': "Proportion de parents",
                    'crossover_type': "Type de croisement",
                    'max_iteration_without_improv': "Max itérations sans amélioration"
                }

    def validate_params(self):
        """ Vérifie que les paramètres ont le bon type de données. """
        if not isinstance(self.max_num_iteration, int) or self.max_num_iteration <= 0:
            raise ValueError("max_num_iteration doit être un entier positif.")

        if not isinstance(self.population_size, int) or self.population_size <= 0:
            raise ValueError("population_size doit être un entier positif.")

        if not isinstance(self.mutation_probability, (float, int)) or not (0 <= self.mutation_probability <= 1):
            raise ValueError("mutation_probability doit être un float entre 0 et 1.")

        if not isinstance(self.elit_ratio, (float, int)) or not (0 <= self.elit_ratio <= 1):
            raise ValueError("elit_ratio doit être un float entre 0 et 1.")

        if not isinstance(self.crossover_probability, (float, int)) or not (0 <= self.crossover_probability <= 1):
            raise ValueError("crossover_probability doit être un float entre 0 et 1.")

        if not isinstance(self.parents_portion, (float, int)) or not (0 <= self.parents_portion <= 1):
            raise ValueError("parents_portion doit être un float entre 0 et 1.")

        if not isinstance(self.crossover_type, str):
            raise ValueError("crossover_type doit être une chaîne de caractères.")

        if self.max_iteration_without_improv is not None and (not isinstance(self.max_iteration_without_improv, int) or self.max_iteration_without_improv < 0):
            raise ValueError("max_iteration_without_improv doit être un entier positif ou None.")

    def to_dict(self):
        """ Retourne les paramètres sous forme de dictionnaire. """
        return {
            'max_num_iteration': self.max_num_iteration,
            'population_size': self.population_size,
            'mutation_probability': self.mutation_probability,
            'elit_ratio': self.elit_ratio,
            'crossover_probability': self.crossover_probability,
            'parents_portion': self.parents_portion,
            'crossover_type': self.crossover_type,
            'max_iteration_without_improv': self.max_iteration_without_improv
        }

    def get_parameter_names(self):
        """ Retourne le dictionnaire des noms des paramètres. """
        return self.parameter_names


########################################################
#   ____  _      ___   _     ____   __    ___   _      #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ |  #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \|  #
#                                                      #
#                  Chad Carlson - 2017                 #
########################################################


from evolearn.algorithms import neat
from evolearn.environments import environment_simple
from evolearn.utils.visualize import VisualizeLeader

import MultiNEAT as mneat
import numpy as np


class SimulationNEAT:

    """SimulationNEAT Experiment Simulation Class.
    
    Allows user to initialize a NEAT simulation of different 'flavors'.

    :param neat_flavor: NEAT experiment type; direct v. indirect encoding. Options: 'NEAT', 'HyperNEAT', 'ES-HyperNEAT'.
    :type neat_flavor: string
    
    :param environment_type: Options: 'SimpleEnvironment'. (Default='SimpleEnvironment')
    :type environment_type: string

    :param population_size: number of agents in experiment population. (Default=300)
    :type population_size: int
    
    :param max_evaluations: number of maximum evaluations an agent can have with the environment. (Default=5)
    :type max_evaluations: int
    
    :param num_generations: number of generations of evolution in experiment. (Default=100)
    :type num_generations: int
    
    :param num_repetitions: number of times entire experiment is replicated in a simulation. (Default=1)
    :type num_repetitions: int
    
    :param verbose: option for Generation and Repetition print strings during a simulation. (Default=True)
    :type verbose: bool
    
    :param performance_plotting: option to generate performance plots across simulation. (Default=False)
    :type performance_plotting: bool
    
    :param visualize_leader: option to build a visualization of leading agent in NetworkX. (Default=False)
    :type visualize_leader: bool
    
    """

    # def __init__(self, neat_flavor='NEAT', environment_type='SimpleEnvironment',
    #              population_size=300, max_evaluations=5, num_generations=100,
    #              num_repetitions=1, verbose=True, performance_plotting=False,
    #              visualize_leader=False):

    def __init__(self, parameters):

        # # -------------------- CONSTANTS --------------------
        #
        # # Load and read from a constants file for experiment reproduction
        #
        # self.params = params


        self.neat_flavor = parameters['neat_flavor']
        self.env_type = parameters['environment_type']
        self.population_size = parameters['population_size']
        self.max_evaluations = parameters['max_evaluations']
        self.num_generations = parameters['num_generations']
        self.num_repetitions = parameters['num_repetitions']
        self.verbose = parameters['verbose']
        self.performance_plotting = parameters['performance_plotting']
        self.visualize_leader = parameters['visualize_leader']

        # # -------------------- ENVIRONMENT --------------------
        #
        # # Construct the environment the population will be evaluated on
        #
        # self.env_type = environment_type
        self.env = self.construct_environment()
        #
        # # -------------------- SIMULATION --------------------
        #
        # # Population parameters
        #
        self.num_inputs = self.env.observation_space
        self.num_outputs = self.env.action_space
        # self.population_size = population_size
        #
        # # Simulation parameters
        #
        # self.max_evaluations = max_evaluations
        # self.num_generations = num_generations
        # self.num_repetitions = num_repetitions
        #
        # # Repetition and Generation verbose
        #
        # self.verbose = verbose
        #
        # # Performance Plotting
        #
        # self.performance_plotting = performance_plotting
        #
        # # Visualizing Leader Agent Networks at End of Simulation
        #
        # self.visualizeLeader = visualize_leader
        #
        # # -------------------- ALGORITHM --------------------
        #
        # # Define the type of experiment (flavor) you are running
        #
        # self.NEAT_flavor = neat_flavor
        #
        # # Define the algorithm to fit that flavor
        #
        self.alg = self.construct_neat_flavor()

    def build_phenotype(self, current_genome):

        """
        Constructs an agent phenotype from its genotype.
        
        :param current_genome: agent genome.
        :return: agent phenotype network.
        """

        net = mneat.NeuralNetwork()
        current_genome.BuildPhenotype(net)

        return net

    def construct_environment(self):

        """
        Construct an Environment object from environment_type string.
        
        :return: Environment object instance. 
        """

        return getattr(environment_simple, self.env_type)()

    def construct_neat_flavor(self):

        """
        Construct NEAT Algorithm object from neat_flavor string.
        
        :return: NEAT Algorithm object instance.
        """

        return getattr(neat, self.neat_flavor)(self.population_size, self.num_inputs, self.num_outputs)

    def evaluate_agent(self, current_genome):

        """
        Evaluate a single agent phenotype on the current environment.
        
        :param current_genome: current agent genome
        :return: performance measure
        """

        # -------------------- ENVIRONMENT --------------------

        # Reset environment and retrieve initial observation

        observation = self.env.reset()
        current_input = np.append(np.random.rand(self.num_inputs - 1,), [1.0])  # DUMMY INPUT

        # -------------------- AGENT --------------------

        # Build the agent phenotype

        net = self.build_phenotype(current_genome)

        # -------------------- EVALUATE AGENT --------------------

        # Initialize evaluation loop variables

        collide, evaluation, fitness = False, 0, 0

        # Main Evaluation Loop

        while (not collide) and (evaluation < self.max_evaluations):

            # Single evaluation on current input

            output = self.alg.single_evaluation(net, current_input)

            # Convert network output into relevant action in the environment

            action = self.env.reformat_action(output)

            # Return resulting observation, state and collide catch

            observation, state, collide = self.env.step(action)

            # Performance Update

            fitness += state

            # Evaluation Loop Step

            evaluation += 1

        return fitness

    def run(self):

        """
        Main simulation function.
        """

        # -------------------- MAIN EXPERIMENT --------------------

        # Main Repetition Loop

        for repetition in range(self.num_repetitions):

            if self.verbose:

                print '- Repetition %d:' % (repetition + 1)

            # Main Generation Loop

            for generation in range(self.num_generations):

                if self.verbose:

                    print '     - Generation %d of %d:' % (generation + 1, self.num_generations)

                # Perform a single generation

                self.single_generation()

        # -------------------- LEADER VISUALIZATION --------------------

        if self.visualize_leader:

            if self.verbose:
                'Visualizing Best Performing Agent...'

            VisualizeLeader(self.alg, self.num_inputs, self.num_outputs, self.neat_flavor)

    def single_generation(self):

        """
        Single generation of evaluation for a population on an environment. 
        
        :return: performance measure (i.e. fitness).
        """

        # Retrieve a list of all genomes in the population

        genome_list = mneat.GetGenomeList(self.alg.pop)

        # Main Population Evaluation Loop

        for current_genome in genome_list:

            # Evaluate the current genome

            fitness = self.evaluate_agent(current_genome)

            # Reset the current genome's fitness

            current_genome.SetFitness(fitness)

        # Call a new Epoch - runs mutation and crossover, creating offspring

        self.alg.pop.Epoch()

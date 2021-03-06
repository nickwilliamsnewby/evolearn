
#######################################################
#   ____  _      ___   _     ____   __    ___   _     #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ | #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \| #
#                                                     #
#                  Chad Carlson - 2017                #
#######################################################


from evolearn.controllers.controller_simple import SimpleAgent

import numpy as np


class SimpleEnvironment:

    """
    Simple wrapped callable nutrient environment.

    Todo:
        * Allow for the import of txt file for defining maze/track boundaries.
        * Connect imported boundaries to evaluation loop break collision flag. 
    """

    def __init__(self):

        # -------------------- ENVIRONMENT --------------------

        # Environment parameters
        self.world_size = 100
        self.world = np.zeros((self.world_size, self.world_size))

        self.walls = False
        self.nutrient_rolling_update = False

        # Reward parameters
        self.variable_nutrients = False
        self.nutrient_density = .25

        self.metabolic_cost = -0.2

        self.nutrient_relative_to_cost = 3
        self.nutrient_value = self.nutrient_relative_to_cost * -1 * self.metabolic_cost

        # -------------------- AGENT --------------------

        # Agent parameters
        self.observation_space = 9
        self.action_space = 5

        # Possible actions in environment
        self.actions = self.build_actions()

        # Define Agent object
        self.agent = SimpleAgent(self.world_size)

    def build_actions(self):

        """
        Builds an accessible dictionary of possible actions to be called with each agent action to provide adjustments
        for location and heading adjustments. 
        
        :return: environment action dict. Indices define position and heading adjustments for a selected action.
        """

        # Position adjustments
        empty_position_adjust = [[0, 0], [0, 0], [0, 0], [0, 0]]

        # Position adjustments are different depending on if there is a rolling nutrient update or not

        if self.nutrient_rolling_update:

            # Namely, when the environment 'rolls', the agent can adjust its row, but never its column
            # Is this necessary? couldn't I just have the agent continuously move across the field without
            # changing its heading? If not, then this isn't exactly right, since it would also require the
            # generation of new columns that fit the originally specified nutrient density

            straight = [[-1, 0], [0, 0], [1, 0], [0, 0]]
            diagonal_right = [[-1, 0], [1, 0], [1, 0], [-1, 0]]
            diagonal_left = [[-1, 0], [-1, 0], [1, 0], [1, 0]]

        else:

            straight = [[-1, 0], [0, 1], [1, 0], [0, -1]]
            diagonal_right = [[-1, 1], [1, 1], [1, -1], [-1, -1]]
            diagonal_left = [[-1, -1], [-1, 1], [1, 1], [1, -1]]

        # Build possible actions with position and heading changes

        actions = {
            0: {'heading_adjust': 0, 'position_adjust': straight},
            1: {'heading_adjust': 0, 'position_adjust': diagonal_right},
            2: {'heading_adjust': 0, 'position_adjust': diagonal_left},
            3: {'heading_adjust': -1, 'position_adjust': empty_position_adjust},
            4: {'heading_adjust': 1, 'position_adjust': empty_position_adjust}
        }

        return actions

    def collision_check(self):

        """
        Collision check to potentially break current agent's evaluation.

        :return: collide Boolean 
        """

        collide = False

        if self.walls:

            if self.world[self.agent.location[0], self.agent.location[1]] > self.nutrient_value:

                collide = True

        return collide

    def initialize_environment(self):

        """
        Initialize environment.
        
        :return: initialized world
        """

        # Define a world with a certain nutrient density

        world = np.random.rand(self.world_size, self.world_size)
        world[world > self.nutrient_density] = 0

        # Inlcude positive rewards

        # Accomodate for variable nutrient values

        if self.variable_nutrients:

            world = self.nutrient_value * ( world / self.nutrient_density )  # normalize for density (and maximum values)

        else:

            world[world > 0] = self.nutrient_value

        # Include negative rewards

        world[world == 0] = self.metabolic_cost

        return world

    def make_observation(self):
        #######################
        """
        Making an observation for a single step through environment.
        """

        return 0

    def move_agent(self, action):
        #######################
        """
        Update agent location based on selected action.
        """
        pass

    def reformat_action(self, agent_output):

        """
        Reformat raw network output into environment-specific (or experiment specified) action/class choice.

        :return: reformatted action/class index
        """
        action = agent_output.index(max(agent_output))

        return action

    def reset(self):

        """
        Complete environment reset.

        :return: intial environment observation
        """

        # Re-initialize world

        self.world = self.initialize_environment()

        # Initialize your agent

        self.agent.reset()

        # Return an initial observation at the agent's current location

        init_observation = self.make_observation()

        return init_observation

    def return_reward(self):

        """
        Returns reward for agent's current location.

        :return: reward/state at agent.location 
        """

        return self.world[self.agent.location[0], self.agent.location[1]]

    def step(self, action):

        """
        Making a single step through the environment. 
        
        :return: next observation, current reward, collision Boolean.
        """

        self.update(action)

        observation = self.make_observation()

        state = self.return_reward()

        collide = self.collision_check()

        return observation, state, collide

    def update(self, action):

        """
        Update environment.world with respect possibly consumed nutrients at agent's current location.
        """

        self.world[self.agent.location[0], self.agent.location[1]] = self.metabolic_cost


class Recognition:
    """
    General image recognition object.
    """

    def __init__(self):
        pass

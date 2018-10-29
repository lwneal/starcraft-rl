import os
import random
import numpy as np
from pysc2_util import register_map
from pysc2.env import sc2_env
from pysc2.lib import actions

MAP_NAME = 'SimpleTowers'
MAP_SIZE = 64
RGB_SCREEN_SIZE = 256

# A simple environment similar to SCAII-RTS Towers
# Follows the interface of OpenAI Gym environments
class SimpleTowersEnvironment():
    def __init__(self):
        self.sc2env = make_sc2env()

    def reset(self):
        # Move the camera in any direction
        # This runs the ResetEpisode trigger built into the map
        action = actions.FUNCTIONS.move_camera([0, 0])
        self.last_timestep = self.sc2env.step([action])[0]

        state, reward, done, info = unpack_timestep(self.last_timestep)
        return state

    # Action space: Choose which of four enemies to attack
    def action_space(self):
        from gym.spaces.discrete import Discrete
        return Discrete(4)

    # Step: Choose which enemy to attack
    def step(self, action):
        if self.can_attack():
            target = action_to_target(action)
            sc2_action = actions.FUNCTIONS.Attack_minimap("now", target)
            self.last_timestep = self.sc2env.step([sc2_action])[0]
        else:
            print('Cannot attack, taking no-op')

        # Wait for a while
        self.noop()

        return unpack_timestep(self.last_timestep)

    def noop(self):
        sc2_action = actions.FUNCTIONS.no_op()
        self.last_timestep = self.sc2env.step([sc2_action])[0]

    def can_attack(self):
        available_actions = self.last_timestep.observation.available_actions
        return actions.FUNCTIONS.Attack_minimap.id in available_actions


# The four actions tell the army to move to
# one of the four corners of the map
def action_to_target(action_id):
    x = random.random()
    map_size = MAP_SIZE
    padding = MAP_SIZE / 4
    if action_id == 0:
        return [padding + x, padding + x]
    elif action_id == 1:
        return [map_size - padding - x, padding + x]
    elif action_id == 2:
        return [map_size - padding - x, map_size - padding - x]
    elif action_id == 3:
        return [padding + x, map_size - padding - x]


# Create the low-level SC2Env object, which we wrap with
#  a high level Gym-style environment
def make_sc2env():
    env_args = {
        'agent_interface_format': sc2_env.AgentInterfaceFormat(
            feature_dimensions=sc2_env.Dimensions(
                screen=(MAP_SIZE, MAP_SIZE),
                minimap=(MAP_SIZE, MAP_SIZE)
            ),
            rgb_dimensions=sc2_env.Dimensions(
                screen=(RGB_SCREEN_SIZE, RGB_SCREEN_SIZE),
                minimap=(RGB_SCREEN_SIZE, RGB_SCREEN_SIZE),
            ),
            action_space=actions.ActionSpace.FEATURES,
        ),
        'map_name': MAP_NAME,
        'step_mul': 170,  # 17 is ~1 action per second
    }
    maps_dir = os.path.join(os.path.dirname(__file__), '..', 'maps')
    register_map(maps_dir, env_args['map_name'])
    return sc2_env.SC2Env(**env_args)


# Convert the SC2Env timestep into a Gym-style tuple
def unpack_timestep(timestep):
    feature_map = np.array(timestep.observation.feature_minimap)
    feature_screen = np.array(timestep.observation.feature_screen)
    rgb_map = np.array(timestep.observation.get('rgb_minimap'))
    rgb_screen = np.array(timestep.observation.get('rgb_screen'))
    state = (feature_map, feature_screen, rgb_map, rgb_screen)

    # See other maps to learn about custom specified rewards
    reward = int(timestep.observation.player['army_count'])

    done = timestep.last()

    # The info dict can include reward decompositions when available
    info = {}
    return state, reward, done, info

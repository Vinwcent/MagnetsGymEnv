import numpy as np
import gymnasium as gym

import gymnasium.spaces as spaces

from sim.SimManager import SimManager



class SimMagnetEnv(gym.Env):
    def __init__(self, map_size, phy_dt, with_render):
        """
        Gym environment for the magnet simulation

        :param map_size list[int]: The size of the simulation (!= screen_size)
        :param phy_dt float: The time step of the simulation
        :param with_render bool: Activate the rendering of the simulation or not
        to save computations
        """
        self.phy_dt = phy_dt
        self.with_render = with_render
        self.map_size = map_size

        self.observation_space = spaces.Box(low=-250,
                                            high=800,
                                            shape=(6,),
                                            dtype=float)
        # Dummy sim_manager to compute the number of magnets
        self.sim_manager = SimManager(self.map_size,
                                      [0, 0],
                                      self.with_render)
        n_magnets = self.sim_manager.get_n_magnets()
        self.action_space = spaces.Box(low=0,
                                       high=1,
                                       shape=(n_magnets,),
                                       dtype=int)

        self.n_step = 0
        self.max_steps = 500

        self.valid_steps = 0
        self.valid_steps_threshold = 30
        self.valid_dist = 30

        self.static_ball_pos = np.array([0, 0])
        self.penalty_steps = 0;
        self.penalty_steps_threshold = 10;
        self.penalty_dist = 75;

    def reset(self, seed=None, options=None): # pyright: ignore
        """
        Reset the environment

        :param seed int: The seed used to reset (unused)
        """
        new_target_pos = np.random.rand(2) * self.map_size
        new_target_pos = list(new_target_pos)

        self.sim_manager = SimManager(self.map_size,
                                      new_target_pos,
                                      self.with_render)
        self.sim_manager.reset_sim()
        ball_pos = self.sim_manager.get_ball_pos_sim()
        ball_speed = self.sim_manager.get_ball_speed()
        target_pos = self.sim_manager.get_target_pos()



        state = np.concatenate([ball_pos, ball_speed, target_pos])

        self.n_step = 0
        self.valid_steps = 0


        return state, {}


    def step(self, action):
        """
        Step function to perform a step in the markov process of our environment

        :param action list[bool]: Activities to set for our magnets
        """
        self.n_step += 1

        self.sim_manager.set_magnets_activity_sim(action)
        self.sim_manager.update_physic(self.phy_dt)
        self.sim_manager.try_render_sim()

        ball_pos = self.sim_manager.get_ball_pos_sim()
        ball_speed = self.sim_manager.get_ball_speed()
        target_pos = np.array(self.sim_manager.get_target_pos().copy())
        delta_pos = np.abs(target_pos - ball_pos)

        self._update_valid_step(delta_pos)
        self._update_penalty_step(ball_pos)

        terminated = self.valid_steps >= self.valid_steps_threshold

        truncated = self.n_step >= self.max_steps

        reward = self._compute_reward(target_pos, ball_pos)

        state = np.concatenate([ball_pos, ball_speed, target_pos])

        return state, reward, terminated, truncated, {}


    def _update_penalty_step(self, ball_pos):
        """
        This is a function used to add a reward penalty if the algorithm stays
        too long on the same position.
        This is used to prevent the algorithm from just learning to stay on the
        magnet that is the nearest of our target position

        :param ball_pos list[int]: The current position of the ball
        """
        delta_pos_step = np.abs(ball_pos - self.static_ball_pos)
        if (np.linalg.norm(delta_pos_step) < self.penalty_dist and
                self.valid_steps == 0):
            self.penalty_steps += 1
        else:
            self.static_ball_pos = ball_pos
            self.penalty_steps = 0


    def _update_valid_step(self, delta_pos):
        """
        Function used to check if we are near enough from the target position to
        consider that we reached the goal

        :param delta_pos list[int]: Delta of position between the current ball
        position and the target position
        """
        if np.linalg.norm(delta_pos) < self.valid_dist:
            self.valid_steps += 1
        else:
            self.valid_steps = 0


    def _compute_reward(self, target_pos, ball_pos):
        """
        Compute the reward and add a penalty if the algorithm just stays on a
        specific position

        :param target_pos list[int]: The goal position
        :param ball_pos list[int]: The current ball position
        """
        reward = -np.linalg.norm(target_pos - ball_pos)

        if self.penalty_steps > self.penalty_steps_threshold:
            reward *= 2

        return reward

    def render(self, mode="human"): # pyright: ignore return
        """
        Unused due to some bugs with ray

        :param mode None: None
        """
        return

    def close(self):
        return








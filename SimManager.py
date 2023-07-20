import numpy as np

from sim.RenderingManager import RenderingManager
from sim.Simlogic import SimLogic

class SimManager:
    def __init__(self,
                 map_size,
                 target_pos,
                 with_render):
        """
        The manager of our simulation which handles and sync the logic and the
        rendering part

        :param map_size list[int]: The size of the container where the
        simulation takes place
        :param target_pos list[int]: The goal position for this sim
        :param with_render bool: Activate the rendering part or not to save
        computation resources
        """
        self.logic_map_size = map_size
        self.screen_size = np.array(map_size) / 0.8;
        self.with_render = with_render
        self.target_pos = target_pos

        self.n_magnets = 4

        self._init_sim()

    def _init_sim(self):
        """
        Function used to init the logic and the rendering at construction
        """
        log_mag_positions = np.array([
            [self.logic_map_size[0]/4, self.logic_map_size[1]/4],
            [self.logic_map_size[0]/4, 3*self.logic_map_size[1]/4],
            [3*self.logic_map_size[0]/4, self.logic_map_size[1]/4],
            [3*self.logic_map_size[0]/4, 3*self.logic_map_size[1]/4]
        ])
        self.logic = SimLogic(self.logic_map_size,
                              log_mag_positions)
        render_mag_positions = log_mag_positions + self.screen_size * 0.1

        if self.with_render:
            self.render = RenderingManager(
                self.screen_size,
                render_mag_positions,
                self._convert_logic2render(self.target_pos)
            )

    def _convert_logic2render(self, position):
        """
        Simple function used to convert logic coord to render coord

        :param position list[int]: The logic position
        """
        new_position = position + 0.1 * self.screen_size;
        return new_position

    def reset_sim(self):
        """
        Function used to reset the logic
        """
        self.logic.set_magnets_activity_logic(np.zeros(4,))
        self.logic.reset_ball_pos()

    def try_render_sim(self):
        """
        Function that checks if rendering is activated and render if it is
        """
        if not self.with_render:
            return
        logic_ball_pos = self.logic.get_ball_pos()
        render_ball_pos = self._convert_logic2render(logic_ball_pos)

        self.render.update_ball_pos_render(render_ball_pos)
        self.render.render()

    def update_physic(self, phy_dt):
        """
        Wrapping function to update the physic logic

        :param phy_dt float: physic time step
        """
        self.logic.update_phy_ball(phy_dt)

    def set_magnets_activity_sim(self, activities):
        """
        Setter of the magnets activity in the simulation

        :param activities list[bool]: List of activities to set
        """
        self.logic.set_magnets_activity_logic(activities)

        if self.with_render:
            self.render.update_magnets_activities_render(activities)

    def get_n_magnets(self):
        """
        Getter for the amount of magnets
        """
        return self.n_magnets

    def get_ball_pos_sim(self):
        """
        Getter for the ball position
        """
        return self.logic.get_ball_pos()

    def get_ball_speed(self):
        """
        Getter for the ball speed
        """
        return self.logic.get_ball_speed()

    def get_target_pos(self):
        """
        Getter for the target position
        """
        return self.target_pos

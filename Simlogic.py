import numpy as np


class SimMagnet():
    def __init__(self, position):
        """
        Single magnet class used by the logic to simulatea single magnetic field
        with the Biot-Savart law

        :param position list[int]: The position of the magnet in the logic
        """
        self.position = np.array(position)
        # The magnet strength in Newton, the doc says 250N in real but it seems
        # to be between 150/250 in the comments of the amazon page
        # Need to measure it when every magnets will be there to have a good
        # approximate
        self.max_magnet_strength = 150
        self.unit_strength = self.max_magnet_strength * 90 ** 2

        self.activated = False

    def get_mag_strength(self, ball_pos):
        """
        Getter function used to calculate the strength created on the ball by
        this magnet

        :param ball_pos list[int]: The current position of the ball
        """
        if not self.activated:
            return 0
        epsilon = 1e-6
        dist_sgd = self.position - ball_pos
        dist_norm = np.linalg.norm(dist_sgd)
        unit_vector = dist_sgd / (dist_norm + epsilon)

        mag_strength = self.unit_strength * unit_vector / (dist_norm ** 2 + epsilon)

        mag_strength = np.clip(mag_strength,
                               -self.max_magnet_strength,
                               self.max_magnet_strength)


        return mag_strength

    def set_activity(self, activity):
        """
        Setter function of the activity of the magnet

        :param activity bool: active if true else false
        """
        self.activated = activity

class SimLogic():
    def __init__(self, map_size, mag_positions):
        """
        Class that handle the whole logic of the simulation

        :param map_size list[int]: the size where the simulation take place
        (different from the screen_size )
        :param mag_positions np.array: The positions of the magnets
        """
        self.map_size = np.array(map_size)

        self.ball_pos = self.map_size / 2
        self.ball_speed = np.array([0., 0.])

        self.magnets: list[SimMagnet] = [SimMagnet(mag_position)
                                         for mag_position in mag_positions]


    def _get_ball_axlr(self):
        """
        Get the current acceleration of the ball
        """
        friction = 0.1
        axlr = 0;

        for magnet in self.magnets:
            axlr += magnet.get_mag_strength(self.ball_pos)
        axlr -= self.ball_speed * friction

        return axlr

    def _is_inside(self, position):
        """
        Check if the ball is inside the container where the ball should stay,
        this function is used to apply collision in case the ball goes out of
        the simulation container

        :param position list[float]: the position to check
        """
        condition_left = position[0] > 0
        condition_right = position[0] < self.map_size[0]
        condition_down = position[1] > 0
        condition_up = position[1] < self.map_size[1]
        return (condition_up and
                condition_down and
                condition_left and
                condition_right)

    def set_magnets_activity_logic(self, activities):
        """
        Set the activity of every magnets in the simulation

        :param activities list[bool]: activities of each magnet
        """
        for idx, magnet in enumerate(self.magnets):
            magnet.set_activity(activities[idx])


    def get_ball_pos(self):
        """
        Getter function of the ball position
        """
        return self.ball_pos

    def get_ball_speed(self):
        """
        Getter function of the ball speed
        """
        return self.ball_speed

    def reset_ball_pos(self):
        """
        Reset function used by the gym environment to reset the environment
        """
        self.ball_pos = self.map_size/2

    def update_phy_ball(self, dt):
        """
        Main function which updates the whole physic on a dt time step

        :param dt float: The time step of the simulation
        """
        axlr = self._get_ball_axlr()

        self.ball_speed += axlr * dt
        hypo_pos = self.ball_pos + self.ball_speed * dt

        while not self._is_inside(hypo_pos):
            condition_left = hypo_pos[0] > 0
            condition_right = hypo_pos[0] < self.map_size[0]
            condition_down = hypo_pos[1] > 0
            condition_up = hypo_pos[1] < self.map_size[1]
            if not condition_left:
                hypo_pos[0] = abs(hypo_pos[0])
                self.ball_speed[0] *= -1
            if not condition_down:
                hypo_pos[1] = abs(hypo_pos[1])
                self.ball_speed[1] *= -1
            if not condition_right:
                delta_border = hypo_pos[0] - self.map_size[0]
                hypo_pos[0] = self.map_size[0] - delta_border
                self.ball_speed[0] *= -1
            if not condition_up:
                delta_border = hypo_pos[1] - self.map_size[1]
                hypo_pos[1] = self.map_size[1] - delta_border
                self.ball_speed[1] *= -1

        self.ball_pos = hypo_pos

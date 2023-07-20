import numpy as np
import pygame as pg
import pygame.sprite as sprite


class EntitiesSprite(sprite.Sprite):
    def __init__(self, screen_size, mag_positions, target_pos):
        """
        Create an EntitiesSprite which manage how entities are rendered
        (entities are magnets and balls here)

        :param screen_size list[int]: (width, height)
        :param mag_positions np.array: Positions of the magnets on the screen
        :param target_pos list[int]: The position to go on the screen
        """
        super(EntitiesSprite, self).__init__()
        self.screen_size = screen_size
        self.surf = pg.Surface((screen_size[0],
                                screen_size[1]))
        self.rect = [0, 0]
        self.ball_pos = [0, 0]

        self.mag_positions = mag_positions
        self.activities = np.zeros(mag_positions.shape[0])

        self.ball_radius = 0.02 * screen_size[0]

        self.target_pos = target_pos


    def _fill_bg(self):
        """
        Function to fill the background of where the ball can move
        """
        ball_surf = pg.Surface((0.8 * self.screen_size[0],
                                 0.8 * self.screen_size[1]))
        ball_surf.fill((100, 100, 100))
        position = [0.1 * self.screen_size[0],
                    0.1 * self.screen_size[1]]
        self.surf.blit(ball_surf, position)

    def _draw_ball(self):
        """
        Draw the ball at the member ball position
        """
        ball_size = np.array([2 * self.ball_radius, 2 * self.ball_radius])
        ball_surf = pg.Surface(list(ball_size))
        ball_surf.set_colorkey((10, 10, 10))
        ball_surf.fill((10, 10, 10))
        pg.draw.circle(ball_surf,
                       (255, 255, 255),
                       list(ball_size/2),
                       self.ball_radius,
                       0)


        self.surf.blit(ball_surf, self.ball_pos - self.ball_radius)


    def _draw_target(self):
        """
        Draw the target position at the member target position
        """
        ball_size = np.array([2 * self.ball_radius, 2 * self.ball_radius])
        ball_surf = pg.Surface(list(ball_size))
        ball_surf.set_colorkey((10, 10, 10))
        ball_surf.fill((10, 10, 10))
        pg.draw.circle(ball_surf,
                       (255, 0, 0),
                       list(ball_size/2),
                       self.ball_radius,
                       0)


        self.surf.blit(ball_surf, self.target_pos - self.ball_radius)

    def update_ball_pos(self, ball_pos):
        """
        Setter for the ball position

        :param ball_pos list[int]: The new ball position
        """
        self.ball_pos = ball_pos

    def update_magnets_activities_entities(self, activities):
        self.activities = activities


    def _draw_magnets(self):
        """
        Draw the magnets with the array of mag positions
        """
        for idx, mag_pos in enumerate(self.mag_positions):
            mag_size = np.array([0.40 * self.screen_size[0],
                                 0.40 * self.screen_size[0]])
            mag_surf = pg.Surface(list(mag_size))
            mag_surf.set_colorkey((10, 10, 10))
            mag_surf.fill((10, 10, 10))
            pg.draw.circle(mag_surf, 
                           (170, 170, 170),
                           list(mag_size/2),
                           mag_size[0]/2,
                           0)
            pg.draw.circle(mag_surf, 
                           (0, 0, 0),
                           list(mag_size/2),
                           mag_size[0]/2 - 10,
                           0)
            if self.activities[idx]:
                pg.draw.circle(mag_surf,
                               (230, 170, 170),
                               list(mag_size/2),
                               mag_size[0]/4,
                               0)
            else:
                pg.draw.circle(mag_surf,
                               (170, 170, 170),
                               list(mag_size/2),
                               mag_size[0]/4,
                               0)

            self.surf.blit(mag_surf, mag_pos - np.array(mag_size)/2)



    def draw_entities(self):
        """
        Draw every entities managed by the EntitiesSprite
        """
        self.surf.fill((0, 0, 0))
        self._fill_bg()
        self._draw_magnets()
        self._draw_target()
        self._draw_ball()

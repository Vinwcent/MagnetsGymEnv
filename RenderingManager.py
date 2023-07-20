import pygame as pg
import pygame.sprite as sprite

from sim.EntitiesSprite import EntitiesSprite

class RenderingManager():
    def __init__(self, screen_size, mag_positions, target_pos):
        """
        Class used to easily manage the rendering part of our simulation

        :param screen_size list[int]: (width, height)
        :param mag_positions np.array: Positions of the magnets on the screen
        :param target_pos list[int]: The position to go on the screen
        """
        self.screen_size = screen_size
        self.display = pg.display

        self.sprites = sprite.Group()

        self._init_screen_and_components(mag_positions, target_pos)

    def update_ball_pos_render(self, ball_pos):
        """
        Update the ball position which is passed to the EntitiesSprite

        :param ball_pos list[int]: The new ball position
        """
        self.entities.update_ball_pos(ball_pos)
        self.entities.draw_entities()

    def update_magnets_activities_render(self, activities):
        """
        Update the activity rendering of the magnets

        :param activities list[bool]: List which tells which magnet is on and
        which if off
        """
        self.entities.update_magnets_activities_entities(activities)
        self.entities.draw_entities()

    def render(self):
        """
        Draw and flip the screen
        """
        self._draw_sprites()
        self._update_screen()


    def _add_sprite(self, sprite):
        """
        Add a sprite to be rendered

        :param sprite Sprite: The new sprite
        """
        self.sprites.add(sprite)

    def _draw_sprites(self):
        """
        Draw every sprites on the current canvas
        """
        for sprite in self.sprites:
            self.screen.blit(sprite.surf, sprite.rect)


    def _update_screen(self):
        """
        Flip swapchain
        """
        self.display.flip()


    def _init_screen_and_components(self, mag_positions, target_pos):
        """
        Function used to init the EntitiesSprite and add the sprites

        :param mag_positions np.array: Positions of the magnets on the screen
        :param target_pos list[int]: The position to go on the screen
        """
        self.screen = self.display.set_mode(size=self.screen_size)
        self.screen.fill((0, 0, 0))
        self.entities = EntitiesSprite(
            self.screen_size,
            mag_positions,
            target_pos)
        self._add_sprite(self.entities)

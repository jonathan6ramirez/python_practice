import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

## I am on page 272


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        # This is the games resources.
        self.clock = pygame.time.Clock()

        # Initialize the settings object.
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )

        # INFO: This is if you want to set the game to FULLSCREEN
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # This sets the game windows name.
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics,
        # and creat a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Initialize the ship
        self.ship = Ship(self)

        # Initialize a group of bullets.
        self.bullets = pygame.sprite.Group()

        # Initialize a group of aliens.
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Make the play button.
        self.play_button = Button(self, "Play")

        # Set the background color.
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Check for events.
            self._check_events()

            if self.stats.game_active:
                # Update the ships location.
                self.ship.update()

                # Update all the bullets.
                self._update_bullets()

                # Update all the aliens.
                self._update_aliens()

            # Update the screen.
            self._update_screen()

            # Set the windows frame rate to 60
            self.clock.tick(60)

    def _start_game(self):
        """Start the game."""
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _start_new_level(self):
        # Destroy existing bullets and create new fleet.
        # Use the 'empty' method that pygame gives you inside the sprites.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level.
        self.stats.level += 1
        self.sb.prep_level()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""

        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            # Move the ship to the left.
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""

        if event.key == pygame.K_RIGHT:
            # Stop moving the ship to the right.
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            # Stop moving the ship to the left.
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the games settings.
            self.settings.initialize_dynamic_settings()
            self._start_game()

            # Prep all the images for the scoreboard except the high score. prep_high=False
            self.sb.prep_images(prep_high=False)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached and edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""

        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # This next line checks to see if aliens exist.
        if not self.aliens:
            self._start_new_level()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""

        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """Create the fleet of aliens."""

        # Create an alien and keep adding aliens until theres no room left.
        # Spacing between aliens is one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""

        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""

        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets."""

        # Update position of bullets.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for _bullet in self.bullets.copy():
            if _bullet.rect.bottom <= 0:
                self.bullets.remove(_bullet)

        # Call the helper method.
        self._check_bullet_alien_collisions()

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""

        self._check_fleet_edges()
        self.aliens.update()

        # Look for any alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")
            self._ship_hit()

        # Look for any aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""

        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        # Update all the bullets and we put this before the ship so they don't
        # start at the top of the ship.
        for _bullet in self.bullets.sprites():
            _bullet.draw_bullet()

        # Draw the ship on the screen.
        self.ship.blitme()

        # Draw the aliens.
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

import sys

import pygame
from pygame.time import Clock

from asteroid import Asteroid, AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, GroupType
from logger import log_event, log_state
from player import Player, Shot


def main():
	pygame.init()
	screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	delta_clock: Clock = pygame.time.Clock()
	dt: float = 0.0

	updatable: GroupType = pygame.sprite.Group()
	drawable: GroupType = pygame.sprite.Group()
	asteroids: GroupType = pygame.sprite.Group()
	shots: GroupType = pygame.sprite.Group()

	Player.containers = (updatable, drawable)
	Asteroid.containers = (asteroids, updatable, drawable)
	AsteroidField.containers = updatable
	Shot.containers = (shots, updatable, drawable)

	player: Player = Player(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0)
	_field: AsteroidField = AsteroidField()

	while True:
		log_state()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		updatable.update(dt)

		screen.fill("black")

		for sprite in drawable:
			sprite.draw(screen)

		pygame.display.flip()

		dt = delta_clock.tick(60) / 1000.0

		for asteroid in asteroids:
			if player.collides_with(asteroid):
				log_event("player_hit")
				print("Game over!")
				sys.exit()


if __name__ == "__main__":
	main()

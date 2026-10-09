import pygame
from pygame.time import Clock

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state


def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	delta_clock: Clock = pygame.time.Clock()
	dt: float = 0.0

	while True:
		log_state()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		screen.fill("black")
		pygame.display.flip()
		dt = delta_clock.tick(60) / 1000.0


if __name__ == "__main__":
	main()

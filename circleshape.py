from typing import override

import pygame

from constants import GroupType


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
	containers: tuple[GroupType, ...]

	def __init__(self, x: float, y: float, radius: float) -> None:
		# we will be using this later
		if hasattr(self, "containers"):
			super().__init__(*self.containers)
		else:
			super().__init__()

		self.position: pygame.Vector2 = pygame.Vector2(x, y)
		self.velocity = pygame.Vector2(0, 0)
		self.radius = radius

	def collides_with(self, other: CircleShape) -> bool:
		distance: float = self.position.distance_to(other.position)
		collide: float = self.radius + other.radius
		return distance <= collide

	def draw(self, _screen: pygame.Surface) -> None:
		pass

	@override
	def update(self, dt: float) -> None:
		# must override
		pass

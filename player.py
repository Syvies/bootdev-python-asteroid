import pygame

from circleshape import CircleShape
from constants import LINE_WIDTH, PLAYER_RADIUS, PLAYER_SPEED, PLAYER_TURN_SPEED


class Player(CircleShape):
	def __init__(self, x: float, y: float) -> None:
		super().__init__(x, y, PLAYER_RADIUS)
		self.rotation: float = 0.0

	def rotate(self, dt: float) -> None:
		self.rotation += PLAYER_TURN_SPEED * dt

	def move(self, dt: float) -> None:
		forward_movement: pygame.Vector2 = pygame.Vector2(0, 1).rotate(self.rotation)
		forward_movement *= PLAYER_SPEED * dt
		self.position += forward_movement

	def update(self, dt: float) -> None:
		keys = pygame.key.get_pressed()

		if keys[pygame.K_q]:
			self.rotate(-dt)
		if keys[pygame.K_d]:
			self.rotate(dt)
		if keys[pygame.K_z]:
			self.move(dt)
		if keys[pygame.K_s]:
			self.move(-dt)

	# in the Player class
	def triangle(self) -> list[pygame.Vector2]:
		forward: pygame.Vector2 = pygame.Vector2(0, 1).rotate(self.rotation)
		right: pygame.Vector2 = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
		a: pygame.Vector2 = self.position + forward * self.radius
		b: pygame.Vector2 = self.position - forward * self.radius - right
		c: pygame.Vector2 = self.position - forward * self.radius + right
		return [a, b, c]

	def draw(self, screen: pygame.Surface) -> None:
		pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

import random
from collections.abc import Callable
from typing import ClassVar, override

import pygame

from circleshape import CircleShape
from constants import (
	ASTEROID_KINDS,
	ASTEROID_MAX_RADIUS,
	ASTEROID_MIN_RADIUS,
	ASTEROID_SPAWN_RATE_SECONDS,
	LINE_WIDTH,
	SCREEN_HEIGHT,
	SCREEN_WIDTH,
	GroupType,
)
from logger import log_event

Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]


class Asteroid(CircleShape):
	def __init__(self, x: float, y: float, radius: float) -> None:
		super().__init__(x, y, radius)

	def split(self) -> None:
		self.kill()
		if self.radius <= ASTEROID_MIN_RADIUS:
			return
		log_event("asteroid_split")
		new_radius: float = self.radius - ASTEROID_MIN_RADIUS
		angle: float = random.uniform(20.0, 50.0)
		vel_1: pygame.Vector2 = self.velocity.rotate(angle)
		vel_2: pygame.Vector2 = self.velocity.rotate(-angle)
		asteroid_1: Asteroid = Asteroid(self.position.x, self.position.y, new_radius)
		asteroid_2: Asteroid = Asteroid(self.position.x, self.position.y, new_radius)
		asteroid_1.velocity = vel_1 * 1.2
		asteroid_2.velocity = vel_2 * 1.2

	@override
	def update(self, dt: float) -> None:
		self.position += self.velocity * dt

	@override
	def draw(self, screen: pygame.Surface) -> None:
		pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)


class AsteroidField(pygame.sprite.Sprite):
	containers: GroupType

	edges: ClassVar[list[Edge]] = [
		(
			pygame.Vector2(1, 0),
			lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
		),
		(
			pygame.Vector2(-1, 0),
			lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
		),
		(
			pygame.Vector2(0, 1),
			lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
		),
		(
			pygame.Vector2(0, -1),
			lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS),
		),
	]

	def __init__(self) -> None:
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.spawn_timer = 0.0

	def spawn(self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2) -> None:
		asteroid = Asteroid(position.x, position.y, radius)
		asteroid.velocity = velocity

	@override
	def update(self, dt: float) -> None:
		self.spawn_timer += dt
		if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
			self.spawn_timer = 0

			# spawn a new asteroid at a random edge
			edge = random.choice(self.edges)
			speed = random.randint(40, 100)
			velocity = edge[0] * speed
			velocity = velocity.rotate(random.randint(-30, 30))
			position = edge[1](random.uniform(0, 1))
			kind = random.randint(1, ASTEROID_KINDS)
			self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)

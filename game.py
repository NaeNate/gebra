import pygame
import random
import math
import time

pygame.init()

width, height, padding = 600, 800, 50
screen = pygame.display.set_mode((width, height))
font = pygame.font.Font(pygame.font.get_default_font(), 24)

clock = pygame.time.Clock()

speed = 3
gravity = .1

score = 1

radius = 10

running = True

delay = 0.1
last_launch = 0

class Ball:
  def __init__(self, angle):
    self.x = width / 2
    self.y = padding + 20
    self.vx = speed * math.cos(angle)
    self.vy = speed * math.sin(angle)

  def draw(self):
    pygame.draw.circle(screen, "white", (self.x, self.y), radius)
  
  def update(self):
    self.vy += gravity
    self.x += self.vx
    self.y += self.vy

    if self.x < padding + radius or self.x > width - padding - radius:
      self.vx *= -1

class Shape:
  def __init__(self):
    self.x = random.randint(padding, width - padding)
    self.y = height - padding * 2
    self.health = 1 + random.randint(int(score / 2), score * 2)
    self.type = random.choice(["square", "circle"])
  
  def draw(self):
    if self.type == "square":
      pygame.draw.rect(screen, "red", (self.x, self.y, 50, 50))
    elif self.type == "circle":
      pygame.draw.circle(screen, "blue", (self.x, self.y), 25)
    
    screen.blit(font.render(str(self.health), True, "white"), (self.x, self.y))
  
  def is_colliding(self, ball):
    if self.type == "square":
      closest_x = max(self.x, min(ball.x, self.x + 50))
      closest_y = max(self.y, min(ball.y, self.y + 50))

      distance_x = ball.x - closest_x
      distance_y = ball.y - closest_y

      return (distance_x ** 2) + (distance_y ** 2) < (radius ** 2)
    elif self.type == "circle":
      dx = ball.x - self.x
      dy = ball.y - self.y

      return math.hypot(dx, dy) < radius + 25
  
  def collision_response(self, ball):
    if self.type == "square":
      dx = ball.x - (self.x + 25)
      dy = ball.y - (self.y + 25)

      if abs(dx) > abs(dy):
        ball.vx *= -1
      else:
        ball.vy *= -1

    elif self.type == "circle":
      dx = ball.x - self.x
      dy = ball.y - self.y
      dist = math.hypot(dx, dy)
      nx = dx / dist
      ny = dy / dist
      dot = ball.vx * nx + ball.vy * ny
      ball.vx -= 2 * dot * nx
      ball.vy -= 2 * dot * ny


shapes = [Shape() for _ in range(5)]
queue = []
balls = []

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if (len(balls) == 0):
        x, y = pygame.mouse.get_pos()
        angle = math.atan2(y - padding + 20, x - width / 2)
        
        for _ in range(score):
          queue.append(Ball(angle))

  screen.fill("black")

  pygame.draw.rect(screen, "grey", (padding, padding, width - padding * 2, height - padding * 2), 3, 3)
  screen.blit(font.render(str(score - 1), True, "white"), (10, 10))

  if len(queue) > 0 and time.time() - last_launch > delay:
    balls.append(queue.pop(0))
    last_launch = time.time()

  for shape in shapes:
    shape.draw()
  
  for ball in balls:
    if ball.y > height - padding:
      balls.remove(ball)

      if len(balls) == 0 and len(queue) == 0:
        score += 1

        for shape in shapes:
          shape.y -= 70

        for _ in range(5):
          shapes.append(Shape())
    
    for shape in shapes:
      if shape.is_colliding(ball):
        shape.collision_response(ball)
        shape.health -= 1

        if shape.health == 0:
          shapes.remove(shape)
    
    ball.update()
    ball.draw()

  pygame.display.flip()
  clock.tick(120)

pygame.quit()
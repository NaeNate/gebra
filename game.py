import pygame
import random
import math
import time

pygame.init()

width, height, padding = 600, 800, 50
screen = pygame.display.set_mode((width, height))
font = pygame.font.Font(pygame.font.get_default_font(), 24)

clock = pygame.time.Clock()

speed = 5
gravity = .5

score = 0

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
    self.health = 50
    self.type = random.choice(["square"])
  
  def draw(self):
    if self.type == "square":
      pygame.draw.rect(screen, "red", (self.x, self.y, 50, 50))
    
    screen.blit(font.render(str(self.health), True, "white"), (self.x, self.y))
  
  def is_colliding(self, ball):
    # return (self.x + radius < ball.x < self.x + 50 + radius) and (self.y + radius < ball.y < self.y + 50 + radius)

    if self.x - radius < ball.x < self.x + 50 + radius:
        if self.y < ball.y < self.y + 50:
            return 'horizontal'

    if self.y - radius < ball.y < self.y + 50 + radius:
        if self.x < ball.x < self.x + 50:
            return 'vertical'

    return None

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
        
        for _ in range(score + 1):
          queue.append(Ball(angle))

  screen.fill("black")

  pygame.draw.rect(screen, "grey", (padding, padding, width - padding * 2, height - padding * 2), 3, 3)
  screen.blit(font.render(str(score), True, "white"), (10, 10))

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
          shape.y -= 50

        for _ in range(5):
          shapes.append(Shape())
    
    for shape in shapes:
      collision = shape.is_colliding(ball)

      if collision:
        shape.health -= 1
        if collision == 'vertical':
            ball.vy *= -1
        elif collision == 'horizontal':
            ball.vx *= -1

        if shape.health == 0:
          shapes.remove(shape)
    
    ball.update()
    ball.draw()

  pygame.display.flip()
  clock.tick(60)

pygame.quit()
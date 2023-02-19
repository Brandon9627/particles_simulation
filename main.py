import pygame
import random
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the width and height of the screen [width, height]
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

# Set the number of circles to simulate
NUM_CIRCLES = 45
RADIUS = 5
# Set the gravitational constant
G = 1


class Circle:
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.RADIUS = radius
        self.color = color
        self.mass = mass
        self.vx = 0
        self.vy = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.RADIUS)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        # # Bounce off edges
        # Bounce off edges
        if self.x < self.RADIUS:
            self.x = self.RADIUS
            self.vx *= -1
        elif self.x > SCREEN_WIDTH - self.RADIUS:
            self.x = SCREEN_WIDTH - self.RADIUS
            self.vx *= -1
        if self.y < self.RADIUS:
            self.y = self.RADIUS
            self.vy *= -1
        elif self.y > SCREEN_HEIGHT - self.RADIUS:
            self.y = SCREEN_HEIGHT - self.RADIUS
            self.vy *= -1

    def apply_gravity(self, other_circles, dt):
        for other in other_circles:
            if other is not self:
                dx = other.x - self.x
                dy = other.y - self.y
                dist = math.sqrt(dx ** 2 + dy ** 2)
                force = G * self.mass * other.mass / dist ** 2
                angle = math.atan2(dy, dx)
                self.vx += math.cos(angle) * force / self.mass * dt
                self.vy += math.sin(angle) * force / self.mass * dt

    def handle_collision(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist <= self.RADIUS + other.RADIUS:
            overlap = 0.2 * (dist - self.RADIUS - other.RADIUS + 1)
            self.x -= overlap * (self.x - other.x) / dist
            self.y -= overlap * (self.y - other.y) / dist
            other.x += overlap * (self.x - other.x) / dist
            other.y += overlap * (self.y - other.y) / dist
            angle = math.atan2(dy, dx)
            self_speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
            other_speed = math.sqrt(other.vx ** 2 + other.vy ** 2)
            self_direction = math.atan2(self.vy, self.vx)
            other_direction = math.atan2(other.vy, other.vx)
            new_self_xspeed = other_speed * math.cos(other_direction - angle)
            new_self_yspeed = other_speed * math.sin(other_direction - angle)
            new_other_xspeed = self_speed * math.cos(self_direction - angle)
            new_other_yspeed = self_speed * math.sin(self_direction - angle)
            self.vx = new_self_xspeed
            self.vy = new_self_yspeed
            other.vx = new_other_xspeed
            other.vy = new_other_yspeed



# Initialize pygame
pygame.init()

# Set the size of the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption("Circle Simulation")

# Create a list of circles
circles = []
for i in range(NUM_CIRCLES):
    x = random.randint(RADIUS, SCREEN_WIDTH - RADIUS)
    y = random.randint(RADIUS, SCREEN_HEIGHT - RADIUS)

    color = (0, random.randint(0, 10)*25, 255)
    mass = RADIUS ** 2
    circle = Circle(x, y, RADIUS, color, mass)
    circles.append(circle)

# Set up the clock
clock = pygame.time.Clock()

# Start the simulation loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Clear the screen
    screen.fill(BLACK)

    # Apply gravity to all circles
    for circle in circles:
        circle.apply_gravity(circles, 0.1)

    # Update the position of all circles
    for circle in circles:
        circle.update(0.8)

    # Handle collisions between circles
    for i in range(len(circles)):
        for j in range(i+1, len(circles)):
            circles[i].handle_collision(circles[j])

    # Draw all circles to the screen
    for circle in circles:
        circle.draw(screen)

    # Draw the frame rate to the screen
    font = pygame.font.Font(None, 36)
    text = font.render("FPS: " + str(int(clock.get_fps())), 1, WHITE)
    screen.blit(text, (10, 10))

    # Update the screen
    pygame.display.update()

    # Limit the frame rate
    clock.tick(100)

# Quit pygame
pygame.quit()
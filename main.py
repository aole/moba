import pygame
import math

class Minion:
    def __init__(self, x, y, size=40):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = (0, 255, 0)  # Green

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Projectile:
    def __init__(self, pos, target_pos):
        self.pos = pygame.math.Vector2(pos)
        self.speed = 5
        direction = pygame.math.Vector2(target_pos) - self.pos
        if direction.length() > 0:
            direction.normalize_ip()
        self.velocity = direction * self.speed
        self.rect = pygame.Rect(self.pos.x - 5, self.pos.y - 5, 10, 10)
        self.color = (255, 0, 0) # Red

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, 5)


from champion import Champion

def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("MOBA Game")

    player = Champion(screen_width // 2, screen_height // 2)
    projectiles = []
    minions = [Minion(100, 100), Minion(700, 100), Minion(100, 500), Minion(700, 500)]

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right-click
                player.move_to(event.pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                mouse_pos = pygame.mouse.get_pos()
                projectiles.append(Projectile(player.pos, mouse_pos))

        player.update()
        for projectile in projectiles[:]:
            projectile.update()
            if not screen.get_rect().colliderect(projectile.rect):
                projectiles.remove(projectile)
            else:
                for minion in minions[:]:
                    if projectile.rect.colliderect(minion.rect):
                        projectiles.remove(projectile)
                        minions.remove(minion)
                        break

        screen.fill((255, 255, 255))
        player.draw(screen)
        for minion in minions:
            minion.draw(screen)
        for projectile in projectiles:
            projectile.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()

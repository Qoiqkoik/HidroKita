import pygame
import math
import random

class WaterFlow:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.phase = 0.0
        self.bubbles = [
            [random.randint(x + 20, x + width - 20), random.randint(y + 15, y + height - 10), random.uniform(1.5, 3.5)]
            for _ in range(18)
        ]

    def update(self, dt, flow_speed=120.0):
        self.phase += dt * 4.0
        for b in self.bubbles:
            b[0] += flow_speed * dt
            b[1] += math.sin(self.phase + b[0] * 0.05) * 0.4
            if b[0] > self.rect.right - 15:
                b[0] = self.rect.left + 15
                b[1] = random.randint(self.rect.top + 15, self.rect.bottom - 10)

    def draw(self, surface, is_healthy=True):
        # Badan pipa PVC bagian belakang
        pygame.draw.rect(surface, (210, 225, 235), self.rect, border_radius=18)

        # Permukaan gelombang air nutrisi
        water_color = (56, 189, 248, 180) if is_healthy else (180, 160, 70, 180)
        water_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        points = []
        water_top = 18
        for px in range(0, self.rect.width + 5, 5):
            wave_y = water_top + math.sin((px * 0.04) + self.phase) * 3.5
            points.append((px, wave_y))
        points.append((self.rect.width, self.rect.height))
        points.append((0, self.rect.height))
        
        pygame.draw.polygon(water_surf, water_color, points)
        surface.blit(water_surf, self.rect.topleft)

        # Gelembung oksigen dalam aliran air
        for b in self.bubbles:
            pygame.draw.circle(surface, (224, 242, 254), (int(b[0]), int(b[1])), int(b[2]))

        # Garis tepi pipa (efek kaca/transparan)
        pygame.draw.rect(surface, (100, 130, 150), self.rect, width=4, border_radius=18)    
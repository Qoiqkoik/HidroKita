import pygame
from graphics.irrigation import IrrigationSystem
from graphics.water_flow import WaterFlow
from graphics.procedural import ProceduralPlant

class SceneGraph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Area pipa NFT utama
        pipe_rect = pygame.Rect(360, 310, 560, 110)
        self.irrigation = IrrigationSystem(pipe_rect)
        self.water_flow = WaterFlow(pipe_rect.x, pipe_rect.y, pipe_rect.width, pipe_rect.height)
        
        # 3 tanaman berjajar di atas pipa NFT
        self.plants = [
            ProceduralPlant(pipe_rect.x + 120, pipe_rect.y),
            ProceduralPlant(pipe_rect.x + 280, pipe_rect.y),
            ProceduralPlant(pipe_rect.x + 440, pipe_rect.y),
        ]

    def update(self, dt, is_pumping=True):
        self.irrigation.update(dt, is_pumping)
        if is_pumping:
            self.water_flow.update(dt)

    def draw(self, surface, stage_idx, health, weather_info):
        # 1. Latar Belakang Langit & Greenhouse
        surface.fill((224, 242, 254))
        
        # Rangka atap greenhouse sederhana
        pygame.draw.line(surface, (186, 230, 253), (280, 120), (640, 40), 4)
        pygame.draw.line(surface, (186, 230, 253), (640, 40), (1000, 120), 4)
        
        # Lantai tanah/paving greenhouse
        pygame.draw.rect(surface, (187, 247, 208), (0, 470, self.width, self.height - 470))
        pygame.draw.line(surface, (134, 239, 172), (0, 470), (self.width, 470), 4)

        # Tiang penyangga meja pipa NFT
        pygame.draw.rect(surface, (100, 116, 139), (410, 420, 14, 110))
        pygame.draw.rect(surface, (100, 116, 139), (860, 420, 14, 110))

        # 2. Gambar Sistem Irigasi & Tandon
        is_healthy = health >= 60
        self.irrigation.draw(surface, is_healthy)

        # 3. Gambar Tanaman & Akar
        for plant in self.plants:
            plant.draw(surface, stage_idx, health)

        # 4. Gambar Pipa & Gelombang Air Nutrisi
        self.water_flow.draw(surface, is_healthy)
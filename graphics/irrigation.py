import pygame

class IrrigationSystem:
    def __init__(self, pipe_rect):
        self.pipe_rect = pipe_rect
        self.tank_rect = pygame.Rect(pipe_rect.left - 90, pipe_rect.bottom + 35, 110, 85)
        self.pump_rect = pygame.Rect(self.tank_rect.centerx - 16, self.tank_rect.bottom - 36, 32, 28)
        self.drop_offset = 0.0

    def update(self, dt, is_pumping=True):
        if is_pumping:
            self.drop_offset = (self.drop_offset + dt * 90) % 24

    def draw(self, surface, is_healthy=True):
        pipe_col = (120, 145, 165)
        water_col = (56, 189, 248) if is_healthy else (180, 160, 70)

        # 1. Pipa Inlet (dari pompa naik ke ujung kiri talang NFT)
        inlet_x = self.pump_rect.centerx
        pygame.draw.line(surface, pipe_col, (inlet_x, self.pump_rect.top), (inlet_x, self.pipe_rect.centery), 8)
        pygame.draw.line(surface, pipe_col, (inlet_x, self.pipe_rect.centery), (self.pipe_rect.left, self.pipe_rect.centery), 8)

        # 2. Pipa Outlet (dari ujung kanan talang NFT kembali ke tandon)
        outlet_x = self.pipe_rect.right - 25
        outlet_y = self.tank_rect.top + 20
        pygame.draw.line(surface, pipe_col, (outlet_x, self.pipe_rect.bottom), (outlet_x, outlet_y), 8)
        pygame.draw.line(surface, pipe_col, (outlet_x, outlet_y), (self.tank_rect.right, outlet_y), 8)

        # Animasi aliran air di pipa vertikal kiri
        for y in range(int(self.pipe_rect.centery), self.pump_rect.top, 24):
            curr_y = y - int(self.drop_offset)
            if self.pipe_rect.centery <= curr_y <= self.pump_rect.top:
                pygame.draw.circle(surface, water_col, (inlet_x, curr_y), 3)

        # 3. Gambar Tandon Nutrisi AB Mix
        pygame.draw.rect(surface, (45, 65, 85), self.tank_rect, border_radius=8)
        water_level = pygame.Rect(
            self.tank_rect.left + 4,
            self.tank_rect.top + 25,
            self.tank_rect.width - 8,
            self.tank_rect.height - 29
        )
        pygame.draw.rect(surface, water_col, water_level, border_bottom_left_radius=6, border_bottom_right_radius=6)
        pygame.draw.rect(surface, (30, 41, 59), self.tank_rect, width=3, border_radius=8)

        # 4. Gambar Pompa Submersible di dalam tandon
        pygame.draw.rect(surface, (239, 68, 68), self.pump_rect, border_radius=4)

        # Label Tandon
        font = pygame.font.SysFont("arial", 13, bold=True)
        lbl = font.render("Tandon AB Mix", True, (30, 41, 59))
        surface.blit(lbl, (self.tank_rect.centerx - lbl.get_width() // 2, self.tank_rect.bottom + 6))
import pygame
import math

class ProceduralPlant:
    def __init__(self, center_x, pipe_top_y):
        self.cx = center_x
        self.pipe_top_y = pipe_top_y

    def draw(self, surface, stage_idx, health):
        # Tentukan warna daun berdasarkan kesehatan tanaman
        if health >= 70:
            leaf_main = (34, 197, 94)
            leaf_dark = (21, 128, 61)
        elif health >= 40:
            leaf_main = (163, 230, 53)
            leaf_dark = (101, 163, 13)
        else:
            leaf_main = (234, 179, 8)   # Menguning / layu
            leaf_dark = (161, 98, 7)

        # 1. Gambar Akar Serabut (muncul mulai tahap 2)
        if stage_idx >= 1:
            root_len = min(85, 15 + stage_idx * 14)
            root_color = (245, 245, 240) if health >= 50 else (160, 130, 90)
            for i in range(-4, 5):
                start = (self.cx + i * 4, self.pipe_top_y + 18)
                mid = (self.cx + i * 8 + math.sin(i) * 5, self.pipe_top_y + 18 + root_len * 0.5)
                end = (self.cx + i * 11, self.pipe_top_y + 18 + root_len)
                pygame.draw.lines(surface, root_color, False, [start, mid, end], 2)

        # 2. Gambar Netpot / Rockwool
        pot_rect = pygame.Rect(self.cx - 24, self.pipe_top_y - 12, 48, 32)
        pygame.draw.polygon(surface, (55, 65, 81), [
            (pot_rect.left, pot_rect.top),
            (pot_rect.right, pot_rect.top),
            (pot_rect.right - 6, pot_rect.bottom),
            (pot_rect.left + 6, pot_rect.bottom)
        ])

        # 3. Gambar Benih / Daun sesuai tahap (0 sampai 5)
        base_y = self.pipe_top_y - 12
        if stage_idx == 0:
            # Benih kecil di atas rockwool
            pygame.draw.ellipse(surface, (180, 130, 70), (self.cx - 6, base_y - 6, 12, 8))
        else:
            # Jumlah dan ukuran daun bertambah tiap tahap
            num_leaves = 2 + stage_idx * 2
            scale = 0.4 + stage_idx * 0.22
            for i in range(num_leaves):
                angle = -140 + (100 / max(1, num_leaves - 1)) * i if num_leaves > 1 else -90
                rad = math.radians(angle)
                length = int(55 * scale)
                width = int(26 * scale)
                
                tip_x = self.cx + math.cos(rad) * length
                tip_y = base_y + math.sin(rad) * length
                
                self._draw_leaf(surface, (self.cx, base_y), (tip_x, tip_y), width, leaf_main, leaf_dark)

    def _draw_leaf(self, surface, start, end, width, color, border_color):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.hypot(dx, dy)
        if length == 0:
            return
        nx, ny = -dy / length, dx / length
        mid_x = (start[0] + end[0]) * 0.55
        mid_y = (start[1] + end[1]) * 0.55

        p1 = start
        p2 = (mid_x + nx * width, mid_y + ny * width)
        p3 = end
        p4 = (mid_x - nx * width, mid_y - ny * width)

        pygame.draw.polygon(surface, color, [p1, p2, p3, p4])
        pygame.draw.polygon(surface, border_color, [p1, p2, p3, p4], 2)
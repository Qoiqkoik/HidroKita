import pygame

class Dashboard:
    def __init__(self):
        self.font_title = pygame.font.SysFont("arial", 18, bold=True)
        self.font_body = pygame.font.SysFont("arial", 14)
        self.font_bold = pygame.font.SysFont("arial", 14, bold=True)
        self.font_small = pygame.font.SysFont("arial", 12, bold=True)

    def draw(self, surface, stages, current_idx, tds, ph, health, score, weather):
        # 1. Header Banner & Skor
        header_rect = pygame.Rect(20, 15, 310, 42)
        pygame.draw.rect(surface, (21, 128, 61), header_rect, border_radius=12)
        pygame.draw.rect(surface, (20, 83, 45), header_rect, width=3, border_radius=12)
        title = self.font_title.render(
            "Visualisasi Pertumbuhan Tanaman Hidroponik",
            True, (255, 255, 255)
        )
        surface.blit(title, (header_rect.x + 18, header_rect.y + 10))

        score_rect = pygame.Rect(830, 15, 150, 42)
        pygame.draw.rect(surface, (30, 41, 59), score_rect, border_radius=12)
        score_txt = self.font_title.render(f"Skor: {score}", True, (250, 204, 21))
        surface.blit(score_txt, (score_rect.x + 25, score_rect.y + 10))

        # 2. Timeline 6 Tahap Pertumbuhan (Top Bar)
        start_x = 310
        for i, stg in enumerate(stages):
            cx = start_x + i * 115
            cy = 98
            is_active = (i == current_idx)
            if i < len(stages) - 1:
                pygame.draw.line(surface, (148, 163, 184), (cx + 22, cy), (cx + 93, cy), 4)

            circle_col = (250, 204, 21) if is_active else (241, 245, 249)
            pygame.draw.circle(surface, circle_col, (cx, cy), 22)
            pygame.draw.circle(surface, (30, 41, 59), (cx, cy), 22, 3)

            num_lbl = self.font_bold.render(str(i + 1), True, (30, 41, 59))
            surface.blit(num_lbl, (cx - num_lbl.get_width() // 2, cy - num_lbl.get_height() // 2))

            short_name = stg["name"].split(". ")[1]
            lbl = self.font_small.render(short_name, True, (30, 41, 59))
            surface.blit(lbl, (cx - lbl.get_width() // 2, cy + 28))

        # 3. Panel Kiri: Informasi tahap pertumbuhan
        panel_rect = pygame.Rect(20, 145, 250, 430)
        pygame.draw.rect(surface, (254, 252, 232), panel_rect, border_radius=14)
        pygame.draw.rect(surface, (161, 98, 7), panel_rect, width=3, border_radius=14)

        stage = stages[current_idx]
        surface.blit(self.font_title.render("Tahap Pertumbuhan", True, (113, 63, 18)), (35, 158))
        surface.blit(
            self.font_bold.render(f"Tahap {current_idx + 1} dari {len(stages)}", True, (30, 41, 59)),
            (35, 190)
        )
        surface.blit(self.font_bold.render(stage["name"], True, (30, 41, 59)), (35, 216))
        surface.blit(self.font_small.render("Deskripsi tahap", True, (71, 85, 105)), (35, 254))
        self._draw_wrapped_text(
            surface, stage["description"], self.font_body, (51, 65, 85),
            35, 274, 215
        )

        surface.blit(self.font_bold.render("Rentang nutrisi acuan", True, (30, 41, 59)), (35, 358))
        surface.blit(
            self.font_small.render(f"TDS: {stage['min_tds']}-{stage['max_tds']} ppm", True, (71, 85, 105)),
            (35, 383)
        )
        surface.blit(
            self.font_small.render(f"pH: {stage['min_ph']}-{stage['max_ph']}", True, (71, 85, 105)),
            (35, 402)
        )

        # Info Cuaca dari CSV
        surface.blit(
            self.font_bold.render(f"Cuaca: {weather['cuaca']} ({weather['suhu_c']}°C)", True, (3, 105, 161)),
            (35, 440)
        )
        surface.blit(
            self.font_small.render(f"Kelembapan: {weather['kelembapan_persen']}%", True, (71, 85, 105)),
            (35, 460)
        )

        # 4. Petunjuk navigasi visualisasi
        tip_rect = pygame.Rect(730, 155, 250, 125)
        pygame.draw.rect(surface, (255, 255, 255), tip_rect, border_radius=12)
        pygame.draw.rect(surface, (148, 163, 184), tip_rect, width=2, border_radius=12)

        tip_title = "Petunjuk visualisasi"
        tip_msg = "Klik tahap pada garis waktu atau gunakan tombol Sebelumnya dan Berikutnya."
        title_col = (3, 105, 161)

        surface.blit(self.font_bold.render(tip_title, True, title_col), (tip_rect.x + 12, tip_rect.y + 10))
        self._draw_wrapped_text(surface, tip_msg, self.font_body, (51, 65, 85), tip_rect.x + 12, tip_rect.y + 34, 226)

    def stage_at_position(self, position, stage_count):
        for index in range(stage_count):
            center_x = 310 + index * 115
            hit_area = pygame.Rect(center_x - 54, 70, 108, 76)
            if hit_area.collidepoint(position):
                return index
        return None

    def _draw_wrapped_text(self, surface, text, font, color, x, y, max_width):
        words = text.split(" ")
        line = ""
        curr_y = y
        for w in words:
            test = line + w + " "
            if font.size(test)[0] <= max_width:
                line = test
            else:
                surface.blit(font.render(line, True, color), (x, curr_y))
                line = w + " "
                curr_y += 18
        if line:
            surface.blit(font.render(line, True, color), (x, curr_y))
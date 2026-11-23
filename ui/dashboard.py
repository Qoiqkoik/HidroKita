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
        title = self.font_title.render("HidroKita: Simulasi NFT", True, (255, 255, 255))
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
            is_done = (i < current_idx)

            if i < len(stages) - 1:
                line_col = (34, 197, 94) if is_done else (148, 163, 184)
                pygame.draw.line(surface, line_col, (cx + 22, cy), (cx + 93, cy), 4)

            circle_col = (250, 204, 21) if is_active else ((34, 197, 94) if is_done else (241, 245, 249))
            pygame.draw.circle(surface, circle_col, (cx, cy), 22)
            pygame.draw.circle(surface, (30, 41, 59), (cx, cy), 22, 3)

            num_lbl = self.font_bold.render(str(i + 1), True, (30, 41, 59))
            surface.blit(num_lbl, (cx - num_lbl.get_width() // 2, cy - num_lbl.get_height() // 2))

            short_name = stg["name"].split(". ")[1]
            lbl = self.font_small.render(short_name, True, (30, 41, 59))
            surface.blit(lbl, (cx - lbl.get_width() // 2, cy + 28))

        # 3. Panel Kiri: Informasi & Kontrol Nutrisi
        panel_rect = pygame.Rect(20, 145, 250, 430)
        pygame.draw.rect(surface, (254, 252, 232), panel_rect, border_radius=14)
        pygame.draw.rect(surface, (161, 98, 7), panel_rect, width=3, border_radius=14)

        stage = stages[current_idx]
        surface.blit(self.font_title.render("Parameter Hidroponik", True, (113, 63, 18)), (35, 158))
        surface.blit(self.font_bold.render(f"Tahap: {stage['name']}", True, (30, 41, 59)), (35, 188))

        # Bar Kesehatan Tanaman
        surface.blit(self.font_bold.render(f"Kesehatan: {int(health)}%", True, (30, 41, 59)), (35, 212))
        pygame.draw.rect(surface, (203, 213, 225), (35, 232, 215, 14), border_radius=6)
        hp_col = (34, 197, 94) if health >= 70 else ((234, 179, 8) if health >= 40 else (239, 68, 68))
        pygame.draw.rect(surface, hp_col, (35, 232, int(215 * (health / 100)), 14), border_radius=6)

        # Indikator TDS
        tds_ok = stage["min_tds"] <= tds <= stage["max_tds"]
        tds_col = (21, 128, 61) if tds_ok else (220, 38, 38)
        tds_lbl = self.font_bold.render(f"{tds} ppm", True, tds_col)
        surface.blit(tds_lbl, (140 - tds_lbl.get_width() // 2, 272))
        ideal_tds = self.font_small.render(f"Ideal TDS: {stage['min_tds']}-{stage['max_tds']} ppm", True, (71, 85, 105))
        surface.blit(ideal_tds, (35, 302))

        # Indikator pH
        ph_ok = stage["min_ph"] <= ph <= stage["max_ph"]
        ph_col = (21, 128, 61) if ph_ok else (220, 38, 38)
        ph_lbl = self.font_bold.render(f"pH {ph:.1f}", True, ph_col)
        surface.blit(ph_lbl, (140 - ph_lbl.get_width() // 2, 342))
        ideal_ph = self.font_small.render(f"Ideal pH: {stage['min_ph']}-{stage['max_ph']}", True, (71, 85, 105))
        surface.blit(ideal_ph, (35, 372))

        # Info Cuaca dari CSV
        surface.blit(self.font_bold.render(f"Cuaca: {weather['cuaca']} ({weather['suhu_c']}°C)", True, (3, 105, 161)), (35, 405))
        surface.blit(self.font_small.render(f"Kelembapan Udara: {weather['kelembapan_persen']}%", True, (71, 85, 105)), (35, 425))

        # 4. Kotak Panduan / Tips di Kanan Atas
        tip_rect = pygame.Rect(730, 155, 250, 95)
        pygame.draw.rect(surface, (255, 255, 255), tip_rect, border_radius=12)
        pygame.draw.rect(surface, (148, 163, 184), tip_rect, width=2, border_radius=12)

        if not tds_ok or not ph_ok:
            tip_title = "Peringatan Nutrisi!"
            tip_msg = "Sesuaikan TDS & pH agar akar menyerap nutrisi optimal."
            title_col = (220, 38, 38)
        elif current_idx == len(stages) - 1:
            tip_title = "Waktunya Panen!"
            tip_msg = "Selada sudah siap. Klik 'Panen Sekarang!' di kiri bawah."
            title_col = (21, 128, 61)
        else:
            tip_title = "Info Tahap Saat Ini"
            tip_msg = stage["description"]
            title_col = (3, 105, 161)

        surface.blit(self.font_bold.render(tip_title, True, title_col), (tip_rect.x + 12, tip_rect.y + 10))
        self._draw_wrapped_text(surface, tip_msg, self.font_body, (51, 65, 85), tip_rect.x + 12, tip_rect.y + 34, 226)

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
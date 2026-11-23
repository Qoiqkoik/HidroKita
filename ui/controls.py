import pygame

class Button:
    def __init__(self, x, y, w, h, text, color=(59, 130, 246), hover_color=(37, 99, 235), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.enabled = True

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos) and self.enabled
        
        if not self.enabled:
            bg = (156, 163, 175)
        else:
            bg = self.hover_color if is_hover else self.color

        pygame.draw.rect(surface, bg, self.rect, border_radius=8)
        pygame.draw.rect(surface, (30, 41, 59), self.rect, width=2, border_radius=8)

        lbl = font.render(self.text, True, self.text_color)
        surface.blit(lbl, (self.rect.centerx - lbl.get_width() // 2, self.rect.centery - lbl.get_height() // 2))

    def is_clicked(self, event):
        if self.enabled and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class ControlPanel:
    def __init__(self):
        # Tombol kontrol TDS (Nutrisi)
        self.btn_tds_minus = Button(40, 265, 45, 32, "-100", (239, 68, 68), (220, 38, 38))
        self.btn_tds_plus = Button(195, 265, 45, 32, "+100", (34, 197, 94), (22, 163, 74))

        # Tombol kontrol pH Air
        self.btn_ph_minus = Button(40, 335, 45, 32, "-0.2", (239, 68, 68), (220, 38, 38))
        self.btn_ph_plus = Button(195, 335, 45, 32, "+0.2", (34, 197, 94), (22, 163, 74))

        # Tombol Navigasi Tahap & Aksi
        self.btn_next = Button(30, 460, 115, 42, "Lanjut >", (245, 158, 11), (217, 119, 6))
        self.btn_reset = Button(155, 460, 105, 42, "Reset", (100, 116, 139), (71, 85, 105))
        self.btn_harvest = Button(30, 515, 230, 44, "Panen Sekarang!", (16, 185, 129), (5, 150, 105))
        self.btn_harvest.enabled = False

    def draw(self, surface, font):
        for btn in [
            self.btn_tds_minus, self.btn_tds_plus,
            self.btn_ph_minus, self.btn_ph_plus,
            self.btn_next, self.btn_reset, self.btn_harvest
        ]:
            btn.draw(surface, font)
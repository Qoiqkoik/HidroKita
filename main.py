import pygame
import sys
from utils.data_loader import load_irrigation_data, load_weather_data
from graphics.scene_graph import SceneGraph
from ui.dashboard import Dashboard
from ui.controls import ControlPanel

WIDTH, HEIGHT = 1000, 600
FPS = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("HidroKita - Simulasi Pertumbuhan Tanaman Hidroponik")
    clock = pygame.time.Clock()

    # Muat data dari folder data/
    stages = load_irrigation_data()["stages"]
    weather_data = load_weather_data()

    # Inisialisasi komponen grafis & UI
    scene = SceneGraph(WIDTH, HEIGHT)
    dashboard = Dashboard()
    controls = ControlPanel()

    # State awal simulasi
    current_stage = 0
    tds = 400
    ph = 6.0
    health = 95.0
    score = 0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        stage_info = stages[current_stage]
        weather = weather_data[current_stage % len(weather_data)]

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if controls.btn_tds_minus.is_clicked(event):
                tds = max(100, tds - 100)
            elif controls.btn_tds_plus.is_clicked(event):
                tds = min(1800, tds + 100)
            elif controls.btn_ph_minus.is_clicked(event):
                ph = round(max(4.0, ph - 0.2), 1)
            elif controls.btn_ph_plus.is_clicked(event):
                ph = round(min(8.5, ph + 0.2), 1)
            elif controls.btn_next.is_clicked(event):
                if current_stage < len(stages) - 1:
                    current_stage += 1
                    score += int(health // 5)
            elif controls.btn_reset.is_clicked(event):
                current_stage = 0
                tds = 400
                ph = 6.0
                health = 95.0
            elif controls.btn_harvest.is_clicked(event):
                score += int(health * 2)
                current_stage = 0
                tds = 400
                ph = 6.0
                health = 95.0

        # Update status tombol aksi
        controls.btn_next.enabled = (current_stage < len(stages) - 1) and (health > 20)
        controls.btn_harvest.enabled = (current_stage == len(stages) - 1) and (health >= 50)

        # Logika kesehatan tanaman berdasarkan kesesuaian TDS dan pH
        tds_ok = stage_info["min_tds"] <= tds <= stage_info["max_tds"]
        ph_ok = stage_info["min_ph"] <= ph <= stage_info["max_ph"]

        if tds_ok and ph_ok:
            health = min(100.0, health + 4.0 * dt)
        else:
            health = max(10.0, health - 6.0 * dt)

        # Update animasi grafis
        scene.update(dt, is_pumping=True)

        # Render seluruh layar
        scene.draw(screen, current_stage, health, weather)
        dashboard.draw(screen, stages, current_stage, tds, ph, health, score, weather)
        controls.draw(screen, dashboard.font_small)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
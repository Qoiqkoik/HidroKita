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
    pygame.display.set_caption("HidroKita - Visualisasi Pertumbuhan Tanaman Hidroponik")
    clock = pygame.time.Clock()

    # Muat data dari folder data/
    stages = load_irrigation_data()["stages"]
    weather_data = load_weather_data()

    # Inisialisasi komponen grafis & UI
    scene = SceneGraph(WIDTH, HEIGHT)
    dashboard = Dashboard()
    controls = ControlPanel()

    # Tahap yang sedang ditampilkan
    current_stage = 0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_stage = max(0, current_stage - 1)
                elif event.key == pygame.K_RIGHT:
                    current_stage = min(len(stages) - 1, current_stage + 1)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                selected_stage = dashboard.stage_at_position(event.pos, len(stages))
                if selected_stage is not None:
                    current_stage = selected_stage
                elif controls.btn_previous.is_clicked(event):
                    current_stage = max(0, current_stage - 1)
                elif controls.btn_next.is_clicked(event):
                    current_stage = min(len(stages) - 1, current_stage + 1)

        controls.btn_previous.enabled = current_stage > 0
        controls.btn_next.enabled = current_stage < len(stages) - 1
        weather = weather_data[min(current_stage, len(weather_data) - 1)]

        # Update animasi grafis
        scene.update(dt, is_pumping=True)

        # Render seluruh layar
        scene.draw(screen, current_stage, 100.0, weather)
        dashboard.draw(screen, stages, current_stage, weather)
        controls.draw(screen, dashboard.font_small)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
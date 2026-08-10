"""
Gera diagramas esquemáticos originais (não copiados de artigos) para ilustrar
cada ferramenta/sensor da metodologia. Estilo consistente com a identidade
visual do app (verde institucional + dourado).
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, Polygon, Wedge
import numpy as np

GREEN_900 = "#0b3d24"
GREEN_700 = "#0f5c34"
GREEN_500 = "#1f7a4d"
GREEN_300 = "#8fc3a3"
GREEN_100 = "#e6f0e9"
GOLD = "#b98a2e"
GRAY = "#5a5a5a"
BG = "#ffffff"

plt.rcParams["font.family"] = "DejaVu Sans"


def new_fig(w=8, h=4.5):
    fig, ax = plt.subplots(figsize=(w, h), dpi=180)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    return fig, ax


# ---------------------------------------------------------------
# 1. LiDAR aerotransportado (UAV) -> nuvem de pontos -> CHM
# ---------------------------------------------------------------
def diagram_lidar():
    fig, ax = new_fig()

    # UAV
    uav_x, uav_y = 2.2, 4.8
    ax.add_patch(Circle((uav_x, uav_y), 0.18, color=GREEN_900, zorder=5))
    for dx, dy in [(-0.5, 0.25), (0.5, 0.25), (-0.5, -0.25), (0.5, -0.25)]:
        ax.plot([uav_x, uav_x + dx], [uav_y, uav_y + dy], color=GREEN_900, lw=2)
        ax.add_patch(Circle((uav_x + dx, uav_y + dy), 0.12, color=GREEN_700, zorder=5))

    # pulsos laser (leques de linhas verdes)
    canopy_y = 2.6
    n_pulses = 9
    xs = np.linspace(1.1, 3.3, n_pulses)
    for x in xs:
        ax.plot([uav_x, x], [uav_y - 0.15, canopy_y - 0.15], color=GREEN_500, lw=0.9, alpha=0.75)

    # dossel (árvores estilizadas, copa para cima)
    tree_x = np.linspace(0.8, 3.6, 7)
    rng = np.random.default_rng(3)
    solo_y = canopy_y - 1.0
    for x in tree_x:
        h = 0.55 + rng.uniform(0, 0.35)
        ax.add_patch(Polygon([[x, solo_y + h], [x - 0.35, solo_y], [x + 0.35, solo_y]], color=GREEN_700))
    ax.add_patch(Rectangle((0.6, solo_y - 0.15), 3.2, 0.15, color="#8a6b4a"))  # solo

    ax.text(2.2, 5.35, "LiDAR aerotransportado (UAV)", ha="center", fontsize=12, fontweight="bold", color=GREEN_900)
    ax.text(2.2, 0.85, "Nuvem de pontos 3D\n≥ 50 pontos/m²", ha="center", fontsize=9, color=GRAY)

    # seta central
    ax.annotate("", xy=(5.4, 3.0), xytext=(4.3, 3.0),
                arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2.2))

    # nuvem de pontos (dispersão colorida por altura)
    ax.text(7.4, 5.35, "Modelo de Altura do Dossel (CHM)", ha="center", fontsize=12, fontweight="bold", color=GREEN_900)
    px = rng.uniform(6.0, 8.8, 220)
    py_base = 1.3
    py = py_base + np.abs(np.sin(px * 2.3)) * 1.6 + rng.uniform(-0.05, 0.05, 220)
    colors = plt.cm.Greens((py - py.min()) / (py.max() - py.min()) * 0.7 + 0.3)
    ax.scatter(px, py, s=4, c=colors, zorder=4)
    ax.add_patch(Rectangle((5.9, 1.15), 3.0, 0.12, color="#8a6b4a"))
    ax.text(7.4, 0.85, "Segmentação individual de copas", ha="center", fontsize=9, color=GRAY)

    fig.text(0.5, 0.03,
              "Adaptado do princípio metodológico de White et al. (2016, The Forestry Chronicle) e "
              "Wallace et al. (2016, Remote Sensing) — diagrama esquemático original.",
              ha="center", fontsize=7.3, color=GRAY, style="italic")
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    return fig


# ---------------------------------------------------------------
# 2. Fotogrametria UAV / SfM -> ortomosaico
# ---------------------------------------------------------------
def diagram_uav_sfm():
    fig, ax = new_fig()

    # trajetória em grade do UAV com sobreposição de imagens
    ax.text(2.4, 5.35, "Fotogrametria UAV (Structure from Motion)", ha="center", fontsize=11.5,
            fontweight="bold", color=GREEN_900)

    rows_y = [4.3, 3.55, 2.8]
    for ry in rows_y:
        ax.plot([0.6, 4.2], [ry, ry], color=GREEN_500, lw=1.4, ls="--", zorder=2)
        for x in np.linspace(0.6, 4.2, 5):
            # footprint da câmera (retângulo semitransparente = sobreposição)
            ax.add_patch(Rectangle((x - 0.42, ry - 0.28), 0.84, 0.56,
                                    facecolor=GREEN_300, edgecolor=GREEN_700, alpha=0.45, lw=0.7))
            ax.add_patch(Circle((x, ry), 0.07, color=GREEN_900, zorder=5))

    ax.text(2.4, 1.9, "Voos em grade · sobreposição\nlateral e longitudinal", ha="center", fontsize=9, color=GRAY)

    ax.annotate("", xy=(5.4, 3.4), xytext=(4.5, 3.4),
                arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2.2))
    ax.text(4.95, 3.65, "SfM", ha="center", fontsize=9, color=GOLD, fontweight="bold")

    # ortomosaico resultante (mosaico de "fotos" verdes)
    ax.text(7.6, 5.35, "Ortomosaico + Modelo de Superfície", ha="center", fontsize=11.5,
            fontweight="bold", color=GREEN_900)
    rng = np.random.default_rng(7)
    for i in range(4):
        for j in range(3):
            x0 = 5.9 + i * 0.85
            y0 = 2.55 + j * 0.68
            shade = GREEN_500 if (i + j) % 2 == 0 else GREEN_700
            ax.add_patch(Rectangle((x0, y0), 0.82, 0.66, facecolor=shade, edgecolor="white", lw=1))
            # pequenas copas circulares (textura de dossel)
            for _ in range(2):
                cx = x0 + rng.uniform(0.15, 0.65)
                cy = y0 + rng.uniform(0.15, 0.5)
                ax.add_patch(Circle((cx, cy), 0.06, color=GREEN_300, alpha=0.8))

    ax.text(7.6, 1.9, "Resolução espacial < 0,10 m\nvalidação da segmentação de copas", ha="center",
            fontsize=9, color=GRAY)

    fig.text(0.5, 0.03,
              "Princípio de aquisição por fotogrametria SfM — Wallace et al. (2016, Remote Sensing 8(1):20). "
              "Diagrama esquemático original.",
              ha="center", fontsize=7.3, color=GRAY, style="italic")
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    return fig


# ---------------------------------------------------------------
# 3. Sensoriamento orbital: Sentinel-1 (SAR) + Sentinel-2 (óptico)
# ---------------------------------------------------------------
def diagram_satellite():
    fig, ax = new_fig()

    # Sentinel-1 (SAR)
    sat1_x, sat1_y = 2.3, 4.9
    ax.add_patch(Rectangle((sat1_x - 0.22, sat1_y - 0.16), 0.44, 0.32, color=GREEN_900))
    ax.add_patch(Rectangle((sat1_x - 0.55, sat1_y - 0.06), 0.28, 0.12, color=GREEN_500))
    ax.add_patch(Rectangle((sat1_x + 0.27, sat1_y - 0.06), 0.28, 0.12, color=GREEN_500))
    ax.text(sat1_x, sat1_y + 0.4, "Sentinel-1 (SAR · banda C)", ha="center", fontsize=10,
            fontweight="bold", color=GREEN_900)

    # ondas de radar (arcos)
    for r in [0.5, 0.9, 1.3]:
        ax.add_patch(Wedge((sat1_x, sat1_y), r, 250, 290, width=0.03, color=GREEN_500, alpha=0.8))

    # Sentinel-2 (óptico)
    sat2_x, sat2_y = 7.7, 4.9
    ax.add_patch(Rectangle((sat2_x - 0.22, sat2_y - 0.16), 0.44, 0.32, color=GREEN_900))
    ax.add_patch(Rectangle((sat2_x - 0.55, sat2_y - 0.06), 0.28, 0.12, color=GOLD))
    ax.add_patch(Rectangle((sat2_x + 0.27, sat2_y - 0.06), 0.28, 0.12, color=GOLD))
    ax.text(sat2_x, sat2_y + 0.4, "Sentinel-2 (óptico · 10 m)", ha="center", fontsize=10,
            fontweight="bold", color=GREEN_900)
    for ang in [255, 265, 275, 285]:
        ax.add_patch(Wedge((sat2_x, sat2_y), 1.3, ang, ang + 3, width=0.9, color=GOLD, alpha=0.25))

    # dossel florestal ao centro-baixo (copa para cima)
    tree_x = np.linspace(2.5, 7.5, 14)
    rng = np.random.default_rng(11)
    solo_y2 = 1.1
    for x in tree_x:
        h = 0.35 + rng.uniform(0, 0.25)
        ax.add_patch(Polygon([[x, solo_y2 + h], [x - 0.25, solo_y2], [x + 0.25, solo_y2]], color=GREEN_700))
    ax.add_patch(Rectangle((2.2, solo_y2 - 0.14), 5.6, 0.14, color="#8a6b4a"))

    ax.text(5.0, 1.9, "Floresta Ombrófila Mista — FLONA de Irati", ha="center", fontsize=9, color=GRAY)
    ax.text(5.0, 2.35, "NDVI · EVI · NBR (óptico)      Retroespalhamento (SAR)", ha="center", fontsize=8.7,
            color=GREEN_900, fontweight="bold")

    fig.text(0.5, 0.03,
              "Complementaridade óptico-SAR para biomassa florestal — Rodríguez-Veiga et al. "
              "(2019, Remote Sensing of Environment 224:98–110). Diagrama esquemático original.",
              ha="center", fontsize=7.3, color=GRAY, style="italic")
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    return fig


# ---------------------------------------------------------------
# 4. Fusão multissensor + Machine Learning -> mapa de biomassa
# ---------------------------------------------------------------
def diagram_ml_fusion():
    fig, ax = new_fig()

    labels = ["Métricas\nLiDAR", "Geometria\nUAV/SfM", "Índices\nespectrais", "Retro-\nespalhamento SAR"]
    ys = [4.6, 3.55, 2.5, 1.45]
    for lab, y in zip(labels, ys):
        ax.add_patch(Rectangle((0.4, y - 0.28), 1.9, 0.56, facecolor=GREEN_100, edgecolor=GREEN_700, lw=1.3))
        ax.text(1.35, y, lab, ha="center", va="center", fontsize=8.3, color=GREEN_900, fontweight="bold")
        ax.annotate("", xy=(3.9, 3.0), xytext=(2.35, y),
                    arrowprops=dict(arrowstyle="-|>", color=GREEN_500, lw=1.3, alpha=0.85,
                                     connectionstyle="arc3,rad=0.15" if y > 3.0 else "arc3,rad=-0.15"))

    # nó central: seleção de variáveis + modelos
    ax.add_patch(Circle((4.7, 3.0), 0.85, facecolor=GREEN_900, edgecolor=GOLD, lw=2, zorder=5))
    ax.text(4.7, 3.25, "Seleção de", ha="center", fontsize=8, color="white", zorder=6)
    ax.text(4.7, 3.02, "variáveis +", ha="center", fontsize=8, color="white", zorder=6)
    ax.text(4.7, 2.79, "Random Forest /", ha="center", fontsize=7.6, color="white", zorder=6)
    ax.text(4.7, 2.58, "Redes Neurais", ha="center", fontsize=7.6, color="white", zorder=6)

    ax.annotate("", xy=(6.3, 3.0), xytext=(5.55, 3.0),
                arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2.4))

    # saída: mapa de biomassa (grade colorida)
    ax.text(8.1, 5.0, "Biomassa por copa e\nagregação por área", ha="center", fontsize=9.3,
            fontweight="bold", color=GREEN_900)
    rng = np.random.default_rng(21)
    grid = rng.uniform(0.3, 1.0, (5, 5))
    cmap = plt.cm.YlGn
    for i in range(5):
        for j in range(5):
            ax.add_patch(Rectangle((6.6 + j * 0.42, 1.3 + i * 0.42), 0.4, 0.4,
                                    facecolor=cmap(grid[i, j]), edgecolor="white", lw=0.6))
    ax.text(8.1, 1.05, "Validação cruzada espacial (RMSE, MAE, R²)", ha="center", fontsize=8, color=GRAY)

    fig.text(0.5, 0.03,
              "Fusão multissensor com aprendizado de máquina — Breiman (2001, Machine Learning 45:5–32); "
              "Zoladz et al. (2021, Remote Sensing 13(2):252). Diagrama esquemático original.",
              ha="center", fontsize=7.3, color=GRAY, style="italic")
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    return fig


if __name__ == "__main__":
    diagrams = {
        "lidar.png": diagram_lidar(),
        "uav_sfm.png": diagram_uav_sfm(),
        "satellite.png": diagram_satellite(),
        "ml_fusion.png": diagram_ml_fusion(),
    }
    for fname, fig in diagrams.items():
        fig.savefig(f"assets/{fname}", dpi=180, facecolor="white", bbox_inches="tight")
        print(f"salvo assets/{fname}")

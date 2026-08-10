import streamlit as st
import geopandas as gpd
import folium
from folium import plugins
from streamlit_folium import st_folium
import pandas as pd

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------
st.set_page_config(
    page_title="PPGF/UNICENTRO | Biomassa de Copa de Araucária",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# ESTILO — inspirado na identidade visual da Unicentro / Depto. de
# Engenharia Florestal (verde institucional escuro, tipografia sóbria,
# estrutura de cabeçalho/rodapé em blocos, como nos sites da universidade)
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=Merriweather:wght@700;900&display=swap');

    :root{
        --uni-green-900:#0b3d24;   /* verde institucional escuro */
        --uni-green-700:#0f5c34;
        --uni-green-500:#1f7a4d;
        --uni-green-300:#6fae82;
        --uni-green-100:#e6f0e9;
        --uni-gray-900:#2b2b2b;
        --uni-gray-600:#5a5a5a;
        --uni-gray-200:#e3e3e3;
        --uni-bg:#f7f8f6;
        --uni-gold:#b98a2e;
    }

    html, body, .stApp { background-color: var(--uni-bg); font-family: 'Source Sans 3', sans-serif; }
    h1, h2, h3 { font-family: 'Merriweather', serif; color: var(--uni-green-900) !important; }
    /* Texto padrão do corpo (fundo claro) */
    .stApp p, .stApp li, .stApp label { color: var(--uni-gray-900); }

    /* -------- cabeçalho institucional -------- */
    .inst-header, .inst-header * {
        color: white !important;
    }
    .inst-header {
        background: var(--uni-green-900);
        padding: 0.5rem 1.5rem;
        font-size: 0.78rem;
        letter-spacing: 0.03em;
        border-bottom: 3px solid var(--uni-gold);
        margin: -1rem -1rem 0 -1rem;
    }
    .inst-header span { color: var(--uni-green-300) !important; }

    .breadcrumb {
        font-size: 0.8rem;
        color: var(--uni-gray-600);
        margin-bottom: 0.6rem;
    }
    .breadcrumb b { color: var(--uni-green-700); }

    .masthead {
        background: linear-gradient(120deg, var(--uni-green-900) 0%, var(--uni-green-700) 55%, var(--uni-green-500) 100%);
        padding: 2.4rem 2.6rem;
        border-radius: 4px;
        color: white;
        margin-bottom: 1.6rem;
        border-left: 6px solid var(--uni-gold);
    }
    .masthead .eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.75rem;
        color: var(--uni-green-100);
        margin-bottom: 0.6rem;
    }
    .masthead, .masthead * { color: white !important; }
    .masthead h1 { font-size: 1.85rem; margin: 0 0 0.5rem 0; line-height:1.3;}
    .masthead p { color: var(--uni-green-100) !important; font-size: 1.02rem; margin:0; }
    .masthead .eyebrow { color: var(--uni-green-100) !important; }

    /* -------- cartões de conteúdo (estilo "ficha técnica") -------- */
    .card {
        background: white;
        border: 1px solid var(--uni-gray-200);
        border-top: 3px solid var(--uni-green-700);
        border-radius: 4px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 1rem;
    }
    .card h4 { margin-top:0; color: var(--uni-green-700) !important; font-size: 1.05rem;}
    .card .fonte { font-size: 0.75rem; color: var(--uni-gray-600); margin-top: 0.6rem; font-style: italic; }

    .stat-box {
        background: white;
        border: 1px solid var(--uni-gray-200);
        border-left: 4px solid var(--uni-green-700);
        border-radius: 4px;
        padding: 1rem 1rem;
        text-align: left;
    }
    .stat-box .big { font-size: 1.7rem; font-weight: 700; color: var(--uni-green-900); display:block; font-family:'Merriweather',serif;}
    .stat-box .label { font-size: 0.78rem; color: var(--uni-gray-600); }

    .fig-caption {
        font-size: 0.82rem;
        color: var(--uni-gray-600);
        background: white;
        border-left: 4px solid var(--uni-gold);
        padding: 0.6rem 1rem;
        margin-top: 0.5rem;
    }
    .fig-caption b { color: var(--uni-green-900); }

    .step-row {
        display:flex;
        gap: 1rem;
        align-items:flex-start;
        background:white;
        border:1px solid var(--uni-gray-200);
        border-radius:4px;
        padding: 1rem 1.3rem;
        margin-bottom: 0.7rem;
    }
    .step-num {
        flex: 0 0 auto;
        background: var(--uni-green-900);
        color: white;
        font-weight:700;
        font-family:'Merriweather',serif;
        width: 34px; height:34px;
        border-radius: 50%;
        display:flex; align-items:center; justify-content:center;
    }
    .step-row h4 { margin: 0 0 0.3rem 0; }
    .step-row p { margin:0; font-size: 0.93rem; }

    /* sidebar institucional */
    section[data-testid="stSidebar"] { background-color: var(--uni-green-900); }
    section[data-testid="stSidebar"] * { color: white !important; }
    section[data-testid="stSidebar"] .stRadio label { font-size: 0.9rem; }
    section[data-testid="stSidebar"] hr { border-color: var(--uni-green-500); }

    /* rodapé institucional */
    .inst-footer, .inst-footer * {
        color: var(--uni-green-100) !important;
    }
    .inst-footer {
        margin-top: 2.5rem;
        background: var(--uni-green-900);
        padding: 1.6rem 2rem;
        border-radius: 4px;
        font-size: 0.82rem;
        display:flex;
        gap: 2.5rem;
        flex-wrap: wrap;
    }
    .inst-footer b { color: white !important; display:block; margin-bottom:0.2rem; }

    hr { border-color: var(--uni-gray-200); }
    </style>

    <div class="inst-header">
        UNICENTRO – Universidade Estadual do Centro-Oeste &nbsp;·&nbsp;
        <span>Câmpus de Irati &nbsp;·&nbsp; Programa de Pós-Graduação em Ciências Florestais (PPGF)</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# DADOS
# ------------------------------------------------------------------
@st.cache_data
def load_data():
    gdf = gpd.read_file("data/Parcelas.gpkg", layer="partes_nicas")
    gdf_m = gdf.to_crs(epsg=32722)  # UTM 22S -> área em metros
    gdf["area_ha"] = (gdf_m.geometry.area / 10000).round(3)
    gdf = gdf.sort_values("Parcela").reset_index(drop=True)
    return gdf

gdf = load_data()
total_ha = gdf["area_ha"].sum()
n_parcelas = len(gdf)
centro = gdf.geometry.union_all().centroid
bounds = gdf.total_bounds  # minx, miny, maxx, maxy

# ------------------------------------------------------------------
# NAVEGAÇÃO
# ------------------------------------------------------------------
st.sidebar.markdown("### 🌲 Departamento de\nEngenharia Florestal")
st.sidebar.caption("Defesa de Projeto de Doutorado")
st.sidebar.markdown("---")
capitulo = st.sidebar.radio(
    "Capítulos",
    [
        "Abertura",
        "O Problema",
        "Área de Estudo",
        "Dados de Campo",
        "Metodologia",
        "Hipóteses & Objetivos",
        "Cronograma",
        "Resultados Esperados",
    ],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.caption("PPGF/UNICENTRO · Câmpus de Irati, PR")

st.markdown(
    f'<div class="breadcrumb">PPGF/UNICENTRO &nbsp;›&nbsp; Doutorado &nbsp;›&nbsp; Projeto de Pesquisa &nbsp;›&nbsp; <b>{capitulo}</b></div>',
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# PÁGINA: ABERTURA
# ------------------------------------------------------------------
if capitulo == "Abertura":
    st.markdown(
        """
        <div class="masthead">
            <div class="eyebrow">Programa de Pós-Graduação em Ciências Florestais · Doutorado</div>
            <h1>Avaliação de biomassa da copa de Araucária em Floresta Ombrófila Mista utilizando métricas estruturais e fusão multissensor</h1>
            <p>Um estudo na Floresta Nacional de Irati (PR), integrando LiDAR, UAV, satélite e aprendizado de máquina.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-box"><span class="big">{n_parcelas}</span><span class="label">parcelas permanentes (1 ha cada)</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-box"><span class="big">2002–2026</span><span class="label">série histórica de remedições</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-box"><span class="big">1.272,9 ha</span><span class="label">floresta nativa na FLONA</span></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-box"><span class="big">4 sensores</span><span class="label">LiDAR, UAV, Sentinel-1/2</span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card">
        <h4>A pergunta que conduz esta tese</h4>
        <p>Já sabemos estimar biomassa florestal em escala de parcela ou de hectare. Mas quando o interesse é a
        <b>árvore individual</b> — a copa isolada de uma Araucária, a maior contribuinte de biomassa do dossel —
        os métodos tradicionais de inventário se tornam inviáveis em escala. Esta pesquisa testa se a fusão de
        dados estruturais (LiDAR), geométricos (UAV) e espectrais (satélite), combinados por aprendizado de
        máquina, consegue preencher essa lacuna.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Use o menu à esquerda para navegar pelos capítulos da apresentação.")

# ------------------------------------------------------------------
# PÁGINA: O PROBLEMA
# ------------------------------------------------------------------
elif capitulo == "O Problema":
    st.markdown("## O Problema de Pesquisa")

    col1, col2 = st.columns([1.4, 1])
    with col1:
        st.markdown(
            """
            <div class="card">
            <h4>Uma floresta definida por uma espécie</h4>
            <p>A Floresta Ombrófila Mista (FOM) — a Floresta com Araucária — é uma formação do Bioma Mata
            Atlântica, dominada por <i>Araucaria angustifolia</i> no dossel superior. Estudos de longo prazo na
            própria FLONA de Irati mostram que a Araucária tem os maiores incrementos diamétricos entre as
            espécies do dossel: 0,42 cm/ano em diâmetro e 0,12 m²/ha/ano em área basal — o que a torna
            desproporcionalmente relevante para os estoques de biomassa e carbono da floresta.</p>
            <p class="fonte">Fonte: Figueiredo Filho et al. (2010), dados das parcelas permanentes de Irati.</p>
            </div>

            <div class="card">
            <h4>Uma espécie sob ameaça</h4>
            <p>A exploração madeireira intensiva do século XX fragmentou os remanescentes de FOM e levou a
            Araucária à Lista Nacional de Espécies Ameaçadas de Extinção (Portaria MMA nº 443/2014). Isso
            transforma a quantificação precisa da sua biomassa de exercício acadêmico em subsídio direto
            para conservação e manejo.</p>
            </div>

            <div class="card">
            <h4>A lacuna metodológica</h4>
            <p>Métodos consolidados estimam biomassa em escala de <b>parcela</b> ou de <b>área</b>. Mas em
            florestas com espécies emergentes como a FOM, poucos indivíduos de grande porte concentram
            parcela expressiva da biomassa total — o que exige uma abordagem em escala de <b>copa individual</b>,
            ainda pouco explorada em florestas nativas devido à dificuldade de segmentar copas com precisão.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="card" style="background:var(--uni-green-100); border-top-color:var(--uni-gold);">
            <h4>Em números</h4>
            <p><b>0,42 cm/ano</b><br><span style="font-size:0.85rem;">incremento diamétrico médio da Araucária</span></p>
            <hr>
            <p><b>0,12 m²/ha/ano</b><br><span style="font-size:0.85rem;">incremento em área basal</span></p>
            <hr>
            <p><b>2014</b><br><span style="font-size:0.85rem;">ano da Portaria MMA que listou a Araucária como ameaçada</span></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------
# PÁGINA: ÁREA DE ESTUDO (MAPA CIENTÍFICO)
# ------------------------------------------------------------------
elif capitulo == "Área de Estudo":
    st.markdown("## Área de Estudo")
    st.markdown(
        """
        <div class="card">
        <p>A pesquisa é desenvolvida na <b>Floresta Nacional (FLONA) de Irati</b>, unidade de conservação do
        ICMBio criada em 1942, no segundo planalto paranaense, entre os municípios de <b>Fernandes Pinheiro</b>
        e <b>Teixeira Soares</b> — cerca de 150 km a oeste de Curitiba. A área está entre as margens dos rios
        das Antas e Imbituva (bacia do rio Tibagi), a 820 m de altitude média e relevo suave ondulado.
        Clima <b>Cfb</b> (Köppen), subtropical úmido mesotérmico: precipitação média de 193,97 mm/mês,
        temperatura média anual de ~18°C (mínima -2°C, máxima 32°C).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m = folium.Map(
        location=[centro.y, centro.x],
        zoom_start=15,
        tiles=None,
        control_scale=True,
    )
    # Satélite como camada padrão (show=True) — imagem de fundo mais informativa
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri, Maxar, Earthstar Geographics",
        name="Imagem de satélite",
        show=True,
    ).add_to(m)
    folium.TileLayer("OpenStreetMap", name="Mapa base (ruas)", show=False).add_to(m)

    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                "fillColor": "#1f7a4d",
                "color": "#ffffff",
                "weight": 1.8,
                "fillOpacity": 0.35,
            },
            highlight_function=lambda x: {"fillColor": "#b98a2e", "fillOpacity": 0.7},
            tooltip=folium.Tooltip(f"Parcela {row['Parcela']}"),
            popup=folium.Popup(
                f"<b>Parcela {row['Parcela']}</b><br>Área: {row['area_ha']:.2f} ha<br>"
                f"Dimensão nominal: 100 m × 100 m",
                max_width=220,
            ),
        ).add_to(m)

        # Rótulo em branco com o número da parcela, centrado no polígono
        label_point = row.geometry.representative_point()
        folium.map.Marker(
            [label_point.y, label_point.x],
            icon=folium.DivIcon(
                icon_size=(40, 18),
                icon_anchor=(20, 9),
                html=(
                    f'<div style="font-family:sans-serif; font-size:12px; font-weight:700; '
                    f'color:#ffffff; text-shadow:0 0 3px #000, 0 0 3px #000, 1px 1px 2px #000; '
                    f'text-align:center;">{row["Parcela"]}</div>'
                ),
            ),
        ).add_to(m)

    # Mini-mapa de situação (locator), replicando a convenção cartográfica
    # da Figura 1 do projeto: mapa de detalhe + mapa de situação regional
    minimap = plugins.MiniMap(
        tile_layer="OpenStreetMap",
        toggle_display=True,
        position="bottomleft",
        width=150,
        height=150,
        zoom_level_offset=-9,
    )
    m.add_child(minimap)

    plugins.Fullscreen(position="topleft").add_to(m)
    plugins.MeasureControl(position="topleft", primary_length_unit="meters").add_to(m)

    # Norte
    north_html = """
    <div style="position: fixed; top: 90px; right: 20px; z-index: 9999;
                background: white; border-radius: 50%; width: 42px; height: 42px;
                box-shadow: 0 1px 4px rgba(0,0,0,0.3); display:flex; align-items:center;
                justify-content:center; font-weight:bold; color:#0b3d24; font-family:sans-serif;">
        N↑
    </div>
    """
    m.get_root().html.add_child(folium.Element(north_html))

    # Legenda
    legend_html = """
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;
                background: white; padding: 10px 14px; border-radius: 4px;
                box-shadow: 0 1px 4px rgba(0,0,0,0.3); font-family:sans-serif; font-size:12.5px; color:#2b2b2b;">
        <b style="color:#0b3d24;">Legenda</b><br>
        <span style="display:inline-block;width:12px;height:12px;background:#1f7a4d;border:1px solid #fff;margin-right:6px;"></span>
        Parcela permanente (1 ha)<br>
        <span style="font-size:11px;color:#5a5a5a;">FLONA de Irati · Fernandes Pinheiro / Teixeira Soares – PR</span>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    folium.LayerControl(position="topleft").add_to(m)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]], padding=(25, 25))

    st_folium(m, height=580, use_container_width=True, returned_objects=[])

    st.markdown(
        f"""
        <div class="fig-caption">
        <b>Figura 1.</b> Localização das {n_parcelas} parcelas permanentes de monitoramento florestal na
        Floresta Nacional (FLONA) de Irati, municípios de Fernandes Pinheiro e Teixeira Soares (PR).
        Clique em cada polígono para ver seus dados; use o minimapa (canto inferior esquerdo) para
        situar a área na região.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div class="stat-box">
                <span class="big">{n_parcelas}</span><span class="label">parcelas mapeadas (rótulos no mapa)</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="stat-box">
                <span class="big">{total_ha:.2f} ha</span><span class="label">área amostral total</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="card">
        <h4>Solos da área amostral</h4>
        <p>Latossolo Vermelho distrófico típico (LVd), Cambissolo Háplico Ta distrófico típico (CXvdt),
        Cambissolo Háplico Ta distrófico léptico (CXvdl) e Cambissolo Háplico alítico típico (CXal)
        (Figueiredo Filho, 2011).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------
# PÁGINA: DADOS DE CAMPO
# ------------------------------------------------------------------
elif capitulo == "Dados de Campo":
    st.markdown("## Dados de Campo")
    st.markdown(
        """
        <div class="card">
        <h4>Uma série histórica rara</h4>
        <p>As 25 parcelas permanentes (100 m × 100 m, subdivididas em subparcelas de 50 m × 50 m e faixas
        de controle de 10 m × 50 m) foram instaladas e medidas pela primeira vez em <b>2002</b>, com
        remedições em <b>2005, 2008 e 2011</b>. Uma nova remedição está prevista para <b>2026</b>, e será a
        base de campo desta pesquisa — garantindo mais de duas décadas de consistência metodológica.</p>
        </div>

        <div class="card">
        <h4>O que será medido em cada árvore (DAP ≥ 10 cm)</h4>
        <ul>
        <li>Diâmetro à altura do peito (DAP, a 1,30 m)</li>
        <li>Altura total e altura de inserção da copa</li>
        <li>Posição espacial (coordenadas X, Y já georreferenciadas)</li>
        <li><b>Exclusivo para Araucária:</b> raios de copa em 4 direções cardeais — base para área de
        projeção e volume de copa, referência de calibração dos modelos remotos</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Linha do tempo das medições")
    anos = ["2002", "2005", "2008", "2011", "2026"]
    cols = st.columns(len(anos))
    for c, ano in zip(cols, anos):
        destaque = ano == "2026"
        cor = "var(--uni-gold)" if destaque else "var(--uni-green-700)"
        label = "próxima remedição · base desta tese" if destaque else "remedição"
        c.markdown(
            f"""
            <div style="text-align:center; padding:0.8rem 0.3rem; border-top:3px solid {cor}; background:white; border-radius:4px;">
            <div style="font-family:'Merriweather',serif; font-weight:700; color:{cor}; font-size:1.1rem;">{ano}</div>
            <div style="font-size:0.72rem; color:var(--uni-gray-600);">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------
# PÁGINA: METODOLOGIA
# ------------------------------------------------------------------
elif capitulo == "Metodologia":
    st.markdown("## Metodologia")
    st.markdown("Da nuvem de pontos ao mapa de biomassa — cinco etapas, três fontes de sensoriamento remoto.")

    # ---- Etapa 1: Aquisição LiDAR ----
    st.markdown(
        """
        <div class="step-row">
            <div class="step-num">1</div>
            <div><h4>Aquisição LiDAR</h4><p>LiDAR aerotransportado por UAV (densidade mínima de 50 pontos/m²)
            sobre as 25 parcelas, gerando uma nuvem de pontos 3D usada para extrair o Modelo de Altura do
            Dossel (CHM) e segmentar copas individuais.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image("assets/lidar.png", use_container_width=True)

    # ---- Etapa 2: Fotogrametria UAV ----
    st.markdown(
        """
        <div class="step-row">
            <div class="step-num">2</div>
            <div><h4>Fotogrametria UAV (SfM)</h4><p>Levantamento RGB complementar com câmera embarcada no UAV,
            em voos de grade com sobreposição lateral e longitudinal, gerando ortomosaico e modelo de
            superfície por Structure from Motion (resolução espacial &lt; 0,10 m) — usado para validar a
            delimitação das copas segmentadas.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image("assets/uav_sfm.png", use_container_width=True)

    # ---- Etapa 3: Sensoriamento orbital ----
    st.markdown(
        """
        <div class="step-row">
            <div class="step-num">3</div>
            <div><h4>Sensoriamento orbital (Sentinel-1 e Sentinel-2)</h4><p>Imagens gratuitas do Copernicus/ESA:
            Sentinel-2 (ótico, 10 m) para índices de vegetação (NDVI, EVI, NBR) relacionados à condição
            biofísica do dossel; Sentinel-1 (SAR, banda C, 10 m) para informação estrutural do dossel,
            operando independentemente de nuvens.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image("assets/satellite.png", use_container_width=True)

    # ---- Etapa 4: Segmentação (sem imagem própria) ----
    st.markdown(
        """
        <div class="step-row">
            <div class="step-num">4</div>
            <div><h4>Segmentação de copas</h4><p>Detecção de máximos locais combinada com crescimento de
            região (algoritmo watershed) sobre o CHM, com parâmetros ajustados à estrutura da Floresta
            Ombrófila Mista; validação por inspeção visual no ortofotomosaico de alta resolução.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Etapa 5: Fusão multissensor + ML ----
    st.markdown(
        """
        <div class="step-row">
            <div class="step-num">5</div>
            <div><h4>Fusão multissensor e aprendizado de máquina</h4><p>Regressão regularizada (Ridge, Lasso),
            Random Forest e redes neurais combinam métricas LiDAR, geometria UAV/SfM e índices espectrais/SAR,
            com ranqueamento de variáveis para medir o ganho de cada sensor. Validação cruzada espacial por
            parcela (RMSE, MAE, R²) contra as equações alométricas da remedição 2026.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image("assets/ml_fusion.png", use_container_width=True)

# ------------------------------------------------------------------
# PÁGINA: HIPÓTESES & OBJETIVOS
# ------------------------------------------------------------------
elif capitulo == "Hipóteses & Objetivos":
    st.markdown("## Hipóteses & Objetivos")

    st.markdown(
        """
        <div class="card" style="border-top-color:var(--uni-gold);">
        <h4>Objetivo geral</h4>
        <p>Desenvolver e validar uma metodologia baseada em métricas estruturais e fusão multissensor
        para a estimativa de biomassa por copa de Araucária em Floresta Ombrófila Mista.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Objetivos específicos")
        for item in [
            "Delimitar e validar copas de Araucárias a partir de LiDAR e fotogrametria UAV",
            "Extrair métricas estruturais e geométricas por copa",
            "Modelar a biomassa por copa a partir das métricas LiDAR",
            "Avaliar o ganho da integração de dados UAV, ópticos e SAR",
            "Aplicar aprendizado de máquina para seleção de variáveis e fusão multissensor",
            "Produzir mapas espaciais de biomassa por copa e por área",
        ]:
            st.markdown(f"- {item}")

    with col2:
        st.markdown("#### Hipóteses")
        for h, texto in [
            ("H1", "Métricas estruturais 3D de LiDAR explicam significativamente a variabilidade da biomassa por copa."),
            ("H2", "Dados UAV melhoram a delimitação das copas e o desempenho dos modelos."),
            ("H3", "A fusão com dados ópticos e SAR aumenta a robustez e a generalização espacial."),
            ("H4", "Aprendizado de máquina captura relações não lineares, melhorando o desempenho dos modelos."),
        ]:
            st.markdown(
                f"""
                <div class="card">
                <h4>{h}</h4>
                <p style="margin:0;">{texto}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ------------------------------------------------------------------
# PÁGINA: CRONOGRAMA
# ------------------------------------------------------------------
elif capitulo == "Cronograma":
    st.markdown("## Cronograma de Execução")

    cronograma = pd.DataFrame(
        {
            "Atividade": [
                "Revisão bibliográfica",
                "Organização de dados de campo",
                "Processamento LiDAR e UAV",
                "Segmentação de copas",
                "Modelagem e integração multissensor",
                "Redação da tese",
                "Defesa",
            ],
            "Ano 1": ["✔", "✔", "", "", "", "", ""],
            "Ano 2": ["", "✔", "✔", "✔", "", "", ""],
            "Ano 3": ["", "", "", "✔", "✔", "✔", ""],
            "Ano 4": ["", "", "", "", "", "✔", "✔"],
        }
    )
    st.dataframe(cronograma, hide_index=True, use_container_width=True)
    st.caption("Programa de Doutorado (4 anos) — PPGF/UNICENTRO.")

# ------------------------------------------------------------------
# PÁGINA: RESULTADOS ESPERADOS
# ------------------------------------------------------------------
elif capitulo == "Resultados Esperados":
    st.markdown("## Resultados Esperados")

    resultados = [
        ("Metodologia validada", "Abordagem robusta e replicável para estimativa de biomassa por copa de Araucária."),
        ("Mapas espaciais", "Biomassa por copa individual e sua agregação em escala de parcela e de área."),
        ("Avaliação quantitativa", "Contribuição isolada e combinada de cada sensor (LiDAR, UAV, óptico, SAR)."),
        ("Subsídio técnico", "Base para manejo e conservação da Floresta Ombrófila Mista e da FLONA de Irati."),
    ]
    for titulo, r in resultados:
        st.markdown(
            f"""
            <div class="card">
            <h4>{titulo}</h4>
            <p style="margin:0;">{r}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="masthead" style="margin-top:1.5rem;">
        <h1 style="font-size:1.4rem;">Obrigado pela atenção.</h1>
        <p>Perguntas, críticas e sugestões da banca são bem-vindas.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------
# RODAPÉ INSTITUCIONAL
# ------------------------------------------------------------------
st.markdown(
    """
    <div class="inst-footer">
        <div><b>Câmpus de Irati</b>Rua Professora Maria Roza Zanon de Almeida<br>Engenheiro Gutierrez – Irati – PR</div>
        <div><b>Programa</b>Pós-Graduação em Ciências Florestais (PPGF)<br>Doutorado — 2026</div>
        <div><b>Departamento</b>Engenharia Florestal<br>Universidade Estadual do Centro-Oeste</div>
    </div>
    """,
    unsafe_allow_html=True,
)

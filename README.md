# Biomassa de Copa de Araucária — Apresentação (Streamlit)

Site de apresentação em alto nível do projeto de doutorado, com storytelling e mapa
interativo das 25 parcelas permanentes de estudo (FLONA de Irati).

## Como rodar localmente

1. Instale as dependências (recomenda-se um ambiente virtual):
   ```bash
   pip install -r requirements.txt
   ```

2. Rode o app:
   ```bash
   streamlit run app.py
   ```

3. O navegador abrirá automaticamente em `http://localhost:8501`.

## Estrutura

```
streamlit_app/
├── app.py              # aplicação principal (todas as páginas/capítulos)
├── requirements.txt
├── data/
│   └── Parcelas.gpkg    # vetorial das 25 parcelas permanentes
└── README.md
```

## Capítulos do site

1. **Início** — abertura com a pergunta central da pesquisa
2. **O Contexto** — Floresta Ombrófila Mista, ameaça à Araucária, problema de pesquisa
3. **Área de Estudo** — mapa interativo das parcelas (clique para ver área/ID)
4. **Metodologia** — as 5 etapas, do campo ao mapa de biomassa
5. **Hipóteses & Objetivos**
6. **Cronograma** — tabela por ano
7. **Resultados Esperados**

## Personalizações fáceis

- **Cores**: edite as variáveis CSS no topo de `app.py` (bloco `<style>`, seção `:root`)
- **Textos**: cada capítulo é um bloco `elif capitulo == "..."` dentro de `app.py`
- **Novas camadas no mapa**: se depois você quiser adicionar outra camada vetorial
  (ex.: limite da FLONA, copas segmentadas), basta carregar com `geopandas` e
  adicionar outro `folium.GeoJson(...)` na página "Área de Estudo"

## Publicar online (opcional)

O jeito mais rápido é o [Streamlit Community Cloud](https://streamlit.io/cloud):
suba esta pasta para um repositório do GitHub e conecte o repositório lá —
gera um link público para compartilhar com os professores.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
from io import BytesIO


# ==========================
# Configuração da página
# ==========================
st.set_page_config(layout="wide")
st.title("Progressive Carries")

# ==========================
# 1. DADOS DAS CORRIDAS
# ==========================
player_name = "Nome do Jogador"

data = {
    "x_start": [81.94, 99.4, 94.74, 98.57],
    "y_start": [23.54, 29.53, 14.07, 23.38],
    "x_end":   [103.72, 103.05, 114.69, 116.35],
    "y_end":   [19.72, 33.35, 16.89, 25.7]
}

df = pd.DataFrame(data)

# ==========================
# 2. FILTRAR CORRIDAS PROGRESSIVAS
# ==========================
df = df[(df["x_start"] >= 60) & (df["x_end"] >= 60)]
df = df[(df["x_end"] - df["x_start"]) >= 1]

# ==========================
# 3. CRIAR CAMPO
# ==========================
pitch = VerticalPitch(
    pitch_type='statsbomb',
    half=True,
    pitch_color='#22312b',
    line_color='#c7d5cc',
    linewidth=1.2
)

fig, ax = pitch.draw(figsize=(6,8))

# ==========================
# 4. SETAS DAS CORRIDAS
# ==========================
pitch.arrows(
    df["x_start"],
    df["y_start"],
    df["x_end"],
    df["y_end"],
    width=1.5,
    headwidth=6,
    headlength=6,
    color="#3e5ff5",
    alpha=0.75,
    ax=ax
)

# ==========================
# 5. MARCAR INÍCIO DAS CORRIDAS
# ==========================
pitch.scatter(
    df["x_start"],
    df["y_start"],
    s=60,
    color="#fcfcfc",
    edgecolors='white',
    linewidth=1,
    zorder=3,
    ax=ax
)

# ==========================
# 6. TÍTULO
# ==========================
ax.set_title(
    f"{player_name} – Progressive Carries",
    fontsize=20,
    color='white',
    pad=20
)

# ==========================
# 7. SALVAR EM BUFFER COM DPI MENOR
# ==========================
buf = BytesIO()
fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
buf.seek(0)

# ==========================
# 8. EXIBIR NO STREAMLIT
# ==========================
col1, col2, col3 = st.columns([1,2,1])  # coluna central maior

with col2:
    st.image(buf, width=600)  # define largura em pixels

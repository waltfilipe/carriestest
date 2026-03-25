import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd
from streamlit_image_coordinates import streamlit_image_coordinates
from io import BytesIO
import numpy as np
from PIL import Image
from matplotlib.lines import Line2D

# ==========================
# Page Configuration
# ==========================
st.set_page_config(layout="wide", page_title="Duel Map Analysis")

st.title("Duel Map Analysis - Multiple Matches")
st.caption("Click on the icons on the pitch to play the corresponding video analysis.")

# ==========================
# Data Setup (All English labels with new data)
# ==========================
events_raw = [
    # -------- vs IMG --------
    ("DUEL OFENSIVO LOST", 35.40, 65.43, None),
    ("DUEL DEFENSIVO LOST", 24.43, 73.08, None),
    ("DUEL DEFENSIVO LOST", 65.49, 56.29, None),
    ("DUEL DEFENSIVO LOST", 53.35, 55.29, None),
    ("DUEL OFENSIVO LOST", 80.78, 66.93, None),
    ("AERIAL WON", 53.18, 33.18, None),
    
    # -------- vs Orlando --------
    ("DUEL OFENSIVO WON", 50.86, 55.79, None),
    ("DUEL DEFENSIVO WON", 56.68, 26.37, None),
    ("BLOQUEIO", 17.28, 49.64, None),
    ("FOULED", 80.45, 49.64, None),
    ("DUEL OFENSIVO LOST", 100.73, 41.00, None),
    ("INTERCEPTACAO", 82.61, 64.77, None),
    ("DUEL DEFENSIVO WON", 70.47, 55.96, None),
    
    # -------- vs Weston --------
    ("DUEL DEFENSIVO WON", 41.05, 27.20, None),
    ("INTERCEPT", 72.30, 10.08, None),
    ("DUEL DEFENSIVO WON", 33.90, 37.01, None),
    ("DUEL OFENSIVO LOST", 94.24, 36.51, None),
    ("DUEL OFENSIVO LOST", 33.90, 46.82, None),
    ("INTERCEPT", 33.57, 43.99, None),
    ("DUEL DEFENSIVO WON", 41.88, 12.74, None),
    ("DUEL DEFENSIVO WON", 38.22, 23.21, None),
    ("INTERCEPT", 69.14, 13.24, None),
    ("DUEL DEFENSIVO WON", 48.03, 14.73, None),
    ("DUEL DEFENSIVO LOST", 69.14, 41.83, None),
    ("INTERCEPT", 65.15, 52.47, None),
    ("FOULED", 40.22, 24.21, None),
    ("DUEL DEFENSIVO LOST", 35.90, 53.13, None),
    ("DUEL DEFENSIVO LOST", 57.51, 75.57, None),
    
    # -------- vs South Florida --------
    ("DUEL DEFENSIVO LOST", 20.79, 55.45, None),
    ("BLOQUEIO", 20.07, 47.68, None),
    ("AERIAL WON", 67.41, 24.73, None),
    ("DUEL DEFENSIVO WON", 27.11, 3.23, None),
    ("DUEL DEFENSIVO WON", 33.98, 14.43, None),
]

df = pd.DataFrame(events_raw, columns=["type", "x", "y", "video"])

def get_style(event_type, has_video):
    """Returns marker, color (rgba), size, and linewidth based on event type"""
    event_type = event_type.upper()
    
    # 1. DUELOS AÉREOS (Aerial Duels)
    if "AERIAL" in event_type:
        if "WON" in event_type:
            # Triangle up (Bright lime green)
            return '^', (0.2, 0.9, 0.2, 0.9), 120, 1.5
        if "LOST" in event_type:
            # Triangle down (Dark red)
            alpha = 0.9 if has_video else 0.15
            return 'v', (0.7, 0, 0, alpha), 120, 1.5

    # 2. DUELOS OFENSIVOS (Offensive Duels)
    if "OFENSIVO" in event_type:
        if "WON" in event_type:
            # Circle (Green)
            return 'o', (0, 0.7, 0, 0.9), 100, 0.5
        if "LOST" in event_type:
            # X marker (Red)
            alpha = 0.9 if has_video else 0.6
            return 'x', (0.9, 0.2, 0.2, alpha), 110, 2.8

    # 3. DUELOS DEFENSIVOS (Defensive Duels)
    if "DEFENSIVO" in event_type:
        if "WON" in event_type:
            # Square (Blue-green/Teal)
            return 's', (0, 0.7, 0.7, 0.9), 100, 0.5
        if "LOST" in event_type:
            # Diamond (Orange-red)
            alpha = 0.9 if has_video else 0.6
            return 'D', (0.9, 0.4, 0.1, alpha), 100, 2.2

    # 4. OTHER EVENTS
    if "BLOQUEIO" in event_type:
        # Star (Purple)
        return '*', (0.7, 0.3, 0.9, 0.8), 140, 0.5

    if "INTERCEPT" in event_type or "INTERCEPTACAO" in event_type:
        # Plus sign (Blue)
        return '+', (0.2, 0.5, 0.9, 0.8), 120, 2.0

    if "FOULED" in event_type:
        # Pentagon (Orange)
        return 'P', (1, 0.5, 0, 0.8), 110, 0.5

    # Default
    return 'o', (0.5, 0.5, 0.5, 0.8), 90, 0.5


# ==========================
# Main Layout
# ==========================
col_map, col_vid = st.columns([1, 1])

with col_map:
    st.subheader("Interactive Pitch Map")
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#f8f8f8', line_color='#4a4a4a')
    fig, ax = pitch.draw(figsize=(10, 7))

    for _, row in df.iterrows():
        has_vid = row["video"] is not None
        marker, color, size, lw = get_style(row["type"], has_vid)
        # Black border for events that contain video
        ec = 'black' if has_vid else color
        pitch.scatter(row.x, row.y, marker=marker, s=size, color=color,
                      edgecolors=ec, linewidths=lw, ax=ax, zorder=3)

    # Attack Arrow
    ax.annotate('', xy=(70, 83), xytext=(50, 83),
        arrowprops=dict(arrowstyle='->', color='#4a4a4a', lw=1.5))
    ax.text(60, 86, "Attack Direction", ha='center', va='center',
        fontsize=9, color='#4a4a4a', fontweight='bold')

    # Legend
    legend_elements = [
        # --- Offensive Duels ---
        Line2D([0], [0], marker='o', color='w', label='Offensive Duel Won',
               markerfacecolor=(0, 0.7, 0, 0.9), markersize=10, linestyle='None'),

        Line2D([0], [0], marker='x', color='w', label='Offensive Duel Lost',
               markeredgecolor=(0.9, 0.2, 0.2, 0.9), markersize=10, markeredgewidth=2.5, linestyle='None'),

        # --- Defensive Duels ---
        Line2D([0], [0], marker='s', color='w', label='Defensive Duel Won',
               markerfacecolor=(0, 0.7, 0.7, 0.9), markersize=10, linestyle='None'),

        Line2D([0], [0], marker='D', color='w', label='Defensive Duel Lost',
               markerfacecolor=(0.9, 0.4, 0.1, 0.9), markersize=10, linestyle='None'),

        # --- Aerial Duels ---
        Line2D([0], [0], marker='^', color='w', label='Aerial Won',
               markerfacecolor=(0.2, 0.9, 0.2, 0.9), markersize=10, linestyle='None'),

        Line2D([0], [0], marker='v', color='w', label='Aerial Lost',
               markerfacecolor=(0.7, 0, 0, 0.8), markersize=10, linestyle='None'),

        # --- Other Events ---
        Line2D([0], [0], marker='*', color='w', label='Block/Bloqueio',
               markerfacecolor=(0.7, 0.3, 0.9, 0.8), markersize=12, linestyle='None'),

        Line2D([0], [0], marker='+', color='w', label='Interception',
               markeredgecolor=(0.2, 0.5, 0.9, 0.8), markersize=10, markeredgewidth=2, linestyle='None'),

        Line2D([0], [0], marker='P', color='w', label='Fouled',
               markerfacecolor=(1, 0.5, 0, 0.8), markersize=10, linestyle='None'),
    ]

    # Apply legend to graphic
    legend = ax.legend(
        handles=legend_elements,
        loc='upper left',
        bbox_to_anchor=(0.01, 0.99),
        frameon=True,
        facecolor='white',
        edgecolor='#333333',
        fontsize='small',
        title="Match Events",
        title_fontsize='medium',
        labelspacing=1.2,
        borderpad=1.0
    )

    legend.get_title().set_fontweight('bold')

    # Convert plot to image for coordinate tracking
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_obj = Image.open(buf)

    # Use fixed width to ensure coordinate scaling works
    click = streamlit_image_coordinates(img_obj, width=700)

# ==========================
# Interaction Logic
# ==========================
selected_event = None

if click is not None:
    real_w, real_h = img_obj.size
    disp_w, disp_h = click["width"], click["height"]

    # Map pixel click to actual image pixels
    pixel_x = click["x"] * (real_w / disp_w)
    pixel_y = click["y"] * (real_h / disp_h)

    # Invert Y for Matplotlib logic and transform to pitch data coordinates
    mpl_pixel_y = real_h - pixel_y
    coords = ax.transData.inverted().transform((pixel_x, mpl_pixel_y))
    field_x, field_y = coords[0], coords[1]

    # Calculate distance to markers
    df["dist"] = np.sqrt((df["x"] - field_x)**2 + (df["y"] - field_y)**2)

    # Radius threshold for easier selection
    RADIUS = 5
    candidates = df[df["dist"] < RADIUS]

    if not candidates.empty:
        selected_event = candidates.loc[candidates["dist"].idxmin()]

# ==========================
# Video Display & Stats
# ==========================
with col_vid:
    st.subheader("Event Details")
    if selected_event is not None:
        st.success(f"**Selected Event:** {selected_event['type']}")
        st.info(f"**Position:** X: {selected_event['x']:.2f}, Y: {selected_event['y']:.2f}")

        if selected_event["video"]:
            try:
                st.video(selected_event["video"])
            except:
                st.error(f"Video file not found: {selected_event['video']}")
        else:
            st.warning("No video footage available for this specific event.")
    else:
        st.info("Select a marker on the pitch to view event details.")

    st.divider()
    st.subheader("Performance Statistics")

    # Prepare analysis data
    df['is_duel'] = df['type'].str.contains('DUEL|AERIAL', case=False)
    df['is_won'] = df['type'].str.contains('WON', case=False)
    df['is_offensive'] = df['type'].str.contains('OFENSIVO|OFFENSIVE', case=False)
    df['is_defensive'] = df['type'].str.contains('DEFENSIVO|DEFENSIVE', case=False)

    # Zone Logic (Statsbomb: Y goes from 0 to 80)
    # Central Corridor: 26.6 to 53.3 | Lateral: 0-26.6 and 53.3-80
    central_mask = (df['y'] > 26.6) & (df['y'] < 53.3)

    # Overall Duel Stats
    all_duels = df[df['is_duel']]
    total_duels = len(all_duels)
    won_duels = all_duels['is_won'].sum()
    overall_rate = (won_duels / total_duels * 100) if total_duels > 0 else 0

    # Offensive Duels
    offensive_duels = df[df['is_offensive'] & df['is_duel']]
    off_total = len(offensive_duels)
    off_wins = offensive_duels['is_won'].sum()
    off_rate = (off_wins / off_total * 100) if off_total > 0 else 0

    # Defensive Duels
    defensive_duels = df[df['is_defensive'] & df['is_duel']]
    def_total = len(defensive_duels)
    def_wins = defensive_duels['is_won'].sum()
    def_rate = (def_wins / def_total * 100) if def_total > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Duels", f"{won_duels}/{total_duels}", f"{overall_rate:.1f}% Success")
    col2.metric("Offensive Duels", f"{off_wins}/{off_total}", f"{off_rate:.1f}% Success")
    col3.metric("Defensive Duels", f"{def_wins}/{def_total}", f"{def_rate:.1f}% Success")

    st.divider()
    st.subheader("Zone Performance")

    # Central Stats (all duels)
    central_duels = df[central_mask & df['is_duel']]
    c_total = len(central_duels)
    c_wins = central_duels['is_won'].sum()
    c_rate = (c_wins / c_total * 100) if c_total > 0 else 0

    # Lateral Stats (all duels)
    lateral_duels = df[~central_mask & df['is_duel']]
    l_total = len(lateral_duels)
    l_wins = lateral_duels['is_won'].sum()
    l_rate = (l_wins / l_total * 100) if l_total > 0 else 0

    zc1, zc2 = st.columns(2)
    zc1.metric("Central Zone", f"{c_wins}/{c_total}", f"{c_rate:.1f}% Success")
    zc2.metric("Lateral Zones", f"{l_wins}/{l_total}", f"{l_rate:.1f}% Success")

    st.divider()
    st.subheader("Event Type Breakdown")

    # Count other events
    blocks = len(df[df['type'].str.contains('BLOQUEIO', case=False)])
    intercepts = len(df[df['type'].str.contains('INTERCEPT', case=False)])
    fouls = len(df[df['type'].str.contains('FOULED', case=False)])

    ec1, ec2, ec3 = st.columns(3)
    ec1.metric("Blocks", blocks)
    ec2.metric("Interceptions", intercepts)
    ec3.metric("Fouls", fouls)

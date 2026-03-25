# ════════════════════════════════════════════════════════════════
# DASHBOARD KPIs REC — Airbus OLMEM4
# Auteur  : Talel TAIEB — Octo Technology
# Projet  : A350 Freighter (MSN 700/701) & ULR (MSN 707/814)
# Stack   : Streamlit + Plotly
# Usage   : streamlit run dashboard.py
# ════════════════════════════════════════════════════════════════

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── PAGE CONFIG ──────────────────────────────────────────────────
st.set_page_config(
    page_title="REC KPIs — A350 Freighter & ULR",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── COLOR SYSTEM ─────────────────────────────────────────────────
MSN_COLORS  = {"700": "#2563EB", "701": "#60A5FA", "707": "#EA580C", "814": "#FB923C"}
FAL_COLORS  = {"PRE-FAL": "#16A34A", "FAL": "#2563EB", "WO NON CREE": "#9CA3AF"}
FREIGHTER   = ["700", "701"]
ULR         = ["707", "814"]

INFLOW_PALETTE = [
    "#2563EB","#60A5FA","#EA580C","#FB923C",
    "#16A34A","#4ADE80","#D97706","#FCD34D",
    "#7C3AED","#C4B5FD","#DC2626","#FCA5A5",
    "#0891B2","#67E8F9"
]

# ── CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #0D1117 !important;
    color: #E6EDF3 !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 3rem 2rem; max-width: 100%; }

/* Force dark sur tous les containers Streamlit */
.stApp { background: #0D1117 !important; }
[data-testid="stAppViewContainer"] { background: #0D1117 !important; }
[data-testid="stHeader"] { background: #0D1117 !important; }
section.main { background: #0D1117 !important; }
.main .block-container { background: #0D1117 !important; }

/* Radio buttons */
.stRadio label p { color: #E6EDF3 !important; }
[data-testid="stRadio"] > div { color: #E6EDF3 !important; }

/* Multiselect */
.stMultiSelect div[data-baseweb="select"] {
    background: #1C2333 !important;
    border-color: #30363D !important;
}
.stMultiSelect div[data-baseweb="select"] span { color: #E6EDF3 !important; }
.stMultiSelect [data-baseweb="tag"] {
    background: rgba(47,129,247,0.3) !important;
    color: #79C0FF !important;
}

/* Dropdown menu */
[data-baseweb="popover"] { background: #1C2333 !important; }
[data-baseweb="menu"] { background: #1C2333 !important; }
[data-baseweb="option"] { background: #1C2333 !important; color: #E6EDF3 !important; }
[data-baseweb="option"]:hover { background: #30363D !important; }

/* Button */
.stButton > button {
    background: #1C2333 !important;
    color: #E6EDF3 !important;
    border: 1px solid #30363D !important;
    border-radius: 6px !important;
}
.stButton > button:hover {
    background: #30363D !important;
    border-color: #7D8590 !important;
}

/* Plotly charts */
.js-plotly-plot .plotly, .stPlotlyChart { background: transparent !important; }

/* Expander */
.streamlit-expanderHeader {
    background: #161B22 !important;
    color: #E6EDF3 !important;
    border: 1px solid #30363D !important;
}
.streamlit-expanderContent {
    background: #161B22 !important;
    border: 1px solid #30363D !important;
}

/* Sticky header */
.sticky-header {
    position: fixed;
    top: 0;
    left: 300px;
    right: 0;
    z-index: 1000;
    background: #0D1117;
    border-bottom: 1px solid #21262D;
    padding: 0.6rem 2rem 0.5rem 2rem;
    display: flex;
    align-items: center;
}

/* Radio nav sticky juste sous le titre */
[data-testid="stRadio"] {
    position: fixed !important;
    top: 52px !important;
    left: 300px !important;
    right: 0 !important;
    z-index: 999 !important;
    background: #0D1117 !important;
    padding: 0.4rem 2rem !important;
    border-bottom: 2px solid #30363D !important;
    margin: 0 !important;
}
.sticky-title-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    color: #7D8590;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.15rem;
}
.sticky-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #E6EDF3;
    line-height: 1;
}
.sticky-nav {
    display: flex;
    gap: 0.4rem;
    align-items: center;
}
.nav-btn {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.35rem 0.75rem;
    border-radius: 6px;
    border: 1px solid #30363D;
    background: transparent;
    color: #7D8590;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.15s;
}
.nav-btn.active {
    background: #2F81F7;
    border-color: #2F81F7;
    color: white;
}
.nav-btn:hover { background: #1C2333; color: #E6EDF3; border-color: #7D8590; }

/* Offset content so it doesn't hide under sticky header */
.content-offset { margin-top: 6.5rem; }

[data-testid="stSidebar"] {
    background: #161B22;
    border-right: 1px solid #30363D;
}
[data-testid="stSidebar"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #7D8590 !important;
}

.kpi-card {
    background: #161B22;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    border: 1px solid #30363D;
    border-top: 3px solid;
    height: 100%;
}
.kpi-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #7D8590;
    margin-bottom: 0.4rem;
}
.kpi-value { font-size: 1.8rem; font-weight: 700; color: #E6EDF3; line-height: 1; }
.kpi-sub { font-family: 'DM Mono', monospace; font-size: 0.62rem; color: #7D8590; margin-top: 0.2rem; }

.prog-header {
    display: flex; align-items: center; gap: 0.6rem;
    margin: 1.8rem 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid #30363D;
}
.prog-dot { width: 10px; height: 10px; border-radius: 3px; flex-shrink: 0; }
.prog-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem; font-weight: 500;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #7D8590;
}

.chart-card {
    background: #161B22;
    border-radius: 12px;
    border: 1px solid #30363D;
    padding: 1rem;
    margin-bottom: 1rem;
}

.qtable { background:#161B22; border-radius:12px; border:1px solid #30363D; overflow:hidden; }
.qrow {
    display:flex; align-items:flex-start; justify-content:space-between;
    padding:0.9rem 1.2rem; border-bottom:1px solid #21262D; gap:1rem;
}
.qrow:last-child { border-bottom:none; }
.qlabel { font-weight:600; font-size:0.85rem; color:#E6EDF3; }
.qdetail { font-family:'DM Mono',monospace; font-size:0.68rem; color:#7D8590; margin-top:0.15rem; }
.qaction { font-size:0.72rem; color:#2F81F7; margin-top:0.2rem; }
.qbadge {
    font-family:'DM Mono',monospace; font-size:0.62rem; font-weight:600;
    padding:0.2rem 0.6rem; border-radius:20px; white-space:nowrap; flex-shrink:0;
}
.ok   { background:rgba(63,185,80,0.15);  color:#3FB950; }
.warn { background:rgba(210,153,34,0.15); color:#D29922; }
.err  { background:rgba(247,129,102,0.15); color:#F78166; }

.badge-fr {
    display:inline-block; background:rgba(47,129,247,0.15); color:#79C0FF;
    font-family:'DM Mono',monospace; font-size:0.62rem;
    padding:0.2rem 0.7rem; border-radius:4px; border:1px solid rgba(47,129,247,0.3); margin-right:0.4rem;
}
.badge-ulr {
    display:inline-block; background:rgba(234,88,12,0.15); color:#FB923C;
    font-family:'DM Mono',monospace; font-size:0.62rem;
    padding:0.2rem 0.7rem; border-radius:4px; border:1px solid rgba(234,88,12,0.3);
}
</style>
""", unsafe_allow_html=True)


# ── PLOTLY THEME ─────────────────────────────────────────────────
def theme(title="", h=360):
    return dict(
        title=dict(text=title, font=dict(size=11, color="#7D8590", family="DM Mono"), x=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#E6EDF3", size=11),
        height=h, margin=dict(l=10, r=10, t=38, b=28),
        legend=dict(bgcolor="rgba(22,27,34,0.9)", bordercolor="#30363D",
                    borderwidth=1, font=dict(size=10, color="#E6EDF3")),
        xaxis=dict(gridcolor="#21262D", linecolor="#30363D",
                   tickfont=dict(size=10, color="#7D8590")),
        yaxis=dict(gridcolor="#21262D", linecolor="#30363D",
                   tickfont=dict(size=10, color="#7D8590")),
    )


# ════════════════════════════════════════════════════════════════
# CHARGEMENT
# ════════════════════════════════════════════════════════════════
@st.cache_data
def process(raw_bytes):
    import io
    df = pd.read_csv(io.BytesIO(raw_bytes))
    df['NUM_MSN'] = pd.to_numeric(df['NUM_MSN'], errors='coerce')
    df = df[df['NUM_MSN'].notna()].copy()
    df['NUM_MSN'] = df['NUM_MSN'].astype(int).astype(str)
    df = df[df['NUM_MSN'].isin(["700","701","707","814"])].copy()
    df['TIME_REAL_HOURS'] = pd.to_numeric(df['TIME_REAL_HOURS'], errors='coerce').fillna(0)
    if 'ORIGIN_DISPLAY' not in df.columns and 'ORIGIN TYPE' in df.columns:
        df['ORIGIN_DISPLAY'] = df['ORIGIN TYPE'].fillna('NON RENSEIGNE')
    elif 'ORIGIN_DISPLAY' in df.columns:
        df['ORIGIN_DISPLAY'] = df['ORIGIN_DISPLAY'].fillna('NON RENSEIGNE')
    df['SECTION']      = df['SECTION'].fillna('N/A') if 'SECTION' in df.columns else 'N/A'
    df['FAL_CATEGORY'] = df['FAL_CATEGORY'].fillna('WO NON CREE') if 'FAL_CATEGORY' in df.columns else 'WO NON CREE'
    q = dict(
        total        = len(df),
        others       = int(df['ORIGIN_DISPLAY'].str.lower().str.contains('others', na=False).sum()),
        first_null   = int(df['FIRST ORIGIN'].isna().sum()) if 'FIRST ORIGIN' in df.columns else 0,
        wo_non_cree  = int((df['FAL_CATEGORY']=='WO NON CREE').sum()),
        time_zero    = int((df['TIME_REAL_HOURS']==0).sum()),
        msn700_prefal= int(((df['NUM_MSN']=='700')&(df['FAL_CATEGORY']=='PRE-FAL')).sum()),
    )
    return df, q

uploaded = st.sidebar.file_uploader("Charger fichier CSV (MEFU transforme)", type="csv")

if uploaded is None:
    st.markdown(
        "<div style='display:flex;flex-direction:column;align-items:center;"
        "justify-content:center;height:60vh;gap:1.5rem;'>"
        "<div style='font-size:3rem;'>✈️</div>"
        "<div style='font-family:sans-serif;font-size:1.8rem;font-weight:800;color:#E6EDF3;'>"
        "Dashboard KPIs REC</div>"
        "<div style='font-family:monospace;font-size:0.8rem;color:#7D8590;'>"
        "Airbus OLMEM4 - A350 Freighter et ULR</div>"
        "<div style='background:#161B22;border:1px dashed #30363D;border-radius:12px;"
        "padding:2rem 3rem;text-align:center;margin-top:1rem;'>"
        "<div style='font-family:monospace;font-size:0.75rem;color:#7D8590;"
        "margin-bottom:0.5rem;text-transform:uppercase;'>Pour demarrer</div>"
        "<div style='font-size:0.95rem;color:#E6EDF3;'>"
        "Chargez votre fichier <b>mefu_transformed.csv</b><br>dans le panneau de gauche</div>"
        "<div style='font-family:monospace;font-size:0.68rem;color:#2F81F7;margin-top:0.8rem;'>"
        "Les donnees restent sur votre poste - Aucun transfert reseau</div>"
        "</div></div>",
        unsafe_allow_html=True
    )
    st.stop()

df, Q = process(uploaded.read())


# ════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 1.2rem;border-bottom:1px solid #30363D;margin-bottom:1.2rem;'>
        <div style='font-family:DM Mono;font-size:0.58rem;color:#7D8590;
                    text-transform:uppercase;letter-spacing:0.1em;'>Airbus OLMEM4</div>
        <div style='font-size:1.1rem;font-weight:700;color:#E6EDF3;margin-top:0.2rem;'>REC KPIs</div>
        <div style='font-family:DM Mono;font-size:0.62rem;color:#2F81F7;margin-top:0.15rem;'>
            A350 Freighter &amp; ULR</div>
    </div>""", unsafe_allow_html=True)

    sel_msn  = st.multiselect("MSN", sorted(df['NUM_MSN'].unique()),
                               default=[], help="Vide = tout affiché")
    sel_sec  = st.multiselect("Section", sorted(df['SECTION'].dropna().unique()),
                               default=[])
    ca_opts  = sorted(df['CA'].dropna().unique()) if 'CA' in df.columns else []
    sel_ca   = st.multiselect("CA", ca_opts, default=[])
    sel_ori  = st.multiselect("Type Inflow", sorted(df['ORIGIN_DISPLAY'].dropna().unique()),
                               default=[])
    sel_fal  = st.multiselect("Inflow Creation", sorted(df['FAL_CATEGORY'].dropna().unique()),
                               default=[])
    st.markdown("---")
    excl_wr  = st.toggle("Exclure les points WR", value=False)

    if st.button("↺ Reset filtres", use_container_width=True):
        sel_msn = []
        sel_sec = []
        sel_ca  = []
        sel_ori = []
        sel_fal = []

    st.markdown(f"""
    <div style='margin-top:1.2rem;padding-top:1rem;border-top:1px solid #30363D;
                font-family:DM Mono;font-size:0.6rem;color:#7D8590;'>
        {Q['total']:,} lignes · 4 MSNs
    </div>""", unsafe_allow_html=True)

# ── Apply filters ────────────────────────────────────────────────
filt = df.copy()
if sel_msn: filt = filt[filt['NUM_MSN'].isin(sel_msn)]
if sel_sec: filt = filt[filt['SECTION'].isin(sel_sec)]
if sel_ca and 'CA' in filt.columns: filt = filt[filt['CA'].isin(sel_ca)]
if sel_ori: filt = filt[filt['ORIGIN_DISPLAY'].isin(sel_ori)]
if sel_fal: filt = filt[filt['FAL_CATEGORY'].isin(sel_fal)]
if excl_wr and 'IS_WR' in filt.columns:
    filt = filt[~filt['IS_WR']]
# Moyenne sans WR (0h biaise le calcul)
if 'W/O OR ROUTING' in filt.columns:
    filt_avg = filt[filt['W/O OR ROUTING'].astype(str).str.strip().str.upper() != 'WR']
else:
    filt_avg = filt.copy()

fr      = filt[filt['NUM_MSN'].isin(FREIGHTER)]
ulr     = filt[filt['NUM_MSN'].isin(ULR)]
fr_avg  = filt_avg[filt_avg['NUM_MSN'].isin(FREIGHTER)]
ulr_avg = filt_avg[filt_avg['NUM_MSN'].isin(ULR)]


# ════════════════════════════════════════════════════════════════
# HEADER STICKY + NAV FONCTIONNELLE
# ════════════════════════════════════════════════════════════════
# Titre sticky via CSS + radio Streamlit rendu sticky via CSS

st.markdown("""
<div class="sticky-header">
    <div>
        <div class="sticky-title-sub">Rework Electric Center - OLMEM4</div>
        <div class="sticky-title">Dashboard KPIs
            <span class="badge-fr" style="margin-left:0.8rem;">✈ Freighter MSN 700 701</span>
            <span class="badge-ulr">✈ ULR MSN 707 814</span>
        </div>
    </div>
</div>
<div class="content-offset"></div>
""", unsafe_allow_html=True)

page = st.radio("", ["Vue Générale","Par Section","Par CA","Par Type Inflow","PRE-FAL vs FAL","Qualité Données","Données"],
                horizontal=True, label_visibility="collapsed")
st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════
def prog_header(title, color):
    st.markdown(f"""<div class="prog-header">
        <div class="prog-dot" style="background:{color};"></div>
        <div class="prog-title">{title}</div>
    </div>""", unsafe_allow_html=True)


def kpi_row(data, data_avg, accent):
    pts  = len(data)
    hrs  = data['TIME_REAL_HOURS'].sum()
    avg  = data_avg['TIME_REAL_HOURS'].mean() if len(data_avg) else 0
    hdv     = data['IS_HANDOVER'].sum() if 'IS_HANDOVER' in data.columns else 0
    pct_hdv = hdv / max(pts, 1) * 100
    c1,c2,c3,c4 = st.columns(4)
    for col, lbl, val, sub in [
        (c1,"Points total",f"{pts:,}","lignes analysées"),
        (c2,"Heures totales",f"{hrs:,.0f}h","temps réel cumulé"),
        (c3,"Moy. par point",f"{avg:.1f}h","hors points WR"),
        (c4,"Handover",f"{pct_hdv:.0f}%",f"{hdv} pts handover"),
    ]:
        with col:
            st.markdown(f"""<div class="kpi-card" style="border-top-color:{accent};">
                <div class="kpi-label">{lbl}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)


def bar_by_section(data, msns, metric, x_col='SECTION', ylabel='', title=''):
    if metric == 'count':
        agg = data[data['NUM_MSN'].isin(msns)]\
              .groupby([x_col,'NUM_MSN']).size().reset_index(name='v')
    else:
        agg = data[data['NUM_MSN'].isin(msns)]\
              .groupby([x_col,'NUM_MSN'])[metric].sum().reset_index()
        agg.columns = [x_col,'NUM_MSN','v']
        agg['v'] = agg['v'].round(1)

    # Ordre personnalisé : HTP/VTP et N/A toujours à la fin
    if x_col == 'SECTION':
        end_vals = ['HTP/VTP', 'N/A']
        all_x = sorted(agg[x_col].dropna().unique())
        ordered_x = [x for x in all_x if x not in end_vals] + [x for x in end_vals if x in all_x]
        agg[x_col] = pd.Categorical(agg[x_col], categories=ordered_x, ordered=True)
        agg = agg.sort_values(x_col)

    fig = go.Figure()
    for msn in msns:
        s = agg[agg['NUM_MSN']==msn]
        fig.add_trace(go.Bar(
            name=f"MSN {msn}", x=s[x_col], y=s['v'],
            marker_color=MSN_COLORS[msn],
            marker_line=dict(color='white',width=1.5),
            text=s['v'].apply(lambda v: f"{v:,.0f}"),
            textposition='outside', textfont_size=10,
            hovertemplate=f"MSN {msn} · %{{x}}<br>{ylabel}: %{{y:,.1f}}<extra></extra>"
        ))
    t = theme(title, h=360)
    t['barmode'] = 'group'
    t['xaxis']['title'] = dict(text=x_col, font=dict(size=10,color='#7D8590'))
    t['yaxis']['title'] = dict(text=ylabel, font=dict(size=10,color='#7D8590'))
    fig.update_layout(**t)
    return fig


def pies_by_msn(data, msns, metric, title_suffix):
    cols = st.columns(len(msns))
    # Couleurs fixes basées sur toutes les catégories du dataset complet
    # On utilise df global pour que le mapping soit stable quel que soit le filtre
    all_cats = sorted(df['ORIGIN_DISPLAY'].dropna().unique())
    color_map = {c: INFLOW_PALETTE[i%len(INFLOW_PALETTE)] for i,c in enumerate(all_cats)}

    for i, msn in enumerate(msns):
        sub = data[data['NUM_MSN']==msn]
        if metric == 'count':
            agg = sub.groupby('ORIGIN_DISPLAY').size().reset_index(name='v')
        else:
            agg = sub.groupby('ORIGIN_DISPLAY')[metric].sum().reset_index()
            agg.columns = ['ORIGIN_DISPLAY','v']
        agg = agg[agg['v']>0].sort_values('v',ascending=False)
        total = agg['v'].sum()
        unit  = "h" if metric!='count' else " pts"

        fig = go.Figure(go.Pie(
            labels=agg['ORIGIN_DISPLAY'], values=agg['v'],
            hole=0.44,
            textposition='inside', textinfo='percent',
            textfont=dict(size=9,color='white'),
            marker=dict(
                colors=[color_map.get(c,'#999') for c in agg['ORIGIN_DISPLAY']],
                line=dict(color='white',width=2)
            ),
            hovertemplate='<b>%{label}</b><br>%{value:,.1f}%{customdata}<br>%{percent}<extra></extra>',
            customdata=[unit]*len(agg)
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=310,
            title=dict(text=f"<b>MSN {msn}</b>", font=dict(
                size=13, color=MSN_COLORS[msn], family="DM Sans"), x=0.5),
            annotations=[dict(
                text=f"<b>{total:,.0f}{unit}</b>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=12, color="#0F172A", family="DM Sans"),
                xanchor='center'
            )],
            showlegend=True,
            legend=dict(font=dict(size=8), orientation='v',
                        x=1.01, y=0.5, bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0,r=90,t=42,b=10),
            font=dict(family="DM Sans")
        )
        with cols[i]:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)


def bar_fal(data, msns, metric, ylabel, title):
    if metric == 'count':
        agg = data[data['NUM_MSN'].isin(msns)]\
              .groupby(['NUM_MSN','FAL_CATEGORY']).size().reset_index(name='v')
    else:
        agg = data[data['NUM_MSN'].isin(msns)]\
              .groupby(['NUM_MSN','FAL_CATEGORY'])[metric].sum().reset_index()
        agg.columns = ['NUM_MSN','FAL_CATEGORY','v']
        agg['v'] = agg['v'].round(1)

    fig = go.Figure()
    for cat in ['PRE-FAL','FAL','WO NON CREE']:
        s = agg[agg['FAL_CATEGORY']==cat]
        if s.empty: continue
        fig.add_trace(go.Bar(
            name=cat, x=s['NUM_MSN'], y=s['v'],
            marker_color=FAL_COLORS[cat],
            marker_line=dict(color='white',width=1.5),
            text=s['v'].apply(lambda v: f"{v:,.0f}"),
            textposition='outside', textfont_size=11,
            hovertemplate=f"{cat}<br>MSN: %{{x}}<br>{ylabel}: %{{y:,.1f}}<extra></extra>"
        ))
    t = theme(title, h=360)
    t['barmode'] = 'group'
    t['xaxis']['title'] = dict(text='MSN', font=dict(size=10,color='#64748B'))
    t['yaxis']['title'] = dict(text=ylabel, font=dict(size=10,color='#64748B'))
    fig.update_layout(**t)
    return fig


# ════════════════════════════════════════════════════════════════
# PAGE — VUE GÉNÉRALE
# ════════════════════════════════════════════════════════════════
if page == "Vue Générale":

    msn_info = [
        ("700", "A350 Freighter", "#2563EB"),
        ("701", "A350 Freighter", "#60A5FA"),
        ("707", "A350 ULR",       "#EA580C"),
        ("814", "A350 ULR",       "#FB923C"),
    ]

    for msn, prog, accent in msn_info:
        data_msn     = filt[filt['NUM_MSN'] == msn]
        data_msn_avg = filt_avg[filt_avg['NUM_MSN'] == msn]

        prog_header(f"{prog} — MSN {msn}", accent)

        pts     = len(data_msn)
        hrs     = data_msn['TIME_REAL_HOURS'].sum()
        avg     = data_msn_avg['TIME_REAL_HOURS'].mean() if len(data_msn_avg) else 0
        hdv     = int(data_msn['IS_HANDOVER'].sum()) if 'IS_HANDOVER' in data_msn.columns else 0
        pct_hdv = hdv / max(pts, 1) * 100

        c1, c2, c3, c4 = st.columns(4)
        for col, lbl, val, sub in [
            (c1, "Points total",  f"{pts:,}",         "lignes analysées"),
            (c2, "Heures totales",f"{hrs:,.0f}h",     "temps réel cumulé"),
            (c3, "Moy. par point",f"{avg:.1f}h",      "hors points WR"),
            (c4, "Handover",      f"{pct_hdv:.0f}%",  f"{hdv} pts handover"),
        ]:
            with col:
                st.markdown(f'''<div class="kpi-card" style="border-top-color:{accent};">
                    <div class="kpi-label">{lbl}</div>
                    <div class="kpi-value">{val}</div>
                    <div class="kpi-sub">{sub}</div>
                </div>''', unsafe_allow_html=True)

        st.markdown("<div style='height:0.3rem;'></div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# PAGE — PAR CA
# ════════════════════════════════════════════════════════════════
elif page == "Par CA":
    if 'CA' not in filt.columns:
        st.warning("Colonne CA non disponible dans le dataset.")
    else:
        top_n = st.slider("Top N CA a afficher", min_value=5, max_value=30, value=15, step=5)

        def bar_top_ca(data, msns, metric, ylabel, title):
            if metric == 'count':
                agg2 = data[data['NUM_MSN'].isin(msns)].groupby(['CA','NUM_MSN']).size().reset_index(name='v')
                total_by_ca = data[data['NUM_MSN'].isin(msns)].groupby('CA').size()
            else:
                agg2 = data[data['NUM_MSN'].isin(msns)].groupby(['CA','NUM_MSN'])[metric].sum().reset_index()
                agg2.columns = ['CA','NUM_MSN','v']
                agg2['v'] = agg2['v'].round(1)
                total_by_ca = data[data['NUM_MSN'].isin(msns)].groupby('CA')[metric].sum()
            top_cas = total_by_ca.nlargest(top_n).index.tolist()
            agg2 = agg2[agg2['CA'].isin(top_cas)]
            order = total_by_ca[top_cas].sort_values(ascending=True).index.tolist()
            fig = go.Figure()
            for msn in msns:
                s = agg2[agg2['NUM_MSN']==msn]
                fig.add_trace(go.Bar(
                    name=f"MSN {msn}", y=s['CA'], x=s['v'],
                    orientation='h',
                    marker_color=MSN_COLORS[msn],
                    marker_line=dict(color='rgba(0,0,0,0)', width=0),
                    text=s['v'].apply(lambda v: f"{v:,.0f}"),
                    textposition='outside', textfont_size=10,
                    hovertemplate=f"MSN {msn} - %{{y}}<br>{ylabel}: %{{x:,.1f}}<extra></extra>"
                ))
            t = theme(title, h=max(320, top_n * 30))
            t['barmode'] = 'group'
            t['yaxis']['categoryorder'] = 'array'
            t['yaxis']['categoryarray'] = order
            t['xaxis']['title'] = dict(text=ylabel, font=dict(size=10, color='#7D8590'))
            fig.update_layout(**t)
            return fig

        prog_header("A350 Freighter - MSN 700 &amp; 701", "#2563EB")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(bar_top_ca(fr, FREIGHTER, 'count', 'Nombre de points',
                            f'Top {top_n} CA - Nombre de points'), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(bar_top_ca(fr, FREIGHTER, 'TIME_REAL_HOURS', 'Heures',
                            f'Top {top_n} CA - Heures'), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        prog_header("A350 ULR - MSN 707 &amp; 814", "#EA580C")
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(bar_top_ca(ulr, ULR, 'count', 'Nombre de points',
                            f'Top {top_n} CA - Nombre de points'), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(bar_top_ca(ulr, ULR, 'TIME_REAL_HOURS', 'Heures',
                            f'Top {top_n} CA - Heures'), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)


# PAGE — PAR SECTION
# ════════════════════════════════════════════════════════════════
elif page == "Par Section":

    prog_header("A350 Freighter — MSN 700 &amp; 701", "#2563EB")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(bar_by_section(fr, FREIGHTER, 'count', 'SECTION', 'Nombre de points', 'Nombre de points par Section'),
                        use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(bar_by_section(fr, FREIGHTER, 'TIME_REAL_HOURS', 'SECTION', 'Heures', 'Heures par Section'),
                        use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    prog_header("A350 ULR — MSN 707 &amp; 814", "#EA580C")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(bar_by_section(ulr, ULR, 'count', 'SECTION', 'Nombre de points', 'Nombre de points par Section'),
                        use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(bar_by_section(ulr, ULR, 'TIME_REAL_HOURS', 'SECTION', 'Heures', 'Heures par Section'),
                        use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# PAGE — PAR TYPE INFLOW
# ════════════════════════════════════════════════════════════════
elif page == "Par Type Inflow":

    prog_header("A350 Freighter — Nombre de points", "#2563EB")
    pies_by_msn(fr, FREIGHTER, 'count', 'pts')

    prog_header("A350 Freighter — Heures", "#2563EB")
    pies_by_msn(fr, FREIGHTER, 'TIME_REAL_HOURS', 'h')

    prog_header("A350 ULR — Nombre de points", "#EA580C")
    pies_by_msn(ulr, ULR, 'count', 'pts')

    prog_header("A350 ULR — Heures", "#EA580C")
    pies_by_msn(ulr, ULR, 'TIME_REAL_HOURS', 'h')


# ════════════════════════════════════════════════════════════════
# PAGE — PRE-FAL vs FAL
# ════════════════════════════════════════════════════════════════
elif page == "PRE-FAL vs FAL":

    prog_header("A350 Freighter — MSN 700 &amp; 701", "#2563EB")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(bar_fal(fr, FREIGHTER, 'count',
                        'Nombre de points', 'Nombre de points — PRE-FAL vs FAL'),
                        use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(bar_fal(fr, FREIGHTER, 'TIME_REAL_HOURS',
                        'Heures', 'Heures cumulées — PRE-FAL vs FAL'),
                        use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    prog_header("A350 ULR — MSN 707 &amp; 814", "#EA580C")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(bar_fal(ulr, ULR, 'count',
                        'Nombre de points', 'Nombre de points — PRE-FAL vs FAL'),
                        use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(bar_fal(ulr, ULR, 'TIME_REAL_HOURS',
                        'Heures', 'Heures cumulées — PRE-FAL vs FAL'),
                        use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("🔍 Split détaillé — Section × Catégorie FAL"):
        for prog, msns, color in [("Freighter", FREIGHTER,"#2563EB"),("ULR",ULR,"#EA580C")]:
            sub = filt[filt['NUM_MSN'].isin(msns)]
            agg = sub.groupby(['SECTION','FAL_CATEGORY']).size().reset_index(name='n')
            fig = px.bar(agg, x='SECTION', y='n', color='FAL_CATEGORY',
                         color_discrete_map=FAL_COLORS, barmode='stack',
                         title=f"{prog} — Répartition par Section",
                         labels={'n':'Nombre de points','SECTION':'Section'})
            fig.update_layout(**theme(h=320))
            st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════
# PAGE — QUALITÉ DONNÉES
# ════════════════════════════════════════════════════════════════
elif page == "Qualité Données":

    prog_header("Points qualité — À valider avec Anne-Laure", "#D97706")

    total = Q['total']
    def pct(v): return f"{v/total*100:.1f}%"
    def bc(v, t1=0.05, t2=0.15):
        p = v/total
        if p==0:  return 'ok',   '✓ OK'
        if p<t1:  return 'warn', f'⚠ {pct(v)}'
        if p<t2:  return 'warn', f'⚠ {pct(v)}'
        return 'err', f'✗ {pct(v)}'

    issues = [
        dict(label="ORIGIN TYPE = Others", value=Q['others'],
             detail=f"{Q['others']:,} lignes sans catégorie standardisée",
             action="Demander à Anne-Laure les règles de mapping FIRST ORIGIN → ORIGIN TYPE"),
        dict(label="FIRST ORIGIN vide", value=Q['first_null'],
             detail=f"{Q['first_null']:,} lignes sans information sur l'origine",
             action="Vérifier dans MEFU pourquoi ces champs ne sont pas renseignés"),
        dict(label="WO NON CREE (W/O CREATION DATE vide)", value=Q['wo_non_cree'],
             detail=f"{Q['wo_non_cree']:,} points sans Work Order créé",
             action="Valider si ces points sont en attente fabricant ou abandonnés"),
        dict(label="TIME REAL = 0h", value=Q['time_zero'],
             detail=f"{Q['time_zero']:,} points avec temps nul (valeur 1900-01-00)",
             action="Confirmer si 0h = non renseigné ou réellement 0 heure travaillée"),
        dict(label="MSN 700 — PRE-FAL = 0", value=Q['msn700_prefal'],
             detail="Aucun point PRE-FAL sur MSN 700 — résultat suspect",
             action="Confirmer la date d'entrée en FAL du MSN 700 (actuellement 2025-08-21)"),
    ]

    st.markdown('<div class="qtable">', unsafe_allow_html=True)
    for iss in issues:
        cls, lbl = bc(iss['value'])
        st.markdown(f"""<div class="qrow">
            <div style="flex:1;">
                <div class="qlabel">{iss['label']}</div>
                <div class="qdetail">{iss['detail']}</div>
                <div class="qaction">→ {iss['action']}</div>
            </div>
            <span class="qbadge {cls}">{iss['value']:,} · {lbl}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    prog_header("Visualisation", "#64748B")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        od = filt['ORIGIN_DISPLAY'].value_counts().reset_index()
        od.columns = ['Type','Count']
        od['color'] = od['Type'].apply(
            lambda t: '#DC2626' if t.lower()=='others' else '#2563EB')
        fig = go.Figure([go.Bar(
            x=od['Count'], y=od['Type'], orientation='h',
            marker_color=od['color'],
            text=od['Count'], textposition='outside',
            hovertemplate='%{y}: %{x} points<extra></extra>'
        )])
        t = theme("Distribution ORIGIN TYPE", h=380)
        t['yaxis']['autorange'] = 'reversed'
        fig.update_layout(**t)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fd = filt['FAL_CATEGORY'].value_counts().reset_index()
        fd.columns = ['Cat','Count']
        fig = go.Figure([go.Pie(
            labels=fd['Cat'], values=fd['Count'], hole=0.45,
            marker=dict(colors=[FAL_COLORS.get(c,'#999') for c in fd['Cat']],
                        line=dict(color='white',width=2)),
            textinfo='percent+label', textfont_size=11,
            hovertemplate='%{label}<br>%{value:,} points<br>%{percent}<extra></extra>'
        )])
        fig.update_layout(**theme("Répartition FAL_CATEGORY", h=380))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# PAGE — DONNÉES
# ════════════════════════════════════════════════════════════════
elif page == "Données":

    prog_header("Explorateur de données", "#7D8590")

    display_cols = list(filt.columns)
    col_sel = st.multiselect(
        "Colonnes a afficher",
        options=display_cols,
        default=display_cols[:min(10, len(display_cols))]
    )

    if not col_sel:
        st.warning("Selectionnez au moins une colonne.")
    else:
        view_df = filt[col_sel].copy()

        search = st.text_input("Recherche dans toutes les colonnes", placeholder="Tapez pour filtrer...")
        if search:
            mask = view_df.apply(lambda col: col.astype(str).str.contains(search, case=False, na=False)).any(axis=1)
            view_df = view_df[mask]

        st.markdown(f"<div style='font-family:monospace;font-size:0.7rem;color:#7D8590;margin-bottom:0.8rem;'>{len(view_df):,} lignes · {len(col_sel)} colonnes affichees</div>", unsafe_allow_html=True)

        col_config = {}
        if 'TIME_REAL_HOURS' in col_sel:
            col_config['TIME_REAL_HOURS'] = st.column_config.NumberColumn('Heures reelles', format="%.2f h")
        if 'IS_WR' in col_sel:
            col_config['IS_WR'] = st.column_config.CheckboxColumn('WR ?')
        if 'IS_HANDOVER' in col_sel:
            col_config['IS_HANDOVER'] = st.column_config.CheckboxColumn('Handover ?')

        st.dataframe(view_df, use_container_width=True, height=600, column_config=col_config)

        csv = view_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Exporter la vue en CSV",
            data=csv,
            file_name="rec_kpis_export.csv",
            mime="text/csv",
        )
"""
MMS Recruitment Analytics Dashboard
Premium executive-grade Streamlit application for HR recruitment analytics.
"""

import os
import base64
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="MMS Recruitment Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# BRAND CONSTANTS
# ============================================================================
PURPLE = "#666EFF"
PURPLE_DARK = "#4348C7"
GREEN = "#30BFA6"
WHITE = "#FFFFFF"
LGRAY = "#EDEDEE"
DGRAY = "#2B2B2B"
RED = "#E8604C"
AMBER = "#F4A623"

CHART_SEQUENCE = [PURPLE, GREEN, AMBER, "#9AA0FF", "#7FE0CF", RED, "#B5B9FF", "#2B2B2B"]

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "Data.xlsx")
LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

NA_LABEL = "Not Specified"


# ============================================================================
# CUSTOM CSS
# ============================================================================
def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        #MainMenu, footer, header {{visibility: hidden;}}

        .stApp {{
            background-color: {LGRAY};
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {DGRAY} 0%, #1c1c24 100%);
        }}
        section[data-testid="stSidebar"] * {{
            color: {WHITE} !important;
        }}
        section[data-testid="stSidebar"] .stRadio label {{
            font-size: 14px;
        }}
        section[data-testid="stSidebar"] hr {{
            border-color: rgba(255,255,255,0.15);
        }}

        div[data-testid="stMetric"] {{
            display: none;
        }}

        .block-container {{
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }}

        .mms-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: {WHITE};
            border-radius: 16px;
            padding: 18px 28px;
            margin-bottom: 18px;
            box-shadow: 0 4px 18px rgba(43,43,43,0.06);
        }}
        .mms-header h1 {{
            font-size: 22px;
            font-weight: 800;
            color: {DGRAY};
            margin: 0;
        }}
        .mms-header p {{
            font-size: 13px;
            color: #8A8D93;
            margin: 0;
        }}
        .mms-badge {{
            background: {LGRAY};
            color: {DGRAY};
            font-size: 12px;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 999px;
        }}

        .kpi-card {{
            background: {WHITE};
            border-radius: 16px;
            padding: 16px 18px;
            box-shadow: 0 4px 16px rgba(43,43,43,0.06);
            border-left: 5px solid {PURPLE};
            height: 112px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: transform 0.15s ease;
        }}
        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 22px rgba(43,43,43,0.12);
        }}
        .kpi-label {{
            font-size: 12px;
            font-weight: 600;
            color: #8A8D93;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            margin-bottom: 6px;
        }}
        .kpi-value {{
            font-size: 26px;
            font-weight: 800;
            color: {DGRAY};
        }}
        .kpi-sub {{
            font-size: 11.5px;
            color: #A2A5AB;
            margin-top: 2px;
        }}

        .section-card {{
            background: {WHITE};
            border-radius: 16px;
            padding: 18px 20px 6px 20px;
            box-shadow: 0 4px 16px rgba(43,43,43,0.06);
            margin-bottom: 18px;
        }}
        .section-title {{
            font-size: 15px;
            font-weight: 700;
            color: {DGRAY};
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .section-title span.tag {{
            background: {PURPLE};
            color: white;
            font-size: 10px;
            padding: 2px 8px;
            border-radius: 6px;
            font-weight: 700;
        }}

        .insight-box {{
            background: linear-gradient(135deg, {PURPLE} 0%, {PURPLE_DARK} 100%);
            color: white;
            border-radius: 14px;
            padding: 14px 18px;
            margin-bottom: 10px;
            font-size: 13.5px;
            line-height: 1.5;
        }}
        .insight-box b {{ font-weight: 700; }}
        .insight-box.green {{
            background: linear-gradient(135deg, {GREEN} 0%, #229c87 100%);
        }}

        .na-box {{
            background: #FFF8E8;
            border: 1px dashed {AMBER};
            border-radius: 10px;
            padding: 10px 14px;
            font-size: 13px;
            color: #8a6d23;
        }}

        .funnel-step {{
            text-align: center;
            padding: 14px 6px;
            border-radius: 12px;
            color: white;
            font-weight: 700;
            font-size: 14px;
        }}

        div[data-baseweb="select"] > div {{
            border-radius: 10px !important;
        }}

        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-thumb {{ background: #c9c9d6; border-radius: 8px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def logo_b64():
    try:
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""


def header(title, subtitle):
    b64 = logo_b64()
    logo_html = f'<img src="data:image/png;base64,{b64}" style="height:34px;" />' if b64 else ""
    st.markdown(
        f"""
        <div class="mms-header">
            <div style="display:flex; align-items:center; gap:16px;">
                {logo_html}
                <div>
                    <h1>{title}</h1>
                    <p>{subtitle}</p>
                </div>
            </div>
            <div class="mms-badge">Last refreshed: {datetime.now().strftime('%d %b %Y, %H:%M')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_start(title, tag=None):
    tag_html = f'<span class="tag">{tag}</span>' if tag else ""
    st.markdown(
        f'<div class="section-card"><div class="section-title">{title}{tag_html}</div>',
        unsafe_allow_html=True,
    )


def section_end():
    st.markdown("</div>", unsafe_allow_html=True)


def kpi_card(label, value, sub="", color=PURPLE):
    st.markdown(
        f"""
        <div class="kpi-card" style="border-left-color:{color};">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def na_message(metric_name):
    st.markdown(
        f'<div class="na-box">⚠️ <b>{metric_name}</b> is unavailable — the source data does not '
        f'contain enough information to calculate this metric reliably.</div>',
        unsafe_allow_html=True,
    )


def base_layout(fig, height=380):
    fig.update_layout(
        font_family="Inter",
        font_color=DGRAY,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
    )
    return fig


# ============================================================================
# DATA LOADING & CLEANING
# ============================================================================
def clean_text(val, default=NA_LABEL):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return default
    s = str(val).replace("\xa0", " ").strip()
    s = " ".join(s.split())
    if s == "" or s.lower() in ("nan", "none", "n/a"):
        return default
    return s


NATIONALITY_MAP = {
    "saudi": "Saudi", "saudi arabia": "Saudi", "ksa": "Saudi", "saudi arabian": "Saudi",
}

DEPT_MAP_SUFFIXES = ["-MMS", "- MMS", "MMS"]


def normalize_department(val):
    s = clean_text(val)
    if s == NA_LABEL:
        return s
    for suf in ["- MMS", "-MMS"]:
        if s.endswith(suf):
            s = s[: -len(suf)].strip()
    s = s.replace("-", " ").strip()
    s = " ".join(w.capitalize() if not w.isupper() else w for w in s.split())
    # fix common capitalization edge cases
    fixes = {"Hr": "HR", "It": "IT", "Cc": "CC", "Mms": "MMS"}
    s = " ".join(fixes.get(w, w) for w in s.split())
    return s


def normalize_nationality(val):
    s = clean_text(val)
    key = s.lower()
    return NATIONALITY_MAP.get(key, s)


def normalize_gender(val):
    s = clean_text(val)
    sl = s.lower()
    if sl.startswith("m"):
        return "Male"
    if sl.startswith("f"):
        return "Female"
    return NA_LABEL


def normalize_existing_new(val):
    s = clean_text(val)
    sl = s.lower()
    if "replac" in sl:
        return "Replacement"
    if "non-budgeted" in sl or "non budgeted" in sl:
        return "New - Non-Budgeted"
    if sl.startswith("new"):
        return "New"
    if sl.startswith("exist"):
        return "Existing"
    return s


@st.cache_data(show_spinner=False)
def load_data(path):
    raw = pd.read_excel(path, sheet_name="Sheet1")
    df = raw.copy()

    rename_map = {
        "Department Name": "Department",
        "Number of Openings": "Openings",
        "Joining date": "Joining Date",
        "Offer status": "Offer Status",
    }
    df = df.rename(columns=rename_map)

    # drop fully empty helper column if present
    df = df.loc[:, [c for c in df.columns if not str(c).startswith("Unnamed")]]

    text_cols_default = {
        "Entity": "Entity", "Job Title": "Job Title", "Line Manager": "Line Manager",
        "Category": "Category", "Hiring Status": "Hiring Status",
        "Vacancy Status": "Vacancy Status", "Candidate Name": "Candidate Name",
        "Recruiter": "Recruiter", "Type of Hire": "Type of Hire",
        "Source of Hire": "Source of Hire", "Offer Status": "Offer Status",
        "Project": "Project",
    }
    for c in text_cols_default:
        if c in df.columns:
            df[c] = df[c].apply(clean_text)

    if "Department" in df.columns:
        df["Department"] = df["Department"].apply(normalize_department)
    if "Nationality" in df.columns:
        df["Nationality"] = df["Nationality"].apply(normalize_nationality)
    if "Gender" in df.columns:
        df["Gender"] = df["Gender"].apply(normalize_gender)
    if "Existing/New" in df.columns:
        df["Existing/New"] = df["Existing/New"].apply(normalize_existing_new)

    for dcol in ["Effective", "Start Hiring Date", "Joining Date"]:
        if dcol in df.columns:
            df[dcol] = pd.to_datetime(df[dcol], errors="coerce")

    if "Grade" in df.columns:
        df["Grade"] = pd.to_numeric(df["Grade"], errors="coerce")
    if "Openings" in df.columns:
        df["Openings"] = pd.to_numeric(df["Openings"], errors="coerce").fillna(0)

    # Time to hire (only where both dates exist)
    if {"Joining Date", "Start Hiring Date"}.issubset(df.columns):
        valid = df["Joining Date"].notna() & df["Start Hiring Date"].notna()
        df["Time to Hire (Days)"] = np.where(
            valid, (df["Joining Date"] - df["Start Hiring Date"]).dt.days, np.nan
        )

    # de-duplicate exact duplicate rows
    df = df.drop_duplicates().reset_index(drop=True)

    # Saudization flag
    if "Nationality" in df.columns:
        df["Is_Saudi"] = df["Nationality"] == "Saudi"

    # Probation flag: joined, with joining date within last 90 days of today
    if "Joining Date" in df.columns:
        today = pd.Timestamp(datetime.now().date())
        df["On_Probation"] = df["Joining Date"].notna() & (
            (today - df["Joining Date"]).dt.days.between(0, 90)
        )
    else:
        df["On_Probation"] = False

    # Month label for trend
    if "Joining Date" in df.columns:
        df["Join_Month"] = df["Joining Date"].dt.to_period("M").astype(str)

    return df


def has_data(series):
    return series is not None and series.notna().any() and len(series.dropna()) > 0


# ============================================================================
# LOAD + SIDEBAR FILTERS
# ============================================================================
inject_css()

if not os.path.exists(DATA_PATH):
    st.error(f"Data file not found at {DATA_PATH}. Please place Data.xlsx in the /data folder.")
    st.stop()

df_full = load_data(DATA_PATH)

with st.sidebar:
    b64 = logo_b64()
    if b64:
        st.markdown(
            f'<div style="text-align:center; padding:10px 0 18px 0;">'
            f'<img src="data:image/png;base64,{b64}" style="height:38px; filter:brightness(0) invert(1);" /></div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        '<p style="text-align:center; font-size:11px; letter-spacing:1px; '
        'color:#9aa0ff; margin-top:-12px;">RECRUITMENT ANALYTICS</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "📊  Executive Dashboard",
            "🔄  Recruitment Pipeline",
            "🏢  Department Analytics",
            "🧑‍💼  Recruiter Performance",
            "👥  Candidate Analytics",
            "📋  Recruitment Data",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**Filters**")

    def ms_filter(label, col):
        if col not in df_full.columns:
            return None
        opts = sorted([o for o in df_full[col].dropna().unique()])
        return st.multiselect(label, opts, default=[])

    f_entity = ms_filter("Entity", "Entity")
    f_dept = ms_filter("Department", "Department")
    f_recruiter = ms_filter("Recruiter", "Recruiter")
    f_project = ms_filter("Project", "Project")
    f_hiring_status = ms_filter("Hiring Status", "Hiring Status")
    f_vacancy_status = ms_filter("Vacancy Status", "Vacancy Status")
    f_gender = ms_filter("Gender", "Gender")
    f_nationality = ms_filter("Nationality", "Nationality")
    f_grade = ms_filter("Grade", "Grade")
    f_category = ms_filter("Category", "Category")
    f_source = ms_filter("Source of Hire", "Source of Hire")

    date_range = None
    if "Joining Date" in df_full.columns and df_full["Joining Date"].notna().any():
        min_d = df_full["Joining Date"].min().date()
        max_d = df_full["Joining Date"].max().date()
        date_range = st.date_input("Joining Date Range", value=(min_d, max_d), min_value=min_d, max_value=max_d)

    st.markdown("---")
    if st.button("↺ Reset Filters", use_container_width=True):
        st.rerun()


def apply_filters(df):
    out = df.copy()
    def f(col, vals):
        nonlocal out
        if vals:
            out = out[out[col].isin(vals)]
    f("Entity", f_entity)
    f("Department", f_dept)
    f("Recruiter", f_recruiter)
    f("Project", f_project)
    f("Hiring Status", f_hiring_status)
    f("Vacancy Status", f_vacancy_status)
    f("Gender", f_gender)
    f("Nationality", f_nationality)
    f("Grade", f_grade)
    f("Category", f_category)
    f("Source of Hire", f_source)
    if date_range and isinstance(date_range, tuple) and len(date_range) == 2 and "Joining Date" in out.columns:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        mask = out["Joining Date"].isna() | out["Joining Date"].between(start, end)
        out = out[mask]
    return out


df = apply_filters(df_full)

if df.empty:
    st.warning("No records match the selected filters. Please adjust your filter selection.")
    st.stop()


# ============================================================================
# SHARED KPI CALCULATIONS
# ============================================================================
def compute_kpis(d):
    k = {}
    k["total_requisitions"] = len(d)
    k["total_openings"] = d["Openings"].sum() if "Openings" in d.columns else None
    k["filled"] = (d["Hiring Status"] == "Joined").sum() if "Hiring Status" in d.columns else None
    k["open_vacancies"] = (d["Vacancy Status"] == "Open").sum() if "Vacancy Status" in d.columns else None

    if "Time to Hire (Days)" in d.columns and d["Time to Hire (Days)"].notna().any():
        k["avg_tth"] = round(d["Time to Hire (Days)"].mean(), 1)
    else:
        k["avg_tth"] = None

    if k["total_openings"] and k["total_openings"] > 0 and k["filled"] is not None:
        k["hiring_plan_pct"] = round(k["filled"] / k["total_openings"] * 100, 1)
    else:
        k["hiring_plan_pct"] = None

    if "Is_Saudi" in d.columns and len(d) > 0 and d["Nationality"].notna().any():
        known = d[d["Nationality"] != NA_LABEL]
        k["saudization"] = round(known["Is_Saudi"].mean() * 100, 1) if len(known) else None
    else:
        k["saudization"] = None

    if "Gender" in d.columns:
        known_g = d[d["Gender"] != NA_LABEL]
        if len(known_g):
            k["male_pct"] = round((known_g["Gender"] == "Male").mean() * 100, 1)
            k["female_pct"] = round((known_g["Gender"] == "Female").mean() * 100, 1)
        else:
            k["male_pct"] = k["female_pct"] = None
    else:
        k["male_pct"] = k["female_pct"] = None

    k["on_probation"] = d["On_Probation"].sum() if "On_Probation" in d.columns else None
    return k


kpis = compute_kpis(df)


def fmt(v, suffix="", none_text="N/A"):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return none_text
    if isinstance(v, float) and v == int(v):
        v = int(v)
    return f"{v}{suffix}"


# ============================================================================
# PAGE 1 — EXECUTIVE DASHBOARD
# ============================================================================
def page_executive():
    header("Executive Dashboard", "Company-wide recruitment performance overview")

    c = st.columns(5)
    with c[0]:
        kpi_card("Total Requisitions", fmt(kpis["total_requisitions"]), "All recruitment requests", PURPLE)
    with c[1]:
        kpi_card("Total Openings", fmt(kpis["total_openings"]), "Positions requested", GREEN)
    with c[2]:
        kpi_card("Filled Positions", fmt(kpis["filled"]), "Status = Joined", PURPLE)
    with c[3]:
        kpi_card("Open Vacancies", fmt(kpis["open_vacancies"]), "Still in progress", AMBER)
    with c[4]:
        kpi_card(
            "Hiring Plan Progress",
            fmt(kpis["hiring_plan_pct"], "%") if kpis["hiring_plan_pct"] is not None else "N/A",
            "Filled ÷ Total Openings", GREEN,
        )

    c2 = st.columns(5)
    with c2[0]:
        kpi_card("Avg. Time to Hire", fmt(kpis["avg_tth"], " days"), "Start Hiring → Joining", PURPLE)
    with c2[1]:
        kpi_card("Saudization Rate", fmt(kpis["saudization"], "%"), "Saudi ÷ Known Nationality", GREEN)
    with c2[2]:
        kpi_card("Male %", fmt(kpis["male_pct"], "%"), "Of known gender", PURPLE)
    with c2[3]:
        kpi_card("Female %", fmt(kpis["female_pct"], "%"), "Of known gender", GREEN)
    with c2[4]:
        kpi_card("On Probation", fmt(kpis["on_probation"]), "Joined within last 90 days", AMBER)

    st.write("")
    left, right = st.columns([1.3, 1])

    with left:
        section_start("Recruitment Funnel", "PIPELINE")
        funnel_stages = []
        if "Vacancy Status" in df.columns:
            funnel_stages.append(("Open Request", len(df)))
        if "Offer Status" in df.columns:
            funnel_stages.append(("Offer Extended", df["Offer Status"].notna().sum() if df["Offer Status"].dtype == object else (df["Offer Status"] != NA_LABEL).sum()))
            funnel_stages.append(("Offer Accepted", (df["Offer Status"] == "Accept").sum()))
        if "Hiring Status" in df.columns:
            funnel_stages.append(("Joined", (df["Hiring Status"] == "Joined").sum()))

        if len(funnel_stages) >= 2:
            labels = [s[0] for s in funnel_stages]
            values = [s[1] for s in funnel_stages]
            fig = go.Figure(go.Funnel(
                y=labels, x=values,
                marker={"color": [PURPLE, "#8388F2", GREEN, "#1F8C77"][:len(labels)]},
                textinfo="value+percent initial",
            ))
            fig = base_layout(fig, 320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Recruitment Funnel")
        section_end()

        section_start("Monthly Hiring Trend", "TREND")
        if "Join_Month" in df.columns and df["Joining Date"].notna().any():
            trend = df.dropna(subset=["Joining Date"]).groupby("Join_Month").size().reset_index(name="Hires")
            trend = trend.sort_values("Join_Month")
            fig = px.line(trend, x="Join_Month", y="Hires", markers=True,
                           color_discrete_sequence=[PURPLE])
            fig.update_traces(line_width=3, marker_size=8)
            fig = base_layout(fig, 300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Monthly Hiring Trend")
        section_end()

    with right:
        section_start("Hiring by Source", "SOURCE")
        if "Source of Hire" in df.columns and df["Source of Hire"].notna().any():
            src = df[df["Source of Hire"] != NA_LABEL]["Source of Hire"].value_counts().reset_index()
            src.columns = ["Source", "Count"]
            if len(src):
                fig = px.pie(src, names="Source", values="Count", hole=0.55,
                              color_discrete_sequence=CHART_SEQUENCE)
                fig = base_layout(fig, 290)
                st.plotly_chart(fig, use_container_width=True)
            else:
                na_message("Hiring by Source")
        else:
            na_message("Hiring by Source")
        section_end()

        section_start("Nationality Distribution", "DIVERSITY")
        if "Nationality" in df.columns and (df["Nationality"] != NA_LABEL).any():
            nat = df[df["Nationality"] != NA_LABEL]["Nationality"].value_counts().reset_index()
            nat.columns = ["Nationality", "Count"]
            fig = px.pie(nat, names="Nationality", values="Count", hole=0.55,
                          color_discrete_sequence=CHART_SEQUENCE)
            fig = base_layout(fig, 290)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Nationality Distribution")
        section_end()

    c3, c4 = st.columns(2)
    with c3:
        section_start("Hiring by Department", "DEPARTMENT")
        if "Department" in df.columns:
            dep = df["Department"].value_counts().reset_index()
            dep.columns = ["Department", "Hires"]
            dep = dep.sort_values("Hires")
            fig = px.bar(dep, x="Hires", y="Department", orientation="h",
                         color_discrete_sequence=[PURPLE], text="Hires")
            fig.update_traces(textposition="outside")
            fig = base_layout(fig, 360)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Hiring by Department")
        section_end()

    with c4:
        section_start("Hiring by Recruiter", "RECRUITER")
        if "Recruiter" in df.columns:
            rec = df["Recruiter"].value_counts().reset_index()
            rec.columns = ["Recruiter", "Hires"]
            rec = rec.sort_values("Hires")
            fig = px.bar(rec, x="Hires", y="Recruiter", orientation="h",
                         color_discrete_sequence=[GREEN], text="Hires")
            fig.update_traces(textposition="outside")
            fig = base_layout(fig, 360)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Hiring by Recruiter")
        section_end()

    section_start("Hiring Status Overview", "STATUS")
    if "Hiring Status" in df.columns and "Department" in df.columns:
        stat = df.groupby(["Department", "Hiring Status"]).size().reset_index(name="Count")
        if len(stat):
            fig = px.bar(stat, x="Department", y="Count", color="Hiring Status",
                         color_discrete_sequence=[PURPLE, AMBER, GREEN], barmode="stack")
            fig = base_layout(fig, 320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Hiring Status Overview")
    else:
        na_message("Hiring Status Overview")
    section_end()

    # AI Executive Insights
    section_start("AI Executive Insights", "AUTO-GENERATED")
    insights = []
    if "Department" in df.columns and len(df):
        top_dept = df["Department"].value_counts().idxmax()
        insights.append(f"<b>{top_dept}</b> has the highest hiring demand with <b>{df['Department'].value_counts().max()}</b> requisitions.")
    if "Recruiter" in df.columns and "Time to Hire (Days)" in df.columns and df["Time to Hire (Days)"].notna().any():
        rec_tth = df.dropna(subset=["Time to Hire (Days)"]).groupby("Recruiter")["Time to Hire (Days)"].mean()
        if len(rec_tth):
            fastest = rec_tth.idxmin()
            insights.append(f"<b>{fastest}</b> is the fastest recruiter, averaging <b>{rec_tth.min():.1f} days</b> to hire.")
    if kpis["avg_tth"] is not None:
        insights.append(f"The average recruitment cycle currently takes <b>{kpis['avg_tth']} days</b> from start of hiring to joining.")
    if kpis["saudization"] is not None:
        health = "strong" if kpis["saudization"] >= 30 else "below target"
        insights.append(f"Saudization stands at <b>{kpis['saudization']}%</b>, considered <b>{health}</b> relative to common Saudization benchmarks.")
    if kpis["on_probation"] is not None:
        insights.append(f"There are currently <b>{kpis['on_probation']}</b> employee(s) within their probation period (joined in the last 90 days).")
    if kpis["hiring_plan_pct"] is not None:
        insights.append(f"Hiring plan completion is at <b>{kpis['hiring_plan_pct']}%</b> of total approved openings.")
    if kpis["open_vacancies"] is not None and kpis["total_requisitions"]:
        ratio = kpis["open_vacancies"] / kpis["total_requisitions"] * 100
        health_label = "healthy" if ratio < 20 else "needs attention"
        insights.append(f"Overall recruitment health looks <b>{health_label}</b>, with open vacancies representing <b>{ratio:.0f}%</b> of all requisitions.")

    if insights:
        for i, txt in enumerate(insights):
            cls = "insight-box green" if i % 2 else "insight-box"
            st.markdown(f'<div class="{cls}">💡 {txt}</div>', unsafe_allow_html=True)
    else:
        na_message("AI Executive Insights")
    section_end()


# ============================================================================
# PAGE 2 — RECRUITMENT PIPELINE
# ============================================================================
def page_pipeline():
    header("Recruitment Pipeline", "Status, offers, and time-to-hire breakdown")

    c1, c2 = st.columns(2)
    with c1:
        section_start("Hiring Status", "PIPELINE")
        if "Hiring Status" in df.columns:
            s = df["Hiring Status"].value_counts().reset_index()
            s.columns = ["Status", "Count"]
            fig = px.bar(s, x="Status", y="Count", color="Status", text="Count",
                         color_discrete_sequence=CHART_SEQUENCE)
            fig.update_traces(textposition="outside")
            fig = base_layout(fig, 320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Hiring Status")
        section_end()

    with c2:
        section_start("Vacancy Status", "PIPELINE")
        if "Vacancy Status" in df.columns:
            s = df["Vacancy Status"].value_counts().reset_index()
            s.columns = ["Status", "Count"]
            fig = px.pie(s, names="Status", values="Count", hole=0.55,
                          color_discrete_sequence=[GREEN, AMBER, PURPLE])
            fig = base_layout(fig, 320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Vacancy Status")
        section_end()

    c3, c4 = st.columns(2)
    with c3:
        section_start("Offer Status", "PIPELINE")
        if "Offer Status" in df.columns and (df["Offer Status"] != NA_LABEL).any():
            s = df[df["Offer Status"] != NA_LABEL]["Offer Status"].value_counts().reset_index()
            s.columns = ["Status", "Count"]
            fig = px.bar(s, x="Status", y="Count", color="Status", text="Count",
                         color_discrete_sequence=[GREEN, RED, AMBER])
            fig.update_traces(textposition="outside")
            fig = base_layout(fig, 320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Offer Status")
        section_end()

    with c4:
        section_start("Pipeline Funnel", "PIPELINE")
        stages = []
        stages.append(("Open Request", len(df)))
        if "Offer Status" in df.columns:
            stages.append(("Offer", (df["Offer Status"] != NA_LABEL).sum()))
            stages.append(("Accepted", (df["Offer Status"] == "Accept").sum()))
        if "Hiring Status" in df.columns:
            stages.append(("Joined", (df["Hiring Status"] == "Joined").sum()))
        if len(stages) >= 2:
            fig = go.Figure(go.Funnel(y=[s[0] for s in stages], x=[s[1] for s in stages],
                                       marker={"color": [PURPLE, "#8388F2", GREEN, "#1F8C77"][:len(stages)]}))
            fig = base_layout(fig, 320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Pipeline Funnel")
        section_end()

    section_start("Time to Hire Analysis", "EFFICIENCY")
    if "Time to Hire (Days)" in df.columns and df["Time to Hire (Days)"].notna().any():
        valid = df.dropna(subset=["Time to Hire (Days)"])
        cL, cR = st.columns([1, 1.4])
        with cL:
            kpi_card("Average Time to Hire", f"{valid['Time to Hire (Days)'].mean():.1f} days", "Across filtered records", PURPLE)
            st.write("")
            kpi_card("Fastest Hire", f"{valid['Time to Hire (Days)'].min():.0f} days", "Minimum observed", GREEN)
            st.write("")
            kpi_card("Slowest Hire", f"{valid['Time to Hire (Days)'].max():.0f} days", "Maximum observed", AMBER)
        with cR:
            fig = px.histogram(valid, x="Time to Hire (Days)", nbins=10, color_discrete_sequence=[PURPLE])
            fig = base_layout(fig, 360)
            st.plotly_chart(fig, use_container_width=True)
    else:
        na_message("Time to Hire Analysis")
    section_end()

    section_start("Hiring Timeline", "TIMELINE")
    if "Joining Date" in df.columns and df["Joining Date"].notna().any():
        tl = df.dropna(subset=["Joining Date"]).sort_values("Joining Date")
        fig = px.scatter(tl, x="Joining Date", y="Department", color="Hiring Status" if "Hiring Status" in tl.columns else None,
                          hover_data=["Candidate Name"] if "Candidate Name" in tl.columns else None,
                          color_discrete_sequence=CHART_SEQUENCE)
        fig.update_traces(marker=dict(size=11))
        fig = base_layout(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
    else:
        na_message("Hiring Timeline")
    section_end()


# ============================================================================
# PAGE 3 — DEPARTMENT ANALYTICS
# ============================================================================
def page_department():
    header("Department Analytics", "Headcount, speed, and diversity by department")

    if "Department" not in df.columns:
        na_message("Department Analytics")
        return

    c1, c2 = st.columns(2)
    with c1:
        section_start("Hiring by Department", "VOLUME")
        dep = df["Department"].value_counts().reset_index()
        dep.columns = ["Department", "Hires"]
        dep = dep.sort_values("Hires")
        fig = px.bar(dep, x="Hires", y="Department", orientation="h",
                     color_discrete_sequence=[PURPLE], text="Hires")
        fig.update_traces(textposition="outside")
        fig = base_layout(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
        section_end()

    with c2:
        section_start("Average Time to Hire by Department", "SPEED")
        if "Time to Hire (Days)" in df.columns and df["Time to Hire (Days)"].notna().any():
            tth = df.dropna(subset=["Time to Hire (Days)"]).groupby("Department")["Time to Hire (Days)"].mean().reset_index()
            tth = tth.sort_values("Time to Hire (Days)")
            fig = px.bar(tth, x="Time to Hire (Days)", y="Department", orientation="h",
                         color_discrete_sequence=[GREEN], text="Time to Hire (Days)")
            fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            fig = base_layout(fig, 380)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Average Time to Hire by Department")
        section_end()

    c3, c4 = st.columns(2)
    with c3:
        section_start("Open Vacancies by Department", "OPEN ROLES")
        if "Vacancy Status" in df.columns:
            ov = df[df["Vacancy Status"] == "Open"]["Department"].value_counts().reset_index()
            ov.columns = ["Department", "Open Vacancies"]
            if len(ov):
                fig = px.bar(ov, x="Open Vacancies", y="Department", orientation="h",
                             color_discrete_sequence=[AMBER], text="Open Vacancies")
                fig.update_traces(textposition="outside")
                fig = base_layout(fig, 320)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("No open vacancies in the current filter selection — all positions are closed.")
        else:
            na_message("Open Vacancies by Department")
        section_end()

    with c4:
        section_start("Saudization by Department", "NATIONALIZATION")
        if "Is_Saudi" in df.columns and (df["Nationality"] != NA_LABEL).any():
            known = df[df["Nationality"] != NA_LABEL]
            sd = known.groupby("Department")["Is_Saudi"].mean().reset_index()
            sd["Saudization %"] = (sd["Is_Saudi"] * 100).round(1)
            sd = sd.sort_values("Saudization %")
            fig = px.bar(sd, x="Saudization %", y="Department", orientation="h",
                         color_discrete_sequence=[GREEN], text="Saudization %")
            fig.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
            fig = base_layout(fig, 320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Saudization by Department")
        section_end()

    c5, c6 = st.columns(2)
    with c5:
        section_start("Gender Distribution by Department", "DIVERSITY")
        if "Gender" in df.columns and (df["Gender"] != NA_LABEL).any():
            gd = df[df["Gender"] != NA_LABEL].groupby(["Department", "Gender"]).size().reset_index(name="Count")
            fig = px.bar(gd, x="Department", y="Count", color="Gender", barmode="group",
                         color_discrete_sequence=[PURPLE, GREEN])
            fig = base_layout(fig, 340)
            fig.update_xaxes(tickangle=-30)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Gender Distribution by Department")
        section_end()

    with c6:
        section_start("Grade Distribution", "STRUCTURE")
        if "Grade" in df.columns and df["Grade"].notna().any():
            gr = df.dropna(subset=["Grade"])
            gr["Grade"] = gr["Grade"].astype(int)
            grc = gr["Grade"].value_counts().sort_index().reset_index()
            grc.columns = ["Grade", "Count"]
            fig = px.bar(grc, x="Grade", y="Count", color_discrete_sequence=[PURPLE], text="Count")
            fig.update_traces(textposition="outside")
            fig = base_layout(fig, 340)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Grade Distribution")
        section_end()


# ============================================================================
# PAGE 4 — RECRUITER PERFORMANCE
# ============================================================================
def page_recruiter():
    header("Recruiter Performance", "Workload, speed, and success rate by recruiter")

    if "Recruiter" not in df.columns:
        na_message("Recruiter Performance")
        return

    c1, c2 = st.columns(2)
    with c1:
        section_start("Hires by Recruiter", "VOLUME")
        rec = df["Recruiter"].value_counts().reset_index()
        rec.columns = ["Recruiter", "Hires"]
        rec = rec.sort_values("Hires")
        fig = px.bar(rec, x="Hires", y="Recruiter", orientation="h",
                     color_discrete_sequence=[PURPLE], text="Hires")
        fig.update_traces(textposition="outside")
        fig = base_layout(fig, 360)
        st.plotly_chart(fig, use_container_width=True)
        section_end()

    with c2:
        section_start("Average Time to Hire by Recruiter", "SPEED")
        if "Time to Hire (Days)" in df.columns and df["Time to Hire (Days)"].notna().any():
            tth = df.dropna(subset=["Time to Hire (Days)"]).groupby("Recruiter")["Time to Hire (Days)"].mean().reset_index()
            tth = tth.sort_values("Time to Hire (Days)")
            fig = px.bar(tth, x="Time to Hire (Days)", y="Recruiter", orientation="h",
                         color_discrete_sequence=[GREEN], text="Time to Hire (Days)")
            fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            fig = base_layout(fig, 360)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Average Time to Hire by Recruiter")
        section_end()

    c3, c4 = st.columns(2)
    with c3:
        section_start("Open Requisitions by Recruiter", "WORKLOAD")
        if "Vacancy Status" in df.columns:
            ov = df[df["Vacancy Status"] == "Open"]["Recruiter"].value_counts().reset_index()
            ov.columns = ["Recruiter", "Open Requisitions"]
            if len(ov):
                fig = px.bar(ov, x="Open Requisitions", y="Recruiter", orientation="h",
                             color_discrete_sequence=[AMBER], text="Open Requisitions")
                fig.update_traces(textposition="outside")
                fig = base_layout(fig, 300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("No open requisitions in the current filter selection.")
        else:
            na_message("Open Requisitions by Recruiter")
        section_end()

    with c4:
        section_start("Offer Success Rate", "CONVERSION")
        if "Offer Status" in df.columns and (df["Offer Status"] != NA_LABEL).any():
            known = df[df["Offer Status"] != NA_LABEL]
            rate = known.groupby("Recruiter")["Offer Status"].apply(lambda s: (s == "Accept").mean() * 100).reset_index(name="Success Rate %")
            rate = rate.sort_values("Success Rate %")
            fig = px.bar(rate, x="Success Rate %", y="Recruiter", orientation="h",
                         color_discrete_sequence=[GREEN], text="Success Rate %")
            fig.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
            fig = base_layout(fig, 300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            na_message("Offer Success Rate")
        section_end()

    section_start("Recruiter Ranking", "LEADERBOARD")
    agg = {"Candidate Name": "count"} if "Candidate Name" in df.columns else {}
    rank = df.groupby("Recruiter").agg(
        Hires=("Recruiter", "size"),
    ).reset_index()
    if "Time to Hire (Days)" in df.columns:
        tth = df.groupby("Recruiter")["Time to Hire (Days)"].mean().reset_index(name="Avg Time to Hire")
        rank = rank.merge(tth, on="Recruiter", how="left")
    if "Offer Status" in df.columns:
        known = df[df["Offer Status"] != NA_LABEL]
        if len(known):
            sr = known.groupby("Recruiter")["Offer Status"].apply(lambda s: (s == "Accept").mean() * 100).reset_index(name="Offer Success %")
            rank = rank.merge(sr, on="Recruiter", how="left")
    rank = rank.sort_values("Hires", ascending=False).reset_index(drop=True)
    rank.index = rank.index + 1
    rank.index.name = "Rank"
    st.dataframe(rank.round(1), use_container_width=True)
    section_end()


# ============================================================================
# PAGE 5 — CANDIDATE ANALYTICS
# ============================================================================
def page_candidate():
    header("Candidate Analytics", "Profile of hired and pipeline candidates")

    pairs = [
        ("Nationality", "Nationality Breakdown", "pie"),
        ("Gender", "Gender Breakdown", "pie"),
        ("Source of Hire", "Source of Hire", "pie"),
        ("Type of Hire", "Type of Hire", "bar"),
        ("Category", "Category", "bar"),
        ("Grade", "Grade", "bar"),
        ("Entity", "Entity", "pie"),
        ("Project", "Project", "bar"),
    ]
    cols = st.columns(2)
    for i, (col, title, kind) in enumerate(pairs):
        with cols[i % 2]:
            section_start(title, "CANDIDATE")
            if col in df.columns:
                sub = df[df[col] != NA_LABEL] if df[col].dtype == object else df.dropna(subset=[col])
                if len(sub):
                    vc = sub[col].value_counts().reset_index()
                    vc.columns = [title, "Count"]
                    if kind == "pie":
                        fig = px.pie(vc, names=title, values="Count", hole=0.55,
                                      color_discrete_sequence=CHART_SEQUENCE)
                        fig = base_layout(fig, 300)
                    else:
                        vc = vc.sort_values("Count")
                        fig = px.bar(vc, x="Count", y=title, orientation="h",
                                     color_discrete_sequence=[PURPLE], text="Count")
                        fig.update_traces(textposition="outside")
                        fig = base_layout(fig, 300)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    na_message(title)
            else:
                na_message(title)
            section_end()


# ============================================================================
# PAGE 6 — RECRUITMENT DATA TABLE
# ============================================================================
def page_table():
    header("Recruitment Data", "Searchable, filterable detailed records")

    section_start("Filtered Records", f"{len(df)} ROWS")
    search = st.text_input("🔍 Search across all fields", "")
    table = df.copy()
    if search:
        mask = table.apply(lambda row: row.astype(str).str.contains(search, case=False, na=False).any(), axis=1)
        table = table[mask]

    display_cols = [c for c in table.columns if c not in ["Is_Saudi", "On_Probation", "Join_Month"]]
    st.dataframe(table[display_cols], use_container_width=True, height=500)

    csv = table[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export to CSV", data=csv, file_name="recruitment_data_export.csv", mime="text/csv")
    section_end()


# ============================================================================
# ROUTER
# ============================================================================
PAGES = {
    "📊  Executive Dashboard": page_executive,
    "🔄  Recruitment Pipeline": page_pipeline,
    "🏢  Department Analytics": page_department,
    "🧑‍💼  Recruiter Performance": page_recruiter,
    "👥  Candidate Analytics": page_candidate,
    "📋  Recruitment Data": page_table,
}

PAGES[page]()

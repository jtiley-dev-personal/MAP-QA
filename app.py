import io
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import pandas as pd
import streamlit as st

st.set_page_config(page_title="MAP Quality Assurance", layout="wide")

# ======= CSS =======
st.markdown("""
    <style>
    /* ======= FONT + BASE STYLE ======= */
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Source Sans Pro', sans-serif !important;
    }

    h1, h2, h3, h4 {
        font-weight: 600 !important;
        color: #111111 !important; /* darker for contrast */
        margin-top: 0.5rem !important;
        margin-bottom: 0.4rem !important;
    }

    /* ======= TIGHTEN TITLE + DESCRIPTION SPACING ======= */
    h1 {
        margin-bottom: 0.25rem !important;
    }
    div[data-testid="stMarkdownContainer"] p {
        margin-top: 0 !important;
        line-height: 1.3 !important;
    }

    /* ======= MAIN APP BACKGROUND ======= */
    body, .stApp {
        background-color: #ffffff !important;
        color: #111111 !important;
    }

    /* ======= FORM LABELS IN MAIN APP ======= */
    div[data-testid="stVerticalBlock"] label p {
        color: #111111 !important;
        font-weight: 500 !important;
    }

    /* ======= TABLE STYLING ======= */
    table {
        border-collapse: collapse !important;
        border: 1px solid #555 !important;
        width: 100%;
        margin-bottom: 1rem;
    }
    th {
        background-color: #F2F2F2 !important;
        color: #111111 !important;
        font-weight: 600 !important;
        text-align: center !important;
        padding: 6px 4px !important;
    }
    td {
        color: #111111 !important;
        border-top: 1px solid #DDD !important;
        text-align: center !important;
        padding: 6px 4px !important;
    }
    tr:nth-child(even) {
        background-color: #FBFBFB !important;
    }

    /* ======= EXTENDED NAVBAR ======= */
    header[data-testid="stHeader"] {
        background-color: #eeeeee !important;
        color: #E0E0E0 !important;
        position: fixed !important;
        top: 0;
        left: 0;
        width: 100% !important;
        z-index: 1000 !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.4) !important;
    }

    header[data-testid="stHeader"]::after {
        content: "MAP Quality Assurance";
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        letter-spacing: 0.5px;
        text-align: center;
        pointer-events: none;
    }

    .block-container {
        padding-top: 3.8rem !important;
        color: #111111 !important;
    }

    header[data-testid="stHeader"]::before {
        background: none !important;
    }

    /* ======= SIDEBAR ======= */
    section[data-testid="stSidebar"] {
        background-color: #eeeeee !important;
        border-right: 2px solid #FFFFFF !important;
        padding-right: 0.8rem !important;   /* increased padding */
        padding-left: 0.6rem !important;
        padding-top: 0rem !important;       /* removes blank space above Upload Files */
        margin-top: 3.8rem !important;      /* keep below navbar */
        z-index: 900 !important;
        position: relative !important;
    }

    /* Section headings */
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        margin-top: 1.4rem !important;   /* slightly more spacing above */
        margin-bottom: 0.8rem !important;
        position: relative;
        padding-top: 0.8rem !important;
    }

    /* White divider lines above section headings */
    section[data-testid="stSidebar"] h2::before,
    section[data-testid="stSidebar"] h3::before {
        content: "";
        display: block;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background-color: #000000 !important;
    }

    /* File upload boxes */
    section[data-testid="stSidebar"] div.stFileUploader {
        background-color: #eeeeee !important;
        border: 1px solid #EB0800 !important;
        border-radius: 10px !important;
        padding: 10px !important;
        margin-bottom: 1.2rem !important;   /* more spacing between upload boxes */
        box-shadow: 0px 0px 6px rgba(235, 8, 0, 0.1);
    }

    /* Upload labels */
    section[data-testid="stSidebar"] div.stFileUploader label > div {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #E0E0E0 !important;
        margin-bottom: 4px !important;
    }

    /* Browse Files button */
    section[data-testid="stSidebar"] div.stFileUploader button {
        color: #E0E0E0 !important;
    }

    /* Sidebar labels */
    section[data-testid="stSidebar"] label p {
        font-size: 1.1rem !important;
        font-weight: 400 !important;
        color: #000000 !important;
        margin-bottom: 0.3rem !important;
    }

    /* Dropdowns & select boxes */
    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #eeeeee !important;
        border: 1px solid #EB0800 !important;
        border-radius: 10px !important;
        color: #000000 !important;
        font-size: 1.05rem !important;
        margin-bottom: 1rem !important; /* increased spacing */
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: transparent !important;
        color: #E0E0E0 !important;
    }

    /* ======= BUTTONS ======= */
    .stDownloadButton button {
        background-color: #333 !important;
        color: #E0E0E0 !important;
        border-radius: 6px !important;
        border: 1px solid #555 !important;
        padding: 0.3rem 0.8rem !important;
        transition: 0.3s;
        font-size: 0.9rem !important;
    }
    .stDownloadButton button:hover {
        background-color: #555 !important;
    }

    div.stButton>button:first-child {
        background-color: #3B63FB !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        transition: 0.3s;
        padding: 0.4rem 1rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    div.stButton>button:first-child:hover {
        background-color: #5476FC !important;
    }

    /* ======= FIX: Dropdown and File Uploader Text Color ======= */

    /* File uploader buttons ("Browse files") */
    section[data-testid="stSidebar"] div.stFileUploader button,
    section[data-testid="stSidebar"] div.stFileUploader div[role="button"] {
        color: #111111 !important;        /* Make "Browse files" text black */
        background-color: #f7f7f7 !important; /* Slightly lighter grey for button */
        border: 1px solid #EB0800 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }

    /* File uploader text ("Drag and drop file here") */
    section[data-testid="stSidebar"] div.stFileUploader div[data-testid="stFileUploaderDropzoneInstructions"] {
        color: #111111 !important;
        font-weight: 500 !important;
    }

    /* Dropdown (Select) text */
    section[data-testid="stSidebar"] div[data-baseweb="select"] div {
        color: #111111 !important;  /* Make dropdown text black */
    }

    /* Dropdown selected items (inside the grey pill tags) */
    section[data-testid="stSidebar"] div[data-baseweb="tag"] {
        background-color: #eaeaea !important;
        color: #111111 !important;
        font-weight: 500 !important;
    }
    </style>


""", unsafe_allow_html=True)


# ======= HEADER SECTION =======
st.title("Overview")

st.markdown(
    """
    <p style="margin-top:0; line-height:1.3; color:#111111;">
    Upload two Excel files — one with MAP raw data and one with your Media Plan — then compare totals at the
    <b>Markets</b>, <b>Channel</b>, and <b>Partners</b> levels for the <b>Budget</b> and <b>Visits</b> metrics.<br>
    You can select one or more <b>Campaigns</b> from your MAP File before comparison.
    </p>
    """,
    unsafe_allow_html=True
)

# How To Use box
st.markdown(
    """
    <div style="
        background-color:#f9f9f9;
        border-left:4px solid #3B63FB;
        padding:1rem;
        border-radius:8px;
        margin-top:0.6rem;
        margin-bottom:1rem;
        color:#111111;
        font-size:0.95rem;
        line-height:1.5;
    ">
        <h4 style="margin-top:0; color:#111111;">How To Use:</h4>
        <ol style="margin-top:0.3rem; padding-left:1.2rem;">
            <li>Upload your <b>MAP</b> file & select sheet for comparison</li>
            <li>Upload your <b>Media Plan</b> file & select sheet for comparison</li>
            <li>Select what <b>levels</b> you would like to compare across the two sheets.</li>
            <li>Select the <b>campaign</b> to be used for comparison — this should match the campaign in your Media Plan.</li>
            <li>Select the <b>columns for comparison</b> in the MAP file. These are auto-populated, but you’ll need to confirm the <b>budget</b> and <b>traffic</b> columns.</li>
            <li>Select the <b>columns for comparison</b> in the Media Plan file. These are auto-populated, but you’ll need to confirm the <b>budget</b> and <b>traffic</b> columns.</li>
            <li>Click the <b>Compare Files</b> button to view results.</li>
        </ol>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------
@dataclass
class Mapping:
    level_cols: Dict[str, Optional[str]]
    budget_col: Optional[str]
    visits_col: Optional[str]

@st.cache_resource(show_spinner=False)
def load_excel(file_bytes) -> Optional[pd.ExcelFile]:
    """Load Excel file into memory once, cache the ExcelFile object."""
    if not file_bytes:
        return None
    try:
        return pd.ExcelFile(file_bytes)
    except Exception as e:
        st.error(f"Failed to read Excel: {e}")
        return None

@st.cache_data(show_spinner=False)
def read_sheet_cached(_xls: pd.ExcelFile, sheet_name: str, header_row: int = 0) -> Optional[pd.DataFrame]:
    """Parse a specific sheet from a cached ExcelFile object."""
    try:
        df = _xls.parse(sheet_name=sheet_name, header=header_row)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Failed to parse sheet '{sheet_name}': {e}")
        return None

def available_columns(df: Optional[pd.DataFrame]) -> List[str]:
    if df is None:
        return []
    non_empty_cols = []
    for col in df.columns:
        if df[col].notna().sum() > 0 and not (df[col].astype(str).str.strip() == "").all():
            non_empty_cols.append(col)
    return non_empty_cols

# ---------------------------------------------------------------------
# Auto-detect helpers (case-insensitive)
# - Uses allowed filters for Budget/Visits
# - Exact-name hints for Markets/Channel/Partners
# ---------------------------------------------------------------------
def auto_detect_columns_filtered(df: Optional[pd.DataFrame]) -> Dict[str, Optional[str]]:
    result = {"Markets": None, "Channel": None, "Partners": None, "Budget": None, "Visits": None}
    if df is None or df.empty:
        return result

    cols = available_columns(df)
    lower = {c.lower(): c for c in cols}

    def find_exact(name: str) -> Optional[str]:
        return lower.get(name.lower())

    def find_first_contains(terms: List[str], in_list: Optional[List[str]] = None) -> Optional[str]:
        pool = in_list if in_list is not None else cols
        for c in pool:
            lc = c.lower()
            if any(t in lc for t in terms):
                return c
        return None

    # Allowed lists for budget/visits
    spend_cols = [c for c in cols if "spend" in c.lower()]
    traffic_cols = [c for c in cols if any(x in c.lower() for x in ["traffic", "visits"])]

    result["Markets"]  = find_exact("Market_Area") or find_first_contains(["market"])
    result["Channel"]  = find_exact("Marketing_Channel_Type") or find_first_contains(["channel"])
    result["Partners"] = find_exact("Platform") or find_first_contains(["platform"])
    result["Budget"]   = find_first_contains(["spend"], spend_cols)
    result["Visits"]   = find_first_contains(["traffic", "visits"], traffic_cols)

    return result

# ---------------------------------------------------------------------
# Mapping UI (auto-select + cross-file mirroring), order restored:
# Markets → Channel → Partners → Budget (Spend) → Visits (Traffic)
# ---------------------------------------------------------------------
def build_mapping_ui(prefix: str, df: Optional[pd.DataFrame], ref_mapping: Optional[Mapping] = None) -> Mapping:
    cols = available_columns(df)
    defaults = auto_detect_columns_filtered(df)

    # Filters (as requested)
    spend_cols   = [c for c in cols if "spend"   in c.lower()]
    traffic_cols = [c for c in cols if any(x in c.lower() for x in ["traffic", "visits"])]

    st.subheader(f"{prefix}:")

    def make_dropdown(label: str, options: List[str], default_val: Optional[str], ref_val: Optional[str], key: str):
        opts = ["-- Select --"] + options
        chosen = ref_val or default_val
        index = 0
        if chosen:
            for i, v in enumerate(opts):
                if v and v.lower() == chosen.lower():
                    index = i
                    break
        return st.selectbox(label, opts, index=index, key=key)

    # Cross-file mirror: prefer ref_mapping value if present in this df
    ref_levels = ref_mapping.level_cols if ref_mapping else {}
    ref_budget = ref_mapping.budget_col if ref_mapping else None
    ref_visits = ref_mapping.visits_col if ref_mapping else None

    # One column layout in the restored order
    # Markets
    markets = make_dropdown(
        "Markets",
        cols,
        defaults.get("Markets"),
        ref_levels.get("Markets") if ref_levels.get("Markets") in cols else None,
        f"{prefix}_markets"
    )
    # Channel
    channel = make_dropdown(
        "Channel",
        cols,
        defaults.get("Channel"),
        ref_levels.get("Channel") if ref_levels.get("Channel") in cols else None,
        f"{prefix}_channel"
    )
    # Partners
    partners = make_dropdown(
        "Partners",
        cols,
        defaults.get("Partners"),
        ref_levels.get("Partners") if ref_levels.get("Partners") in cols else None,
        f"{prefix}_partners"
    )
    # Budget (Spend-only list)
    budget = make_dropdown(
        "Budget (Spend)",
        spend_cols,
        defaults.get("Budget"),
        ref_budget if (ref_budget in spend_cols) else None,
        f"{prefix}_budget"
    )
    # Visits (Traffic/Visits list)
    visits = make_dropdown(
        "Visits (Traffic)",
        traffic_cols,
        defaults.get("Visits"),
        ref_visits if (ref_visits in traffic_cols) else None,
        f"{prefix}_visits"
    )

    return Mapping(
        level_cols={
            "Markets": None if markets == "-- Select --" else markets,
            "Channel": None if channel == "-- Select --" else channel,
            "Partners": None if partners == "-- Select --" else partners,
        },
        budget_col=None if budget == "-- Select --" else budget,
        visits_col=None if visits == "-- Select --" else visits,
    )

# ---------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------
def harmonize_channels(df: pd.DataFrame, channel_col: Optional[str]):
    if channel_col and channel_col in df.columns:
        df[channel_col] = (
            df[channel_col]
            .astype(str)
            .str.title()
            .apply(lambda x: "Paid Social" if "social" in x.lower() else "Display" if "programmatic" in x.lower() else x)
        )
    return df

def summarise_by_levels(df: pd.DataFrame, mapping: Mapping, selected_levels: List[str]) -> Dict[str, pd.DataFrame]:
    results: Dict[str, pd.DataFrame] = {}
    df = harmonize_channels(df, mapping.level_cols.get("Channel"))
    for level in selected_levels:
        level_col = mapping.level_cols.get(level)
        if not level_col or level_col not in df.columns:
            continue
        metric_cols = [c for c in [mapping.budget_col, mapping.visits_col] if c and c in df.columns]
        if not metric_cols:
            continue

        tmp = df[[level_col] + metric_cols].copy()
        tmp[level_col] = tmp[level_col].astype(str).str.title()
        for m in metric_cols:
            tmp[m] = pd.to_numeric(tmp[m], errors="coerce") / 7  # weekly → daily

        g = tmp.groupby(level_col, dropna=False)[metric_cols].sum(numeric_only=True).reset_index()
        g.rename(columns={level_col: level}, inplace=True)
        rename_map = {mapping.budget_col: "Budget", mapping.visits_col: "Visits"}
        g.rename(columns=rename_map, inplace=True)
        if "Budget" not in g.columns:
            g["Budget"] = 0.0
        if "Visits" not in g.columns:
            g["Visits"] = 0.0
        results[level] = g[[level, "Budget", "Visits"]]
    return results

def add_total_row(df: pd.DataFrame, level: str) -> pd.DataFrame:
    total = {level: "TOTAL"}
    for col in df.columns:
        if col != level and pd.api.types.is_numeric_dtype(df[col]):
            total[col] = df[col].sum()
    if "Budget (MAP)" in df.columns:
        m_sum, p_sum = df["Budget (MAP)"].sum(), df["Budget (Media Plan)"].sum()
        total["Budget (% Diff.)"] = ((p_sum - m_sum) / m_sum * 100) if m_sum else 0
    if "Visits (MAP)" in df.columns:
        m_sum, p_sum = df["Visits (MAP)"].sum(), df["Visits (Media Plan)"].sum()
        total["Visits (% Diff.)"] = ((p_sum - m_sum) / m_sum * 100) if m_sum else 0
    return pd.concat([df, pd.DataFrame([total])], ignore_index=True)

def align_and_compare(a: pd.DataFrame, b: pd.DataFrame, level: str) -> pd.DataFrame:
    a = a.rename(columns={"Budget": "Budget (MAP)", "Visits": "Visits (MAP)"})
    b = b.rename(columns={"Budget": "Budget (Media Plan)", "Visits": "Visits (Media Plan)"})
    merged = pd.merge(a, b, on=level, how="outer")

    for col in ["Budget (MAP)", "Budget (Media Plan)", "Visits (MAP)", "Visits (Media Plan)"]:
        merged[col] = pd.to_numeric(merged[col], errors="coerce").fillna(0.0)

    merged["Budget ($ Diff.)"] = merged["Budget (MAP)"] - merged["Budget (Media Plan)"]
    merged["Visits (Diff.)"] = merged["Visits (MAP)"] - merged["Visits (Media Plan)"]

    merged["Budget (% Diff.)"] = merged.apply(
        lambda r: ((r["Budget (Media Plan)"] - r["Budget (MAP)"]) / r["Budget (MAP)"] * 100)
        if r["Budget (MAP)"] != 0 else 0,
        axis=1,
    )
    merged["Visits (% Diff.)"] = merged.apply(
        lambda r: ((r["Visits (Media Plan)"] - r["Visits (MAP)"]) / r["Visits (MAP)"] * 100)
        if r["Visits (MAP)"] != 0 else 0,
        axis=1,
    )

    merged = merged[
        [
            level,
            "Budget (MAP)",
            "Budget (Media Plan)",
            "Budget ($ Diff.)",
            "Budget (% Diff.)",
            "Visits (MAP)",
            "Visits (Media Plan)",
            "Visits (Diff.)",
            "Visits (% Diff.)",
        ]
    ]
    return add_total_row(merged, level)

# ===============================================================
# 1️⃣ + 2️⃣ MAP & Media Plan Upload (Side-by-Side)
# ===============================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 1) MAP File Upload")
    file_a = st.file_uploader("Upload your **MAP File** (.xlsx, .xls, .xlsm)", type=["xlsx", "xls", "xlsm"], key="map_upload")

    xls_a, map_sheets, sheet_a, df_a = None, [], "-", None
    if file_a:
        try:
            xls_a = load_excel(file_a)
            map_sheets = [
                s for s in xls_a.sheet_names
                if "demand cr & pr archive" in s.lower() or "map" in s.lower()
            ] or xls_a.sheet_names
            sheet_a = st.selectbox("Select MAP Sheet", map_sheets, key="sheet_a")
            df_a = read_sheet_cached(xls_a, sheet_a, 0)
            if df_a is not None:
                st.success(f"✅ MAP File loaded: **{sheet_a}** ({len(df_a):,} rows)")
        except Exception as e:
            st.error(f"Failed to read MAP file: {e}")
    else:
        st.info("Please upload your MAP file to continue.")

with col2:
    st.markdown("### 2) Media Plan Upload")
    file_b = st.file_uploader("Upload your **Media Plan File** (.xlsx, .xls, .xlsm)", type=["xlsx", "xls", "xlsm"], key="media_upload")

    xls_b, media_sheets, sheet_b, df_b = None, [], "-", None
    if file_b:
        try:
            xls_b = load_excel(file_b)
            all_sheets = xls_b.sheet_names
            media_sheets = [
                s for s in all_sheets
                if any(k in s.lower() for k in ["mapexport", "plan", "media"])
            ] or all_sheets
            default_media = (
                next((s for s in media_sheets if "mapexport" in s.lower()), None)
                or media_sheets[0]
            )
            sheet_b = st.selectbox(
                "Select Media Plan Sheet",
                media_sheets,
                index=media_sheets.index(default_media) if default_media in media_sheets else 0,
                key="sheet_b",
            )
            df_b = read_sheet_cached(xls_b, sheet_b, 1)
            if df_b is not None:
                st.success(f"✅ Media Plan loaded: **{sheet_b}** ({len(df_b):,} rows)")
        except Exception as e:
            st.error(f"Failed to read Media Plan file: {e}")
    else:
        st.info("Please upload your Media Plan file to continue.")

# ===============================================================
# 3️⃣ + 4️⃣ Comparison Settings & Campaign Selection (Always Visible)
# ===============================================================
st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.markdown("### 3) Comparison Settings")
    levels = st.multiselect(
        "Choose levels to compare",
        ["Markets", "Channel", "Partners"],
        default=["Markets", "Channel", "Partners"],
        key="levels_select",
    )

with col4:
    st.markdown("### 4) Select Campaign(s)")
    if df_a is not None and "Campaign" in df_a.columns:
        campaigns = sorted(df_a["Campaign"].dropna().astype(str).unique())
        selected = st.multiselect(
            "Choose one or more campaigns",
            campaigns,
            placeholder="Select campaigns..."
        )
        if selected:
            df_a = df_a[df_a["Campaign"].astype(str).isin(selected)]
    else:
        st.multiselect(
            "Choose one or more campaigns",
            [],
            placeholder="Upload a MAP file to enable campaign selection...",
            disabled=True
        )


# ===============================================================
# 5️⃣ & 6️⃣ Column Mapping (Side-by-Side)
# ===============================================================
st.markdown("---")

col5, col6 = st.columns(2)

with col5:
    map_a = build_mapping_ui("5) MAP Column Selection", df_a)

with col6:
    map_b = build_mapping_ui("6) Media Plan Column Selection", df_b, ref_mapping=map_a)

# ---------------------------------------------------------------------
# Run comparison
# ---------------------------------------------------------------------
st.divider()
if st.button("🔎 Compare Files", type="primary", disabled=(df_a is None or df_b is None)):
    if not levels:
        st.warning("Select at least one level to compare.")
    else:
        sums_a, sums_b = summarise_by_levels(df_a, map_a, levels), summarise_by_levels(df_b, map_b, levels)
        tabs = st.tabs(levels)
        for i, lvl in enumerate(levels):
            with tabs[i]:
                a_lvl, b_lvl = sums_a.get(lvl), sums_b.get(lvl)
                if a_lvl is None or b_lvl is None:
                    st.warning(f"{lvl}: missing mapping.")
                    continue
                comp = align_and_compare(a_lvl, b_lvl, lvl)

                # Level label display rule: <=3 chars → UPPER, else Title; keep TOTAL as-is
                comp[lvl] = comp[lvl].apply(
                    lambda x: "TOTAL" if str(x) == "TOTAL" else (str(x).upper() if len(str(x)) <= 3 else str(x).title())
                )

                # Format output (centered)
                df_fmt = comp.copy()
                for col in df_fmt.columns:
                    if "Budget" in col and not col.endswith("% Diff.)"):
                        df_fmt[col] = df_fmt[col].apply(lambda x: f"${x:,.2f}")
                    elif "Visits" in col and not col.endswith("% Diff.)"):
                        df_fmt[col] = df_fmt[col].apply(lambda x: f"{int(round(x)):,}")
                    elif col.endswith("% Diff.)"):
                        df_fmt[col] = df_fmt[col].apply(
                            lambda x: f"<span style='color:{'red' if abs(x) > 5 else 'black'};"
                                      f"font-weight:{'bold' if abs(x) > 5 else 'normal'}'>{x:.2f}%</span>"
                        )
                    # Bold TOTAL row
                    if lvl in df_fmt.columns:
                        df_fmt.loc[df_fmt[lvl] == "TOTAL", col] = "<b>" + df_fmt.loc[df_fmt[lvl] == "TOTAL", col].astype(str) + "</b>"

                html_table = df_fmt.to_html(escape=False, index=False, justify="center")
                html_table = html_table.replace('<table ', '<table style="margin:auto;text-align:center" ')
                st.markdown(html_table, unsafe_allow_html=True)

                # Add vertical spacing before download button
                st.markdown("<br>", unsafe_allow_html=True)

                # Downloads
                csv_buf = io.StringIO()
                comp.to_csv(csv_buf, index=False)
                st.download_button(
                    f"⬇️ Download {lvl} Comparison",
                    csv_buf.getvalue(),
                    f"comparison_{lvl}.csv",
                    "text/csv",
                )

import streamlit as st
from PIL import Image, ImageDraw
import random
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Monitoring Sawit",
    page_icon="📊",
    layout="wide"
)

img_logo = Image.open('images.jpeg')
st.logo(img_logo, size="large")

st.markdown("""
    <style>
        @media (min-width: 1024px) {
            .stMainBlockContainer{
                padding: 0px;
                padding-top: 60px;
                max-width: 1600px;
            }
        }
        .stToolbarActions, .stMainMenu, .stAppDeployButton{
            display: none !important;
        }
        .stAppHeader{
            background: black;
            border-bottom: 1px solid white;
        }
        .stSidebar{
            border-top-right-radius: 40px;
            border-bottom-right-radius: 40px;
            box-shadow: 5px 0px 5px 1px rgba(0, 0, 0, 0.1);
            width: 270px !important;
            background: white;
        }
        /* Hide the image inside the sidebar collapsed control */
        [data-testid="stSidebarCollapsedControl"]{
            top: 0px
        }
        [data-testid="stSidebarCollapsedControl"] img {
            display: none !important;
        }

        /* Add your custom text */
        [data-testid="stSidebarCollapsedControl"]::before {
            content: "🌴 Dashboard Monitoring Sawit";  /* Replace with your desired text */
            font-size: 24px;
            color: white;
            display: block;
            text-align: center;
            padding: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Dummy data
dummy_sites = {
    "Site 1": {
        "areas": ["Sektor A", "Sektor B", "Sektor C"],
        "diseases": [
            {"name": "Hama Fungi", "status": "warning", "date": "12 Mei 2024 10:00 WIB"},
            {"name": "Hama Tikus", "status": "warning", "date": "19 Mei 2024 12:15 WIB"},
            {"name": "Hama Insect", "status": "warning", "date": "Belum ada update"},
            {"name": "Hama Tanaman", "status": "ok", "date": "12 Mei 2024 10:00 WIB"},
            {"name": "Genetic", "status": "ok", "date": "19 Mei 2024 12:15 WIB"},
        ],
    },
    "Site 2": {
        "areas": ["Sektor D", "Sektor E", "Sektor F"],
        "diseases": [
            {"name": "Hama Fungi", "status": "warning", "date": "11 Mei 2024 11:00 WIB"},
            {"name": "Hama Tikus", "status": "ok", "date": "20 Mei 2024 12:00 WIB"},
            {"name": "Hama Insect", "status": "ok", "date": "Update minggu ini"},
            {"name": "Hama Tanaman", "status": "warning", "date": "10 Mei 2024 09:00 WIB"},
            {"name": "Genetic", "status": "ok", "date": "20 Mei 2024 13:15 WIB"},
        ],
    },
}

# Initialize session state
if "selected_tree" not in st.session_state:
    st.session_state.selected_tree = None

# Layout columns
# st.set_page_config(layout="wide")
# st.markdown("<h4 style='text-align:center;'>Dashboard Monitoring Sawit</h4>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 5, 3], gap="small")

# --- Sidebar (Left)
with col1:
    # Sidebar dropdown and search bar
    selected_site  = st.selectbox("Daftar Main Site", list(dummy_sites.keys()))
    site_data = dummy_sites[selected_site]

    st.text_input("Cari Area dalam Site")

    # Simulated images (use your real image files here)
    # For demonstration, we use the same image repeatedly
    uploaded_image = "images.jpeg"
    image = Image.open(f"{uploaded_image}")

    # Sector data
    sectors = [
        ("Sektor A (10 Ha)", image),
        ("Sektor B (13 Ha)", image),
        ("Sektor C (10 Ha)", image),
        ("Area D (12 Ha)", image),
        ("Sektor E", image),
        ("Sektor F", image),
        ("Sektor G", image),
        ("Sektor H", image),
        ("Sektor C", image),
        ("Sektor C", image)
    ]

    # Display images in a grid
    cols = st.columns(2)
    for idx, (label, img) in enumerate(sectors):
        with cols[idx % 2]:
            st.image(img, caption=label, use_container_width=True)

# --- Center Content
with col2:
    st.markdown("### Citra Satelit dan AI Mapping")
    left_img, right_img = st.columns(2)
    with left_img:
        st.image("https://www.shutterstock.com/image-photo/aerial-view-green-palm-plantation-600nw-2493810749.jpg", caption="Citra Satelit", use_container_width =True)

    # Right image with bounding boxes (simulate tree detection)
    with right_img:
        # Draw dummy bounding boxes
        def draw_tree_map():
            image = Image.new("RGB", (264, 200), "green")
            draw = ImageDraw.Draw(image)
            boxes = [(60, 40), (100, 90), (200, 130), (300, 200)]
            for idx, (x, y) in enumerate(boxes, 1):
                draw.rectangle([x, y, x + 30, y + 30], outline="red", width=2)
                draw.text((x + 5, y + 5), f"T{idx}", fill="white")
            return image, boxes

        image, boxes = draw_tree_map()
        st.image(image, caption="Palm Tree Map", use_container_width=True)

        

    st.markdown("""
        <style>
            .section-header {
                font-size: 20px;
                font-weight: 600;
                border-bottom: 1px solid #555;
                margin-bottom: 10px;
            }
            .row {
                display: flex;
                align-items: center;
                margin-bottom: 12px;
            }
            .row span {
                margin-left: 10px;
            }
            .ok-box {
                background-color: #00cc66;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            .icon {
                font-size: 18px;
            }
            .no-data {
                background-color: white;
                color: black;
                font-weight: bold;
                padding: 4px 10px;
                border-radius: 4px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Split into two columns
    col1, col2 = st.columns(2)

    # Column 1: Kondisi Lima Penyakit
    with col1:
        st.markdown("<div class='section-header'>Kondisi Lima Penyakit “Area A” Minggu Ini/ Periode Ini</div>", unsafe_allow_html=True)

        st.markdown("""
            <div class="row">⚠️ <span>Hama Fungi<br><small>12 Mei 2024 10:00 WIB</small></span></div>
            <div class="row">⚠️ <span>Hama Tikus<br><small>19 Mei 2024 12:15 WIB</small></span></div>
            <div class="row"><div class="no-data">No Data</div> <span>Hama Insect<br><small>Belum ada update minggu ini</small></span></div>
            <div class="row"><div class="ok-box">OK</div> <span>Hama Tanaman<br><small>12 Mei 2024 10:00 WIB</small></span></div>
            <div class="row"><div class="ok-box">OK</div> <span>Genetic<br><small>19 Mei 2024 12:15 WIB</small></span></div>
        """, unsafe_allow_html=True)

    # Column 2: Metadata Area
    with col2:
        st.markdown("<div class='section-header'>Metadata Area</div>", unsafe_allow_html=True)

        entries = [
            ("Panen", "12 Mei 2024 10:00 WIB"),
            ("Pupuk Tahunan 2", "19 Mei 2024 12:15 WIB"),
            ("Panen", "19 Mei 2024 13:00 WIB"),
            ("Panen", "12 Mei 2024 10:00 WIB"),
            ("Prunning Tahunan 1", "19 Mei 2024 12:15 WIB"),
            ("Pupuk Tahunan 1", "19 Januari 2024 13:00 WIB"),
        ]

        for title, date in entries:
            st.markdown(f"""
                <div class="row">📍 <span>{title}<br><small>{date}</small></span> <span style='margin-left:auto;'>⚠️</span></div>
            """, unsafe_allow_html=True)

# --- Right Dashboard
with col3:
    # Custom CSS
    st.markdown("""
        <style>
            body {
                background-color: #111;
                color: white;
            }
            .metric-box-atas {
                border: 5px solid #1e1e1e;
                border-radius: 7px;
                padding: 10px;
                text-align: center;
            }
            .metric-box {
                background-color: #1e1e1e;
                border-radius: 7px;
                padding: 10px;
                text-align: center;
            }
            .title {
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .subtitle {
                font-size: 17px;
                margin: 10px 0;
            }
            .box-header {
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 10px;
            }
            .task-box {
                padding: 15px;
                margin-bottom: 10px;
            }
            .task-entry {
                display: flex;
                justify-content: space-between;
                margin-bottom: 8px;
            }
            .ok {
                background-color: #00cc66;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            .icon {
                font-size: 18px;
            }
                
            .info-big{
                font-size: 18px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("<div class='title'>Dashboard Monitoring Sawit</div>", unsafe_allow_html=True)

    # Site and month
    col1, col2 = st.columns([1, 1])
    with col1:
        # st.markdown("<div class='subtitle'>Site 1</div>", unsafe_allow_html=True)
        st.markdown("### Site 1")
    with col2:
        st.selectbox("Pilih Bulan", ["Januari", "Februari", "Maret"], label_visibility="collapsed")

    # Top Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-box-atas'><div class='box-header'>Luas</div><h2 class='info-big'>1.000 Ha</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-box-atas'><div class='box-header'>Jumlah Pohon/Area</div><h2 class='info-big'>64.000 / 20 Area</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-box-atas'><div class='box-header'>Perlu Tindak Lanjut</div><h2 class='info-big'>320</h2></div>", unsafe_allow_html=True)

    # Mid Section Title
    st.markdown("##### Tindak Lanjut dibutuhkan Minggu/Periode Ini")

    # Indikasi Berpenyakit & Rencana Panen
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='metric-box' style='margin-bottom: 20px;'><div class='box-header'>Indikasi Berpenyakit</div><h2 class='info-big'>320</h2></div>", unsafe_allow_html=True)
        for site in ["Site 1 Area 5", "Site 1 Area 2", "Site 3 Area 1", "Site 3 Area 5", "Site 3 Area 12"]:
            st.markdown(f"""
                <div class='task-box'>
                    <div class='task-entry'>
                        <span>📍 {site}<br><small>12 Mei 2024 10:00 WIB</small></span>
                        <span class='icon'>⚠️</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)


    with col2:
        st.markdown("<div class='metric-box' style='margin-bottom: 20px;'><div class='box-header'>Rencana Panen</div><h2 class='info-big'>2.240</h2></div>", unsafe_allow_html=True)
        for site in ["Site 1 Area 5", "Site 1 Area 2", "Site 3 Area 1", "Site 3 Area 5", "Site 3 Area 12"]:
            st.markdown(f"""
                <div class='task-box'>
                    <div class='task-entry'>
                        <span>📍 {site}<br><small>19 Mei 2024 12:15 WIB</small></span>
                        <span class='icon'>⚠️</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Rencana Pupuk & Rencana Prunning
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='metric-box' style='margin-bottom: 20px;'><div class='box-header'>Rencana Pupuk</div><h2 class='info-big'>320</h2></div>", unsafe_allow_html=True)
        for i in range(1, 4):
            st.markdown(f"""
                <div class='task-box'>
                    <div class='task-entry'>
                        <span>📍 Pemupukan {i}<br><small>12 Mei 2024 10:00 WIB</small></span>
                        <span class='ok'>OK</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='metric-box'  style='margin-bottom: 20px;'><div class='box-header'>Rencana Prunning</div><h2 class='info-big'>2.240</h2></div>", unsafe_allow_html=True)
        for i, month in enumerate(["Februari", "July", "October"], 1):
            ok_badge = "<span class='ok'>OK</span>" if i < 3 else "<span class='icon'>⚠️</span>"
            st.markdown(f"""
                <div class='task-box'>
                    <div class='task-entry'>
                        <span>📍 Prunning Tahunan {i}<br><small>{month}</small></span>
                        {ok_badge}
                    </div>
                </div>
            """, unsafe_allow_html=True)

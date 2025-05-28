import streamlit as st
from PIL import Image, ImageDraw
import random
from datetime import datetime
from streamlit_image_select import image_select
import base64
import json
import streamlit.components.v1 as components

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
    <style>
        .image-container {{
            position: relative;
            width: 100%;
        }}

        .responsive-img {{
            width: 100%;
            height: auto;
            display: block;
        }}

        .bbox {{
            position: absolute;
            border: 2px solid red;
            box-sizing: border-box;
        }}

        .bbox:hover {{
            background-color: rgba(255, 0, 0, 0.2);
        }}

        .tooltip {{
            visibility: hidden;
            width: max-content;
            background-color: black;
            color: white;
            text-align: left;
            border-radius: 5px;
            padding: 6px;
            position: absolute;
            z-index: 1;
            top: -10px;
            left: 105%;
            white-space: nowrap;
            font-size: 12px;
        }}

        .bbox:hover .tooltip {{
            visibility: visible;
        }}
    </style>
""", unsafe_allow_html=True)

# Dummy data
dummy_sites = {
    "Site 1": {
        "luas": "1.000 Ha",
        "jumlah_pohon": "64.000 / 20 Area",
        "Perlu Tindak Lanjut": "320",
        "Indikasi Berpenyakit": 320,
        "rencana panen": 2240,
        "tindak lanjut minggu ini": [
            [
                {"title": "Site 1 Area 1", "subtitle": "12 Mei 2024 10:00 WIB", "icon": "⚠️"},
                {"title": "Site 1 Area 2", "subtitle": "13 Mei 2024 09:00 WIB", "icon": "🛠️"},
                {"title": "Site 1 Area 3", "subtitle": "14 Mei 2024 14:00 WIB", "icon": "✅"},
                {"title": "Site 1 Area 4", "subtitle": "15 Mei 2024 08:30 WIB", "icon": "⚠️"},
                {"title": "Site 1 Area 5", "subtitle": "16 Mei 2024 11:45 WIB", "icon": "🛠️"}
            ]
        ],
        "areas": [
            {"name": "Sektor A", "luas": "10 Ha", "metadata": [{"title": "Panen", "subtitle": "12 Mei 2024 10:00 WIB", "icon": "⚠️"}]},
            {"name": "Sektor B", "luas": "12 Ha", "metadata": [{"title": "Penyemprotan", "subtitle": "13 Mei 2024 09:00 WIB", "icon": "🛠️"}]},
            {"name": "Sektor C", "luas": "15 Ha", "metadata": [{"title": "Pemupukan", "subtitle": "14 Mei 2024 14:00 WIB", "icon": "✅"}]},
            {"name": "Sektor D", "luas": "8 Ha", "metadata": [{"title": "Penyulaman", "subtitle": "15 Mei 2024 08:30 WIB", "icon": "⚠️"}]},
            {"name": "Sektor E", "luas": "11 Ha", "metadata": [{"title": "Pengamatan", "subtitle": "16 Mei 2024 11:45 WIB", "icon": "🛠️"}]}
        ]
    },
    "Site 2": {
        "luas": "850 Ha",
        "jumlah_pohon": "45.500 / 18 Area",
        "Perlu Tindak Lanjut": "275",
        "Indikasi Berpenyakit": 198,
        "rencana panen": 1800,
        "tindak lanjut minggu ini": [
            [
                {"title": "Site 2 Area 1", "subtitle": "10 Mei 2024 08:00 WIB", "icon": "🛠️"},
                {"title": "Site 2 Area 2", "subtitle": "11 Mei 2024 09:30 WIB", "icon": "⚠️"},
                {"title": "Site 2 Area 3", "subtitle": "12 Mei 2024 13:00 WIB", "icon": "✅"},
                {"title": "Site 2 Area 4", "subtitle": "13 Mei 2024 15:30 WIB", "icon": "⚠️"},
                {"title": "Site 2 Area 5", "subtitle": "14 Mei 2024 07:45 WIB", "icon": "🛠️"}
            ]
        ],
        "areas": [
            {"name": "Blok A", "luas": "9 Ha", "metadata": [{"title": "Pemupukan", "subtitle": "10 Mei 2024 08:00 WIB", "icon": "🛠️"}]},
            {"name": "Blok B", "luas": "10 Ha", "metadata": [{"title": "Pengamatan", "subtitle": "11 Mei 2024 09:30 WIB", "icon": "⚠️"}]},
            {"name": "Blok C", "luas": "7 Ha", "metadata": [{"title": "Panen", "subtitle": "12 Mei 2024 13:00 WIB", "icon": "✅"}]},
            {"name": "Blok D", "luas": "14 Ha", "metadata": [{"title": "Penyulaman", "subtitle": "13 Mei 2024 15:30 WIB", "icon": "⚠️"}]},
            {"name": "Blok E", "luas": "11 Ha", "metadata": [{"title": "Penyemprotan", "subtitle": "14 Mei 2024 07:45 WIB", "icon": "🛠️"}]}
        ]
    },
    "Site 3": {
        "luas": "1.200 Ha",
        "jumlah_pohon": "70.000 / 22 Area",
        "Perlu Tindak Lanjut": "350",
        "Indikasi Berpenyakit": 290,
        "rencana panen": 2500,
        "tindak lanjut minggu ini": [
            [
                {"title": "Site 3 Area 1", "subtitle": "10 Mei 2024 08:15 WIB", "icon": "⚠️"},
                {"title": "Site 3 Area 2", "subtitle": "11 Mei 2024 10:45 WIB", "icon": "🛠️"},
                {"title": "Site 3 Area 3", "subtitle": "12 Mei 2024 12:00 WIB", "icon": "✅"},
                {"title": "Site 3 Area 4", "subtitle": "13 Mei 2024 14:20 WIB", "icon": "⚠️"},
                {"title": "Site 3 Area 5", "subtitle": "14 Mei 2024 09:15 WIB", "icon": "🛠️"}
            ]
        ],
        "areas": [
            {"name": "Unit A", "luas": "10 Ha", "metadata": [{"title": "Pembersihan", "subtitle": "10 Mei 2024 08:15 WIB", "icon": "⚠️"}]},
            {"name": "Unit B", "luas": "9 Ha", "metadata": [{"title": "Penyulaman", "subtitle": "11 Mei 2024 10:45 WIB", "icon": "🛠️"}]},
            {"name": "Unit C", "luas": "12 Ha", "metadata": [{"title": "Panen", "subtitle": "12 Mei 2024 12:00 WIB", "icon": "✅"}]},
            {"name": "Unit D", "luas": "13 Ha", "metadata": [{"title": "Penyemprotan", "subtitle": "13 Mei 2024 14:20 WIB", "icon": "⚠️"}]},
            {"name": "Unit E", "luas": "15 Ha", "metadata": [{"title": "Pemupukan", "subtitle": "14 Mei 2024 09:15 WIB", "icon": "🛠️"}]}
        ]
    },
    "Site 4": {
        "luas": "900 Ha",
        "jumlah_pohon": "50.000 / 16 Area",
        "Perlu Tindak Lanjut": "290",
        "Indikasi Berpenyakit": 210,
        "rencana panen": 1900,
        "tindak lanjut minggu ini": [
            [
                {"title": "Site 4 Area 1", "subtitle": "09 Mei 2024 07:30 WIB", "icon": "🛠️"},
                {"title": "Site 4 Area 2", "subtitle": "10 Mei 2024 10:15 WIB", "icon": "⚠️"},
                {"title": "Site 4 Area 3", "subtitle": "11 Mei 2024 11:45 WIB", "icon": "✅"},
                {"title": "Site 4 Area 4", "subtitle": "12 Mei 2024 13:30 WIB", "icon": "⚠️"},
                {"title": "Site 4 Area 5", "subtitle": "13 Mei 2024 08:10 WIB", "icon": "🛠️"}
            ]
        ],
        "areas": [
            {"name": "Zona A", "luas": "8 Ha", "metadata": [{"title": "Pemangkasan", "subtitle": "09 Mei 2024 07:30 WIB", "icon": "🛠️"}]},
            {"name": "Zona B", "luas": "9 Ha", "metadata": [{"title": "Pembersihan", "subtitle": "10 Mei 2024 10:15 WIB", "icon": "⚠️"}]},
            {"name": "Zona C", "luas": "10 Ha", "metadata": [{"title": "Panen", "subtitle": "11 Mei 2024 11:45 WIB", "icon": "✅"}]},
            {"name": "Zona D", "luas": "11 Ha", "metadata": [{"title": "Penyemprotan", "subtitle": "12 Mei 2024 13:30 WIB", "icon": "⚠️"}]},
            {"name": "Zona E", "luas": "12 Ha", "metadata": [{"title": "Pengamatan", "subtitle": "13 Mei 2024 08:10 WIB", "icon": "🛠️"}]}
        ]
    },
    "Site 5": {
        "luas": "1.100 Ha",
        "jumlah_pohon": "67.000 / 21 Area",
        "Perlu Tindak Lanjut": "310",
        "Indikasi Berpenyakit": 240,
        "rencana panen": 2300,
        "tindak lanjut minggu ini": [
            [
                {"title": "Site 5 Area 1", "subtitle": "08 Mei 2024 07:00 WIB", "icon": "⚠️"},
                {"title": "Site 5 Area 2", "subtitle": "09 Mei 2024 08:45 WIB", "icon": "🛠️"},
                {"title": "Site 5 Area 3", "subtitle": "10 Mei 2024 09:30 WIB", "icon": "✅"},
                {"title": "Site 5 Area 4", "subtitle": "11 Mei 2024 14:15 WIB", "icon": "⚠️"},
                {"title": "Site 5 Area 5", "subtitle": "12 Mei 2024 15:00 WIB", "icon": "🛠️"}
            ]
        ],
        "areas": [
            {"name": "Wilayah A", "file_gambar": "142129.png", "luas": "10 Ha", "metadata": [{"title": "Pemupukan", "subtitle": "08 Mei 2024 07:00 WIB", "icon": "⚠️"}]},
            {"name": "Wilayah B", "file_gambar": "142759.png", "luas": "12 Ha", "metadata": [{"title": "Penyemprotan", "subtitle": "09 Mei 2024 08:45 WIB", "icon": "🛠️"}]},
            {"name": "Wilayah C", "file_gambar": "143948.png", "luas": "14 Ha", "metadata": [{"title": "Panen", "subtitle": "10 Mei 2024 09:30 WIB", "icon": "✅"}]},
            {"name": "Wilayah D", "file_gambar": "144214.png", "luas": "9 Ha", "metadata": [{"title": "Pembersihan", "subtitle": "11 Mei 2024 14:15 WIB", "icon": "⚠️"}]},
            {"name": "Wilayah E", "file_gambar": "144239.png", "luas": "11 Ha", "metadata": [{"title": "Pengamatan", "subtitle": "12 Mei 2024 15:00 WIB", "icon": "🛠️"}]}
        ]
    }
}

# Initialize session state
if "selected_tree" not in st.session_state:
    st.session_state.selected_tree = None

# Layout columns
# st.set_page_config(layout="wide")
# st.markdown("<h4 style='text-align:center;'>Dashboard Monitoring Sawit</h4>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2.3, 5, 2.7], gap="small")

# --- Sidebar (Left)
with col1:
    # Sidebar dropdown and search bar
    selected_site  = st.selectbox("Daftar Main Site", list(dummy_sites.keys()), index=4)
    site_data = dummy_sites[selected_site]
    nama_folder = selected_site.lower().replace(" ", "")

    names_area = [item["name"] for item in site_data["areas"]]
    picts_area = [f'site5/{item["file_gambar"]}' for item in site_data["areas"]]

    # st.write(picts_area)

    st.text_input("Cari Area :", placeholder="Cari Area disini ...")

    # Simulated images (use your real image files here)
    # For demonstration, we use the same image repeatedly
    uploaded_image = "images.jpeg"
    image = Image.open(f"{uploaded_image}")

    # resized_image = image.resize((50, 50))
    
    # st_image_button("Title", "images.jpeg", "150px", "outlined")
    img_selected = image_select("PIlih Area :", picts_area, names_area, use_container_width=False)

    st.write(img_selected)

def image_to_base64(img):
    from io import BytesIO
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str 
    
def render_html_bounding_box(image_path):
    # Load image
    image = Image.open(image_path)
    img_width, img_height = image.size
    img_base64 = image_to_base64(image)

    # Load boxes from JSON
    json_path = image_path.replace(".png", ".json")
    with open(json_path, "r") as f:
        # boxes = json.load(f)
        box_data = json.load(f)
        if isinstance(box_data, dict):
            box_data = [box_data]

    # Generate bounding boxes HTML
    box_divs = ""
    for idx, box in enumerate(box_data, 1):
        x1, y1, x2, y2 = box["x1"], box["y1"], box["x2"], box["y2"]
        left_pct = (x1 / img_width) * 100
        top_pct = (y1 / img_height) * 100
        width_pct = ((x2 - x1) / img_width) * 100
        height_pct = ((y2 - y1) / img_height) * 100

        is_sehat = box.get('kesehatan', '-')

        tooltip = (
            f"<b>Pohon {idx}</b><br>"
            f"Confidence: {box.get('confidence', 0):.2f}<br>"
            f"Kesehatan: {box.get('kesehatan', '-')}" + "<br>"
            f"Butuh Panen: {box.get('butuh_panen', '-')}" + "<br>"
            f"Butuh Prunning: {box.get('butuh_prunning', '-')}" + "<br>"
            f"Butuh Pupuk: {box.get('butuh_pupuk', '-')}"
        )

        box_divs += f"""
        <div class="bbox {is_sehat} hidden" id="box{idx}" style="
            left: {left_pct:.2f}%;
            top: {top_pct:.2f}%;
            width: {width_pct:.2f}%;
            height: {height_pct:.2f}%;
        ">
            <span class="tooltip">{tooltip}</span>
        </div>
        """

    # Final HTML with script to auto-resize iframe
    html_content = f"""
    <html>
    <head>
    <style>
    body {{
        margin: 0;
    }}
    .image-container {{
        position: relative;
        width: 100%;
    }}
    .responsive-img {{
        width: 100%;
        height: auto;
        display: block;
    }}
    .bbox {{
        position: absolute;
        box-sizing: border-box;
    }}
    .hidden {{
        display: none;
    }}

    .bbox.sehat{{
        border: 2px solid blue;
    }}
    .bbox.sakit{{
        border: 2px solid red;
    }}
    .bbox:hover {{
        background-color: rgba(0, 0, 0, 0.4);
        cursor: pointer;
    }}
    .tooltip {{
        visibility: hidden;
        background-color: rgba(0, 0, 0, 0.85);
        color: #fff;
        text-align: left;
        border-radius: 6px;
        padding: 6px;
        position: absolute;
        z-index: 99;
        top: -10px;
        left: 105%;
        font-size: 12px;
        white-space: nowrap;
    }}
    .bbox:hover .tooltip {{
        visibility: visible;
    }}

    .overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.25); /* semi-transparent overlay */
        z-index: 1;
    }}
    #container {{
        position: relative;
        display: inline-block;
    }}
    #progress-indicator {{
        position: absolute;
        top: 10px;
        left: 10px;
        background: rgba(0,0,0,0.6);
        color: white;
        padding: 8px 12px;
        font-size: 14px;
        border-radius: 6px;
        z-index: 10;
    }}
    </style>
    </head>
    <body>
        <div class="image-container" id="container">
            <img src="data:image/png;base64,{img_base64}" class="responsive-img" id="img">
            <div class="overlay"></div>
            <div id="progress-indicator">Mem-proses: 0%, 0 pohon terdeteksi</div>
            {box_divs}
        </div>

        <script>
            function updateIframeHeight() {{
                const height = document.getElementById("container").offsetHeight;
                window.parent.postMessage({{ "streamlitHeight": height }}, "*");
            }}
            //window.addEventListener("load", updateIframeHeight);
            //window.addEventListener("resize", updateIframeHeight);

            const totalBoxes = {len(box_data)};
            let shownBoxes = 0;

            function showNextBatch() {{
                let batchSize = Math.floor(Math.random() * 3) + 2;  // show 2-4 boxes randomly
                for (let i = 0; i < batchSize && shownBoxes < totalBoxes; i++) {{
                    const box = document.getElementById('box' + shownBoxes);
                    if (box) {{
                        box.classList.remove('hidden');
                    }}
                    shownBoxes++;
                }}
                const percent = Math.floor((shownBoxes / totalBoxes) * 100);
                const progressEl = document.getElementById('progress-indicator');
                const overlayEl = document.querySelector('.overlay');
                progressEl.innerText = `Progress: ${{percent}}%, ${{shownBoxes}} trees detected`;

                if (shownBoxes < totalBoxes) {{
                    setTimeout(showNextBatch, Math.floor(Math.random() * 100) + 50);  // delay 500–1500ms
                }} else {{
                    if (overlayEl) overlayEl.remove();
                    if (progressEl) progressEl.remove();
                }}
            }}

            window.onload = () => {{
                showNextBatch();
            }};
        </script>
    </body>
    </html>
    """

    # Minimal initial height, actual height adjusts automatically
    components.html(html_content, height=400, scrolling=False)

# --- Center Content
with col2:
    st.markdown("### Citra Satelit dan AI Mapping")
    left_img, right_img = st.columns(2)
    with left_img:
        st.image(img_selected, caption="Citra Satelit", use_container_width =True)

    # Right image with bounding boxes (simulate tree detection)
    with right_img:
        render_html_bounding_box(img_selected)
        

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
        st.markdown(f"### {selected_site}")
    with col2:
        st.selectbox("Pilih Bulan", ["Januari", "Februari", "Maret"], label_visibility="collapsed")

    # Top Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-box-atas'><div class='box-header'>Luas</div><h2 class='info-big'>{site_data["luas"]}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box-atas'><div class='box-header'>Jumlah Pohon/Area</div><h2 class='info-big'>{site_data["jumlah_pohon"]}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box-atas'><div class='box-header'>Perlu Tindak Lanjut</div><h2 class='info-big'>{site_data["Perlu Tindak Lanjut"]}</h2></div>", unsafe_allow_html=True)

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

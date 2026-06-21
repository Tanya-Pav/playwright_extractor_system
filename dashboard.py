import streamlit as st
import pandas as pd
import plotly.express as px
import config
import io  # Модуль для работы с буфером памяти при экспорте в XLSX

# Custom CSS theme (Coffee-caramel palette)
custom_coffee_style = """
<style>
    /* App main background and text */
    .stApp {
        background-color: #FDFBF7; 
        color: #4A3B32; 
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #5C4033; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* KPI Cards */
    [data-testid="stMetricValue"] {
        color: #8B5A2B; 
        font-weight: bold;
    }
    [data-testid="stMetricLabel"] {
        color: #6F4E37; 
    }
    div[data-testid="stMetric"] {
        background-color: #F4EAE1; 
        padding: 15px 25px;
        border-radius: 10px;
        border: 1px solid #E6D5C3;
    }

    /* Sidebar container */
    section[data-testid="stSidebar"] {
        background-color: #EFE6DD; 
        border-right: 1px solid #D7C4B7;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #5C4033;
    }

    /* Text input fields */
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF;
        border: 1px solid #D7C4B7;
        color: #4A3B32;
        border-radius: 8px;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #8B5A2B;
        box-shadow: 0 0 0 1px #8B5A2B;
    }

    /* Navigation tabs overrides */
    button[data-baseweb="tab"] {
        color: #6F4E37 !important;
        font-size: 16px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #5C4033 !important;
        border-bottom-color: #8B5A2B !important;
        font-weight: bold !important;
    }

    /* Custom HTML data tables */
    .coffee-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 16px;
        background-color: #FDFBF7;
        color: #4A3B32;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .coffee-table th {
        background-color: #EFE6DD;
        color: #5C4033;
        text-align: left;
        padding: 14px;
        font-weight: bold;
        border-bottom: 2px solid #D7C4B7;
    }
    .coffee-table td {
        padding: 12px;
        border-bottom: 1px solid #E6D5C3;
        background-color: #F9F3EB; 
    }
    .coffee-table tr:hover td {
        background-color: #F4EAE1; 
    }

    /* Action buttons overrides */
    div[data-testid="stDownloadButton"] button, 
    div.stDownloadButton > button,
    .stDownloadButton p {
        background-color: #8B5A2B !important; 
        color: #FFFFFF !important; 
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 24px !important;
        width: 100% !important; 
        transition: all 0.3s ease !important;
    }

    div[data-testid="stDownloadButton"] button:hover {
        background-color: #5C4033 !important; 
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(139, 90, 43, 0.3) !important;
        transform: translateY(-1px);
    }

    /* Code blocks and badge overrides */
    div[data-testid="stMarkdownContainer"] code {
        background-color: #EFE6DD !important; 
        color: #5C4033 !important; 
        border: 1px solid #D7C4B7 !important; 
        padding: 4px 8px !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
</style>
"""

# Page layout configuration
st.set_page_config(page_title="Data Extraction Dashboard", page_icon="📊", layout="wide")
st.markdown(custom_coffee_style, unsafe_allow_html=True)

# Header section
st.title("Playwright Web Automation & Data Extraction System")
st.markdown("This interactive dashboard displays production-ready data extracted by the automated system.")

# --- БЛОК НАВИГАЦИИ (Sidebar) ---
st.sidebar.header("📁 System Configuration")

# Инициализируем внутреннее состояние сессии, если приложение открыто впервые
if "active_case" not in st.session_state:
    st.session_state.active_case = config.CURRENT_CASE

# Выпадающий список привязан к session_state
current_case = st.sidebar.selectbox(
    "Active Case (Visual Mode):",
    ["quotes", "ecommerce"],
    index=0 if st.session_state.active_case == "quotes" else 1
)

# Если пользователь изменил выбор — обновляем глобальный конфиг и перезапускаем
if current_case != st.session_state.active_case:
    st.session_state.active_case = current_case
    config.CURRENT_CASE = current_case
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("💡 Technical Stack Illustrated:")
st.sidebar.markdown(
    "- **Playwright Engine**\n"
    "- **Asynchronous Pipeline**\n"
    "- **Network Response Interception**\n"
    "- **Dynamic HTML DOM Parsing**\n"
    "- **Multi-format Data Delivery**"
)

# Core data pipeline verification (Используем новые функции получения путей)
df_loaded = False
raw_df = pd.DataFrame()

if config.get_output_xlsx().exists():
    try:
        raw_df = pd.read_excel(config.get_output_xlsx())
        df_loaded = True
    except Exception as e:
        st.sidebar.warning("Excel read skipped, trying CSV alternative...")

if not df_loaded and config.get_output_csv().exists():
    try:
        raw_df = pd.read_csv(config.get_output_csv())
        df_loaded = True
    except Exception as e:
        st.error(f"Error loading CSV data file: {e}")

if raw_df.empty:
    st.warning(f"⚠️ No valid extracted data found for profile '{st.session_state.active_case.upper()}'. Please run `main.py` first to generate datasets.")
else:
    # Динамически сопоставляем колонки, проверяя их реальное количество в файле
    if len(raw_df.columns) >= 3:
        if st.session_state.active_case == "quotes":
            raw_df.columns = ["Author Name", "Quote Text", "Associated Tags"] + list(raw_df.columns[3:])
            extraction_method = "API Network Interception"
            df = raw_df.drop_duplicates(subset=["Quote Text"]).dropna(subset=["Quote Text"])
        else:
            raw_df.columns = ["Product Title", "Price", "Product SKU"] + list(raw_df.columns[3:])
            extraction_method = "Dynamic HTML DOM Parsing"
            df = raw_df.drop_duplicates(subset=["Product SKU"]).dropna(subset=["Product Title", "Price"])

            # Strict parsing to numeric float types to guarantee data safety
            df["Price"] = df["Price"].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df["Price"] = pd.to_numeric(df["Price"], errors='coerce')
            df = df.dropna(subset=["Price"])
    else:
        st.error("The generated dataset has an invalid structure. Please re-run main.py")
        st.stop()

    # Display processing logs in sidebar
    st.sidebar.info(
        f"**Active Mode:** {st.session_state.active_case.upper()}\n\n"
        f"Raw Records: {len(raw_df)}\n"
        f"Cleaned Records: {len(df)}\n"
        f"Duplicates Removed: {len(raw_df) - len(df)}"
    )

    # Primary KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Cleaned Records", value=len(df))
    with col2:
        st.metric(label="System Status", value="Success")
    with col3:
        st.metric(label="Extraction Methodology", value=extraction_method)

    st.markdown("---")

    # UI view structure setup
    tab_data, tab_analytics = st.tabs(["🔍 Data Preview & Search", "📈 Advanced Analytics (EDA)"])

    # Tab 1: Interactive Data Browser
    with tab_data:
        st.subheader("Granular Data Explorer")
        search_query = st.text_input("Search across all fields:", "").strip()

        # Поиск выполняется только если строка не пустая
        if search_query:
            mask = df.astype(str).apply(lambda res: res.str.contains(search_query, case=False, na=False)).any(axis=1)
            filtered_df = df[mask]
        else:
            filtered_df = df

        # Выводим сообщение о пустом поиске корректно
        if search_query and filtered_df.empty:
            st.info(f"ℹ️ No results found for '{search_query}'. Try checking the spelling or case.")
        else:
            html_table = filtered_df.to_html(classes='coffee-table', index=False)
            st.markdown(html_table, unsafe_allow_html=True)

        # Export pipelines triggering
        st.markdown("### 📥 Download Cleaned Deliverables")
        col_down1, col_down2 = st.columns(2)

        # Генерация Excel в оперативной памяти
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Cleaned Data')
        processed_data_xlsx = buffer.getvalue()

        with col_down1:
            st.download_button(
                label="Download Excel Dataset (.xlsx)",
                data=processed_data_xlsx,
                file_name=config.get_output_xlsx().name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with col_down2:
            st.download_button(
                label="Download CSV Dataset (.csv)",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=config.get_output_csv().name,
                mime="text/csv"
            )

    # Tab 2: Statistical Analytics Visualizations
    with tab_analytics:
        st.subheader(f"Exploratory Data Analysis — `{st.session_state.active_case.upper()}` Mode")

        # Общие настройки осей для кофейной палитры
        axis_theme = dict(
            title_font=dict(color="#5C4033", size=14),
            tickfont=dict(color="#4A3B32", size=12),
            gridcolor="#E6D5C3",
            zerolinecolor="#D7C4B7"
        )

        if st.session_state.active_case == "quotes":
            # --- АНАЛИЗ ДЛЯ КЕЙСА QUOTES ---
            quotes_df = df.dropna(subset=["Quote Text", "Author Name"]).copy()
            quotes_df["Quote Text"] = quotes_df["Quote Text"].astype(str)
            quotes_df["Author Name"] = quotes_df["Author Name"].astype(str)

            g1, g2 = st.columns(2)

            with g1:
                st.write("#### Top 10 Most Popular Tags")
                all_tags = quotes_df["Associated Tags"].dropna().astype(str).str.split(',')
                flat_tags = [tag.strip() for sublist in all_tags for tag in sublist if
                             tag.strip() and not tag.startswith("SKU")]

                if flat_tags:
                    tag_counts = pd.Series(flat_tags).value_counts().head(10).reset_index()
                    tag_counts.columns = ["Tag", "Count"]

                    fig_tags = px.bar(tag_counts, x="Count", y="Tag", orientation='h',
                                      color="Count", color_continuous_scale=["#E6D5C3", "#8B5A2B", "#5C4033"],
                                      labels={"Count": "Number of Quotes", "Tag": "Tag"})

                    fig_tags.update_layout(
                        yaxis={'categoryorder': 'total ascending', **axis_theme},
                        xaxis=axis_theme,
                        showlegend=False,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="#4A3B32"),
                        coloraxis_colorbar=dict(
                            title=dict(font=dict(color="#5C4033")),
                            tickfont=dict(color="#4A3B32")
                        )
                    )
                    st.plotly_chart(fig_tags, use_container_width=True)
                else:
                    st.info("No valid tags available for analysis.")

            with g2:
                st.write("#### Top Authors Distribution")
                author_counts = quotes_df["Author Name"].value_counts().head(7).reset_index()
                author_counts.columns = ["Author", "Quotes Count"]

                if not author_counts.empty:
                    fig_authors = px.pie(author_counts, values="Quotes Count", names="Author",
                                         color_discrete_sequence=["#5C4033", "#6F4E37", "#8B5A2B", "#D7C4B7", "#E6D5C3"],
                                         hole=0.3)
                    fig_authors.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="#4A3B32"),
                        legend=dict(
                            orientation="h",
                            y=-0.1,
                            font=dict(color="#4A3B32")
                        )
                    )
                    st.plotly_chart(fig_authors, use_container_width=True)
                else:
                    st.info("No author data available.")

            st.write("#### Quote Text Length Distribution (Character Count)")
            quotes_df["Quote Length"] = quotes_df["Quote Text"].str.len()

            fig_len = px.histogram(quotes_df, x="Quote Length", nbins=15,
                                   color_discrete_sequence=["#8B5A2B"],
                                   labels={"Quote Length": "Character Count", "count": "Quotes Count"})
            fig_len.update_layout(
                xaxis=axis_theme,
                yaxis=axis_theme,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#4A3B32")
            )
            st.plotly_chart(fig_len, use_container_width=True)

        else:
            # --- АНАЛИЗ ДЛЯ КЕЙСА E-COMMERCE ---
            prices = pd.to_numeric(df["Price"], errors='coerce').dropna()

            if not prices.empty:
                stat1, stat2, stat3 = st.columns(3)
                with stat1:
                    st.metric("Minimum Product Price", f"${float(prices.min()):.2f}")
                with stat2:
                    st.metric("Average Market Price", f"${float(prices.mean()):.2f}")
                with stat3:
                    st.metric("Maximum Product Price", f"${float(prices.max()):.2f}")

                st.markdown("<br>", unsafe_allow_html=True)
                g1, g2 = st.columns(2)

                with g1:
                    st.write("#### Price Density Histogram")
                    fig_hist = px.histogram(df, x="Price", nbins=12,
                                            color_discrete_sequence=["#6F4E37"],
                                            marginal="box",
                                            labels={"Price": "Price ($)", "count": "Product Count"})
                    fig_hist.update_layout(
                        xaxis=axis_theme,
                        yaxis=axis_theme,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="#4A3B32")
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)

                with g2:
                    st.write("#### Statistical Outliers & Price Anomalies Detection")
                    fig_box = px.box(df, y="Price", points="all",
                                     color_discrete_sequence=["#8B5A2B"],
                                     labels={"Price": "Market Price ($)"})
                    fig_box.update_layout(
                        xaxis=axis_theme,
                        yaxis=axis_theme,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="#4A3B32")
                    )
                    st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("No numeric price payload ready for evaluation metrics.")
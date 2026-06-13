import streamlit as st
import plotly.graph_objects as go
from backend import hitung_risiko_pinjaman

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="BijakPinjam",
    page_icon="💳",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.main{
    background-color:#f5f7fb;
}

.block-container{
    padding-top:1rem;
}

[data-testid="stMetric"]{
    background:white;
    border-radius:15px;
    padding:15px;
    border:1px solid #e5e7eb;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("💳 BijakPinjam")

    st.caption(
        "AI Loan Decision Support System"
    )

    st.divider()

    menu = st.radio(
        "Pilih Menu",
        [
            "Belum Pinjam",
            "Sudah Pinjam",
            "Tentang Model"
        ]
    )

    st.divider()

    st.success(
        "🤖 XGBoost Classifier"
    )

    st.info(
        "🎯 Accuracy 80.31%"
    )

# =====================================================
# HEADER
# =====================================================

st.title(
    "💳 Sistem Analisis & Rekomendasi Pinjaman Berbasis AI"
)

st.caption(
    """
    Membantu menganalisis risiko kredit
    menggunakan Machine Learning XGBoost.
    """
)

# =====================================================
# FUNCTION TAMPILKAN HASIL
# =====================================================

def tampilkan_hasil(data, pendapatan, pengeluaran):

    st.divider()

    col1,col2,col3,col4 = st.columns(4)

    col1.metric(
        "💸 Cicilan Bulanan",
        f"Rp {data['cicilan_bulanan']:,.0f}"
    )

    col2.metric(
        "🏦 Total Pinjaman",
        f"Rp {data['total_pinjaman']:,.0f}"
    )

    col3.metric(
        "💰 Sisa Pendapatan",
        f"Rp {data['sisa_pendapatan']:,.0f}"
    )

    col4.metric(
        "📊 DTI",
        f"{data['rasio_hutang']}%"
    )

    st.divider()

    kiri, kanan = st.columns([1,1])

    with kiri:

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=float(data["risk_score"]),
                number={"suffix":"%"},
                title={"text":"Risk Score"},
                gauge={
                    "axis":{"range":[0,100]},
                    "bar":{"color":"royalblue"},
                    "steps":[
                        {
                            "range":[0,30],
                            "color":"#DCFCE7"
                        },
                        {
                            "range":[30,60],
                            "color":"#FEF3C7"
                        },
                        {
                            "range":[60,100],
                            "color":"#FEE2E2"
                        }
                    ]
                }
            )
        )

        gauge.update_layout(
            height=280,
            margin=dict(l=0,r=0,t=40,b=0)
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

        if data["risk_level"] == "Bahaya":

            st.error(
                f"🚨 Risiko Tinggi ({data['risk_score']:.1f}%)"
            )

        elif data["risk_level"] == "Waspada":

            st.warning(
                f"⚠️ Risiko Sedang ({data['risk_score']}%)"
            )

        else:

            st.success(
                f"✅ Risiko Rendah ({data['risk_score']}%)"
            )

    with kanan:

        st.subheader(
            "📈 Financial Health Score"
        )

        st.progress(
            data["financial_health_score"] / 100
        )

        if data["health_level"] == "Sangat Baik":
            st.success(
                f"Score: {data['financial_health_score']}/100\n\nStatus: {data['health_level']}"
            )

        elif data["health_level"] == "Baik":
            st.info(
                f"Score: {data['financial_health_score']}/100\n\nStatus: {data['health_level']}"
            )

        elif data["health_level"] == "Cukup":
            st.warning(
                f"Score: {data['financial_health_score']}/100\n\nStatus: {data['health_level']}"
            )

        else:
            st.error(
                f"Score: {data['financial_health_score']}/100\n\nStatus: {data['health_level']}"
            )

        st.subheader("🤖 Insight AI")

        for item in data["insight"]:
            st.info("• " + item)

        st.subheader("💡 Rekomendasi")

        for item in data["rekomendasi"]:
            st.write("✅ " + item)

            st.divider()

    st.subheader("📊 Visualisasi Keuangan")

    chart1, chart2, chart3 = st.columns(3)

    with chart1:

        pie = go.Figure(
            data=[
                go.Pie(
                    labels=[
                        "Pengeluaran",
                        "Cicilan",
                        "Sisa Dana"
                    ],
                    values=[
                        pengeluaran,
                        data["cicilan_bulanan"],
                        max(data["sisa_pendapatan"], 0)
                    ],
                    hole=0.6
                )
            ]
        )

        pie.update_layout(
            title="Komposisi Keuangan Bulanan",
            height=400
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

    with chart2:

        bar = go.Figure()

        bar.add_trace(
            go.Bar(
                x=[
                    "Pendapatan",
                    "Pengeluaran",
                    "Cicilan",
                    "Sisa Dana"
                ],
                y=[
                    pendapatan / 1000000,
                    pengeluaran / 1000000,
                    data["cicilan_bulanan"] / 1000000,
                    max(data["sisa_pendapatan"], 0) / 1000000
                ]
            )
        )

        bar.update_layout(
            title="Perbandingan Finansial",
            yaxis_title="Juta Rupiah",
            height=400
        )

        st.plotly_chart(
            bar,
            use_container_width=True
        )

    st.subheader("📈 Dampak Pinjaman terhadap Cashflow")

    sisa_sebelum = (
        pendapatan
        - pengeluaran
    )

    sisa_sesudah = (
        pendapatan
        - pengeluaran
        - data["cicilan_bulanan"]
    )

    compare = go.Figure()

    compare.add_trace(
        go.Bar(
            name="Sebelum Pinjaman",
            x=["Cashflow"],
            y=[sisa_sebelum / 1000000]
        )
    )

    compare.add_trace(
        go.Bar(
            name="Sesudah Pinjaman",
            x=["Cashflow"],
            y=[sisa_sesudah / 1000000]
        )
    )

    compare.update_layout(
        barmode="group",
        height=450,
        yaxis_title="Juta Rupiah"
    )

    st.plotly_chart(
        compare,
        use_container_width=True
    )

# =====================================================
# BELUM PINJAM
# =====================================================

if menu == "Belum Pinjam":

    st.subheader(
        "📝 Simulasi Pengajuan Pinjaman Baru"
    )

    col1,col2 = st.columns(2)

    with col1:

        pendapatan = st.number_input(
            "Pendapatan Bulanan (Rp)",
            min_value=1,
            value=5000000,
            step=100000
        )

        pengeluaran = st.number_input(
            "Pengeluaran Bulanan (Rp)",
            min_value=0,
            value=3000000,
            step=100000
        )

        pekerjaan = st.selectbox(
            "Status Pekerjaan",
            [
                "Freelance",
                "Kontrak",
                "Pegawai Tetap",
                "Wirausaha"
            ]
        )

    with col2:

        pinjaman = st.number_input(
            "Jumlah Pinjaman Baru (Rp)",
            min_value=0,
            value=5000000,
            step=500000
        )

        tenor = st.selectbox(
            "Tenor (Bulan)",
            [12,24,36,48,60]
        )

        bunga = st.slider(
            "Bunga Tahunan (%)",
            1,
            30,
            15
        )

    if st.button(
        "🚀 Analisis Sekarang",
        use_container_width=True
    ):

        hasil = hitung_risiko_pinjaman(
            pendapatan_bulanan=pendapatan,
            pengeluaran_bulanan=pengeluaran,
            jumlah_pinjaman_baru=pinjaman,
            tenor_pinjaman_baru=tenor,
            suku_bunga_baru=bunga,
            status_pekerjaan=pekerjaan
        )

        if hasil["success"]:

            tampilkan_hasil(
                hasil["data"],
                pendapatan,
                pengeluaran
            )

        else:

            st.error(
                hasil["error"]
            )

# =====================================================
# SUDAH PINJAM
# =====================================================

elif menu == "Sudah Pinjam":

    st.subheader(
        "🏦 Simulasi Pinjaman Tambahan"
    )

    col1,col2 = st.columns(2)

    with col1:

        pendapatan = st.number_input(
            "Pendapatan Bulanan",
            min_value=1,
            value=6000000
        )

        pengeluaran = st.number_input(
            "Pengeluaran Bulanan",
            min_value=0,
            value=3500000
        )

        pekerjaan = st.selectbox(
            "Status Pekerjaan",
            [
                "Freelance",
                "Kontrak",
                "Pegawai Tetap",
                "Wirausaha"
            ]
        )

        pinjaman_lama = st.number_input(
            "Sisa Pinjaman Saat Ini",
            min_value=0,
            value=3000000
        )

    with col2:

        pinjaman_baru = st.number_input(
            "Pinjaman Tambahan",
            min_value=0,
            value=1500000
        )

        tenor_baru = st.selectbox(
            "Tenor Baru",
            [12,24,36,48,60]
        )

        bunga_baru = st.slider(
            "Bunga Baru (%)",
            1,
            30,
            15
        )

    if st.button(
        "📈 Analisis Pinjaman Tambahan",
        use_container_width=True
    ):

        hasil = hitung_risiko_pinjaman(
            pendapatan_bulanan=pendapatan,
            pengeluaran_bulanan=pengeluaran,
            jumlah_pinjaman_baru=pinjaman_baru,
            tenor_pinjaman_baru=tenor_baru,
            suku_bunga_baru=bunga_baru,
            jumlah_pinjaman_sekarang=pinjaman_lama,
            status_pekerjaan=pekerjaan
        )

        if hasil["success"]:

            tampilkan_hasil(
                hasil["data"],
                pendapatan,
                pengeluaran
            )

        else:

            st.error(
                hasil["error"]
            )

# =====================================================
# TENTANG MODEL
# =====================================================

else:

    st.header("🤖 Tentang Model")

    st.success(
        """
XGBoost Classifier

Accuracy : 80.31%

Precision : 74%

Recall : 77%

F1 Score : 75%
"""
    )

    st.subheader(
        "🏆 Feature Importance"
    )

    st.markdown("""
1. Debt To Income Ratio (DTI)

2. Remaining Income

3. Pendapatan Tahunan

4. Monthly Installment

5. Jumlah Pinjaman Diajukan

6. Total Utang Saat Ini

7. Bunga Tahunan

8. Status Pekerjaan

9. Tenor Pinjaman
""")
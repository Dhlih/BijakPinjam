import pandas as pd
import joblib


def hitung_risiko_pinjaman(
    pendapatan_bulanan,
    suku_bunga_baru,
    jumlah_pinjaman_baru,
    tenor_pinjaman_baru,
    status_pekerjaan,
    pengeluaran_bulanan=0,
    jumlah_pinjaman_sekarang=0,
    suku_bunga_sekarang=0,
    tenor_pinjaman_sekarang=0
):

    try:

        # ==================================
        # VALIDASI
        # ==================================

        if pendapatan_bulanan <= 0:
            return {
                "success": False,
                "error": "Pendapatan harus lebih dari 0"
            }

        # ==================================
        # PERHITUNGAN FINANSIAL
        # ==================================

        bunga_desimal_baru = suku_bunga_baru / 100
        bunga_bulanan_baru = bunga_desimal_baru / 12

        monthly_installment = (
            (jumlah_pinjaman_baru / tenor_pinjaman_baru)
            + (jumlah_pinjaman_baru * bunga_bulanan_baru)
        )

        pendapatan_tahunan = pendapatan_bulanan * 12

        estimasi_cicilan_lama = (
            jumlah_pinjaman_sekarang * 0.05
        )

        debt_to_income_ratio = (
            (
                estimasi_cicilan_lama
                + monthly_installment
            )
            / pendapatan_bulanan
        ) * 100

        remaining_income = (
            pendapatan_bulanan
            - pengeluaran_bulanan
            - monthly_installment
            - estimasi_cicilan_lama
        )

        total_pinjaman = (
            jumlah_pinjaman_baru
            + jumlah_pinjaman_sekarang
        )

        # ==================================
        # ENCODER
        # ==================================

        encoder = joblib.load(
            "./models/encoder_status_pekerjaan.joblib"
        )

        status_pekerjaan_encoded = (
            encoder.transform(
                [status_pekerjaan]
            )[0]
        )

        # ==================================
        # SCALER
        # ==================================

        scaler = joblib.load(
            "./machine_learning/scaler_finansial.joblib"
        )

        kolom_kontinu = [
            "pendapatan_tahunan",
            "total_utang_saat_ini",
            "jumlah_pinjaman_diajukan",
            "monthly_installment",
            "debt_to_income_ratio",
            "remaining_income"
        ]

        data = pd.DataFrame(
            [[
                pendapatan_tahunan,
                jumlah_pinjaman_sekarang,
                jumlah_pinjaman_baru,
                monthly_installment,
                debt_to_income_ratio,
                remaining_income
            ]],
            columns=kolom_kontinu
        )

        data_scaled = scaler.transform(data)

        df_final = pd.DataFrame(
            data_scaled,
            columns=kolom_kontinu
        )

        df_final["tenor_bulan"] = tenor_pinjaman_baru
        df_final["bunga_tahunan"] = bunga_desimal_baru
        df_final["status_pekerjaan_encoded"] = (
            status_pekerjaan_encoded
        )

        urutan_kolom = [
            "pendapatan_tahunan",
            "total_utang_saat_ini",
            "jumlah_pinjaman_diajukan",
            "tenor_bulan",
            "bunga_tahunan",
            "monthly_installment",
            "debt_to_income_ratio",
            "remaining_income",
            "status_pekerjaan_encoded"
        ]

        df_final = df_final[urutan_kolom]

        # ==================================
        # MODEL
        # ==================================

        model = joblib.load(
            "./machine_learning/model_risiko_pinjaman_xgb.pkl"
        )

        prediksi = model.predict(
            df_final
        )[0]

        prediksi_label = (
            "TINGGI"
            if prediksi == 1
            else "RENDAH"
        )

        try:

            probabilitas = (
                model.predict_proba(df_final)[0]
            )

            risk_score = float(
                round(
                    probabilitas[1] * 100,
                    2
                )
            )

        except:

            risk_score = 50.0

        # ==================================
        # RISK LEVEL
        # ==================================

        if risk_score >= 70:
            risk_level = "Bahaya"

        elif risk_score >= 40:
            risk_level = "Waspada"

        else:
            risk_level = "Aman"

        # ==================================
        # HEALTH SCORE
        # ==================================

        financial_health_score = round(
            max(
                0,
                min(
                    100,
                    (
                        100
                        - debt_to_income_ratio
                        - (
                            (
                                pengeluaran_bulanan
                                / pendapatan_bulanan
                            ) * 30
                        )
                    )
                )
            )
        )

        if financial_health_score >= 80:
            health_level = "Sangat Baik"

        elif financial_health_score >= 60:
            health_level = "Baik"

        elif financial_health_score >= 40:
            health_level = "Cukup"

        else:
            health_level = "Buruk"

        # ==================================
        # INSIGHT
        # ==================================

        insight = []

        if debt_to_income_ratio > 40:
            insight.append(
                "Debt To Income Ratio berada di atas batas aman."
            )

        if remaining_income < 1000000:
            insight.append(
                "Sisa pendapatan setelah cicilan cukup rendah."
            )

        if monthly_installment > (
            pendapatan_bulanan * 0.35
        ):
            insight.append(
                "Cicilan melebihi batas ideal 35% pendapatan."
            )

        if remaining_income > 2000000:
            insight.append(
                "Cashflow bulanan masih tergolong sehat."
            )

        if len(insight) == 0:
            insight.append(
                "Kondisi finansial relatif stabil."
            )

        # ==================================
        # REKOMENDASI
        # ==================================

        rekomendasi = []

        if prediksi_label == "TINGGI":

            rekomendasi.extend([
                "Kurangi nominal pinjaman yang diajukan.",
                "Pilih tenor lebih panjang untuk menurunkan cicilan.",
                "Kurangi beban utang sebelum mengajukan pinjaman baru.",
                "Tingkatkan dana darurat sebelum mengambil pinjaman."
            ])

        else:

            rekomendasi.extend([
                "Pinjaman masih dalam batas aman.",
                "Pertahankan rasio DTI di bawah 30%.",
                "Pastikan pembayaran cicilan tepat waktu.",
                "Gunakan dana pinjaman untuk kebutuhan produktif."
            ])

        return {
            "success": True,
            "data": {
                "prediksi_risiko": prediksi_label,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "financial_health_score": financial_health_score,
                "health_level": health_level,
                "cicilan_bulanan": int(monthly_installment),
                "sisa_pendapatan": int(remaining_income),
                "rasio_hutang": round(debt_to_income_ratio, 2),
                "total_pinjaman": int(total_pinjaman),
                "insight": insight,
                "rekomendasi": rekomendasi
            }
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
import streamlit as st

# Pengaturan Halaman
st.set_page_config(page_title="Smart Anti-Overtraining", page_icon="🏋️‍♂️", layout="centered")

# --- TAMPILAN UTAMA ---
st.title("🏋️‍♂️ Anti-Overtraining Assistant")
st.write("Masukkan data fisik dan kondisi latihan Anda hari ini untuk mendeteksi risiko latihan berlebih (*overtraining*).")

st.markdown("---")

# --- PROFIL FISIK ---
st.subheader("👤 Profil Fisik Anda")
col1, col2 = st.columns(2)
with col1:
    height = st.number_input("Tinggi Badan (TB) dalam cm:", min_value=100, max_value=250, value=165)
with col2:
    weight = st.number_input("Berat Badan (BB) dalam kg:", min_value=30, max_value=200, value=60)

# --- DATA OLAHRAGA ---
st.subheader("📊 Aktivitas Olahraga Hari Ini")
workout_type = st.selectbox(
    "Jenis olahraga hari ini?",
    ["Lari / Kardio Intensitas Tinggi", "Angkat Beban (Weightlifting)", "Bersepeda / Berenang", "Senam / Kalistenik", "Jalan Santai / Yoga"]
)
col3, col4 = st.columns(2)
with col3:
    duration = st.number_input("Durasi latihan (menit):", min_value=0, max_value=300, value=60, step=5)
with col4:
    rpe = st.slider("Intensitas Latihan (Skala RPE 1-10):", min_value=1, max_value=10, value=5)

# --- KONDISI PEMULIHAN ---
st.subheader("🛌 Kondisi Tubuh & Pemulihan")
sleep_quality = st.selectbox("Kualitas tidur semalam?", ["Sangat Baik", "Cukup / Biasa Saja", "Buruk / Kurang Tidur"])
muscle_soreness = st.selectbox("Apakah merasakan nyeri otot parah?", ["Tidak / Pegal Ringan", "Ya, Cukup Mengganggu", "Ya, Sangat Parah"])
resting_hr_spike = st.checkbox("Detak jantung istirahat (RHR) pagi ini naik tidak wajar?")

st.markdown("---")

if st.button("Analisis Kondisi & Cek Rekomendasi", type="primary"):
    # 1. Hitung IMT (Indeks Massa Tubuh)
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    
    if bmi < 18.5:
        bmi_status = "Underweight (Kurus)"
    elif 18.5 <= bmi < 25:
        bmi_status = "Normal (Ideal)"
    elif 25 <= bmi < 30:
        bmi_status = "Overweight (Gemuk)"
    else:
        bmi_status = "Obese (Obesitas)"
    
    # 2. Hitung Beban Latihan & Risiko Kelelahan
    training_load = duration * rpe
    risk_points = 0
    if sleep_quality == "Buruk / Kurang Tidur": risk_points += 2
    if muscle_soreness == "Ya, Cukup Mengganggu": risk_points += 1
    elif muscle_soreness == "Ya, Sangat Parah": risk_points += 3
    if resting_hr_spike: risk_points += 2
    
    # Menentukan Status Kelelahan Akhir
    if training_load > 600 or risk_points >= 4:
        fatigue_status = "Tinggi"
    elif 400 <= training_load <= 600 or (2 <= risk_points < 4):
        fatigue_status = "Sedang"
    else:
        fatigue_status = "Aman"

    # --- TAMPILAN HASIL ANALISIS ---
    st.subheader("🔍 Hasil Analisis Keseluruhan")
    st.info(f"💡 **Indeks Massa Tubuh (IMT):** {bmi:.1f} — **Kategori:** {bmi_status}")
    
    if fatigue_status == "Tinggi":
        st.error(f"🚨 **Risiko Overtraining TINGGI!** (Beban: {training_load} poin)")
        st.write("### 🛑 JADWALKAN: REST DAY TOTAL")
        st.write("Mengingat tingkat kelelahan Anda yang sangat tinggi, olahraga intensitas apa pun tidak disarankan untuk sesi berikutnya. Sangat disarankan untuk mengambil tidur berkualitas atau peregangan ringan saja.")
    
    elif fatigue_status == "Sedang":
        st.warning(f"⚠️ **Risiko Overtraining SEDANG.** (Beban: {training_load} poin)")
        st.write("### ⚠️ JADWALKAN: DELOAD SESSION (LATIHAN RINGAN)")
        if bmi_status in ["Overweight (Gemuk)", "Obese (Obesitas)"]:
            st.write("Lakukan latihan kardio berbeban sendi rendah (*low-impact*) seperti sepeda statis santai atau berenang gaya dada selama 30 menit.")
        else:
            st.write("Anda boleh joging santai atau senam kalistenik dasar tanpa beban tambahan dengan memotong volume latihan Anda hingga 50%.")
    
    else:
        st.success(f"🟢 **Kondisi AMAN.** (Beban: {training_load} poin)")
        st.write("### 💪 JADWALKAN: PROGRESSIVE OVERLOAD")
        if bmi_status == "Underweight (Kurus)":
            st.write("Fokus pada latihan beban (angkat beban) untuk menaikkan massa otot dan batasi kardio durasi panjang agar kalori tidak terlalu banyak terbakar.")
        elif bmi_status in ["Overweight (Gemuk)", "Obese (Obesitas)"]:
            st.write("Lanjutkan latihan beban kombinasi mesin dan latihan kardio intensitas menengah secara rutin untuk menjaga metabolisme.")
        else:
            st.write("Tubuh Anda prima. Silakan lanjutkan program latihan Anda, atau kombinasikan latihan kekuatan dengan kardio intensitas menengah.")

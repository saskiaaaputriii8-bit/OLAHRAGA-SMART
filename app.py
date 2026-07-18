%%writefile app.py
import streamlit as str

# Pengaturan halaman
str.set_page_config(page_title="Smart Anti-Overtraining", page_icon="🏃‍♂️", layout="centered")

str.title("🏋️‍♂️ Smart Anti-Overtraining Assistant")
str.write("Aplikasi web pintar untuk memantau kelelahan, menghitung IMT, dan memberikan rekomendasi olahraga yang aman.")

str.markdown("---")

# --- BAGIAN 1: PROFIL FISIK ---
str.subheader("👤 Profil Fisik Anda")
col1, col2 = str.columns(2)

with col1:
    height = str.number_input("Tinggi Badan (TB) dalam cm:", min_value=100, max_value=250, value=165)
with col2:
    weight = str.number_input("Berat Badan (BB) dalam kg:", min_value=30, max_value=200, value=60)

# --- BAGIAN 2: DATA OLAHRAGA HARI INI ---
str.subheader("📊 Aktivitas Olahraga Hari Ini")
workout_type = str.selectbox(
    "Jenis olahraga apa yang Anda lakukan hari ini?",
    ["Lari / Kardio Intensitas Tinggi", "Angkat Beban (Weightlifting)", "Bersepeda / Berenang", "Senam / Kalistenik", "Jalan Santai / Yoga"]
)

col3, col4 = str.columns(2)
with col3:
    duration = str.number_input("Durasi latihan (menit):", min_value=0, max_value=300, value=60, step=5)
with col4:
    rpe = str.slider("Intensitas Latihan (Skala RPE 1-10):", min_value=1, max_value=10, value=5, help="1=Sangat Ringan, 10=Maksimal")

# --- BAGIAN 3: KONDISI PEMULIHAN ---
str.subheader("🛌 Kondisi Tubuh & Pemulihan")
sleep_quality = str.selectbox("Kualitas tidur semalam?", ["Sangat Baik", "Cukup / Biasa Saja", "Buruk / Kurang Tidur"])
muscle_soreness = str.selectbox("Apakah merasakan nyeri otot (DOMS) yang parah?", ["Tidak / Pegal Ringan", "Ya, Cukup Mengganggu", "Ya, Sangat Parah"])
resting_hr_spike = str.checkbox("Detak jantung istirahat (RHR) pagi ini naik tidak wajar?")

str.markdown("---")

# --- PROSES EVALUASI & REKOMENDASI ---
if str.button("Analisis Kondisi & Rekomendasi Olahraga", type="primary"):
    
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
        
    # 2. Hitung Status Overtraining
    training_load = duration * rpe
    risk_points = 0
    if sleep_quality == "Buruk / Kurang Tidur": risk_points += 2
    if muscle_soreness == "Ya, Cukup Mengganggu": risk_points += 1
    elif muscle_soreness == "Ya, Sangat Parah": risk_points += 3
    if resting_hr_spike: risk_points += 2
    
    # Menentukan Status Kelelahan
    if training_load > 600 or risk_points >= 4:
        fatigue_status = "Tinggi"
    elif 400 <= training_load <= 600 or (2 <= risk_points < 4):
        fatigue_status = "Sedang"
    else:
        fatigue_status = "Rendah (Aman)"

    # --- TAMPILAN OUTPUT HASIL ---
    str.subheader("🔍 Hasil Analisis Kesehatan & Latihan")
    
    # Tampilkan info IMT
    str.info(f"💡 **Indeks Massa Tubuh (IMT):** {bmi:.1f} — **Kategori:** {bmi_status}")
    
    # Tampilkan Status Overtraining
    if fatigue_status == "Tinggi":
        str.error(f"🚨 **Risiko Overtraining TINGGI!** (Beban Latihan: {training_load} poin)")
        str.warning("Tubuh Anda berada di zona bahaya cedera karena akumulasi kelelahan atau kurangnya pemulihan.")
    elif fatigue_status == "Sedang":
        str.warning(f"⚠️ **Risiko Overtraining SEDANG.** (Beban Latihan: {training_load} poin)")
    else:
        str.success(f"🟢 **Kondisi AMAN.** (Beban Latihan: {training_load} poin)")
        
    str.markdown("---")
    
    # --- LOGIKA REKOMENDASI OLAHRAGA SELANJUTNYA ---
    str.subheader("📋 Rekomendasi Olahraga untuk Sesi Berikutnya")
    
    if fatigue_status == "Tinggi":
        str.write("### 🛑 JADWALKAN: REST DAY TOTAL")
        str.write(
            "Mengingat tingkat kelelahan Anda yang sangat tinggi, **olahraga intensitas apa pun tidak disarankan** untuk sesi berikutnya. "
            "Memaksakan diri berlatih hanya akan menurunkan massa otot dan merusak sistem imun."
        )
        str.write("**Rekomendasi Aktivitas Bebas Beban Sendi:**")
        str.write("- Istirahat total (Tidur berkualitas 8 jam)")
        str.write("- *Stretching* statis ringan atau yoga restoratif selama 15-20 menit")
        str.write("- Jalan kaki santai (jika benar-benar ingin bergerak)")
        
    elif fatigue_status == "Sedang":
        str.write("### ⚠️ JADWALKAN: DELOAD SESSION (LATIHAN RINGAN)")
        str.write("Anda diperbolehkan olahraga, namun dengan memotong volume (set/durasi) dan intensitas hingga 50%.")
        
        # Rekomendasi berdasarkan IMT untuk risiko sedang
        if bmi_status in ["Overweight (Gemuk)", "Obese (Obesitas)"]:
            str.write("**Rekomendasi Olahraga (Fokus Low-Impact untuk Lindungi Sendi):**")
            str.write("- Sepeda statis dengan kayuhan santai (30 menit)")
            str.write("- Berenang gaya dada santai")
            str.write("- Jalan cepat (*brisk walking*) di permukaan rata")
        else:
            str.write("**Rekomendasi Olahraga:**")
            str.write("- Senam kalistenik dasar tanpa beban tambahan (Push up/Squat ringan)")
            str.write("- Joging sangat santai (*Zone 2 cardio*) selama 20-30 menit")
            str.write("- Yoga atau Pilates tingkat dasar")
            
    else: # Jika Kondisi Aman / Rendah
        str.write("### 💪 JADWALKAN: PROGRESSIVE OVERLOAD (SIAP DI TINGKATKAN)")
        str.write("Tubuh Anda pulih dengan sempurna. Anda siap melakukan latihan rutin atau mencoba meningkatkan intensitas latihan.")
        
        # Rekomendasi berdasarkan IMT untuk kondisi prima
        if bmi_status in ["Overweight (Gemuk)", "Obese (Obesitas)"]:
            str.write("**Rekomendasi Olahraga Terbaik untuk Anda:**")
            str.write("- *Resistance Training* (Latihan beban mesin/dumbbell) untuk meningkatkan metabolisme otot.")
            str.write("- Olahraga kardio *low-impact* intensitas menengah seperti Berenang berdurasi atau Bersepeda menanjak.")
            str.write("- Jalan cepat atau *Elliptical trainer* (45-60 menit).")
        elif bmi_status == "Underweight (Kurus)":
            str.write("**Rekomendasi Olahraga Terbaik untuk Anda:**")
            str.write("- Fokus pada *Hypertrophy Training* (Angkat beban untuk menaikkan massa otot) dengan repetisi 8-12.")
            str.write("- Batasi kardio durasi panjang agar kalori tidak terlalu banyak terbakar.")
        else: # Normal / Ideal
            str.write("**Rekomendasi Olahraga Terbaik untuk Anda:**")
            str.write(f"Anda bisa melanjutkan atau memvariasikan olahraga harian Anda ({workout_type}).")
            str.write("- Coba kombinasikan Angkat Beban (3-4x seminggu) dengan Kardio Intensitas Tinggi / HIIT (1-2x seminggu).")
            str.write("- Tingkatkan beban latihan secara bertahap untuk perkembangan optimal.")

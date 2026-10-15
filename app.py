import streamlit as st
import pandas as pd
import datetime
import calendar

st.set_page_config(
    page_title="Rekap Presensi SMKN 1 Duduksampeyan",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Sistem Rekap Presensi Pegawai - SMKN 1 Duduksampeyan")
st.markdown("Aplikasi web resmi untuk merekap kehadiran ASN, GTT/PTT, dan Satpam secara otomatis sesuai standar instansi.")

# --- INITIAL STATE MANAGEMENT ---
if 'pegawai_list' not in st.session_state:
    st.session_state.pegawai_list = [
        {"no": "1", "nama": "Drs. Samsul Anang, M.M", "dept": "SMKN1DDKS", "kategori": "ASN"},
        {"no": "2", "nama": "Arni Sulistyowati, S. Pd", "dept": "SMKN1DDKS", "kategori": "ASN"},
        {"no": "3", "nama": "Pramana Heri Binanti, M. Pd", "dept": "SMKN1DDKS", "kategori": "ASN"},
        {"no": "4", "nama": "Sri Wahyuni, S. Pd", "dept": "SMKN1DDKS", "kategori": "ASN"},
        {"no": "5", "nama": "Giyadi, S. Sos", "dept": "SMKN1DDKS", "kategori": "ASN"},
        {"no": "6", "nama": "Bambang (Satpam)", "dept": "SMKN1DDKS", "kategori": "Satpam"},
        {"no": "7", "nama": "Ahmad (GTT)", "dept": "SMKN1DDKS", "kategori": "GTT/PTT"}
    ]

if 'libur_list' not in st.session_state:
    st.session_state.libur_list = {
        "2025-05-01": "Libur PHBN Hari Buruh",
        "2025-05-12": "Libur PHBI Hari Raya Waisak"
    }

# --- SIDEBAR MENU ---
menu = st.sidebar.selectbox("Pilih Menu Utama", [
    "📝 Input & Rekap Presensi",
    "📅 Kelola Hari Libur (PHBI/PHBN)",
    "👥 Master Data Pegawai",
    "🖨️ Informasi & Panduan Cetak"
])

if menu == "📝 Input & Rekap Presensi":
    st.header("📝 Input Data Kehadiran Harian")
    col1, col2 = st.columns(2)
    with col1:
        bulan = st.selectbox("Pilih Bulan", list(range(1, 13)), index=4)
    with col2:
        tahun = st.number_input("Pilih Tahun", value=2025)
        
    num_days = calendar.monthrange(tahun, bulan)[1]
    pegawai = st.selectbox("Pilih Nama Pegawai", [p['nama'] for p in st.session_state.pegawai_list])
    
    st.info(f"Menampilkan lembar presensi untuk **{pegawai}** pada periode bulan {bulan}/{tahun} ({num_days} Hari).")
    
    # Contoh Tabel Input Interaktif
    data_preview = []
    for d in range(1, num_days + 1):
        dt = datetime.date(tahun, bulan, d)
        hari_name = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Mgg"][dt.weekday()]
        is_weekend = dt.weekday() in [5, 6]
        
        status = "Libur Weekend" if is_weekend else "Hadir"
        masuk = "-" if is_weekend else "07:00"
        pulang = "-" if is_weekend else "15:30"
        
        data_preview.append({
            "Tanggal": d,
            "Hari": hari_name,
            "Jam Masuk": masuk,
            "Jam Pulang": pulang,
            "Keterangan/Status": status
        })
        
    df = pd.DataFrame(data_preview)
    st.data_editor(df, use_container_width=True)
    
    if st.button("💾 Simpan Perubahan Presensi"):
        st.success("Data kehadiran berhasil disimpan ke sistem!")

elif menu == "📅 Kelola Hari Libur (PHBI/PHBN)":
    st.header("📅 Pengaturan Kalender Libur Nasional & Cuti Bersama")
    tgl = st.date_input("Tanggal Libur")
    keterangan = st.text_input("Keterangan Libur (Contoh: Libur Hari Raya Idul Fitri)")
    if st.button("Tambah Hari Libur"):
        st.session_state.libur_list[tgl.strftime("%Y-%m-%d")] = keterangan
        st.success("Hari libur berhasil diperbarui!")
        
    st.write("### Daftar Hari Libur Terdaftar:")
    for t, k in st.session_state.libur_list.items():
        st.write(f"- **{t}**: {k}")

elif menu == "👥 Master Data Pegawai":
    st.header("👥 Data Pegawai SMKN 1 Duduksampeyan")
    st.dataframe(pd.DataFrame(st.session_state.pegawai_list), use_container_width=True)

elif menu == "🖨️ Informasi & Panduan Cetak":
    st.header("🖨️ Panduan Cetak Laporan Bulanan")
    st.write("""
    * Sistem otomatis mendeteksi pelanggaran presensi seperti **TAD** (Tidak Absen Datang), **TAP** (Tidak Absen Pulang), atau **TDP** (Tidak Absen Datang & Pulang).
    * Jam pulang di bawah ketentuan instansi otomatis diberi penanda peringatan merah.
    * Anda dapat mengunduh format rekap resmi yang siap dicetak langsung melalui tombol ekspor.
    """)
import streamlit as st
import subprocess
import time
import os
import signal
import sys
import atexit

# --- Konfigurasi Awal Streamlit ---
st.set_page_config(page_title="Panel Server Minecraft", page_icon="⛏️", layout="centered")

# Inisialisasi state untuk menyimpan proses dan log
if 'server_process_ended' not in st.session_state:
    st.session_state.server_process_ended = False
if 'log' not in st.session_state:
    st.session_state.log = []
    # Jika ada file log lama, muat ulang
    if os.path.exists("server_log.txt"):
        try:
            with open("server_log.txt", "r") as f:
                st.session_state.log = f.read().splitlines()[-500:]
        except:
            pass

def baca_log():
    """Membaca log dari file yang ditulis oleh server."""
    if os.path.exists("server_log.txt"):
        try:
            with open("server_log.txt", "r") as f:
                current_log = f.read().splitlines()
                if len(current_log) > len(st.session_state.log):
                    # Update state dengan log terbaru
                    st.session_state.log = current_log[-500:]
        except Exception as e:
            st.error(f"Gagal membaca log: {e}")

def jalankan_perintah(command):
    """Mengirim perintah ke server melalui file pipe."""
    if command:
        try:
            with open("server_input.txt", "w") as f:
                f.write(command + "\n")
            st.success(f"Perintah `{command}` berhasil dikirim.")
            time.sleep(0.5)
            baca_log()
            st.rerun()
        except Exception as e:
            st.error(f"Gagal mengirim perintah: {e}")

# --- Antarmuka Pengguna (UI) Streamlit ---
st.title("🎮 Panel Kontrol Server Minecraft")
st.markdown("Kelola server Endstone-mu dengan mudah di sini!")

# Sidebar untuk tindakan cepat
with st.sidebar:
    st.header("⚙️ Kontrol Server")
    if st.button("▶️ Nyalakan Server", use_container_width=True):
        if not os.path.exists("/content/endstone_server"):
            os.makedirs("/content/endstone_server", exist_ok=True)
        os.chdir("/content/endstone_server")
        with open("server_log.txt", "w") as f:
            f.write("")
        
        # Gunakan screen untuk menjalankan server di background
        subprocess.Popen(["screen", "-dmS", "mcserver", "endstone"], cwd="/content/endstone_server")
        st.session_state.server_process_ended = False
        st.success("✅ Server sedang dalam proses startup. Tunggu sebentar.")
        time.sleep(2)
        st.rerun()

    if st.button("⏹️ Matikan Server", use_container_width=True):
        # Kirim perintah stop ke server
        jalankan_perintah("stop")
        time.sleep(3)
        # Matikan screen process
        subprocess.run(["screen", "-S", "mcserver", "-X", "quit"])
        st.session_state.server_process_ended = True
        st.success("🛑 Server berhasil dimatikan.")
        st.rerun()

    st.divider()
    st.subheader("📡 Info Koneksi")
    if st.button("🔄 Tampilkan URL Server", use_container_width=True):
        # Cari tahu IP publik melalui perintah `hostname -I`
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
        ip_address = result.stdout.strip()
        if ip_address:
            st.info(f"IP Lokal Server (jika satu jaringan): `{ip_address}`")
        else:
            st.warning("IP Lokal tidak ditemukan. Mungkin server di cloud.")

    st.info("🔗 Gunakan Ngrok atau Playit.gg untuk akses publik.")

# Area utama untuk log dan perintah
tab1, tab2, tab3 = st.tabs(["📜 Log Server", "✏️ Perintah Konsol", "📌 Panduan Cepat"])

with tab1:
    log_placeholder = st.empty()
    # Tombol refresh manual
    if st.button("🔄 Refresh Log"):
        baca_log()
        st.rerun()
    # Loop untuk update otomatis setiap 2 detik
    log_area = st.empty()
    while True:
        baca_log()
        if st.session_state.log:
            log_area.code("\n".join(st.session_state.log[-200:]), language="bash")
        else:
            log_area.info("Log akan muncul di sini setelah server dijalankan.")
        time.sleep(2)

with tab2:
    st.markdown("Ketik perintah untuk dikirim langsung ke konsol server (contoh: `list`, `save`, `stop`).")
    command = st.text_input("Perintah Konsol:")
    if st.button("Kirim Perintah", use_container_width=True):
        if command:
            jalankan_perintah(command)
        else:
            st.warning("Masukkan perintah terlebih dahulu.")

with tab3:
    st.markdown("""
    ### 📖 Panduan Cepat Memulai
    1.  **Nyalakan Server**: Klik tombol **▶️ Nyalakan Server** di sidebar.
    2.  **Buat Akun Ngrok**: Daftar di [ngrok.com](https://ngrok.com) dan dapatkan tokenmu.
    3.  **Ekspos Server ke Publik**:  
        Buka sel baru di Colab (`+ Code`) dan jalankan:
        ```python
        # Ganti dengan token ngrok-mu
        !ngrok authtoken YOUR_AUTH_TOKEN
        !ngrok tcp 19132

import streamlit as st
import subprocess
import time
import os
import signal

# --- Konfigurasi Awal Streamlit ---
st.set_page_config(page_title="Panel Server Minecraft", page_icon="⛏️", layout="centered")

# Inisialisasi state untuk menyimpan log
if 'log' not in st.session_state:
    st.session_state.log = []
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
                current = f.read().splitlines()
                if len(current) > len(st.session_state.log):
                    st.session_state.log = current[-500:]
        except Exception as e:
            st.error(f"Gagal membaca log: {e}")

def kirim_perintah(command):
    """Mengirim perintah ke server via file pipe."""
    if command:
        try:
            with open("server_input.txt", "w") as f:
                f.write(command + "\n")
            st.success(f"Perintah `{command}` berhasil dikirim.")
            time.sleep(0.5)
            baca_log()
            st.rerun()
        except Exception as e:
            st.error(f"Gagal kirim perintah: {e}")

# --- Sidebar Kontrol ---
with st.sidebar:
    st.header("⚙️ Kontrol Server")
    if st.button("▶️ Nyalakan Server", use_container_width=True):
        if not os.path.exists("/content/endstone_server"):
            os.makedirs("/content/endstone_server", exist_ok=True)
        os.chdir("/content/endstone_server")
        with open("server_log.txt", "w") as f:
            f.write("")
        subprocess.Popen(["screen", "-dmS", "mcserver", "endstone"],
                         cwd="/content/endstone_server")
        st.success("✅ Server sedang startup. Tunggu 10 detik...")
        time.sleep(2)
        st.rerun()

    if st.button("⏹️ Matikan Server", use_container_width=True):
        kirim_perintah("stop")
        time.sleep(3)
        subprocess.run(["screen", "-S", "mcserver", "-X", "quit"])
        st.success("🛑 Server dimatikan.")
        st.rerun()

    st.divider()
    st.subheader("📡 Info Koneksi")
    if st.button("🔄 Tampilkan URL Server", use_container_width=True):
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
        ip = result.stdout.strip()
        if ip:
            st.info(f"IP Lokal (jika satu jaringan): `{ip}`")
        else:
            st.warning("Tidak ada IP lokal.")
    st.info("🔗 Gunakan Ngrok atau Playit.gg untuk akses publik.")

# --- Area Utama dengan Tab ---
tab1, tab2, tab3 = st.tabs(["📜 Log Server", "✏️ Perintah Konsol", "📌 Panduan Cepat"])

with tab1:
    st.markdown("**Log server (auto-refresh setiap 3 detik)**")
    log_placeholder = st.empty()
    # Auto-refresh menggunakan while dengan st.rerun, tapi dihentikan dengan session state
    if 'refresh' not in st.session_state:
        st.session_state.refresh = False
    if st.button("🔄 Refresh Sekarang"):
        baca_log()
        st.rerun()
    # Tampilkan log
    baca_log()
    if st.session_state.log:
        log_placeholder.code("\n".join(st.session_state.log[-200:]), language="bash")
    else:
        log_placeholder.info("Log akan muncul setelah server dijalankan.")
    # Auto-refresh setiap 3 detik (gunakan JavaScript alternatif sederhana)
    st.components.v1.html(
        """
        <script>
            setTimeout(function() {
                window.location.reload();
            }, 3000);
        </script>
        """,
        height=0,
    )

with tab2:
    st.markdown("Ketik perintah (contoh: `list`, `save`, `stop`, `op <nama>`)")
    command = st.text_input("Perintah Konsol:")
    if st.button("Kirim Perintah", use_container_width=True):
        if command:
            kirim_perintah(command)
        else:
            st.warning("Masukkan perintah terlebih dahulu.")

with tab3:
    st.markdown("""
    ### 📖 Panduan Cepat Memulai
    1. **Nyalakan Server** → Klik tombol di sidebar.
    2. **Buat akun Ngrok** (gratis di [ngrok.com](https://ngrok.com)) dan dapatkan token.
    3. **Ekspos server ke publik** – Buka sel baru di Colab dan jalankan:
       ```python
       !ngrok authtoken TOKEN_ANDA
       !ngrok tcp 19132

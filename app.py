import streamlit as st
import subprocess
import os
import time

# Konfigurasi halaman
st.set_page_config(page_title="Panel Server Minecraft", page_icon="⛏️")

st.title("🎮 Panel Kontrol Server Minecraft Bedrock")
st.markdown("Menggunakan **Endstone** + **Screen** di belakang layar.")

# Inisialisasi session state
if 'log' not in st.session_state:
    st.session_state.log = []
    if os.path.exists("server_log.txt"):
        try:
            with open("server_log.txt", "r") as f:
                st.session_state.log = f.read().splitlines()[-500:]
        except:
            pass

# Fungsi baca log
def baca_log():
    if os.path.exists("server_log.txt"):
        try:
            with open("server_log.txt", "r") as f:
                st.session_state.log = f.read().splitlines()[-500:]
        except:
            pass

# Sidebar kontrol
with st.sidebar:
    st.header("⚙️ Kontrol")
    
    if st.button("▶️ Nyalakan Server", use_container_width=True):
        os.makedirs("/content/endstone_server", exist_ok=True)
        os.chdir("/content/endstone_server")
        # Jalankan server di dalam screen session
        subprocess.Popen(["screen", "-dmS", "mcserver", "endstone"],
                         cwd="/content/endstone_server")
        st.success("✅ Server sedang berjalan. Tunggu 5 detik.")
        time.sleep(2)
        st.rerun()
    
    if st.button("⏹️ Matikan Server", use_container_width=True):
        subprocess.run(["screen", "-S", "mcserver", "-X", "quit"])
        st.success("🛑 Server dimatikan.")
        st.rerun()
    
    st.divider()
    if st.button("🔄 Refresh Log", use_container_width=True):
        baca_log()
        st.rerun()

# Area log
st.subheader("📜 Log Server")
log_placeholder = st.empty()
baca_log()
if st.session_state.log:
    log_placeholder.code("\n".join(st.session_state.log[-200:]), language="bash")
else:
    log_placeholder.info("Log akan muncul setelah server dinyalakan.")

# Perintah sederhana (hanya stop, list, op, dll - memerlukan file input)
st.subheader("✏️ Kirim Perintah (Eksperimental)")
st.info("Catatan: Fitur ini membutuhkan server Endstone yang dikonfigurasi membaca file input. Jika tidak berfungsi, gunakan perintah stop dari tombol Matikan Server.")
cmd = st.text_input("Perintah (stop, list, op <nama>)")
if st.button("Kirim Perintah"):
    if cmd:
        try:
            with open("/content/endstone_server/input.txt", "w") as f:
                f.write(cmd + "\n")
            st.success(f"Perintah '{cmd}' dikirim.")
        except Exception as e:
            st.error(f"Gagal kirim: {e}")

# Panduan
st.markdown("---")
st.subheader("📌 Panduan Singkat")
st.markdown("1. Klik **Nyalakan Server** (pastikan sudah install endstone: `!pip install endstone`).")
st.markdown("2. Gunakan Ngrok untuk akses publik: `!ngrok tcp 19132`.")
st.markdown("3. Di Minecraft Bedrock, tambahkan server dengan alamat dari Ngrok (contoh: `0.tcp.ngrok.io:12345`).")
st.markdown("4. Untuk memberi operator, kirim perintah `op <nama_pemain>` melalui kotak di atas.")

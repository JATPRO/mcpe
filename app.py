import streamlit as st
import os

st.set_page_config(page_title="Panel Server Minecraft", page_icon="⛏️")
st.title("🎮 Panel Kontrol Server Minecraft Bedrock")
st.warning("⚠️ **Streamlit Cloud tidak dapat menjalankan server game secara langsung.** Gunakan Google Colab untuk server sungguhan. Panel ini hanya sebagai contoh antarmuka.")

# Gunakan direktori yang sudah ada (tidak perlu membuat /content)
DATA_DIR = os.path.join(os.getcwd(), "server_data")
if not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        st.success(f"Direktori {DATA_DIR} siap.")
    except Exception as e:
        st.error(f"Gagal membuat direktori: {e}")

# Inisialisasi session state untuk log
if 'log' not in st.session_state:
    st.session_state.log = []
    log_file = os.path.join(DATA_DIR, "server_log.txt")
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                st.session_state.log = f.read().splitlines()[-500:]
        except:
            pass

# Fungsi baca log
def baca_log():
    log_file = os.path.join(DATA_DIR, "server_log.txt")
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                st.session_state.log = f.read().splitlines()[-500:]
        except:
            pass

# Sidebar kontrol (hanya simulasi)
with st.sidebar:
    st.header("⚙️ Kontrol (Simulasi)")
    if st.button("▶️ Nyalakan Server (Demo)", use_container_width=True):
        st.info("⚠️ Di Streamlit Cloud, server tidak benar-benar berjalan. Gunakan Google Colab untuk fungsi sebenarnya.")
    if st.button("⏹️ Matikan Server (Demo)", use_container_width=True):
        st.info("⚠️ Hanya simulasi.")
    if st.button("🔄 Refresh Log", use_container_width=True):
        baca_log()
        st.rerun()

# Area log
st.subheader("📜 Log Server (Demo)")
log_placeholder = st.empty()
baca_log()
if st.session_state.log:
    log_placeholder.code("\n".join(st.session_state.log[-200:]), language="bash")
else:
    log_placeholder.info("Log akan muncul jika file server_log.txt ada. (Simulasi)")

# Panduan
st.markdown("---")
st.subheader("📌 Cara Benar Menjalankan Server Minecraft + Streamlit Panel")
st.markdown("""
### Gunakan Google Colab (Gratis, 100% Browser)
1. Buka [Google Colab](https://colab.research.google.com)
2. Buat notebook baru, ubah runtime ke **T4 GPU**
3. Jalankan perintah berikut:
   ```python
   !pip install endstone streamlit pyngrok
   !apt-get install -y screen

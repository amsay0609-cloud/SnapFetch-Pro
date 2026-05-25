import streamlit as st
import yt_dlp
import os

# 1. Page Setup
st.set_page_config(page_title="SnapFetch AI", page_icon="🚀", layout="centered")

if "video_ready" not in st.session_state:
    st.session_state.video_ready = False
if "video_bytes" not in st.session_state:
    st.session_state.video_bytes = b""

st.markdown("""
    <style>
        :root { --slate-950: #020617; --text-main: #e2e8f0; }
        .stApp { background: radial-gradient(circle at top, #131f38 0%, var(--slate-950) 56%); color: var(--text-main); }
        .glass-card { background: rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.1); }
        div.stButton > button { background: linear-gradient(120deg, #4f46e5 0%, #7c3aed 100%); border-radius: 14px; color: white; width: 100%; border: none; padding: 0.6rem; }
        div.stDownloadButton > button { background: linear-gradient(120deg, #10b981 0%, #0ea5e9 100%); border-radius: 14px; color: white; width: 100%; border: none; padding: 0.6rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center;"><h1>✦ SnapFetch AI</h1><p style="color:#94a3b8;">Universal Multi-Platform Media Downloader</p></div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    url = st.text_input("Media URL", placeholder="Paste YouTube, FB, Pinterest, or Insta link...")
    fetch_clicked = st.button("Unlock Media")

    if st.session_state.video_ready:
        st.download_button(
            label="Download MP4",
            data=st.session_state.video_bytes,
            file_name="SnapFetch_Video.mp4",
            mime="video/mp4",
            use_container_width=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

if fetch_clicked:
    if not url:
        st.toast("Please paste a URL!", icon="⚠️")
    else:
        temp_base = "downloaded_video"
        temp_file = f"{temp_base}.mp4"
        
        st.session_state.video_ready = False
        st.session_state.video_bytes = b""

        with st.status("Initializing Universal Bypass...", expanded=True) as status:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

                # Upgraded Options: Agar merge fail hua toh single integrated MP4 utha lega automatic
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'merge_output_format': 'mp4',
                    'outtmpl': temp_base,
                    'cookiefile': 'cookies.txt',
                    'quiet': False,
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                    'referer': 'https://www.google.com/',
                    'http_headers': {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Connection': 'keep-alive'
                    }
                }

                status.write("Piercing firewalls & extracting media streams...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # Agar normal download extension add nahi kar paya toh rename fallback lagaya hai
                if not os.path.exists(temp_file) and os.path.exists(temp_base):
                    os.rename(temp_base, temp_file)

                if os.path.exists(temp_file):
                    status.write("Finalizing high-speed transfer...")
                    with open(temp_file, "rb") as f:
                        st.session_state.video_bytes = f.read()
                    st.session_state.video_ready = True
                    status.update(label="Media Successfully Unlocked!", state="complete")
                    st.toast("Click the green button to download!", icon="✅")
                    st.rerun()
                else:
                    status.update(label="Extraction blocked by platform server.", state="error")
                    st.error("Please update cookies.txt or try a different link.")

            except Exception as e:
                status.update(label="Unlock Failed", state="error")
                st.error(f"Reason: {str(e)}")

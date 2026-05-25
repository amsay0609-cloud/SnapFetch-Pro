import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="SnapFetch AI", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
        :root { --slate-950: #020617; --text-main: #e2e8f0; }
        .stApp { background: radial-gradient(circle at top, #131f38 0%, var(--slate-950) 56%); color: var(--text-main); }
        .glass-card { background: rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1rem; }
        div.stButton > button { background: linear-gradient(120deg, #4f46e5 0%, #7c3aed 100%); border-radius: 14px; color: white; width: 100%; border: none; padding: 0.7rem; font-weight: bold; }
        div.stDownloadButton > button { background: linear-gradient(120deg, #10b981 0%, #0ea5e9 100%); border-radius: 14px; color: white; width: 100%; border: none; padding: 0.7rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center;"><h1>✦ SnapFetch AI</h1><p style="color:#94a3b8;">Universal Cloud Media Capture</p></div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    url = st.text_input("Media URL", placeholder="Paste your video link here...")
    fetch_clicked = st.button("Unlock Media")
    st.markdown('</div>', unsafe_allow_html=True)

if fetch_clicked:
    if not url:
        st.toast("Please paste a valid link first!", icon="⚠️")
    else:
        temp_base = "downloaded_video"
        temp_file = f"{temp_base}.mp4"
        
        # Clean up any leftover files from previous attempts
        for ext in ["", ".mp4", ".mkv", ".webm"]:
            if os.path.exists(temp_base + ext):
                try: os.remove(temp_base + ext)
                except: pass

        with st.status("Processing link locally...", expanded=True) as status:
            try:
                ydl_opts = {
                    # 'best' pulls the combined standard format which Pinterest requires
                    'format': 'best',
                    'outtmpl': temp_base + '.%(ext)s',
                    'quiet': False,
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
                }
                status.write("Capturing stream from your home IP...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url.strip()])

                # Dynamic file finder logic to look for any extension yt-dlp dropped
                found_file = None
                for ext in [".mp4", ".mkv", ".webm"]:
                    if os.path.exists(temp_base + ext):
                        found_file = temp_base + ext
                        break

                if found_file:
                    # Rename whatever format came down to standard mp4 for the downloader
                    if found_file != temp_file:
                        if os.path.exists(temp_file): os.remove(temp_file)
                        os.rename(found_file, temp_file)

                if os.path.exists(temp_file):
                    status.write("Loading file...")
                    with open(temp_file, "rb") as f:
                        video_bytes = f.read()
                    
                    status.update(label="Media Unlocked!", state="complete")
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.success("Ready!")
                    st.download_button(label="⬇️ Save MP4 to Device", data=video_bytes, file_name="SnapFetch_Media.mp4", mime="video/mp4", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    status.update(label="Failed", state="error")
                    st.error("File downloaded but format conversion failed. Please try again.")
            except Exception as e:
                status.update(label="Error", state="error")
                st.error(f"Reason: {str(e)}")

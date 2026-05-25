import streamlit as st
import yt_dlp
import os

# 1. Page Configuration
st.set_page_config(page_title="SnapFetch AI", page_icon="🚀", layout="centered")

# CSS for Premium Look
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

# 2. UI Card
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    url = st.text_input("Media URL", placeholder="Paste actual video or pin link here...")
    fetch_clicked = st.button("Unlock Media")
    st.markdown('</div>', unsafe_allow_html=True)

# 3. Download Execution Loop
if fetch_clicked:
    if not url:
        st.toast("Please paste a valid link first!", icon="⚠️")
    elif url.strip() in ["https://www.pinterest.com/", "https://pinterest.com", "https://www.youtube.com/", "https://youtube.com"]:
        st.error("Bhai, yeh website ka homepage hai. Kripya kisi actual video ya pin ka specific link paste karein!")
    else:
        temp_base = "downloaded_video"
        temp_file = f"{temp_base}.mp4"
        
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(temp_base):
            os.remove(temp_base)

        with st.status("Extracting cloud streams...", expanded=True) as status:
            try:
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'merge_output_format': 'mp4',
                    'outtmpl': temp_base,
                    'cookiefile': 'cookies.txt',
                    'quiet': False,
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                    'referer': 'https://www.google.com/'
                }

                status.write("Bypassing server restrictions...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url.strip()])

                if not os.path.exists(temp_file) and os.path.exists(temp_base):
                    os.rename(temp_base, temp_file)

                if os.path.exists(temp_file):
                    status.write("Loading decrypted file bytes...")
                    with open(temp_file, "rb") as f:
                        video_bytes = f.read()
                    
                    status.update(label="Media Fully Unlocked!", state="complete")
                    
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.success("Your file is ready for download!")
                    st.download_button(
                        label="⬇️ Save MP4 to Device",
                        data=video_bytes,
                        file_name="SnapFetch_Media.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                else:
                    status.update(label="Extraction Failed", state="error")
                    st.error("Platform blocked the request. Try checking your link or updating cookies.txt.")
                    
            except Exception as e:
                status.update(label="System Error", state="error")
                if "Unsupported URL" in str(e):
                    st.error("Error: Yeh URL sahi nahi hai. Kripya kisi post/video ka direct link dalein.")
                else:
                    st.error(f"Reason: {str(e)}")

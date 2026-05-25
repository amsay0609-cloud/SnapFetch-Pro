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
    url = st.text_input("Media URL", placeholder="Paste your video link here...")
    fetch_clicked = st.button("Unlock Media")
    st.markdown('</div>', unsafe_allow_html=True)

# 3. Download Execution Loop
if fetch_clicked:
    if not url:
        st.toast("Please paste a valid link first!", icon="⚠️")
    else:
        temp_base = "downloaded_video"
        temp_file = f"{temp_base}.mp4"
        
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(temp_base):
            os.remove(temp_base)

        with st.status("Executing Stealth Bypass...", expanded=True) as status:
            try:
                # Upgraded Options: Mimicking a real android device app connection
                ydl_opts = {
                    'format': 'best', # Single integrated stream for maximum compatibility
                    'outtmpl': temp_base,
                    'cookiefile': 'cookies.txt',
                    'quiet': False,
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                    'referer': 'https://www.pinterest.com/',
                    'extractor_args': {
                        'pinterest': {'skip': ['dash', 'hls']} # Avoid complex formats if blocked
                    },
                    'http_headers': {
                        'Accept': '*/*',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site'
                    }
                }

                status.write("Piercing cloud blocks & capturing streams...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url.strip()])

                # Fallback renaming logic
                if not os.path.exists(temp_file) and os.path.exists(temp_base):
                    os.rename(temp_base, temp_file)
                if not os.path.exists(temp_file) and os.path.exists(f"{temp_base}.mkv"):
                    os.rename(f"{temp_base}.mkv", temp_file)

                if os.path.exists(temp_file):
                    status.write("Finalizing media payload...")
                    with open(temp_file, "rb") as f:
                        video_bytes = f.read()
                    
                    status.update(label="Media Successfully Unlocked!", state="complete")
                    
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
                    status.update(label="Platform Block Active", state="error")
                    st.error("Pinterest blocked this specific server IP. Please reboot the app via Streamlit Dashboard.")
                    
            except Exception as e:
                status.update(label="System Blocked", state="error")
                st.error(f"Reason: {str(e)}")

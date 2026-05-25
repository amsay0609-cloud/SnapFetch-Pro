import streamlit as st
import yt_dlp
import os
import re

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
        temp_file = "downloaded_video.mp4"
        if os.path.exists(temp_file):
            try: os.remove(temp_file)
            except: pass

        with st.status("Processing link locally...", expanded=True) as status:
            try:
                # Force update internal extractors inside the script execution
                ydl_opts = {
                    # 'format': '0' or 'worst' forces yt-dlp to grab the raw progressive fallback HTTP stream 
                    # instead of fighting with the m3u8 adaptive stream layers.
                    'format': 'best/worst/0',
                    'outtmpl': 'downloaded_video.%(ext)s',
                    'quiet': False,
                    'nocheckcertificate': True,
                    'ignoreerrors': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                }
                
                status.write("Analyzing page architecture...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Clean up the pin.it URL structure 
                    cleaned_url = url.strip()
                    ydl.download([cleaned_url])

                # Scan folder for whatever output format dropped down
                found_file = None
                for ext in [".mp4", ".mkv", ".webm", ""]:
                    if os.path.exists("downloaded_video" + ext):
                        found_file = "downloaded_video" + ext
                        break

                if found_file:
                    if found_file != temp_file:
                        os.rename(found_file, temp_file)

                if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
                    status.write("Loading stream containers...")
                    with open(temp_file, "rb") as f:
                        video_bytes = f.read()
                    
                    status.update(label="Media Unlocked!", state="complete")
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.success("Ready!")
                    st.download_button(label="⬇️ Save MP4 to Device", data=video_bytes, file_name="SnapFetch_Media.mp4", mime="video/mp4", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    status.update(label="Format Fallback Triggered", state="running")
                    status.write("Direct scraping via fallback engine...")
                    # Ultimate fallback: extraction via direct source scraping if extractor drops the format completely
                    import requests
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                    r = requests.get(cleaned_url, headers=headers, allow_redirects=True)
                    video_url = re.search(r'"videoUrl":"(https://v1\.pinimg\.com/videos/v720p/.*?\.mp4)"', r.text)
                    if not video_url:
                        video_url = re.search(r'https://v1\.pinimg\.com/videos/.*?\.mp4', r.text)
                    
                    if video_url:
                        direct_mp4 = video_url.group(0).replace(r'\u0026', '&')
                        vid_data = requests.get(direct_mp4, headers=headers).content
                        status.update(label="Media Unlocked via Fallback Engine!", state="complete")
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.success("Ready!")
                        st.download_button(label="⬇️ Save MP4 to Device", data=vid_data, file_name="SnapFetch_Media.mp4", mime="video/mp4", use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        raise Exception("Pinterest stream hidden behind account walls. Try another public link.")
            except Exception as e:
                status.update(label="Error", state="error")
                st.error(f"Reason: {str(e)}")

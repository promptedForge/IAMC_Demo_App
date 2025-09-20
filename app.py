import time

import streamlit as st

from data_pipeline import (
    analyze,
    categorize,
    generate_content,
    get_demo_radar,
)

# CSS Loader Function
def load_css(file_path):
    """Load and inject custom CSS with Mission Control styling"""
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.set_page_config(
    page_title="IAMC Advocacy Intelligence Demo", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Load Mission Control CSS theme
try:
    load_css("assets/mission_control.css")
except FileNotFoundError:
    st.warning("Mission Control CSS not found. Using default theme.")

voice = st.sidebar.radio(
    "Voice",
    ["Advocacy", "Analyst"],
    index=0 if st.session_state.get("voice", "Advocacy") == "Advocacy" else 1,
)
st.session_state.voice = voice

# Mission Control Header with modern glass morphism styling
st.markdown(
    """<div style='
        background: linear-gradient(135deg, rgba(10, 14, 39, 0.7) 0%, rgba(17, 21, 48, 0.6) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0 2rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    '>
        <div style='
            position: absolute;
            top: 0;
            left: -100%;
            width: 200%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent, 
                rgba(0, 212, 255, 0.1), 
                transparent);
            animation: glass-shine 8s infinite;
        '></div>
        <h1 style='
            text-align: center; 
            color: #00D4FF; 
            text-shadow: 
                0 0 40px rgba(0, 212, 255, 0.8),
                0 0 80px rgba(0, 212, 255, 0.4);
            font-weight: 200;
            letter-spacing: 0.2em;
            margin: 0;
            font-size: 2.5rem;
            position: relative;
            z-index: 1;
        '>IAMC ADVOCACY INTELLIGENCE</h1>
        <p style='
            text-align: center; 
            color: #B8B8C8; 
            font-family: monospace; 
            letter-spacing: 0.15em;
            margin: 1rem 0 0.5rem 0;
            font-size: 0.85rem;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        '>MISSION CONTROL • SIGNALS → DAILY RADAR → MASTER BRIEF → CONTENT DRAFTS</p>
        <p style='
            text-align: center; 
            color: #B8B8C8; 
            font-size: 0.8rem;
            opacity: 0.7;
            margin: 0;
            position: relative;
            z-index: 1;
        '>Each step requires human approval before continuing</p>
    </div>""", 
    unsafe_allow_html=True
)

# Session state to track progress and processing flag
if "step" not in st.session_state:
    st.session_state.step = 1
if "processing" not in st.session_state:
    st.session_state.processing = False
if "demo_data" not in st.session_state:
    st.session_state.demo_data = {}


def advance(to_step: int, payload_key: str | None = None, payload=None) -> None:
    """Advance to the next step if the current step matches ``to_step``.

    Any provided ``payload`` is stored under ``payload_key`` in
    ``st.session_state.demo_data`` before progressing.
    """
    if st.session_state.step != to_step:
        return

    st.session_state.processing = True

    if payload_key is not None:
        st.session_state.demo_data[payload_key] = payload

    # Update state; Streamlit reruns when session state changes
    st.session_state.processing = False
    st.session_state.step += 1

    
# ----------------- Step 1: Collect Signals ----------------- #
if st.session_state.step == 1:
    st.markdown(
        """<div style='
            background: linear-gradient(135deg, rgba(26, 31, 58, 0.6) 0%, rgba(42, 51, 78, 0.4) 100%);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        '>
            <h2 style='
                color: #00D4FF;
                margin: 0;
                font-weight: 400;
                letter-spacing: 0.1em;
                text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
            '>Step 1 – Collect Signals (Radar Feed)</h2>
        </div>""",
        unsafe_allow_html=True
    )
    with st.spinner("Analyzing radar feed..."):
        time.sleep(0.5)
        stories = get_demo_radar(st.session_state.voice)

    progress = st.progress(0)
    feed_container = st.container()
    for i, story in enumerate(stories):
        time.sleep(0.1)
        with feed_container.expander(story["title"]):
            st.markdown(
                f"**Source:** {story['source']}  \n"
                f"**Date:** {story['date']}  \n"
                f"**URL:** {story['url']}  \n"
                f"**Confidence:** {story['confidence']}"
            )
            st.write(story["summary"])
        progress.progress(int((i + 1) / len(stories) * 100))

    if st.button("Approve & Continue", disabled=st.session_state.processing):
        advance(to_step=1, payload_key="radar_feed", payload=stories)
        st.rerun()

# ----------------- Step 2: Daily Radar ----------------- #
elif st.session_state.step == 2:
    st.markdown(
        """<div style='
            background: linear-gradient(135deg, rgba(26, 31, 58, 0.6) 0%, rgba(42, 51, 78, 0.4) 100%);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        '>
            <h2 style='
                color: #00D4FF;
                margin: 0;
                font-weight: 400;
                letter-spacing: 0.1em;
                text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
            '>Step 2 – Daily Radar</h2>
        </div>""",
        unsafe_allow_html=True
    )
    placeholder = st.empty()
    with st.spinner("Synthesizing daily radar..."):
        time.sleep(0.5)
        radar_md = categorize(
            st.session_state.demo_data.get("radar_feed", []),
            st.session_state.voice,
        )

    progress = st.progress(0)
    lines = radar_md.splitlines()
    partial = ""
    for i, line in enumerate(lines):
        partial += line + "\n"
        placeholder.markdown(partial)
        progress.progress(int((i + 1) / len(lines) * 100))
        time.sleep(0.05)

    if st.button("Approve & Continue", disabled=st.session_state.processing):
        advance(to_step=2, payload_key="daily_radar", payload=radar_md)
        st.rerun()

# ----------------- Step 3: Master Brief ----------------- #
elif st.session_state.step == 3:
    st.markdown(
        """<div style='
            background: linear-gradient(135deg, rgba(26, 31, 58, 0.6) 0%, rgba(42, 51, 78, 0.4) 100%);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        '>
            <h2 style='
                color: #00D4FF;
                margin: 0;
                font-weight: 400;
                letter-spacing: 0.1em;
                text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
            '>Step 3 – Master Brief</h2>
        </div>""",
        unsafe_allow_html=True
    )
    placeholder = st.empty()
    with st.spinner("Assembling master brief..."):
        time.sleep(0.5)
        brief = analyze(
            st.session_state.demo_data.get("daily_radar", ""), st.session_state.voice
        )

    progress = st.progress(0)
    lines = brief.splitlines()
    partial = ""
    for i, line in enumerate(lines):
        partial += line + "\n"
        placeholder.markdown(partial)
        progress.progress(int((i + 1) / len(lines) * 100))
        time.sleep(0.05)

    if st.button("Approve & Continue", disabled=st.session_state.processing):
        advance(to_step=3, payload_key="master_brief", payload=brief)
        st.rerun()

# ----------------- Step 4: Content Drafts ----------------- #
elif st.session_state.step == 4:
    st.markdown(
        """<div style='
            background: linear-gradient(135deg, rgba(26, 31, 58, 0.6) 0%, rgba(42, 51, 78, 0.4) 100%);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        '>
            <h2 style='
                color: #00D4FF;
                margin: 0;
                font-weight: 400;
                letter-spacing: 0.1em;
                text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
            '>Step 4 – Content Drafts</h2>
        </div>""",
        unsafe_allow_html=True
    )
    with st.spinner("Generating content drafts..."):
        time.sleep(0.5)
        drafts = generate_content(
            st.session_state.demo_data.get("master_brief", ""), st.session_state.voice
        )

    def gradual_text_area(label: str, text: str, height: int) -> None:
        area = st.empty()
        progress = st.progress(0)
        lines = text.splitlines()
        content = ""
        for i, line in enumerate(lines):
            content += line + "\n"
            area.text_area(label, content, height=height)
            progress.progress(int((i + 1) / len(lines) * 100))
            time.sleep(0.05)

    # Create glass card containers for each draft section
    st.markdown(
        """<div style='
            background: linear-gradient(135deg, rgba(15, 20, 40, 0.6) 0%, rgba(26, 31, 58, 0.4) 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 
                0 4px 16px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        ' 
        onmouseover="this.style.transform='translateY(-4px) scale(1.01)'; this.style.boxShadow='0 8px 32px rgba(0, 0, 0, 0.4), 0 0 30px rgba(0, 212, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.05)';" 
        onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 4px 16px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05)';">
            <h3 style='color: #00D4FF; margin: 0 0 1rem 0; font-weight: 400;'>Press Release (Draft)</h3>
        </div>""",
        unsafe_allow_html=True
    )
    gradual_text_area("Press Release", drafts["press_release"], height=250)

    st.markdown(
        """<div style='
            background: linear-gradient(135deg, rgba(15, 20, 40, 0.6) 0%, rgba(26, 31, 58, 0.4) 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 
                0 4px 16px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        ' 
        onmouseover="this.style.transform='translateY(-4px) scale(1.01)'; this.style.boxShadow='0 8px 32px rgba(0, 0, 0, 0.4), 0 0 30px rgba(0, 212, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.05)';" 
        onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 4px 16px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05)';">
            <h3 style='color: #00D4FF; margin: 0 0 1rem 0; font-weight: 400;'>Social Media Posts (Drafts)</h3>
        </div>""",
        unsafe_allow_html=True
    )
    gradual_text_area("Social Posts", drafts["social_posts"], height=200)

    st.markdown(
        """<div style='
            background: linear-gradient(135deg, rgba(15, 20, 40, 0.6) 0%, rgba(26, 31, 58, 0.4) 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 
                0 4px 16px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        ' 
        onmouseover="this.style.transform='translateY(-4px) scale(1.01)'; this.style.boxShadow='0 8px 32px rgba(0, 0, 0, 0.4), 0 0 30px rgba(0, 212, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.05)';" 
        onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 4px 16px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05)';">
            <h3 style='color: #00D4FF; margin: 0 0 1rem 0; font-weight: 400;'>Newsletter Section (Draft)</h3>
        </div>""",
        unsafe_allow_html=True
    )
    gradual_text_area("Newsletter", drafts["newsletter"], height=300)

    st.markdown(
        """<div style='
            background: linear-gradient(135deg, rgba(15, 20, 40, 0.6) 0%, rgba(26, 31, 58, 0.4) 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 
                0 4px 16px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        ' 
        onmouseover="this.style.transform='translateY(-4px) scale(1.01)'; this.style.boxShadow='0 8px 32px rgba(0, 0, 0, 0.4), 0 0 30px rgba(0, 212, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.05)';" 
        onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 4px 16px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05)';">
            <h3 style='color: #00D4FF; margin: 0 0 1rem 0; font-weight: 400;'>LinkedIn Op-ed (Draft)</h3>
        </div>""",
        unsafe_allow_html=True
    )
    gradual_text_area("LinkedIn Op-ed", drafts["linkedin_oped"], height=300)

    st.success("✅ Pipeline complete – All outputs loaded.")

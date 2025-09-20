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

# Mission Control Header with custom styling
st.markdown(
    """<h1 style='text-align: center; color: #00D4FF; text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);'>
    IAMC ADVOCACY INTELLIGENCE</h1>""", 
    unsafe_allow_html=True
)
st.markdown(
    """<p style='text-align: center; color: #B8B8C8; font-family: monospace; letter-spacing: 0.1em;'>
    MISSION CONTROL • SIGNALS → DAILY RADAR → MASTER BRIEF → CONTENT DRAFTS</p>""", 
    unsafe_allow_html=True
)
st.markdown(
    """<p style='text-align: center; color: #B8B8C8; font-size: 0.9em;'>
    Each step requires human approval before continuing.</p>""", 
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
    st.header("Step 1 – Collect Signals (Radar Feed)")
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
    st.header("Step 2 – Daily Radar")
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
    st.header("Step 3 – Master Brief")
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
    st.header("Step 4 – Content Drafts")
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

    st.subheader("Press Release (Draft)")
    gradual_text_area("Press Release", drafts["press_release"], height=250)

    st.subheader("Social Media Posts (Drafts)")
    gradual_text_area("Social Posts", drafts["social_posts"], height=200)

    st.subheader("Newsletter Section (Draft)")
    gradual_text_area("Newsletter", drafts["newsletter"], height=300)

    st.subheader("LinkedIn Op-ed (Draft)")
    gradual_text_area("LinkedIn Op-ed", drafts["linkedin_oped"], height=300)

    st.success("✅ Pipeline complete – All outputs loaded.")

import streamlit as st

from data_pipeline import (
    analyze,
    categorize,
    generate_content,
    get_demo_radar,
)

st.set_page_config(page_title="IAMC Advocacy Intelligence Demo", layout="centered")

voice = st.sidebar.radio(
    "Voice",
    ["Advocacy", "Analyst"],
    index=0 if st.session_state.get("voice", "Advocacy") == "Advocacy" else 1,
)
st.session_state.voice = voice

st.title("IAMC Advocacy Intelligence Demo")
st.write("Pipeline: Signals → Daily Radar → Master Brief → Content Drafts")
st.write("Each step requires human approval before continuing.")

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

    # Update state and trigger rerun
    st.session_state.processing = False
    st.session_state.step += 1
    st.rerun()

# ----------------- Step 1: Collect Signals ----------------- #
if st.session_state.step == 1:
    st.header("Step 1 – Collect Signals (Radar Feed)")
    with st.status("Loading radar feed...", expanded=True) as status:
        status.write("Reading radar_feed.json")
        stories = get_demo_radar(st.session_state.voice)
        status.update(label="Radar feed loaded", state="complete")

    for story in stories:
        with st.expander(story["title"]):
            st.markdown(
                f"**Source:** {story['source']}  \n"
                f"**Date:** {story['date']}  \n"
                f"**URL:** {story['url']}  \n"
                f"**Confidence:** {story['confidence']}"
            )
            st.write(story["summary"])

    st.button(
        "Approve & Continue",
        on_click=advance,
        kwargs={"to_step": 1, "payload_key": "radar_feed", "payload": stories},
        disabled=st.session_state.processing,
    )

# ----------------- Step 2: Daily Radar ----------------- #
elif st.session_state.step == 2:
    st.header("Step 2 – Daily Radar")
    placeholder = st.empty()
    with st.status("Loading daily radar...", expanded=True) as status:
        status.write("Reading daily_radar.md")
        radar_md = categorize(
            st.session_state.demo_data.get("radar_feed", []),
            st.session_state.voice,
        )
        status.update(label="Daily radar loaded", state="complete")
    placeholder.markdown(radar_md)

    st.button(
        "Approve & Continue",
        on_click=advance,
        kwargs={"to_step": 2, "payload_key": "daily_radar", "payload": radar_md},
        disabled=st.session_state.processing,
    )

# ----------------- Step 3: Master Brief ----------------- #
elif st.session_state.step == 3:
    st.header("Step 3 – Master Brief")
    placeholder = st.empty()
    with st.status("Loading master brief...", expanded=True) as status:
        status.write("Reading master_brief.md")
        brief = analyze(
            st.session_state.demo_data.get("daily_radar", ""), st.session_state.voice
        )
        status.update(label="Master brief loaded", state="complete")
    placeholder.markdown(brief)

    st.button(
        "Approve & Continue",
        on_click=advance,
        kwargs={"to_step": 3, "payload_key": "master_brief", "payload": brief},
        disabled=st.session_state.processing,
    )

# ----------------- Step 4: Content Drafts ----------------- #
elif st.session_state.step == 4:
    st.header("Step 4 – Content Drafts")
    with st.status("Loading content drafts...", expanded=True) as status:
        drafts = generate_content(
            st.session_state.demo_data.get("master_brief", ""), st.session_state.voice
        )
        status.update(label="Content drafts loaded", state="complete")

    # Press Release
    st.subheader("Press Release (Draft)")
    st.text_area(
        "Press Release", drafts["press_release"], height=250, disabled=True
    )

    # Social Posts
    st.subheader("Social Media Posts (Drafts)")
    st.text_area(
        "Social Posts", drafts["social_posts"], height=200, disabled=True
    )

    # Newsletter
    st.subheader("Newsletter Section (Draft)")
    st.text_area(
        "Newsletter", drafts["newsletter"], height=300, disabled=True
    )

    # LinkedIn Op-ed
    st.subheader("LinkedIn Op-ed (Draft)")
    st.text_area(
        "LinkedIn Op-ed", drafts["linkedin_oped"], height=300, disabled=True
    )

    st.success("✅ Pipeline complete – All outputs loaded.")

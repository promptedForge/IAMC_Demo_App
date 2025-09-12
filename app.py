import streamlit as st
import json

st.set_page_config(page_title="IAMC Advocacy Intelligence Demo", layout="centered")

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
    with open("1_Radar_Feed/radar_feed.json") as f:
        stories = json.load(f)
    st.json(stories)

    st.button(
        "Approve & Continue",
        on_click=advance,
        kwargs={"to_step": 1, "payload_key": "radar_feed", "payload": stories},
        disabled=st.session_state.processing,
    )

# ----------------- Step 2: Daily Radar ----------------- #
elif st.session_state.step == 2:
    st.header("Step 2 – Daily Radar")
    with open("2_Daily_Radar/daily_radar.md") as f:
        radar_md = f.read()
    st.markdown(radar_md)

    st.button(
        "Approve & Continue",
        on_click=advance,
        kwargs={"to_step": 2, "payload_key": "daily_radar", "payload": radar_md},
        disabled=st.session_state.processing,
    )

# ----------------- Step 3: Master Brief ----------------- #
elif st.session_state.step == 3:
    st.header("Step 3 – Master Brief")
    with open("3_Master_Brief/master_brief.md") as f:
        brief = f.read()
    st.markdown(brief)

    st.button(
        "Approve & Continue",
        on_click=advance,
        kwargs={"to_step": 3, "payload_key": "master_brief", "payload": brief},
        disabled=st.session_state.processing,
    )

# ----------------- Step 4: Content Drafts ----------------- #
elif st.session_state.step == 4:
    st.header("Step 4 – Content Drafts")

    # Press Release
    st.subheader("Press Release (Draft)")
    with open("4_Content_Drafts/press_release_draft.md") as f:
        press_release = f.read()
    st.text_area("Press Release", press_release, height=250)

    # Social Posts
    st.subheader("Social Media Posts (Drafts)")
    with open("4_Content_Drafts/social_post.txt") as f:
        social_posts = f.read()
    st.text_area("Social Posts", social_posts, height=200)

    # Newsletter
    st.subheader("Newsletter Section (Draft)")
    with open("4_Content_Drafts/newsletter_snippet.md") as f:
        newsletter = f.read()
    st.text_area("Newsletter", newsletter, height=300)

    # LinkedIn Op-ed
    st.subheader("LinkedIn Op-ed (Draft)")
    with open("4_Content_Drafts/linkedin_oped_draft.md") as f:
        linkedin_oped = f.read()
    st.text_area("LinkedIn Op-ed", linkedin_oped, height=300)

    st.success("✅ Pipeline complete – All outputs loaded.")

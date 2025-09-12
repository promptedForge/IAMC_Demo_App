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


def get_demo_radar() -> dict:
    """Return the demo radar feed."""
    with open("1_Radar_Feed/radar_feed.json") as f:
        return json.load(f)


def get_daily_radar() -> str:
    """Return the demo daily radar markdown."""
    with open("2_Daily_Radar/daily_radar.md") as f:
        return f.read()


def get_master_brief() -> str:
    """Return the demo master brief markdown."""
    with open("3_Master_Brief/master_brief.md") as f:
        return f.read()


def get_content_drafts() -> dict:
    """Return all content drafts used in the demo."""
    with open("4_Content_Drafts/press_release_draft.md") as f:
        press_release = f.read()
    with open("4_Content_Drafts/social_post.txt") as f:
        social_posts = f.read()
    with open("4_Content_Drafts/newsletter_snippet.md") as f:
        newsletter = f.read()
    with open("4_Content_Drafts/linkedin_oped_draft.md") as f:
        linkedin_oped = f.read()
    return {
        "press_release": press_release,
        "social_posts": social_posts,
        "newsletter": newsletter,
        "linkedin_oped": linkedin_oped,
    }


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
    placeholder = st.empty()
    with st.status("Loading radar feed...", expanded=True) as status:
        status.write("Reading radar_feed.json")
        stories = get_demo_radar()
        status.update(label="Radar feed loaded", state="complete")
    placeholder.json(stories)

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
        radar_md = get_daily_radar()
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
        brief = get_master_brief()
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
        drafts = get_content_drafts()
        status.update(label="Content drafts loaded", state="complete")

    # Press Release
    st.subheader("Press Release (Draft)")
    st.text_area("Press Release", drafts["press_release"], height=250)

    # Social Posts
    st.subheader("Social Media Posts (Drafts)")
    st.text_area("Social Posts", drafts["social_posts"], height=200)

    # Newsletter
    st.subheader("Newsletter Section (Draft)")
    st.text_area("Newsletter", drafts["newsletter"], height=300)

    # LinkedIn Op-ed
    st.subheader("LinkedIn Op-ed (Draft)")
    st.text_area("LinkedIn Op-ed", drafts["linkedin_oped"], height=300)

    st.success("✅ Pipeline complete – All outputs loaded.")

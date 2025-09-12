import json
from typing import List

from models import Article, ContentBundle


def get_demo_radar() -> List[Article]:
    """Load the demo radar feed from disk."""
    with open("1_Radar_Feed/radar_feed.json") as f:
        data: List[Article] = json.load(f)
    return data


def categorize(stories: List[Article]) -> str:
    """Return the demo daily radar markdown."""
    with open("2_Daily_Radar/daily_radar.md") as f:
        return f.read()


def analyze(daily_radar: str) -> str:
    """Return the demo master brief markdown."""
    with open("3_Master_Brief/master_brief.md") as f:
        return f.read()


def generate_content(master_brief: str) -> ContentBundle:
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

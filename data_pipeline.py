import json
from pathlib import Path
from typing import List

from models import Article, ContentBundle

def get_demo_radar(voice: str = "Advocacy") -> List[Article]:
    """Load the demo radar feed from disk respecting ``voice``."""
    default_path = Path("1_Radar_Feed/radar_feed.json")
    voice_path = Path(f"1_Radar_Feed/radar_feed_{voice.lower()}.json")
    path = voice_path if voice_path.exists() else default_path
    with open(path) as f:
        data: List[Article] = json.load(f)
    return data


def categorize(stories: List[Article], voice: str = "Advocacy") -> str:
    """Return the demo daily radar markdown respecting ``voice``."""
    default_path = Path("2_Daily_Radar/daily_radar.md")
    voice_path = Path(f"2_Daily_Radar/daily_radar_{voice.lower()}.md")
    path = voice_path if voice_path.exists() else default_path
    with open(path) as f:
        return f.read()


def analyze(daily_radar: str, voice: str = "Advocacy") -> str:
    """Return the demo master brief markdown respecting ``voice``."""
    default_path = Path("3_Master_Brief/master_brief.md")
    voice_path = Path(f"3_Master_Brief/master_brief_{voice.lower()}.md")
    path = voice_path if voice_path.exists() else default_path
    with open(path) as f:
        return f.read()


def generate_content(master_brief: str, voice: str = "Advocacy") -> ContentBundle:
    """Return all content drafts used in the demo respecting ``voice``."""
    base = Path("4_Content_Drafts")
    suffix = f"_{voice.lower()}" if voice.lower() != "advocacy" else ""

    def _load(name: str, ext: str) -> str:
        voice_file = base / f"{name}{suffix}{ext}"
        default_file = base / f"{name}{ext}"
        path = voice_file if voice_file.exists() else default_file
        with open(path) as f:
            return f.read()

    press_release = _load("press_release_draft", ".md")
    social_posts = _load("social_post", ".txt")
    newsletter = _load("newsletter_snippet", ".md")
    linkedin_oped = _load("linkedin_oped_draft", ".md")
    return {
        "press_release": press_release,
        "social_posts": social_posts,
        "newsletter": newsletter,
        "linkedin_oped": linkedin_oped,
    }

from typing import TypedDict

class Article(TypedDict):
    title: str
    source: str
    date: str  # ISO 8601 formatted date
    summary: str
    url: str
    confidence: float


class CategorizedStory(TypedDict):
    category: str
    article: Article
    annotation: str


class MasterBrief(TypedDict):
    content: str


class ContentBundle(TypedDict):
    press_release: str
    social_posts: str
    newsletter: str
    linkedin_oped: str

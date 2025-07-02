from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class FormattedNewsArticle:
    """Typed container for scraped / pre-processed news."""
    headline: str
    content: str
    timestamp: datetime
    url: str
    source: str



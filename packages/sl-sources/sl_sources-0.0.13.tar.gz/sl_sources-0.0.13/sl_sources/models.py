from enum import Enum
import hashlib
from uuid import uuid4
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


def create_consistent_uuid(input_string: str) -> str:
    """
    Create a consistent UUID from a string input.

    This function generates a UUID based on the MD5 hash of the input string.
    It ensures that the same input always produces the same UUID.

    Parameters
    ----------
    input_string : str
        The input string to generate a UUID from.

    Returns
    -------
    str
        A string representation of the generated UUID.

    Notes
    -----
    This function is useful for creating consistent identifiers across different
    runs or systems, as long as the input string remains the same.
    """
    # Generate an MD5 hash of the input string
    md5_hash = hashlib.md5(input_string.encode()).hexdigest()
    # Create a UUID from the MD5 hash
    return str(uuid.UUID(md5_hash))


class SOURCE_TYPES(str, Enum):
    GOOGLE_BOOKS = "google_books"
    GOOGLE_SCHOLAR = "google_scholar"
    SEMANTIC_SCHOLAR = "semantic_scholar"
    OPENALEX = "openalex"
    TWITTER = "twitter"
    DOI = "doi"
    GOOGLE = "google"
    PODCAST = "podcast"
    VIDEO = "video"
    CRAWL = "crawl"


# Define ENTITY_TYPES as a Literal type
class ENTITY_TYPES(str, Enum):
    PUBLISHER = "publisher"
    INSTITUTION = "institution"
    PUBLICATION = "publication"
    AUTHOR = "author"
    WORK = "work"
    OTHER = "other"  # this should never happen
    UNKNOWN = "unknown"


class WORK_TYPES(str, Enum):
    PAPER = "paper"
    ARTICLE = "article"
    BOOK = "book"
    VIDEO = "video"
    PODCAST = "podcast"
    POST = "post"
    UNKNOWN = "unknown"


class INSTITUTION_TYPES(str, Enum):
    ACADEMIC = "academic"
    COMPANY = "company"
    GOVERNMENT = "government"
    MEDIA = "media"
    FACILITY = "facility"
    NON_PROFIT = "non-profit"
    CONFERENCE = "conference"
    OTHER = "other"
    UNKNOWN = "unknown"


class PUBLICATION_TYPES(str, Enum):
    JOURNAL = "journal"
    BOOK = "book"
    CONFERENCE_PROCEEDINGS = "conference_proceedings"
    OTHER = "other"
    UNKNOWN = "unknown"


class Entity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: ENTITY_TYPES
    source_type: SOURCE_TYPES


class Publisher(Entity):
    type: Literal["publisher"] = "publisher"
    name: str
    url: Optional[str] = None
    description: Optional[str] = None


class Institution(Entity):
    type: Literal["institution"] = "institution"
    institution_type: INSTITUTION_TYPES = INSTITUTION_TYPES.UNKNOWN
    name: str
    url: Optional[str] = None
    description: Optional[str] = None


class Publication(Entity):
    type: Literal["publication"] = "publication"
    publication_type: PUBLICATION_TYPES = PUBLICATION_TYPES.UNKNOWN
    name: str
    url: Optional[str] = None
    description: Optional[str] = None
    publisher: Optional[Publisher] = None
    institutions: List[Institution] = []
    doi: Optional[str] = None


class Author(Entity):
    type: Literal["author"] = "author"
    name: str
    institutions: List[Institution] = []


class Work(Entity):
    type: Literal["work"] = "work"
    work_type: WORK_TYPES = WORK_TYPES.UNKNOWN
    name: str
    url: str
    abstract: Optional[str] = None
    full_text: Optional[str] = None
    authors: List[Author] = []
    institutions: List[Institution] = []
    publications: List[Publication] = []
    year: Optional[int] = None
    doi: Optional[str] = None
    links: List[str] = []
    relevant: bool = True


class SearchInput(BaseModel):
    query: str
    num_results: int = 10
    source_type: Optional[SOURCE_TYPES] = None
    entity_types: List[ENTITY_TYPES] = Field(default_factory=list)
    file_type: Optional[str] = None


class CrawlInput(BaseModel):
    urls: List[str]
    keywords: List[str]
    sources: List[str]
    use_cloud_function: bool
    max_depth: int = 3
    research_topic: Optional[str] = None


ENTITY_MODELS = {
    ENTITY_TYPES.PUBLISHER: Publisher,
    ENTITY_TYPES.INSTITUTION: Institution,
    ENTITY_TYPES.PUBLICATION: Publication,
    ENTITY_TYPES.AUTHOR: Author,
    ENTITY_TYPES.WORK: Work,
}

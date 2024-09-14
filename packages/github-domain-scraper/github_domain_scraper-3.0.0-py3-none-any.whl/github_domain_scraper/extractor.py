import sys
from typing import Any, Dict, Optional, Union, List

from .logger import get_logger
from .backends import ListRepositoriesBackend, UserProfileBackend

logger = get_logger(__file__)


class LinkExtractor:
    def __init__(
        self, initial_link: str, total_links_to_download: Optional[int] = None
    ):
        self.initial_link = initial_link
        self.total_links_to_download = total_links_to_download or sys.maxsize

    def extract(self) -> List[Optional[str]]:
        logger.info("Extracting...")
        backend = ListRepositoriesBackend(
            total_links_to_download=self.total_links_to_download
        )
        urls = backend.process(url=self.initial_link)
        return urls[: self.total_links_to_download]


class UserProfileInformationExtractor:
    def __init__(self, github_username: Union[str, List[str]]):
        self.github_usernames = (
            github_username if isinstance(github_username, list) else [github_username]
        )

    def extract(self) -> Dict[str, Dict[str, Any]]:
        logger.info("Extracting...")
        backend = UserProfileBackend()
        return backend.process(usernames=self.github_usernames)

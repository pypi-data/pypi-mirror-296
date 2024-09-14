from abc import ABC, abstractmethod
import contextlib
import time
from typing import Any, Dict, List, Optional, Type

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from github_domain_scraper.driver import SeleniumWebDriver
from github_domain_scraper.exceptions import InvalidSearchType
from github_domain_scraper.logger import get_logger


class BaseBackend:
    webdriver_waiting_time = 10
    banned_waiting_time = 30

    def __init__(self, banned_waiting_time: Optional[int] = None):
        self.wd = SeleniumWebDriver(headless=True)
        self.banned_waiting_time = banned_waiting_time or self.banned_waiting_time

    @property
    def _is_banned(self) -> bool:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            self.wd.web_driver_wait_till_existence(
                by=By.XPATH, value="//title[contains(text(),'Rate limit')]", timeout=0.5
            )
            return True

        with contextlib.suppress(TimeoutException, NoSuchElementException):
            self.wd.web_driver_wait_till_existence(
                by=By.XPATH, value="//title[contains(text(),'Error 429')]", timeout=0.5
            )
            return True

        return False


class BaseLink(ABC):

    def __init__(self, url: str):
        self.url = url
        self.metadata: Dict[str, str] = self.get_metadata()
        self.is_url_supported = self.check_url_match()

    @abstractmethod
    def check_url_match(self) -> bool:
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, str]:
        pass


class BaseListRepositoriesBackend(BaseBackend, ABC):
    logger = get_logger("list_repositories_backend")
    link_classes: List[Type[BaseLink]] = []

    def __init__(
        self,
        total_links_to_download: int,
        banned_waiting_time: Optional[int] = None,
    ):
        super().__init__(banned_waiting_time=banned_waiting_time)
        self.total_links_to_download = total_links_to_download
        self.links: List[Optional[str]] = []

    def process(self, url: str) -> List[Optional[str]]:
        for link_class in self.link_classes:
            try:
                link_object = link_class(url=url)
            except (NotImplementedError, InvalidSearchType) as e:
                self.logger.error(e)
                continue

            if link_object.is_url_supported:
                self.logger.debug(
                    f"URL matched for {link_object.__class__.__name__} class"
                )
                self._start(link_object)
                break
        else:
            self.logger.error(
                "Provided link does not support extraction yet. Please contact package owner to add feature."
            )

        return self.links

    def _start(self, link_object: BaseLink) -> None:
        link = link_object.metadata.get("url")
        if not link:
            raise NotImplementedError(
                f"meta property method of {link_object.__class__.__name__} class "
                f"have not implemented correctly. It must return a dict with 'url' key."
            )

        try:
            self.wd.get(link)
            self.wd.switch_to_last_tab()
            while link and len(self.links) < self.total_links_to_download:
                self.logger.info(f"Crawling url {link}")
                next_link = self._parse(link_object=link_object)
                if self._is_banned:
                    self.logger.info(
                        f"Banned!! Script will retry after {self.banned_waiting_time} seconds"
                    )
                    time.sleep(self.banned_waiting_time)
                    self.wd.get(link)
                else:
                    link = next_link
                    time.sleep(1)
        except KeyboardInterrupt:
            self.logger.error("Stopping crawler...")
        finally:
            self.wd.quit()
            self.logger.info("Crawler Stopped")

    def _parse(self, link_object: BaseLink) -> Optional[str]:
        element = link_object.metadata.get("xpath")
        if not element:
            raise NotImplementedError(
                f"meta property method of {link_object.__class__.__name__} class "
                f"have not implemented correctly. It must return a dict with 'xpath' key."
            )

        try:
            self.wd.web_driver_wait_till_all_existence(by=By.XPATH, value=element)
        except TimeoutException:
            self.logger.debug(f"Error in detecting links using xpath - {element}")
            return None

        repositories: List[Optional[str]] = [
            elem.get_attribute("href")
            for elem in self.wd.find_elements(By.XPATH, element)
        ]
        self.links.extend(repositories)

        next_xpath = link_object.metadata.get("next_xpath")
        if not next_xpath:
            raise NotImplementedError(
                f"meta property method of {self.__class__.__name__} class "
                f"have not implemented correctly. It must return a dict with 'next_xpath' key."
            )

        # next_page_element = None
        # with contextlib.suppress(NoSuchElementException):
        #     next_page_element = self.wd.find_element(By.XPATH, next_xpath)

        # if next_page_element:
        #     next_page_element.click()
        #     time.sleep(1)
        #     next_link: str = self.wd.current_url
        #     return next_link

        with contextlib.suppress(NoSuchElementException, TimeoutException):
            self.wd.web_driver_wait_and_click(by=By.XPATH, value=next_xpath, timeout=2)
            time.sleep(1)
            next_link: str = self.wd.current_url
            return next_link

        return None


class BaseUserProfileBackend(BaseBackend, ABC):
    user_profile_url = "https://github.com/%s"
    fields: List[str] = []
    logger = get_logger("user_profile_backend")

    def process(self, usernames: List[str]) -> Dict[str, Dict[str, Any]]:
        users_information = {}
        try:
            self.wd.switch_to_last_tab()
            for username in usernames:
                self.logger.info(f"Crawling for user {username}")
                users_information[username] = self._start(username=username)
        except KeyboardInterrupt:
            self.logger.error("Stopping crawler...")
        finally:
            self.wd.quit()
            self.logger.info("Crawler Stopped")

        return users_information

    def _start(self, username: str) -> Dict[str, Any]:
        url = self.user_profile_url % username
        if self._is_banned:
            self.logger.info(
                f"Banned!! Script will retry after {self.banned_waiting_time} seconds"
            )
            time.sleep(self.banned_waiting_time)
            return self._start(url)

        self.wd.get(url)
        return {field: getattr(self, f"_{field}") for field in self.fields}

import contextlib
from typing import List, Optional

from .base import BaseUserProfileBackend

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class UserProfileBackend(BaseUserProfileBackend):
    fields = [
        "avatar",
        "fullname",
        "username",
        "bio",
        "followers",
        "following",
        "works_for",
        "home_location",
        "email",
        "profile_website_url",
        "social",
        "achievements",
        "organizations",
        "number_of_repositories",
        "number_of_stars",
        "pinned_repositories",
    ]
    timeout = 0.5

    @property
    def _avatar(self) -> Optional[str]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            element = self.wd.web_driver_wait_till_existence(
                By.XPATH,
                '//a[@itemprop="image"]',
                timeout=self.timeout,
            )
            link: Optional[str] = element.get_attribute("href")
            return link
        return None

    @property
    def _fullname(self) -> Optional[str]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            element = self.wd.web_driver_wait_till_existence(
                By.XPATH,
                '//h1[@class="vcard-names "]/span[1]',
                timeout=self.timeout,
            )
            fullname: str = element.text
            return fullname
        return None

    @property
    def _username(self) -> Optional[str]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            element = self.wd.web_driver_wait_till_existence(
                By.XPATH,
                '//h1[@class="vcard-names "]/span[2]',
                timeout=self.timeout,
            )
            fullname: str = element.text
            return fullname
        return None

    @property
    def _bio(self) -> Optional[str]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            element = self.wd.web_driver_wait_till_existence(
                By.XPATH,
                '//div[contains(@class, "user-profile-bio")]/div',
                timeout=self.timeout,
            )
            bio: str = element.text
            return bio
        return None

    @property
    def _followers(self) -> Optional[str]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            element = self.wd.web_driver_wait_till_existence(
                By.XPATH,
                '//div[contains(@class, "js-profile-editable-area")]/div[2]//a[1]/span',
                timeout=self.timeout,
            )
            followers: str = element.text
            return followers
        return None

    @property
    def _following(self) -> Optional[str]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            element = self.wd.web_driver_wait_till_existence(
                By.XPATH,
                '//div[contains(@class, "js-profile-editable-area")]/div[2]//a[2]/span',
                timeout=self.timeout,
            )
            following: str = element.text
            return following
        return None

    @property
    def _works_for(self) -> Optional[str]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            element = self.wd.web_driver_wait_till_existence(
                By.XPATH,
                '//ul[@class="vcard-details"]/li[@itemprop="worksFor"]/span/div',
                timeout=self.timeout,
            )
            works_for: str = element.text
            return works_for
        return None

    @property
    def _home_location(self) -> Optional[str]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            element = self.wd.web_driver_wait_till_existence(
                By.XPATH,
                '//ul[@class="vcard-details"]/li[@itemprop="homeLocation"]/span',
                timeout=self.timeout,
            )
            home_location: str = element.text
            return home_location
        return None

    @property
    def _email(self) -> Optional[str]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            element = self.wd.web_driver_wait_till_existence(
                By.XPATH,
                '//ul[@class="vcard-details"]/li[@itemprop="email"]/a',
                timeout=self.timeout,
            )
            email: str = element.text
            return email
        return None

    @property
    def _profile_website_url(self) -> Optional[str]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            element = self.wd.web_driver_wait_till_existence(
                By.XPATH,
                '//ul[@class="vcard-details"]/li[@itemprop="url"]/a',
                timeout=self.timeout,
            )
            profile_website_url: str = element.text
            return profile_website_url
        return None

    @property
    def _social(self) -> Optional[List[Optional[str]]]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            elements = self.wd.web_driver_wait_till_all_existence(
                By.XPATH,
                '//ul[@class="vcard-details"]/li[@itemprop="social"]/a',
                timeout=self.timeout,
            )
            social: List[Optional[str]] = [
                element.get_attribute("href") for element in elements
            ]
            return social
        return None

    @property
    def _achievements(self) -> Optional[List[Optional[str]]]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            elements = self.wd.web_driver_wait_till_all_existence(
                By.XPATH,
                '//img[@data-hovercard-type="achievement"]',
                timeout=self.timeout,
            )
            achievements: List[Optional[str]] = []
            for element in elements:
                if alt := element.get_attribute("alt"):
                    achievements.append(alt.replace("Achievement: ", ""))
            return achievements
        return None

    @property
    def _organizations(self) -> Optional[List[Optional[str]]]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            elements = self.wd.web_driver_wait_till_all_existence(
                By.XPATH,
                '//a[@data-hovercard-type="organization" and @itemprop="follows"]',
                timeout=self.timeout,
            )
            organizations: List[Optional[str]] = [
                element.get_attribute("href") for element in elements
            ]
            return organizations
        return None

    @property
    def _number_of_repositories(self) -> Optional[str]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            element = self.wd.web_driver_wait_till_existence(
                By.XPATH,
                '//a[@data-tab-item="repositories"]/span',
                timeout=self.timeout,
            )
            number_of_repositories: str = element.text
            return number_of_repositories
        return None

    @property
    def _number_of_stars(self) -> Optional[str]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            element = self.wd.web_driver_wait_till_existence(
                By.XPATH,
                '//a[@data-tab-item="stars"]/span',
                timeout=self.timeout,
            )
            number_of_stars: str = element.text
            return number_of_stars
        return None

    @property
    def _pinned_repositories(self) -> Optional[List[Optional[str]]]:
        with contextlib.suppress(TimeoutException, NoSuchElementException):
            elements = self.wd.web_driver_wait_till_all_existence(
                By.XPATH,
                '//div[@class="pinned-item-list-item-content"]/div/div/a',
                timeout=self.timeout,
            )
            pinned_repositories: List[Optional[str]] = [
                element.get_attribute("href") for element in elements
            ]
            return pinned_repositories
        return None

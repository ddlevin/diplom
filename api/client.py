import allure
import requests
from typing import Optional


class PoiskKinoClient:

    def __init__(self, base_url: str, api_key: str, timeout: int = 10) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.headers: dict = {
            "X-API-KEY": api_key,
            "Accept": "application/json",
        }

    @allure.step("api. Поиск фильма по названию {query}")
    def search_movie(self, query: str, page: int = 1, limit: int = 10) -> requests.Response:
        url = f"{self.base_url}/v1.4/movie/search"
        params: dict = {"query": query, "page": page, "limit": limit}
        return requests.get(url, headers=self.headers, params=params, timeout=self.timeout)

    @allure.step("api. Получить карточку фильма по id={movie_id}")
    def get_movie_by_id(self, movie_id: int) -> requests.Response:
        url = f"{self.base_url}/v1.4/movie/{movie_id}"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    @allure.step("api. Фильтрация: жанр={genre}, год={year}, рейтинг={rating}")
    def filter_movies(
        self,
        genre: Optional[str] = None,
        year: Optional[int] = None,
        rating: Optional[str] = None,
        limit: int = 10,
    ) -> requests.Response:
        url = f"{self.base_url}/v1.4/movie"
        params: dict = {"limit": limit}
        if genre:
            params["genres.name"] = genre
        if year:
            params["year"] = year
        if rating:
            params["rating.kp"] = rating
        return requests.get(url, headers=self.headers, params=params, timeout=self.timeout)

    @allure.step("api. Поиск без query (негативный)")
    def search_without_query(self) -> requests.Response:
        url = f"{self.base_url}/v1.4/movie/search"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    @allure.step("api. Запрос с невалидным токеном (негативный)")
    def get_with_invalid_token(self, movie_id: int = 301) -> requests.Response:
        url = f"{self.base_url}/v1.4/movie/{movie_id}"
        bad_headers: dict = {"X-API-KEY": "invalid-key-12345"}
        return requests.get(url, headers=bad_headers, timeout=self.timeout)

    @allure.step("api. Запрос с limit={limit} (негативный)")
    def filter_with_big_limit(self, limit: int = 999999) -> requests.Response:
        url = f"{self.base_url}/v1.4/movie"
        params: dict = {"limit": limit}
        return requests.get(url, headers=self.headers, params=params, timeout=self.timeout)

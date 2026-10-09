import allure
import pytest
from config.config import BASE_URL, API_KEY
from api.client import PoiskKinoClient


@pytest.fixture(scope="module")
def client() -> PoiskKinoClient:
    """Фикстура: API-клиент для всех тестов модуля."""
    return PoiskKinoClient(BASE_URL, API_KEY)


@allure.epic("PoiskKino API")
@allure.feature("Поиск фильмов")
class TestSearchMovie:
    """Тесты поиска фильмов."""

    @allure.id("API-001")
    @allure.story("Поиск по точному названию")
    @allure.title("Поиск фильма по точному названию")
    @allure.description("Отправляем GET /v1.4/movie/search?query=Матрица и проверяем наличие 'Матрица' в docs")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_by_exact_title(self, client: PoiskKinoClient) -> None:
        with allure.step("Отправить запрос на поиск 'Матрица'"):
            response = client.search_movie("Матрица")

        with allure.step("Проверить статус-код = 200"):
            assert response.status_code == 200

        with allure.step("Проверить структуру ответа"):
            data = response.json()
            assert "docs" in data
            assert isinstance(data["docs"], list)
            assert len(data["docs"]) > 0

        with allure.step("Проверить, что среди найденных фильмов есть 'Матрица'"):
            names = [movie["name"] for movie in data["docs"]]
            assert any("Матрица" in name for name in names)

    @allure.id("API-002")
    @allure.story("Поиск с опечаткой")
    @allure.title("Поиск фильма с опечаткой (fuzzy)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_with_typo(self, client: PoiskKinoClient) -> None:
        with allure.step("Отправить запрос на поиск 'Матреца'"):
            response = client.search_movie("Матреца")

        with allure.step("Проверить статус-код = 200"):
            assert response.status_code == 200

        with allure.step("Проверить, что docs не пустой"):
            data = response.json()
            assert "docs" in data
            assert len(data["docs"]) > 0


@allure.epic("PoiskKino API")
@allure.feature("Карточка фильма")
class TestGetMovie:
    """Тесты получения карточки фильма."""

    @allure.id("API-003")
    @allure.story("Получение по ID")
    @allure.title("Получение карточки фильма по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_movie_by_id(self, client: PoiskKinoClient) -> None:
        with allure.step("Отправить GET /v1.4/movie/301"):
            response = client.get_movie_by_id(301)

        with allure.step("Проверить статус-код = 200"):
            assert response.status_code == 200

        with allure.step("Проверить поля ответа"):
            data = response.json()
            assert data["id"] == 301
            assert "name" in data
            assert "year" in data
            assert data["type"] == "movie"

    @allure.id("API-004")
    @allure.story("Проверка описания")
    @allure.title("Карточка фильма содержит описание")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movie_has_description(self, client: PoiskKinoClient) -> None:
        with allure.step("Отправить GET /v1.4/movie/301"):
            response = client.get_movie_by_id(301)

        with allure.step("Проверить статус-код = 200"):
            assert response.status_code == 200

        with allure.step("Проверить, что description и shortDescription непустые"):
            data = response.json()
            assert "description" in data
            assert len(data["description"]) > 0
            assert "shortDescription" in data
            assert "movieLength" in data
            assert data["movieLength"] > 0


@allure.epic("PoiskKino API")
@allure.feature("Фильтрация фильмов")
class TestFilterMovies:
    """Тесты фильтрации фильмов."""

    @allure.id("API-005")
    @allure.story("Фильтр по жанру")
    @allure.title("Фильтрация фильмов по жанру 'драма'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_by_genre(self, client: PoiskKinoClient) -> None:
        with allure.step("Отправить запрос с genres.name=драма&limit=5"):
            response = client.filter_movies(genre="драма", limit=5)

        with allure.step("Проверить статус-код = 200"):
            assert response.status_code == 200

        with allure.step("Проверить, что все фильмы — в жанре 'драма'"):
            data = response.json()
            assert "docs" in data
            assert len(data["docs"]) <= 5
            for movie in data["docs"]:
                genres = [g["name"] for g in movie.get("genres", [])]
                assert "драма" in genres

    @allure.id("API-006")
    @allure.story("Фильтр по году и рейтингу")
    @allure.title("Фильтрация фильмов по году 2020 и рейтингу 7-10")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_by_year_and_rating(self, client: PoiskKinoClient) -> None:
        with allure.step("Отправить запрос с year=2020&rating.kp=7-10"):
            response = client.filter_movies(year=2020, rating="7-10", limit=5)

        with allure.step("Проверить статус-код = 200"):
            assert response.status_code == 200

        with allure.step("Проверить год и рейтинг у всех фильмов"):
            data = response.json()
            for movie in data["docs"]:
                assert movie.get("year") == 2020
                rating_kp = movie.get("rating", {}).get("kp")
                assert rating_kp is not None
                assert 7 <= rating_kp <= 10

    @allure.id("API-007")
    @allure.story("Комбинированная фильтрация")
    @allure.title("Комбинированная фильтрация: жанр + год + рейтинг")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_combined(self, client: PoiskKinoClient) -> None:
        with allure.step("Отправить комбинированный запрос"):
            response = client.filter_movies(genre="драма", year=2020, rating="7-10", limit=3)

        with allure.step("Проверить статус-код = 200"):
            assert response.status_code == 200

        with allure.step("Проверить, что у всех фильмов year=2020"):
            data = response.json()
            for movie in data["docs"]:
                assert movie.get("year") == 2020


@allure.epic("PoiskKino API")
@allure.feature("Негативные сценарии")
class TestNegativeCases:
    """Негативные API-тесты."""

    @allure.id("API-008")
    @allure.story("Поиск без query")
    @allure.title("Поиск без параметра query")
    @allure.severity(allure.severity_level.MINOR)
    def test_search_without_query(self, client: PoiskKinoClient) -> None:
        with allure.step("Отправить GET /v1.4/movie/search без query"):
            response = client.search_without_query()

        with allure.step("Проверить, что статус в [200, 400, 422]"):
            assert response.status_code in [200, 400, 422]

    @allure.id("API-009")
    @allure.story("Невалидный токен")
    @allure.title("Запрос с невалидным API-ключом")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_token(self, client: PoiskKinoClient) -> None:
        with allure.step("Отправить запрос с X-API-KEY: invalid-key"):
            response = client.get_with_invalid_token()

        with allure.step("Проверить, что статус 401 или 403"):
            assert response.status_code in [401, 403]

    @allure.id("API-010")
    @allure.story("Слишком большой limit")
    @allure.title("Запрос с limit=999999")
    @allure.severity(allure.severity_level.NORMAL)
    def test_too_big_limit(self, client: PoiskKinoClient) -> None:
        with allure.step("Отправить GET /v1.4/movie?limit=999999"):
            response = client.filter_with_big_limit()

        with allure.step("Проверить статус 400"):
            assert response.status_code == 400

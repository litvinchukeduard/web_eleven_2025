from datetime import date
from unittest.mock import patch, Mock

import pytest
from fastapi import HTTPException, status

from src.services import movie_service
from src.models import Movie


class TestMovieService:
    def test_get_all_movies_returns_a_list_of_movies(self):
        mock_session = Mock()
        movies = [
            Movie(id=1, title='Pulp Fiction', release_date=date(2025, 8, 1)),
            Movie(id=1, title='From Dusk Till Dawn', release_date=date(2025, 8, 2))
        ]

        with patch('src.services.movie_service.movie_repository') as mock_movie_repo:
            mock_movie_repo.get_all_movies.return_value = movies

            result_movies = movie_service.get_all_movies(mock_session)
            assert result_movies == movies

    # create movie: test if movie already exists
    def test_create_movie_movie_already_exists(self):
        mock_session = Mock()
        existing_movie = Movie(id=1, title='Pulp Fiction', release_date=date(2025, 8, 1))

        with patch('src.services.movie_service.movie_repository') as mock_movie_repo:
            mock_movie_repo.get_movie_by_title.return_value = existing_movie

            with pytest.raises(HTTPException) as already_exists_exception:
                movie_service.create_movie(existing_movie.title, existing_movie.release_date, mock_session)

            assert already_exists_exception.value.status_code == status.HTTP_400_BAD_REQUEST
            mock_movie_repo.create.assert_not_called()

    # create movie: test if movie does not exist
    def test_create_movie_successes(self):
        mock_session = Mock()
        existing_movie = Movie(id=1, title='Pulp Fiction', release_date=date(2025, 8, 1))

        with patch('src.services.movie_service.movie_repository') as mock_movie_repo:
            mock_movie_repo.get_movie_by_title.return_value = None
            mock_movie_repo.create.return_value = existing_movie

            result = movie_service.create_movie(existing_movie.title, existing_movie.release_date, mock_session)
            assert result == existing_movie
            mock_movie_repo.create.assert_called_once()
            
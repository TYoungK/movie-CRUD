from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status
from .models import Movie


class MovieCRUDTest(APITestCase):
    def setUp(self):
        self.data = {
            "title": "화양연화",
            "genre": "로맨스, 드라마",
            "running_time": 99,
            "director": "Wong Kar-wai",
            "casts": "TonyReung, Maggie",
            "release_date": "2000-02-01"
        }
        self.response = self.client.post(
            reverse('movie:movie-list'),
            self.data,
            format="json")

    def test_post_movie(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_movies(self):
        response = self.client.get(reverse('movie:movie-list'), format='json')
        if Movie.objects.count() == 0:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_movie(self):
        movie = Movie.objects.get()
        response = self.client.get(reverse('movie:movie-detail', kwargs={'pk': movie.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), movie.id)

    def test_put_movie(self):
        movie_data = {
            "title": "추격자",
            "genre": "스릴러 공포",
            "running_time": 140,
            "director": "나홍진",
            "casts": "김윤석,하정우"
        }
        movie = Movie.objects.get()
        response = self.client.put(reverse('movie:movie-detail', kwargs={'pk': movie.id}), movie_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data.get('title'), movie_data['title'])
        self.assertEqual(response.data.get('genre'), movie_data['genre'])
        self.assertEqual(response.data.get('running_time'), movie_data['running_time'])
        self.assertEqual(response.data.get('director'), movie_data['director'])
        self.assertEqual(response.data.get('casts'), movie_data['casts'])

    def test_delete_movie(self):
        movie = Movie.objects.get()
        response = self.client.delete(reverse('movie:movie-detail', kwargs={'pk': movie.id}), format='json', follow=True)

        self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)

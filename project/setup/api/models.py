from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режиссёр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Бибо Бержерон'),
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Йеллоустоун'),
    'description': fields.String(required=True, max_length=255, example='Text'),
    'trailer': fields.String(required=True, max_length=255, example='https://www.youtube.com/watch?v=UKei_d0cbP4'),
    'year': fields.Integer(required=True, example=1900),
    'rating': fields.Float(required=True, example=5.5),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director),
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=100, example='sae@hfhf.com'),
    'password': fields.String(required=True, max_length=255, example='dgdfg'),
    'name': fields.String(required=True, max_length=100, example='dik'),
    'surname': fields.String(required=True, max_length=100, example='dik'),
    'favorite_genre': fields.Nested(genre),


})

favorites: Model = api.model('Избранные фильмы', {
    'id': fields.Integer(required=True, example=1),
    'user_id': fields.Nested(user),
    'movie_id': fields.Nested(movie),

})
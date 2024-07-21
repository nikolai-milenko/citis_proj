from flask import Flask, jsonify
from flask_restx import Api, Resource, fields

# Создаем API
api = Api(
    version='1.0',
    title='Articles Parsing API',
    description='API для парсинга статей',
    doc='/doc'
)

# Создаем namespace для articles API
articles_ns = api.namespace('articles', path='/', description='Операции парсинга статей')

# Модель для входных данных
articles_query_model = articles_ns.model('ArticlesQuery', {
    'query': fields.String(required=True, example='попугаи', description='Поисковый запрос для статей')
})

# Пустая модель для успешного результата
empty_response_model = articles_ns.schema_model('EmptyResponse', {
    'type': 'object',
    'properties': {},
    'description': 'Пустой объект, возвращаемый при успешном выполнении запроса'
})

# Модель для ошибки
error_model = articles_ns.model('Error', {
    'error': fields.String(description='Описание ошибки', example='Пустой запрос')
})


# @articles_ns.route('/parse')
# class ArticleParser(Resource):
#     @articles_ns.expect(articles_query_model, validate=True)
#     @articles_ns.response(200, 'Success', empty_response_model)
#     @articles_ns.response(400, 'Bad Request', error_model)
#     def post(self):
#         """
#         Парсинг статей по заданному поисковому запросу.
#
#         Возвращает пустой JSON при успешном выполнении. Если возникла ошибка, возвращает описание ошибки.
#         """
#         return {}


api.add_namespace(articles_ns, path='/')


def init_swagger(app):
    api.init_app(app)
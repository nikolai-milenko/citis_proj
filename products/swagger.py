from flask_restx import Api, Resource, fields

# Создаем API
api = Api(
    version='1.0',
    title='Products Parsing API',
    description='API для парсинга продуктов',
    doc='/doc'
)

# Создаем namespace для products API
products_ns = api.namespace('products', path='/', description='Операции парсинга продуктов')

# Модель для входных данных
products_query_model = products_ns.model('ProductsQuery', {
    'query': fields.String(required=True, description='Поисковый запрос для продуктов')
})


product_model = products_ns.model('Product', {
    'query': fields.String(description='Поисковый запрос для продуктов', example="купить ноутбук"),
    'results': fields.List(fields.Nested(products_ns.model('ProductResult', {
        'url': fields.String(description='URL продукта', example="https://laptop.com/hp/1"),
        'name': fields.String(description='Название продукта', example="HP Probook 10g"),
        'price': fields.String(description='Цена продукта', example="89999.00"),
        'rating': fields.String(description='Рейтинг продукта', example="4.7"),
        'reviews': fields.List(fields.Nested(products_ns.model('Review', {
            'rating': fields.String(description='Рейтинг обзора', example="5"),
            'review': fields.String(description='Текст обзора', example="Классный ноутбук!")
        })))
    })))
})

# @products_ns.route('/parse')
# class ProductParser(Resource):
#     @products_ns.expect(products_query_model, validate=True)
#     @products_ns.marshal_with(product_model, code=200)
#     def post(self):
#         """
#         Парсинг продуктов по заданному поисковому запросу.
#
#         Возвращает список продуктов с их данными.
#         """
#         return {}

api.add_namespace(products_ns, path='/')

def init_swagger(app):
    api.init_app(app)

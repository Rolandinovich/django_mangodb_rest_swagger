import coreapi
import coreschema
from django.utils.six.moves.urllib import parse as urlparse
from rest_framework.schemas import AutoSchema
from api.login_request.models import StatusChoice


# def list_status_HTML():
#     return (f'<li>{item.name} - {item.value}</li>' for item in StatusChoice)
#
#
# def string_status():
#     return (f'{item.name} - {item.value}' for item in StatusChoice)
#
#
# ORDERS_NOTES = f'''
# <ul>Доступные статусы:
#     {''.join(list_status_HTML())}
# </ul>
# <p>Для того чтобы вывести корзину, нужно в status добавить параметр <b>{StatusChoice.FM.name}</b></p>
# '''
#
# ORDERS_ITEM_NOTES = f'''
# <p>При добавлении карточки, если корзины ещё нет, то она автоматически создаётся.</p>
# <p>В статусе <b>{StatusChoice.FM.name}</b> может быть только один заказ(корзина)</p>
# '''
#

class LoginRequestSchema(AutoSchema):
    def get_description(self, path, method):
        if method == 'GET':
            return 'Вывод всех заявок'.format('<br>')


class OrderReturnSchema(AutoSchema):
    def get_description(self, path, method):
        if method == 'GET':
            return 'Вывод списка всех заказов юзера{}'.format('<br>')


class OrderSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        fields = self.get_path_fields(path, method)
        fields += self.get_serializer_fields(path, method)
        fields += self.get_pagination_fields(path, method)
        if self.view.action in ['list']:
            fields += self.get_filter_fields(path, method)

        manual_fields = self.get_manual_fields(path, method)
        fields = self.update_fields(fields, manual_fields)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method)
        else:
            encoding = None

        description = self.get_description(path, method)

        if base_url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urlparse.urljoin(base_url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=description
        )

    def get_description(self, path, method):
        if method == 'POST':
            return 'Создание заказа.'
        if method == 'GET':
            if self.view.action in ['list']:
                return 'Вывод списка всех заказов юзера{}{}'.format('<br>', ORDERS_NOTES)
            else:
                return 'Вывод отдельного заказа по его ID'
        if method == 'DELETE':
            return 'Удаление заказа'
        if method in ['PUT', 'PATCH']:
            return 'Изменение заказа'

    def get_encoding(self, path, method):
        return 'application/json'

    def get_filter_fields(self, path, method):
        fields = []
        if method == 'GET':
            fields = [
                coreapi.Field(
                    name='status',
                    required=False,
                    location="query",
                    schema=coreschema.String(title='status',
                                             default='FM',
                                             description='status'),
                    description='Выводит список заказов со статусом'
                ),
                coreapi.Field(
                    name='status_ne',
                    required=False,
                    location="query",
                    schema=coreschema.String(title='status_ne',
                                             default='FM',
                                             description='status_ne'),
                    description='Выводит список всех заказов без указанного в поле статуса'
                ),
            ]

        return fields

    def get_serializer_fields(self, path, method):
        fields = []
        if method == 'POST':
            fields = [
                coreapi.Field(
                    name='street',
                    required=True,
                    location="form",
                    schema=coreschema.String(title='street',
                                             default=None,
                                             description='street'),
                    description='street'
                ),
                coreapi.Field(
                    name='apartment',
                    required=True,
                    location="form",
                    schema=coreschema.String(title='apartment',
                                             default=None,
                                             description='apartment'),
                    description='apartment'
                ),
                coreapi.Field(
                    name='tel',
                    required=True,
                    location="form",
                    schema=coreschema.String(title='tel',
                                             default=None,
                                             description='tel'),
                    description='Tel'
                ),
            ]

        elif method in ['PUT', 'PATCH']:
            fields = [
                coreapi.Field(
                    name='tel',
                    required=False,
                    location="form",
                    schema=coreschema.String(title='tel',
                                             default=None,
                                             description='Phone number'),
                    description='Phone number'
                ),
                coreapi.Field(
                    name='street',
                    required=True,
                    location="form",
                    schema=coreschema.String(title='street',
                                             default=None,
                                             description='street'),
                    description='street'
                ),
                coreapi.Field(
                    name='house_number',
                    required=True,
                    location="form",
                    schema=coreschema.String(title='house_number',
                                             default=None,
                                             description='house_number'),
                    description='house_number'
                ),
                coreapi.Field(
                    name='apartment',
                    required=True,
                    location="form",
                    schema=coreschema.String(title='apartment',
                                             default=None,
                                             description='apartment'),
                    description='apartment'
                ),

                coreapi.Field(
                    name='status',
                    required=True,
                    location="form",
                    schema=coreschema.String(title='status',
                                             default=StatusChoice.FM.name,
                                             description='status'),
                    # schema=coreschema.Enum(enum=StatusChoice),
                    description=f'{", ".join(string_status())}'
                ),
            ]
        return fields


class OrderItemSchema(AutoSchema):
    def get_description(self, path, method):
        if method == 'POST':
            return 'Добавление карточки в заказ{}{}'.format('<br>', ORDERS_ITEM_NOTES)
        if method == 'DELETE':
            return 'Удаляет карточку из заказаных'

        return None

    def get_encoding(self, path, method):
        return 'application/json'

    def get_serializer_fields(self, path, method):
        fields = []
        if method == 'POST':
            fields = [
                coreapi.Field(
                    name='clothe_id',
                    required=True,
                    location="form",
                    schema=coreschema.Integer(title='Clothes ID',
                                              default=None,
                                              description='Clothes ID'),
                    description='id clothes'
                ),
                coreapi.Field(
                    name='quantity',
                    required=True,
                    location="form",
                    schema=coreschema.Integer(title='quantity',
                                              default=1,
                                              description='Quantity'),
                    description='quantity'
                ),
            ]
        return fields

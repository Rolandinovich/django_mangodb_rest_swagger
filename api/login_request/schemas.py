import coreapi
import coreschema
from rest_framework.schemas import AutoSchema
from api.login_request.models import StatusChoice


def list_status_HTML():
    return (f'<li>{item.name} - {item.value}</li>' for item in StatusChoice)


def string_status():
    return (f'{item.name} - {item.value}' for item in StatusChoice)


NOTES = f'''
<ul>Доступные статусы:
    {''.join(list_status_HTML())}
</ul>
'''


class LoginRequestSchema(AutoSchema):
    def get_description(self, path, method):
        if method == 'GET':

            if self.view.action in ['list']:
                return 'Вывод всех заявок'.format('<br>')
            else:
                return 'Вывод заявки по ID'
        if method == 'POST':
            return 'Добавить заявку'.format('<br>')
        if method == 'PUT':
            return 'Изменить заявку'.format('<br>', NOTES)

    def get_serializer_fields(self, path, method):
        fields = []
        if method == 'PUT':
            fields = [
                coreapi.Field(
                    name='status',
                    required=True,
                    location="form",
                    schema=coreschema.String(title='status',
                                             default=StatusChoice.SNT.name,
                                             description='status'),
                    description=f'{", ".join(string_status())}'
                ),
            ]
        if method == 'POST':
            fields = [
                coreapi.Field(
                    name='message',
                    required=True,
                    location="form",
                    schema=coreschema.String(title='message',
                                             default=None,
                                             description='message'),
                    description='Текст заявки'
                ),
            ]
        return fields


class ChangeUserStatusSchema(AutoSchema):
    def get_description(self, path, method):
        if method == 'PUT':
            return 'Изменение статуса "менеджер" у пользователя'.format('<br>', )
        if method == 'GET':
            return 'Получение статуса "менеджер" у пользователя'.format('<br>', )

    def get_serializer_fields(self, path, method):
        fields = []
        return fields

# Generated by Django 2.1.5 on 2019-05-29 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Текст заявки')),
                ('status', models.CharField(choices=[('SNT', 'Sent'), ('UC', 'Under consideration'), ('APT', 'Accept'), ('DCN', 'Decline')], default='SNT', max_length=3, verbose_name='статус')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 4.2.7 on 2023-12-02 20:43
# Generated by Django 4.2.7 on 2023-11-30 19:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0008_lesson_owner_payment_owner'),
        ('users', '0003_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(blank=True, max_length=300, null=True, verbose_name='Название подписки')),
                ('is_subscribed', models.BooleanField(default=False, verbose_name='Подписка оформлена')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='education.course', verbose_name='Курс для подписки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подписка на курс',
                'verbose_name_plural': 'Подписки на курс',
            },
        ),
    ]

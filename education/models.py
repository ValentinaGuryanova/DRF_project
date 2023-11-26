from django.conf import settings
from django.db import models
from django.utils import timezone

#from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='education/', verbose_name='изображение', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец курса', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='education/', verbose_name='изображение', **NULLABLE)
    video_link = models.URLField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):

    PAY_CARD = 'card'
    PAY_CASH = 'cash'

    PAY_TYPES = (
        (PAY_CASH, 'наличные'),
        (PAY_CARD, 'перевод')
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, verbose_name='оплаченный курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, verbose_name='оплаченный урок')
    # user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateField(default=timezone.now, verbose_name='дата оплаты')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')
    pay_type = models.CharField(choices=PAY_TYPES, default=PAY_CASH, max_length=100, verbose_name='способ оплаты')

    def __str__(self):
        if self.payment_date:
            return f'Платеж на сумму {self.amount} курса {self.course}'
        else:
            return f'Платеж на сумму {self.amount} курса {self.lesson}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ('-payment_date',)

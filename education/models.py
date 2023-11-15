from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='education/', verbose_name='изображение', **NULLABLE)

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


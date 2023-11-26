from django.core.management import BaseCommand

from education.models import Course, Payment, Lesson
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        payment_date = [
            {"course": Course.objects.get(pk=2),
             "payment_date": "2023-11-21",
             "amount": 1000,
             "pay_type": 'cash'
             },
            {"course": Course.objects.get(pk=5),
             "payment_date": "2023-11-23",
             "amount": 2000,
             "pay_type": 'cash'
             },
            {"course": Course.objects.get(pk=7),
             "payment_date": "2023-11-24",
             "amount": 3000,
             "pay_type": 'card'
             },
            {"course": Course.objects.get(pk=8),
             "payment_date": "2023-11-22",
             "amount": 4000,
             "pay_type": 'cash'
             },
            {"course": Course.objects.get(pk=21),
             "payment_date": "2023-11-20",
             "amount": 5000,
             "pay_type": 'card'
             }
        ]

        payment_for_create = []

        for data in payment_date:
            payment_for_create.append(Payment(**data))

        Payment.objects.bulk_create(payment_for_create)

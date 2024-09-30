from django.core.management.base import BaseCommand
from faker import Faker
import random
from apps.users.models import CustomUser
from ...models import Field, Journal, Research

class Command(BaseCommand):
    help = 'Seed database with Field, Journal, and Research data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # توليد بيانات جدول Field
        for _ in range(10):
            Field.objects.create(
                name=fake.word(),
                description=fake.text(),
            )

        # توليد بيانات جدول Journal
        for _ in range(10):
            Journal.objects.create(
                name=fake.company(),
                abbreviation=fake.lexify(text='?????'),
                logo='journals_logo/sample_logo.png',
                website_url=fake.url()
            )

        # توليد بيانات جدول Research
        for _ in range(20):
            Research.objects.create(
                title=fake.sentence(),
                abstract=fake.paragraph(nb_sentences=5),
                publication_date=fake.date_this_decade(),
                journal=random.choice(Journal.objects.all()),
                authors=fake.name(),
                institution=fake.company(),
                file='research/sample.pdf',
                field=random.choice(Field.objects.all()),
                views_count=random.randint(0, 1000),
                downloads_count=random.randint(0, 500),
                user=random.choice(CustomUser.objects.all())
            )

        self.stdout.write(self.style.SUCCESS('Data seeded successfully!'))

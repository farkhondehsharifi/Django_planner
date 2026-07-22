import factory
from django.utils import timezone  
from reminders.models import Reminder
from accounts.tests.factories import UserFactory

class ReminderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reminder

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=4)
    date = factory.LazyFunction(lambda: (timezone.now() + timezone.timedelta(hours=1)).date())
    time = factory.LazyFunction(lambda: (timezone.now() + timezone.timedelta(hours=1)).time())
    color = factory.Faker('hex_color')
    description = factory.Faker('paragraph', nb_sentences=3)
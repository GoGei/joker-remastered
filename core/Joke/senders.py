from core.Emailer.models import EmailNotification
from core.Joke.models import Joke


class EmailSender(object):
    def __init__(self):
        pass

    def send(self, joke: Joke, receiver: str):
        context = {
            'text': joke.text,
        }

        notification = EmailNotification.get_by_slug('joke_email')
        notification.send(receiver, context)
        return context

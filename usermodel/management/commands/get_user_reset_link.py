from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):

    help = 'Input user email, output reset password link'

    def add_arguments(self, parser):
        parser.add_argument('email_id', type=str)

    def handle(self, *args, **kwargs):
        email_id = kwargs['email_id']
        try:
            if User.objects.get(email=email_id):
                user = User.objects.get(email=email_id)
                reset_link = user.get_password_reset_url()
                self.stdout.write('Please use this link to create a password')
                self.stdout.write(f'Reset link: {reset_link}')
            else:
                self.stdout.write(f'User with email: {email_id} does not exist')
        except Exception as e:
            self.stderr.write(f'There was an error {e}')
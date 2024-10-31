from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from random_username.generate import generate_username

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates user with email argument and generates a password reset link. If duplicate key error for username occurs, just run it again'

    def add_arguments(self, parser):
        parser.add_argument('email_id', type=str)

    def handle(self, *args, **kwargs):
        email_id = kwargs['email_id']
        gen_username = generate_username()
        gen_password = get_random_string(10)

        try:
            u = None
            if not User.objects.filter(email=email_id).exists():
                self.stdout.write('No user with email found, creating one')
                u = User.objects.create_user(email=email_id, username=gen_username, password=gen_password)
                self.stdout.write('Created user. Now creating password reset link')
                reset_link = u.get_password_reset_url()
                self.stdout.write('Created password reset link')
                self.stdout.write('----------')
                self.stdout.write(f'Welcome to Salted Vanilla\'s beta V2, {gen_username}')
                self.stdout.write('Your email and password reset link are listed below')
                self.stdout.write(f'Email: {email_id}')
                # self.stdout.write(f'Username: {gen_username}')
                self.stdout.write('Please use this link to create a password')
                self.stdout.write(f'Reset link: {reset_link}')
                self.stdout.write('Remember this is a beta, not a finished product')
                self.stdout.write('All data you choose to enter may be wiped before the public version is released')
                self.stdout.write('Thank you for inquiring Salted Vanilla, please let me know your thoughts!')
                self.stdout.write('----------')
            else:
                self.stdout.write('A user with this email address already exists')
        except Exception as e:
            self.stderr.write(f'There was an error {e}')


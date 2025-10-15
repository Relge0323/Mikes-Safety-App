from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile

class Command(BaseCommand):
    help = 'Creates profiles for users that don\'t have one'

    def handle(self, *args, **kwargs):
        users_without_profile = []
        
        for user in User.objects.all():
            try:
                # Try to access the profile
                _ = user.profile
            except Profile.DoesNotExist:
                # If it doesn't exist, create it
                Profile.objects.create(user=user)
                users_without_profile.append(user.username)
        
        if users_without_profile:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created profiles for: {", ".join(users_without_profile)}'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('All users already have profiles!')
            )
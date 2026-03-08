from django.core.management.base import BaseCommand
from leadership.models import ManagementPost, OfficeBearer
from datetime import date

class Command(BaseCommand):
    help = 'Add Sonikot Youth members and leaders to the leadership section'

    def handle(self, *args, **options):
        # Create positions if not exist
        member_post, created = ManagementPost.objects.get_or_create(
            title='Member',
            defaults={'priority': 10, 'description': 'General member of Sonikot Youth'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created "Member" position'))

        president_post, created = ManagementPost.objects.get_or_create(
            title='President',
            defaults={'priority': 1, 'description': 'President of Sonikot Youth'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created "President" position'))

        vice_president_post, created = ManagementPost.objects.get_or_create(
            title='Vice President',
            defaults={'priority': 2, 'description': 'Vice President of Sonikot Youth'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created "Vice President" position'))

        # Photo mapping
        photo_mapping = {
            'Abbas Lone': 'Abbas Lone.jpeg',
            'Abdullah Dogar': 'Abdullha Dogar.webp',
            'Ahmed Dogar': 'Ahmed Dogar.jpeg',
            'Ahsan Khan': 'Ahsan Khan.jpeg',
            'Arif Dogar': 'Arif Dogar.jpeg',
            'Azhar Lone': 'Azhar LOne.jpeg',
            'Faheem Dogar': 'Faheem Dogar.jpeg',
            'Hassam Khan': 'Hassam Khan.jpeg',
            'Ishaq Lone': 'Ishaq Lone.jpeg',
            'Mirbaz Dogar': 'Mirbaz Dogar.jpeg',
            'Muhammad Ibrahim Rajpot': 'Muhammad Ibrahim Rajpot.jpeg',
            'Shakir hussain': 'Shakir hussain.jpeg',
            'Shebaz Dogar': 'Shebaz Dogar.jpeg',
            'syed Noman Shah': 'syed Noman Shah.jpeg',
            'Tayab Dogar': 'Tayab Dogar.jpeg',
            'Zahaq Awan': 'Zahaq Awan.jpeg',
            'Akhunzada Zubair': 'Akhunxada Zubair.jpeg',
            'Umer Uddin': 'umer uddin.jpeg'
        }

        # List of members
        members = [
            'Abbas Lone',
            'Abdullah Dogar',
            'Ahmed Dogar',
            'Ahsan Khan',
            'Arif Dogar',
            'Azhar Lone',
            'Faheem Dogar',
            'Hassam Khan',
            'Ishaq Lone',
            'Mirbaz Dogar',
            'Muhammad Ibrahim Rajpot',
            'Shakir hussain',
            'Shebaz Dogar',
            'syed Noman Shah',
            'Tayab Dogar',
            'Zahaq Awan'
        ]

        # Add members
        for name in members:
            photo_filename = photo_mapping.get(name)
            photo_path = f'images/{photo_filename}' if photo_filename else None
            bearer, created = OfficeBearer.objects.get_or_create(
                full_name=name,
                defaults={
                    'post': member_post,
                    'status': 'current',
                    'term_start': date.today(),
                    'photo': photo_path
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Added member: {name}'))
            else:
                # Update photo if not set OR if the path is incorrect (starts with 'static/')
                needs_update = False
                if not bearer.photo and photo_path:
                    needs_update = True
                elif bearer.photo and str(bearer.photo).startswith('static/'):
                    needs_update = True
                
                if needs_update and photo_path:
                    bearer.photo = photo_path
                    bearer.save()

        # Add leaders
        leaders = [
            ('Akhunzada Zubair', president_post),
            ('Umer Uddin', vice_president_post)
        ]

        for name, post in leaders:
            photo_path = photo_mapping.get(name)
            bearer, created = OfficeBearer.objects.get_or_create(
                full_name=name,
                defaults={
                    'post': post,
                    'status': 'current',
                    'term_start': date.today(),
                    'photo': photo_path
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Added leader: {name} as {post.title}'))
            else:
                self.stdout.write(f'Leader {name} already exists')

        self.stdout.write(self.style.SUCCESS('All members and leaders processed'))

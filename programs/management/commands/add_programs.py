"""
Management command to add initial welfare programs.
"""

from django.core.management.base import BaseCommand
from programs.models import ProgramCategory, WelfareProgram
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Add initial welfare programs to the database'

    def handle(self, *args, **options):
        self.stdout.write('Creating program categories...')
        
        # Create categories
        categories_data = [
            {
                'name': 'Flood Relief',
                'icon': 'fa-water',
                'description': 'Emergency relief programs for flood-affected communities',
                'color': '#dc3545',
                'priority': 1
            },
            {
                'name': 'Help Poor People',
                'icon': 'fa-hands-helping',
                'description': 'Support for impoverished individuals and families',
                'color': '#ffc107',
                'priority': 2
            },
            {
                'name': 'Educational Help',
                'icon': 'fa-graduation-cap',
                'description': 'Education support and scholarship programs',
                'color': '#28a745',
                'priority': 3
            },
            {
                'name': 'Social Help',
                'icon': 'fa-users',
                'description': 'Social welfare and community development programs',
                'color': '#17a2b8',
                'priority': 4
            },
            {
                'name': 'Economic Help',
                'icon': 'fa-coins',
                'description': 'Economic empowerment and livelihood programs',
                'color': '#6f42c1',
                'priority': 5
            },
            {
                'name': 'Natural Disaster Relief',
                'icon': 'fa-exclamation-triangle',
                'description': 'Emergency response and relief for natural disasters',
                'color': '#fd7e14',
                'priority': 6
            },
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = ProgramCategory.objects.update_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[category.name] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Updated category: {category.name}'))
        
        self.stdout.write('Creating welfare programs...')
        
        # Create programs
        programs_data = [
            {
                'title': 'Emergency Flood Relief Campaign 2026',
                'category': 'Flood Relief',
                'short_description': 'Providing emergency relief to families affected by recent flooding in Sonikot and surrounding areas.',
                'detailed_description': 'Our Emergency Flood Relief Campaign aims to provide immediate assistance to families affected by devastating floods in Sonikot and surrounding areas. We are distributing essential supplies including food packages, clean drinking water, medicines, and temporary shelter materials.',
                'objectives': '- Provide emergency food packages to 500 families\n- Distribute clean drinking water to 1000 people\n- Supply medicines and medical assistance',
                'status': 'ongoing',
                'start_date': timezone.now().date(),
                'estimated_budget': 5000000,
                'actual_cost': 2500000,
                'target_beneficiaries': 5000,
                'actual_beneficiaries': 2500,
                'location': 'Sonikot, Gilgit-Baltistan',
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'Food Support for Needy Families',
                'category': 'Help Poor People',
                'short_description': 'Monthly food distribution program for underprivileged families in Sonikot.',
                'detailed_description': 'Our Food Support Program provides monthly food packages to the most needy families in Sonikot and surrounding villages.',
                'objectives': '- Identify and verify 200 needy families\n- Provide monthly food packages\n- Ensure food security for vulnerable populations',
                'status': 'ongoing',
                'start_date': timezone.now().date() - timedelta(days=180),
                'estimated_budget': 2400000,
                'actual_cost': 1200000,
                'target_beneficiaries': 1000,
                'actual_beneficiaries': 600,
                'location': 'Sonikot, Gilgit-Baltistan',
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'School Scholarship Program',
                'category': 'Educational Help',
                'short_description': 'Providing scholarships for underprivileged students to continue their education.',
                'detailed_description': 'Our School Scholarship Program aims to ensure that financial constraints do not prevent talented students from continuing their education.',
                'objectives': '- Provide scholarships to 100 students annually\n- Cover tuition fees and educational materials\n- Monitor academic progress',
                'status': 'ongoing',
                'start_date': timezone.now().date() - timedelta(days=365),
                'estimated_budget': 1500000,
                'actual_cost': 750000,
                'target_beneficiaries': 100,
                'actual_beneficiaries': 65,
                'location': 'Sonikot, Gilgit-Baltistan',
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'Free Medical Camps',
                'category': 'Social Help',
                'short_description': 'Organizing free medical camps to provide healthcare to remote communities.',
                'detailed_description': 'Our Free Medical Camps program brings healthcare services to remote and underserved communities in Sonikot and surrounding areas.',
                'objectives': '- Organize 12 medical camps per year\n- Provide free consultations to 2000 patients\n- Distribute free medicines',
                'status': 'ongoing',
                'start_date': timezone.now().date() - timedelta(days=180),
                'estimated_budget': 800000,
                'actual_cost': 400000,
                'target_beneficiaries': 2000,
                'actual_beneficiaries': 1200,
                'location': 'Sonikot and surrounding villages',
                'is_active': True,
                'is_featured': False,
            },
            {
                'title': 'Women Entrepreneurship Program',
                'category': 'Economic Help',
                'short_description': 'Empowering women through skills training and micro-finance support.',
                'detailed_description': 'Our Women Entrepreneurship Program aims to empower women by providing them with skills training and financial support to start their own businesses.',
                'objectives': '- Train 50 women in entrepreneurship skills\n- Provide micro-finance support to 30 women\n- Help establish women-owned businesses',
                'status': 'ongoing',
                'start_date': timezone.now().date() - timedelta(days=90),
                'estimated_budget': 1000000,
                'actual_cost': 300000,
                'target_beneficiaries': 50,
                'actual_beneficiaries': 25,
                'location': 'Sonikot, Gilgit-Baltistan',
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'Earthquake Emergency Response',
                'category': 'Natural Disaster Relief',
                'short_description': 'Rapid response unit for earthquake-affected areas in Gilgit-Baltistan.',
                'detailed_description': 'Our Earthquake Emergency Response program is prepared to provide immediate assistance when earthquakes strike. We maintain emergency supplies and have a trained response team ready to deploy quickly.',
                'objectives': '- Maintain emergency supply reserves\n- Train response teams in disaster management\n- Provide immediate relief within 24 hours',
                'status': 'planning',
                'start_date': timezone.now().date(),
                'estimated_budget': 2000000,
                'actual_cost': 0,
                'target_beneficiaries': 5000,
                'actual_beneficiaries': 0,
                'location': 'Gilgit-Baltistan Region',
                'is_active': True,
                'is_featured': False,
            },
            {
                'title': 'Winter Relief Program',
                'category': 'Help Poor People',
                'short_description': 'Providing warm clothing and heating fuel to families during harsh winters.',
                'detailed_description': 'Our Winter Relief Program addresses the severe challenges faced by poor families during the harsh winter months in Gilgit-Baltistan.',
                'objectives': '- Provide winter clothing to 300 families\n- Distribute blankets and heating fuel\n- Ensure warmth and safety during winter',
                'status': 'completed',
                'start_date': timezone.now().date() - timedelta(days=90),
                'end_date': timezone.now().date() - timedelta(days=30),
                'estimated_budget': 600000,
                'actual_cost': 550000,
                'target_beneficiaries': 1500,
                'actual_beneficiaries': 1400,
                'location': 'Sonikot and surrounding areas',
                'is_active': True,
                'is_featured': False,
            },
            {
                'title': 'IT Training Center',
                'category': 'Educational Help',
                'short_description': 'Free computer training for youth to develop digital skills for employment.',
                'detailed_description': 'Our IT Training Center provides free computer and digital literacy training to youth in Sonikot.',
                'objectives': '- Train 200 youth in basic IT skills\n- Provide computer lab access\n- Offer certification upon completion',
                'status': 'ongoing',
                'start_date': timezone.now().date() - timedelta(days=60),
                'estimated_budget': 500000,
                'actual_cost': 200000,
                'target_beneficiaries': 200,
                'actual_beneficiaries': 80,
                'location': 'Sonikot, Gilgit-Baltistan',
                'is_active': True,
                'is_featured': False,
            },
        ]
        
        for prog_data in programs_data:
            category_name = prog_data.pop('category')
            category = categories.get(category_name)
            
            if category:
                program, created = WelfareProgram.objects.update_or_create(
                    title=prog_data['title'],
                    defaults={**prog_data, 'category': category}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created program: {program.title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Updated program: {program.title}'))
            else:
                self.stdout.write(self.style.ERROR(f'Category not found: {category_name}'))
        
        self.stdout.write(self.style.SUCCESS('\nSuccessfully added all programs!'))
        self.stdout.write(f'Total categories: {ProgramCategory.objects.count()}')
        self.stdout.write(f'Total programs: {WelfareProgram.objects.count()}')


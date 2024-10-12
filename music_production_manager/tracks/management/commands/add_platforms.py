from django.core.management.base import BaseCommand

from tracks.models import Platform


class Command(BaseCommand):
    help = 'プラットフォームをデータベースに追加します'

    def handle(self, *args, **options):
        platforms = [
            'AudioStock',
            'MotionElements',
            'Pond5',
            'DEMO',
            'TuneCore'
        ]

        for platform_name in platforms:
            Platform.objects.get_or_create(name=platform_name)
            self.stdout.write(self.style.SUCCESS(f'プラットフォーム "{platform_name}" を追加しました'))

        self.stdout.write(self.style.SUCCESS('すべてのプラットフォームを追加しました'))
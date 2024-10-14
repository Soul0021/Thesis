from django.core.management.base import BaseCommand
from userauths.models import Vowel

class Command(BaseCommand):
    help = 'Populate the database with initial Hangul vowels and their sounds.'

    def handle(self, *args, **kwargs):
        # Define the vowel-sound pairs
        vowel_sound_pairs = [
            {'symbol': 'ㅏ', 'sound': 'a'},
            {'symbol': 'ㅑ', 'sound': 'ya'},
            {'symbol': 'ㅓ', 'sound': 'eo'},
            {'symbol': 'ㅕ', 'sound': 'yeo'},
            {'symbol': 'ㅗ', 'sound': 'o'},
            {'symbol': 'ㅛ', 'sound': 'yo'},
            {'symbol': 'ㅜ', 'sound': 'u'},
            {'symbol': 'ㅠ', 'sound': 'yu'},
            {'symbol': 'ㅡ', 'sound': 'eu'},
            {'symbol': 'ㅣ', 'sound': 'i'},
        ]

        # Insert the vowel-sound pairs into the database
        for pair in vowel_sound_pairs:
            Vowel.objects.get_or_create(symbol=pair['symbol'], sound=pair['sound'])

        self.stdout.write(self.style.SUCCESS('Successfully populated the vowels and sounds.'))

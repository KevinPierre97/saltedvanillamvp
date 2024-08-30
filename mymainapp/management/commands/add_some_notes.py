import pandas as pd
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Add some notes. This is useful for development purposes. Only add the notes necessary to the candles in the candles list'

    # dev run command: python manage.py add_some_notes mymainapp/static/csv2/candle_notes.csv mymainapp/static/csv2/list_of_scents.csv

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str, help='the file that lists out the notes')
        parser.add_argument('filename2', type=str, nargs='+', help='the file that lists out all the possible scents')

    def handle(self, *args, **options):
        file_name = options['filename'][0]
        filename2 = options['filename2'][0]
        df = pd.read_csv(file_name)
        df2 = pd.read_csv(filename2)


        scent_list = []

        for scents in df['Note']:
            scent_list.append(scents)
            # self.stdout.write(scents)

        df_cut = df2.query('Note in @scent_list')

        for scent in scent_list:
            found = 0
            for index, row in df_cut.iterrows():
                # self.stdout.write(row['Genre'])
                if scent in row['Note']:
                    self.stdout.write(f"Family: {row['Family']}, Genre: {row['Genre']}, Note: {row['Note']}")
                    found = 1

            if found == 0:
                self.stdout.write(f'{scent} is not in the total scents list')
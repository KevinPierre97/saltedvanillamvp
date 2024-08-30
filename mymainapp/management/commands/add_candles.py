import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from mymainapp.models import ScentFamily, ScentGenre, ScentNote, Candle, Brand


class Command(BaseCommand):
    help = 'Add list candles, notes, and photos to db.'
    # dev run command: python manage.py add_candles mymainapp/static/csv/list_of_candles.csv mymainapp/static/csv/list_of_scents.csv
    # move list_of_candles and list_of_scents to mymainapp/static/csv
    # move candle_pics folder into media/

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str, help='csv for candles to add')
        parser.add_argument('filename2', type=str, nargs='+', help='csv for scents db')

    def handle(self, *args, **options):
        # Defining parameters
        file_name = options['filename'][0]  # List of candales
        filename2 = options['filename2'][0]  # list of scents
        df = pd.read_csv(file_name)
        df2 = pd.read_csv(filename2)

        family_count = 0
        genre_count = 0
        note_count = 0
        candle_count = 0

        # Actually not word list, but list of every scent in list of candles
        word_list = []

        for scents in df["Notes"]:
            clean = scents.strip("[]").split(", ")
            for word in clean:
                if word not in word_list:
                    word_list.append(word)
                    # self.stdout.write(word)

        # df_cut cuts list of scents to scents only found in list of candles
        df_cut = df2.query('Note in @word_list').drop_duplicates(subset=['Note'], keep='first')

        # First it adds all scents found in list of candles, then it adds all scents not found
        # iterate across df_cut to add all scents
        for index, row in df_cut.iterrows():
            # print(row['Family'].strip(), row['Genre'].strip(), row['Note'])
            scent_family_str = row['Family'].strip()
            scent_genre_str = row['Genre'].strip()
            scent_note_str = row['Note'].strip()

            if not ScentFamily.objects.filter(name=scent_family_str).exists():
                ScentFamily.objects.create(
                    name=scent_family_str
                )
                family_count = family_count + 1
                self.stdout.write(f"created scent family: {scent_family_str}")
            if not ScentGenre.objects.filter(name=scent_genre_str).exists():
                ScentGenre.objects.create(
                    name=scent_genre_str,
                    family=ScentFamily.objects.get(name=scent_family_str),
                )
                genre_count = genre_count + 1
                self.stdout.write(f"created scent genre: {scent_genre_str}")
            if not ScentNote.objects.filter(name=scent_note_str).exists():
                ScentNote.objects.create(
                    name=scent_note_str,
                    genre=ScentGenre.objects.get(name=scent_genre_str),
                )
                note_count = note_count + 1
                self.stdout.write(f"created scent: {scent_note_str}")
        if family_count:
            self.stdout.write(self.style.SUCCESS(f"added {family_count} scent families"))
        else:
            self.stdout.write(self.style.SUCCESS(f"no scent families were added!"))
        if genre_count:
            self.stdout.write(self.style.SUCCESS(f"added {genre_count} scent genres"))
        else:
            self.stdout.write(self.style.SUCCESS(f"no scent genres were added!"))
        if note_count:
            self.stdout.write(self.style.SUCCESS(f"added {note_count} scent notes"))
        else:
            self.stdout.write(self.style.SUCCESS(f"no scent notes were added!"))

        # Processing for all scents that aren't in the list of scents but are in list of candles
        if not ScentFamily.objects.filter(name ="Not defined").exists():
            notDefFamily = ScentFamily.objects.create(name="Not defined")

        if not ScentGenre.objects.filter(name ="Not defined").exists():
            notDefGenre = ScentGenre.objects.create(
                name="Not defined",
                family=ScentFamily.objects.get(name="Not defined")
            )

        for word in word_list:
            if word not in df_cut['Note'].values:
                if not ScentNote.objects.filter(name=word).exists():
                    new_note = ScentNote.objects.create(
                        name=word,
                        genre=ScentGenre.objects.get(name="Not defined")
                    )
                    self.stdout.write(f"Added note: {new_note.name}")

        # Now to add all candles
        # First create brand, then create candle, then add all scents
        for index, row in df.iterrows():

            brandName = row['Brand'].strip()
            add_brand = Brand.objects.get_or_create(
                name=brandName
            )

            if not Candle.objects.filter(name=row['Name']).exists():
                candle = Candle.objects.create(
                    name=row['Name'],
                    brand_id=Brand.objects.get(name=brandName),
                    isImageAdminApproved=True,
                )
                candle_count = candle_count + 1

                clean = row["Notes"].strip("[]").split(", ")
                for scent in clean:
                    candle.notes.add(ScentNote.objects.get(name=scent))
                candle.save()
                self.stdout.write(f'Added candle: {candle.name}')
                #########ADD IMAGES###################################
                img_path = "candle_pics/"+str(int(str(index)) + 2) + ".jpg"
                candle.candle_image = img_path
                candle.save()
                self.stdout.write('Added image')
                #########################################################

        if candle_count:
            self.stdout.write(self.style.SUCCESS(f"added {candle_count} candles"))
        else:
            self.stdout.write(self.style.SUCCESS(f"no candles were added!"))
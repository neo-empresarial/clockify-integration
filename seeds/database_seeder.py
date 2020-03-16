from orator.seeds import Seeder
from .indicator_table_seeder import IndicatorTableSeeder


class DatabaseSeeder(Seeder):
    def run(self):
        """
        Run the database seeds.
        """
        IndicatorTableSeeder.run(self)

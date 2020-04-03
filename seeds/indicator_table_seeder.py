from orator.seeds import Seeder


class IndicatorTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('indicator').insert({
            'name': 'prep',
            'frequency': 'weekly'
        })


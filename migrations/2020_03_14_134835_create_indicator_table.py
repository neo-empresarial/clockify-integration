from orator.migrations import Migration


class CreateIndicatorTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('indicator') as table:
            table.increments('id')
            table.string('name').unique()
            table.string('frequency')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('indicator')

from orator.migrations import Migration


class CreateClientTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('client') as table:
            table.string('clockify_id').primary()
            table.string('name')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('client')

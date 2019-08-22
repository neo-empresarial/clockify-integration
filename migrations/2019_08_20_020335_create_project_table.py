from orator.migrations import Migration


class CreateProjectTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('project') as table:
            table.string('clockify_id').primary()
            table.string('name')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('project')

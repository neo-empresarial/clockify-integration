from orator.migrations import Migration


class CreateActivityTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('activity') as table:
            table.increments('id')
            table.string('name')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('activity')

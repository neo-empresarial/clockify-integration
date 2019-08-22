from orator.migrations import Migration


class CreateMemberTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('member') as table:
            table.string('clockify_id').primary()
            table.string('acronym')
            table.string('email')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('member')

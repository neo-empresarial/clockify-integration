from orator.migrations import Migration


class CreateTimeEntryTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('time_entry') as table:
            table.string('clockify_id').primary()
            table.string('member_id')
            table.foreign('member_id').references('clockify_id').on('member')
            table.string('project_id')
            table.foreign('project_id').references('clockify_id').on('project')
            table.integer('activity_id').unsigned()
            table.foreign('activity_id').references('id').on('activity')
            table.string('client_id')
            table.foreign('client_id').references('clockify_id').on('client')
            table.timestamp('start')
            table.timestamp('end')
            table.string('description')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('time_entry')

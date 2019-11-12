from orator.migrations import Migration


class CreateTimeEntryTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('time_entry') as table:
            table.increments('id')
            table.string('clockify_id').unique().nullable()
            table.integer('member_id').unsigned()
            table.foreign('member_id').references('id').on('member')
            table.integer('project_id').unsigned()
            table.foreign('project_id').references('id').on('project')
            table.integer('activity_id').unsigned()
            table.foreign('activity_id').references('id').on('activity')
            table.integer('client_id').unsigned()
            table.foreign('client_id').references('id').on('client')
            table.timestamp('start')
            table.timestamp('end')
            table.string('description').nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('time_entry')

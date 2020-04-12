from orator.migrations import Migration

class AddTimezoneToTimeEntryTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('time_entry') as table:
            self.db.update("SET timezone='UTC';")
            self.db.update('ALTER TABLE time_entry ALTER COLUMN "start" TYPE TIMESTAMP WITH TIME ZONE;')
            self.db.update('ALTER TABLE time_entry ALTER COLUMN "end" TYPE TIMESTAMP WITH TIME ZONE;')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('time_entry') as table:
            self.db.update("SET timezone='UTC';")
            self.db.update('ALTER TABLE time_entry ALTER COLUMN "start" TYPE TIMESTAMP WITHOUT TIME ZONE;')
            self.db.update('ALTER TABLE time_entry ALTER COLUMN "end" TYPE TIMESTAMP WITHOUT TIME ZONE;')

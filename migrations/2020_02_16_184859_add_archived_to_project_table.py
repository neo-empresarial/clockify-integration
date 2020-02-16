from orator.migrations import Migration


class AddArchivedToProjectTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table("project") as table:
            table.boolean("archived").default(0)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table("project") as table:
            table.drop_column("archived")

from orator.migrations import Migration


class AddClientToProjectTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table("project") as table:
            table.integer("client_id").unsigned().nullable()
            table.foreign("client_id").references("id").on("client")

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table("project") as table:
            table.drop_column("client_id")

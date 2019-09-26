from orator.migrations import Migration


class CreateProjectTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("project") as table:
            table.increments("id")
            table.string("clockify_id").unique().nullable()
            table.string("name")
            table.integer("client_id").unsigned()
            table.foreign("client_id").references("id").on("client")
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("project")

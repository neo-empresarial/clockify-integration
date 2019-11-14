from orator.migrations import Migration


class CreateProjectActivityTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("project_activity") as table:
            table.increments("id")
            table.integer("project_id").unsigned()
            table.foreign("project_id").references("id").on("project")
            table.integer("activity_id").unsigned()
            table.foreign("activity_id").references("id").on("activity")
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("project_activity")

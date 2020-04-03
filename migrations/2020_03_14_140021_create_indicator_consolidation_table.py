from orator.migrations import Migration


class CreateIndicatorConsolidationTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("indicator_consolidation") as table:
            table.increments("id")
            table.float("value")
            table.timestamp("start_date")
            table.timestamp("end_date")
            table.integer("member_id").unsigned()
            table.foreign("member_id").references("id").on("member")
            table.integer("indicator_id").unsigned()
            table.foreign("indicator_id").references("id").on("indicator")
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("indicator_consolidation")

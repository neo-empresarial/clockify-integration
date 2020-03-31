from orator.migrations import Migration


class AddActiveToMemberTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table("member") as table:
            table.boolean("is_active").default(True)
            table.timestamp("date_deactivated").nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table("member") as table:
            table.drop_column("is_active")
            table.drop_column("date_deactivated")

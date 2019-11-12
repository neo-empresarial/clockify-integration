from orator.migrations import Migration


class Addclt(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table("member") as table:
            table.boolean("is_clt").default(0)
            pass

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table("member") as table:
            table.drop_column("is_clt")
            pass

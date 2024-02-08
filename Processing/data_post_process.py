from Sensors.Data import DataStruct, RawDS
from Sensors.Sqlite_Adapt import SqliteAdapt


def main(adapt: SqliteAdapt):
    print("Starting Post Processing")
    raw_tables = [table for table in adapt.get_tables() if "raw" in table]

    for table in raw_tables:
        adapt.clear_table(table.replace("raw_", ""))
        raws = adapt.get_raws(table)
        while raws.hasRows:
            raw_rows = raws.getNext()
            for row in raw_rows:
                adapt.write_row(DataStruct(RawDS(row[1], row[0])), table.replace("raw_", ""))
            adapt.commit()



if __name__ == "__main__":
    main(SqliteAdapt("/Users/max/Downloads/2024-01-21_20-57-23_data.db"))
    print("done")

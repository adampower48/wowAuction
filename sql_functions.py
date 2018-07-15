import mysql.connector as sql

db_config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "database": "wowauction"
}


class Tables:
    ITEM_INFO = "item_info"
    AUCTIONS = "auctions"


db = None
cursor = None


def open_db():
    global db, cursor
    db = sql.connect(**db_config)
    cursor = db.cursor(buffered=True)


def close_db():
    cursor.close()
    db.close()


def sql_check_exists(table, keys_values, primary_key):
    com = "SELECT count(1) FROM {} WHERE {} = {}".format(
        table, primary_key, keys_values[primary_key]
    )

    cursor.execute(com)
    return cursor.fetchone()[0]


def sql_insert(table, keys_values, primary_key=None):
    if not primary_key or not sql_check_exists(table, keys_values, primary_key):
        command = (
            "INSERT INTO {} (".format(table) +
            ", ".join(keys_values.keys()) +
            ") VALUES (%(" +
            ")s, %(".join(keys_values.keys()) +
            ")s)"
        )
        cursor.execute(command, keys_values)


def sql_query(table, **kwargs):
    if len(kwargs) > 0:
        command = (
            "SELECT * FROM {} WHERE ".format(table) +
            " AND ".join(["{} = %({})s".format(k, k) for k in kwargs.keys()])
        )
    else:
        command = "SELECT * FROM {}".format(table)

    cursor.execute(command, kwargs)

    return [dict(zip(cursor.column_names, vals)) for vals in cursor.fetchall()]


def sql_query_custom(command):
    cursor.execute(command)
    return cursor.fetchall()


def sql_update(table, keys_values, primary_key):
    if sql_check_exists(table, keys_values, primary_key):
        command = (
            "UPDATE {} SET ".format(table) +
            ", ".join(["{} = %({})s".format(k, k) for k in keys_values.keys()]) +
            " WHERE {} = %({})s".format(primary_key, primary_key)
        )

        cursor.execute(command, keys_values)


def sql_clear_table(table):
    cursor.execute("DELETE FROM {}".format(table))


def trim_json_object(obj):
    # Filters values containing dict and list objects which cant be entered into the database
    return {k: v for (k, v) in obj.items() if type(v) not in (list, dict)}


def update_item_info(item_info_dict):
    for v in item_info_dict.values():
        sql_insert("item_info", trim_json_object(v), primary_key="id")

    db.commit()


def update_auctions(auctions_list):
    sql_clear_table("auctions")
    for v in auctions_list:
        sql_insert("auctions", trim_json_object(v), primary_key="auc")

    db.commit()


if __name__ == '__main__':
    open_db()

    items = sql_query("item_info")

    close_db()

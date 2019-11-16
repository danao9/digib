import pymysql
import pandas as pd


def main():
    # fetch_from_db()
    insert_into_db()


def fetch_from_db():
    # connect to database
    db = pymysql.connect(host="localhost", port=3406, user="root", passwd="public16", db="digib")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT * FROM test")

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print(data)

    # disconnect from server now
    db.close()


def insert_into_db():
    # connect to database
    db = pymysql.connect(host="localhost", port=3406, user="root", passwd="public16", db="digib")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method

    # Create dataframe
    data = pd.DataFrame({
        'product': ['acid', 'growth formulas', 'cosmetics'],
        'sales': [29, 23, 27]
    })

    cols = "`,`".join([str(i) for i in data.columns.tolist()])
    for i, row in data.iterrows():
        try:
            sql_auto = "INSERT INTO `test` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
            cursor.execute(sql_auto, tuple(row))
            db.commit()

        except Exception as e:
            print(e)
            db.rollback()

    # disconnect from server now
    db.close()


if __name__ == "__main__":
    main()

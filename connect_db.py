import pymysql


def main():
    #fetch_from_db()
    insert_into_db()


def fetch_from_db():

    # connect to database
    db = pymysql.connect("35.190.197.53", "root", "public16", "digib")

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
    db = pymysql.connect("35.190.197.53", "root", "public16", "digib")

    # execute SQL query using execute() method.
    sql = """ INSERT INTO test (product, sales)
        VALUES ("solution",65), ("conditioner",78) """

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()

    except:
        # Rollback in case there is any error
        db.rollback()

    # disconnect from server now
    db.close()


if __name__ == "__main__":
    main()

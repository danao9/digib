import pymysql

if __name__ == "__main__":
    db = pymysql.connect("35.190.197.53", "root", "public16", "digib")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    sql0 = """SELECT * FROM test"""
    sql = """ INSERT INTO test (product, sales)
    VALUES ("shampoo",45), ("ariel",678) """

    # # Fetch a single row using fetchone() method.
    # data = cursor.fetchone()
    # print(data)

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()

    except:
        # Rollback in case there is any error
        db.rollback()

    # disconnect from server
    db.close()

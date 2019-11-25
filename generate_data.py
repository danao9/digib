# generate data for DigiB project
import random
import numpy as np
import pandas as pd
from faker import Faker
from sklearn.preprocessing import MinMaxScaler
import pymysql


def main():

    #PRODUCTS

    product_list = ["acetic","ammonium","barium","calcium","castor","dymethyl","ethoxy","formic acid","glycine","hexylene","isobtyl",'magnesium',"nitric acid","phosphoric acid","potassium nitrate","sodium bicarbonate","sodium chloride","sulphuric acid","titanium dioxide","zinc axide"]
    ID_product=[]
    price=[]
    for prod in product_list:
        ID_product.append("P"+str(random.randint(1000, 9000)))
        price.append(random.randint(150, 550))

    products={ "product_name": product_list,
               "ID_product": ID_product,
               "Available_in": ["bags" for _ in product_list],
               "Price_per_bag": price  }
    products_df=pd.DataFrame(products)





    #CUSTOMERS
    # create customer table: id_customer, name, address, #history_orders_current_tear, #history_amount, loyal
    size_cust = 150
    fake = Faker('nl_NL')
    customers = {'Name': [fake.name() for _ in range(size_cust)],
                 'City_NL': [fake.city() for _ in range(size_cust)],
                 'ID_customer': ["CUST" + str(random.randint(10000000, 90000000)) for _ in range(size_cust) ],
                 'history_orders_current_Y': [random.randint(0, 1000) for _ in range(size_cust)]}
    customers_df = pd.DataFrame(customers)

    # create promoter variable
    prom = np.array(customers_df["history_orders_current_Y"]).reshape(-1, 1) * 0.03
    scaler = MinMaxScaler(feature_range=(2, 10))
    scaler.fit(prom)
    promoter0 = scaler.transform(prom)
    promoter=[]
    for val in promoter0:
        if val >= 9:
            promoter.append("Promoter")
        elif val >= 7 and val <= 8:
            promoter.append("Passive")
        else:
            promoter.append("Detractor")
    customers_df['promoter_score'] = pd.DataFrame(promoter0)
    customers_df['promoter'] = pd.DataFrame(promoter)

    #create loyal variable
    loyal=["loyal" if val >350 else "new" for val in  np.array(customers_df["history_orders_current_Y"]) ]
    customers_df["loyal"]=pd.DataFrame(loyal)


    #ORDERS
    size_ord = 1000
    order_arr = []
    prod_arr = []
    price_arr = []
    quant_arr = []
    prod_val_arr = []
    customer_arr=[]
    ID_order = ["ORDER"+str(random.randint(1000000, 9000000)) for _ in range(size_ord)]
    for ord in ID_order:
        nr_pro = random.randint(1,15)
        customer = random.sample(list(customers_df["ID_customer"]), 1).pop()
        for prd in random.sample(product_list, nr_pro):
            order_arr.append(ord)
            customer_arr.append(customer)
            prod_arr.append(prd)
            price = products_df.loc[products_df["product_name"] == prd, "Price_per_bag"].values[0]
            price_arr.append(price)
            quant = random.randint(20, 100)
            quant_arr.append(quant)
            prod_val_arr.append(price*quant)
    orders = {"ID_order": order_arr,
              "ID_customer": customer_arr,
            "Product_name": prod_arr,
            "Price_per_bag": price_arr,
            "Quantity_product": quant_arr,
            "Total_price_product": prod_val_arr}
    orders_df = pd.DataFrame(orders)




    # connect to database
    db = pymysql.connect(host="localhost", port=3406, user="root", passwd="public16", db="digib")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()


    def load_data_cust(data):
        cols = "`,`".join([str(i) for i in data.columns.tolist()])
        for i, row in data.iterrows():
            try:
                sql_auto = "INSERT INTO `customers_df` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
                cursor.execute(sql_auto, tuple(row))
                db.commit()
            except Exception as e:
                print("customers: ",e)
                db.rollback()
    load_data_cust(customers_df)



    #products
    def load_data_prod(data):
        cols = "`,`".join([str(i) for i in data.columns.tolist()])
        for i, row in data.iterrows():
            try:
                sql_auto = "INSERT INTO `products_df` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
                cursor.execute(sql_auto, tuple(row))
                db.commit()
            except Exception as e:
                print("products: ",e)
                db.rollback()
    load_data_prod(products_df)


    #orders
    def load_data_ord(data):
        cols = "`,`".join([str(i) for i in data.columns.tolist()])
        for i, row in data.iterrows():
            try:
                sql_auto = "INSERT INTO `orders_df` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
                cursor.execute(sql_auto, tuple(row))
                db.commit()
            except Exception as e:
                print("orders: ", e)
                db.rollback()
    load_data_ord(orders_df)


    # disconnect from server now
    db.close()


if __name__ == "__main__":
    main()

# SQL
#
#  create table customers_df (
#  Name varchar(50) NOT NULL,
#  Address varchar (100),
#  ID_customer INT NOT NULL,
# history_orders_current_Y INT NOT NULL,
#  promoter FLOAT,
#  PRIMARY KEY (ID_customer) );

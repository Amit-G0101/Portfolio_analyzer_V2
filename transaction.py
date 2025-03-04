import mysql.connector
from userinput import Transaction,usr_input

def insert_into_db(transaction: Transaction):
    """Inserts a transaction record into the MySQL database."""
    con=None
    try:
        con=mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="amit",
            database="invest"
        )

        cursor=con.cursor()
        insrt_query="""Insert Into trnsc_fact (stock_id,broker_id ,trnsc_type,qty,price,tax_charg,
        trnsc_date,total_amount ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (
            transaction.stock_id, transaction.broker_id, transaction.trnsc_type,
            transaction.qty, transaction.price, transaction.tax_charg,
            transaction.trnsc_date, transaction.total_amount
        )
        #test_value=("101","111","BUY",12,20.20,100.11,"2024-01-01",200.100)
        cursor.execute(insrt_query,values)
        con.commit()
        print("\n✅ Transaction successfully inserted into MySQL database!")
    except mysql.connector.Error as e:
        print(f"❌ Database Error: {e}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()


def add_transaction():
    # get user_input and return all details in transaction object
    trnsc_ob=usr_input()


    # insert transaction data in MYSQL database
    insert_into_db(trnsc_ob)

# Test
#add_transaction()

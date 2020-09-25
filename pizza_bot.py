from flask import Flask, request, jsonify, make_response
# from mysql.connector import connect, errorcode, Error
import MySqlConnect as connect
import GenerateResponse as res


# import error as err


def ReturnConnectionError():
    return jsonify({"error_msg": "Connection error"})


def ReturnFetchError():
    return jsonify({"error_msg": "Unable to fetch data"})


'''def ConnectMySql():
    try:
        my_db = connect(
            host="localhost", user="root", password="password", database="mydatabase",
        )
        return my_db
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return False
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return False
        else:
            print(err)
            return False '''

app = Flask(__name__)


@app.route("/fetch", methods=["get", "post"])
def fetch():
    conn = connect.ConnectMySql()
    print(f"Connection status : {conn}")

    if conn is False:
        return ReturnConnectionError()
    else:
        try:
            cur = conn.cursor()
            print(f"Cursor object : {cur}")
            query = "select * from pizza"
            cur.execute(query)
            msg = "Data fetched successfully"
            return jsonify(
                {"fulfillmentMessages": [{"text": {"text": ["hello world"]}}]}
            )
        except Exception as e:
            print(e)
            return ReturnFetchError()
        finally:
            conn.close()


def json_extract(obj, key):
    arr = []

    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


def results():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    data = request.get_json(force=True)
    user_name = json_extract(data, 'name')
    user_address = json_extract(data, 'address')
    user_number = json_extract(data, 'mobile')
    conn = connect.ConnectMySql()
    cur = conn.cursor()
    user_name = str(user_name[0])
    user_address = str(user_address[0])
    user_number = str(user_number[0])
    print(user_number, user_address, user_name)
    query = "INSERT INTO pizzaOrder_customer_details (customer_name, mobile_number, Address) VALUES (%s,%s,%s); "
    string = (user_name, user_number, user_address)
    cur.execute(query, string)
    conn.commit()
    print(cur.rowcount, "is Inserted")
    cur.execute("SHOW tables;")
    for i in cur:
        print(i)
    get_order_id = "SELECT order_id FROM pizzaOrder_customer_details WHERE mobile_number = %s;"
    string = (user_number,)
    cur.execute(get_order_id, string)
    result_id = str(cur.fetchall())
    print(result_id)
    # order_id = cur.execute("SELECT order_id FROM pizzaOrder_customer_details WHERE mobile_number = user_number;")
    return {'fulfillmentText': 'Your Order id is ' + result_id + '...Thank you Mr.' + user_name + '..we will send your pizza to your mention [ ' + user_address + '] and  your mobile number is ' + user_number}


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))


if __name__ == "__main__":
    app.run(debug=True, port=80)

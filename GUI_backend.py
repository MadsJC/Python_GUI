import pandas as pd
import mysql.connector
import datetime as dt


def connect():
    mydb = mysql.connector.connect(
    host="phhw-140801.cust.powerhosting.dk",
    user="ruby-rejser_dk",
    passwd="Yg4M0w1g6mOKM3C2",
    database="ruby-rejser_dk")

SQL_command = "SELECT CONCAT('#',sales_order.increment_id) as 'increment_id', \
        fornavn.value as 'Fornavn', efternavn.value as 'Efternavn', \
        departure_date.value as 'Departure date', return_date.value as 'Return date', \
        rr_bookings_extra.frontend_label as 'Transfer type', rr_bookings_extra.extra_name as 'Rute', \
        sales_order_item.name as 'Opholdsnavn', sales_order_item.sku as 'Rejsekode', sales_order.status \
        FROM sales_order_item \
        INNER JOIN sales_order ON sales_order_item.order_id = sales_order.entity_id \
            AND sales_order.is_deleted = '0' \
            AND sales_order.status != 'canceled' \
        INNER JOIN rr_bookings_extra ON sales_order_item.order_id = rr_bookings_extra.order_id \
             AND rr_bookings_extra.frontend_label IN ('Transfer til Ile Rouse, Algajola og Calvi', 'Transfer', \
                                                      'Transfer til Ile Rousse, Algajola og Calvi') \
        LEFT JOIN rr_bookings_eav as fornavn ON sales_order_item.order_id = fornavn.order_id \
            AND REPLACE(fornavn.eav_code, 'g_fornavn','') = rr_bookings_extra.sub_group \
        LEFT JOIN rr_bookings_eav as efternavn ON sales_order_item.order_id = efternavn.order_id \
            AND REPLACE(efternavn.eav_code, 'g_efternavn','') = rr_bookings_extra.sub_group \
        LEFT JOIN rr_bookings_eav as departure_date ON sales_order_item.order_id = departure_date.order_id \
            AND departure_date.eav_code = 'departure_date' \
        LEFT JOIN rr_bookings_eav as return_date ON sales_order_item.order_id = return_date.order_id \
            AND return_date.eav_code = 'return_date' \
        WHERE sales_order_item.sku IN ('KO-01','KO-02', 'KO-03', 'KO-04', 'KO-05', 'KO-06',\
                                       'KO-07', 'KO-08', 'KO-09', 'KO-10', 'KBH-BASTIA') \
        GROUP BY rr_bookings_extra.order_id, rr_bookings_extra.sub_group \
        ORDER BY rr_bookings_extra.order_id DESC;"

def view():
    mydb = mysql.connector.connect(
    host="phhw-140801.cust.powerhosting.dk",
    user="ruby-rejser_dk",
    passwd="Yg4M0w1g6mOKM3C2",
    database="ruby-rejser_dk")
    mycursor = mydb.cursor()
    mycursor.execute(SQL_command)
    myresult = mycursor.fetchall()
    return myresult

def download():
    mydb = mysql.connector.connect(
    host="phhw-140801.cust.powerhosting.dk",
    user="ruby-rejser_dk",
    passwd="Yg4M0w1g6mOKM3C2",
    database="ruby-rejser_dk")
    mycursor = mydb.cursor()
    mycursor.execute(SQL_command)
    myresult = mycursor.fetchall()
    sql_data_download = pd.DataFrame(myresult, columns=('increment_id', 'Fornavn', 'Efternavn', 'Departure date', 'Return date', \
                                               'Transfer type', 'Rute', 'Opholdsnavn', 'Rejsekode', 'status'))
    today = dt.datetime.today().strftime('%d-%m-%Y')
    output_file = 'Transferliste_{}.csv'.format(today)
    csv = sql_data_download.to_csv(path_or_buf = output_file + '.csv', index = False)
    return csv

connect()
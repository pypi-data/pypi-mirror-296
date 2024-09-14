import pyodbc
import pandas as pd
import locale
from datetime import datetime

# sudo locale-gen es_ES.UTF-8 if error
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def get_conn(server, database, username, password):
    try:
        connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;"
        conn = pyodbc.connect(connection_string, timeout=30)
        cursor = conn.cursor()        

        print("Connection to SQL Server DB successful")
        return cursor, conn
    except Exception as e:
        print(e)
        return None, None

def close_connection(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.close()
        print("SQL Server connection is closed")

def extract_date_parts(datetime_str):
    if not datetime_str or pd.isnull(datetime_str):
        return None, None, None, None, None, None, None, None

    datetime_object = datetime_str
    year_month = datetime_object.strftime("%Y-%m")
    time = datetime_object.strftime("%H:%M:%S")

    return (
        datetime_object.date(),
        datetime_object.year,
        year_month,
        datetime_object.day,
        datetime_object.month,
        datetime_object.strftime("%A"),
        datetime_object.strftime("%B"),
        time,
    )

def get_raw_data(cursor, dateInit, dateEnd=None):
    if dateEnd is None:
        condition = f"CAST(t.dtDate AS DATE) = '{dateInit}'"
    else:
        condition = f"CAST(t.dtDate AS DATE) BETWEEN '{dateInit}' AND '{dateEnd}'"
    
    sql = f"""
    SELECT
	t.biTransactionID as order_id,
	t.dtDate as invoice_datetime,
	d.iItemID as product_id,
	i.vName as product_name,
	i.tiSubGroupID as product_hierarchy_id,
	ISNULL(g.vName, '') + ' - ' + ISNULL(sg.vName, '') AS product_category,
	d.mItemPrice as price,
	d.dQuantity as quantity,
	d.fDiscountPercentage * d.dQuantity * d.mItemPrice / 100 as discount,	
	d.dQuantity * d.mItemPrice * (100 - d.fDiscountPercentage) / 100 as paid,
	d.dQuantity * d.mItemPrice  * d.dTaxPercentage / 100 as tax
	FROM 
		T_TransactionOrderDetail d 
	LEFT JOIN 
		T_Transaction t 
	ON 
		d.biTransactionID = t.biTransactionID
	LEFT JOIN 
		T_Item i
	ON
		d.iItemID = i.iItemId
	LEFT JOIN
		T_Group g
	ON
		i.tiGroupID = g.tiGroupID
	LEFT JOIN
		T_SubGroup sg
	ON
		i.tiSubGroupID = sg.tiSubGroupID
	WHERE 
		t.tiTransactionTypeID = 5
	AND {condition}
	;
    """    

    product_sales = cursor.execute(sql).fetchall()
    
    sql2 = f"""
    SELECT
	foo3.biTransactionID as order_id,
	AVG(foo3.total) as total,
	AVG(foo3.taxes) as taxes,
	AVG(foo3.discounts) as discounts,
	MIN(foo3.date) as date,
	MIN(foo3.waiter_id) as waiter_id,
	MIN(foo3.table_id) as table_id,
	SUM(foo3.dCredit) as amount_total,
	SUM(foo3.mTip) as gratuity
	FROM
	(SELECT 
		foo2.biTransactionID, 
		foo2.total, 
		foo2.taxes,
		foo2.discounts,
		foo2.date,
		foo2.waiter_id,
		foo2.table_id,
		pd.dDebit, 
		pd.dCredit,
		pd.mTip 
	FROM 
		(SELECT 
			foo.biTransactionID, 
			SUM(foo.paid) as total, 
			SUM(foo.tax) as taxes,
			SUM(foo.discount) as discounts,
			MIN(foo.dtDate) as date,
			MAX(foo.biEmployeeID_Detail) as waiter_id,
			MIN(foo.tiTableID)	as table_id	
		FROM 
			(SELECT
				t.biTransactionID,
				t.dtDate,
				d.iItemID,
				i.vName as item,
				d.fDiscountPercentage * d.dQuantity * d.mItemPrice / 100 as discount,	
				d.dQuantity * d.mItemPrice * (100 - d.fDiscountPercentage) / 100 as paid,
				d.dQuantity * d.mItemPrice  * d.dTaxPercentage / 100 as tax,
				d.biEmployeeID_Detail,
				t.tiTableID
			FROM 
				T_TransactionOrderDetail d 
			LEFT JOIN 
				T_Transaction t 
			ON 
				d.biTransactionID = t.biTransactionID
			LEFT JOIN 
				T_Item i
			ON
				d.iItemID = i.iItemId
			WHERE 
				t.tiTransactionTypeID = 5 AND {condition}) as foo 
		GROUP BY foo.biTransactionID) as foo2
	LEFT JOIN
		T_PaymentDetail pd
	ON foo2.biTransactionID = pd.biTransactionID) as foo3
	GROUP BY foo3.biTransactionID
	;
    """
    
    sales = cursor.execute(sql2).fetchall()
    
    
    
    
    return product_sales, sales
    
    
def clean_data(product_sales, sales):
    df_product_sales = pd.DataFrame.from_records(
        product_sales,
        columns=[
            'order_id',
            'invoice_datetime',
            'product_id',
            'product_name',
            'product_hierarchy_id',
            'product_category',
            'price',
            'quantity',
            'discount',
            'paid',
            'tax'
        ]
    )
    
    df_product_sales[["date", "year", "yearmonth", "day", "month", "weekday", "monthstr", "hour"]] = (df_product_sales["invoice_datetime"].apply(lambda x: pd.Series(extract_date_parts(x))))
        
    df_product_sales['price'] = df_product_sales['price'].astype('float64')
    df_product_sales['quantity'] = df_product_sales['quantity'].astype('i')
    df_product_sales['discount'] = df_product_sales['discount'].astype('float64')
    df_product_sales['paid'] = df_product_sales['paid'].astype('float64')
    df_product_sales['tax'] = df_product_sales['tax'].astype('float64')
    

    df_sales = pd.DataFrame.from_records(
        sales,
        columns=[
            'order_id',
            'total',
            'taxes',
            'discounts',
            'invoice_datetime',
            'waiter_id',
            'table_id',
            'amount_total',
            'gratuity'
        ]
    )
    
    df_sales['amount_total'] = df_sales['amount_total'].astype('float64')
    df_sales['gratuity'] = df_sales['gratuity'].astype('float64')
    df_sales['taxes'] = df_sales['taxes'].astype('float64')
    
    df_sales[["date", "year", "yearmonth", "day", "month", "weekday", "monthstr", "hour"]] = (df_sales["invoice_datetime"].apply(lambda x: pd.Series(extract_date_parts(x))))
	
    
    return df_product_sales, df_sales
    

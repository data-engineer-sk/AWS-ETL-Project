import logging
import boto3
import pandas as pd
import numpy as np
import io

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
s3_client = boto3.client('s3')

headerList = ["Timestamp of Purchase", 
                    "Store Name", 
                    "Customer Name", 
                    "Basket Items (Name, Size & Price)", 
                    "Total Price", 
                    "Cash/Card", 
                    "Card Number (Empty if Cash)"]

def handler(event, context):
    LOGGER.info(f'Event structure: {event}')
    extract()
    transform()
    normalize_transaction()
    normalize_branch_sales()

def extract():
    response = s3_client.get_object(Bucket="deman4-group3", Key="chesterfield_07-12-2022_09-00-00.csv")
    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Successful S3 get_object response. Status - {status}")
        df = pd.read_csv(response.get("Body"))
        logging.info('dataframe head - {}'.format(df.head()))       
    else:
        print(f"Unsuccessful S3 get_object response. Status - {status}")

    with io.StringIO() as csv_buffer:
        df.to_csv(csv_buffer, header=headerList, index=False)
        response2 = s3_client.put_object(Bucket="deman4-group3", Key="extracted_chesterfield_07-12-2022.csv", Body=csv_buffer.getvalue())
    print("\nSuccessful\n")

def transform():
    response3 = s3_client.get_object(Bucket="deman4-group3", Key="extracted_chesterfield_07-12-2022.csv")
    df = pd.read_csv(response3.get("Body"))
    print('\nTransform Basket Item\n')
    to_drop = ["Customer Name", "Card Number (Empty if Cash)", "Store Name", "Total Price", "Cash/Card"]
    df.drop(columns=to_drop, inplace=True)
    df['Timestamp of Purchase'] = pd.to_datetime(df['Timestamp of Purchase'])

    df.index = np.arange(1, len(df) + 1)
    df = df.reset_index()
    df.rename(columns = {'index':'Customer_Id'}, inplace = True)
    df = df.set_index(['Customer_Id']).astype(str).apply(lambda x:x.str.split(',').explode()).reset_index()
    df = df.groupby(by=["Customer_Id","Basket Items (Name, Size & Price)"], as_index=False, dropna=False).count()\
        .rename(columns={"Timestamp of Purchase": "Quantity"})
    
    new = df["Basket Items (Name, Size & Price)"].str.split("-", n=2, expand = True)
    df["item_size_name"]= new[0]
    df["item_name_price"]= new[1]
    df["item_price"]= new[2]
    df.drop(columns =["Basket Items (Name, Size & Price)"], inplace = True)   
    new = df["item_size_name"].str.split(" ", n=2, expand = True)
    df["item_size"]= new[0]
    df["item_name2"]= new[1]
    df["item_name1"]= new[2]
    df.drop(columns =["item_size_name"], inplace = True)  
    df["item_price"].fillna(df.item_name_price, inplace = True)   
    df.loc[df["item_size"] == '', 'item_size'] = df['item_name2']   
    df["item_name"] = df["item_name2"] + ' ' + df["item_name1"] + df["item_name_price"]
    df.drop(columns =["item_name_price", "item_name1", "item_name2"], inplace = True)
    
    df["item_name"] = df["item_name"].str.replace('\d+', '')
    df["item_name"] = df["item_name"].str.replace('Regular+', '')
    df["item_name"] = df["item_name"].str.replace('Large+', '')
    df["item_name"] = df["item_name"].str.replace('\.', '')
    df["item_name"] = df["item_name"].str.strip(' ')
    df["item_price"] = df["item_price"].str.strip(' ')
    df.rename(columns = {'item_name':'Item_Name'}, inplace = True)
    df.rename(columns = {'item_size':'Item_Size'}, inplace = True)
    df.rename(columns = {'item_price':'Item_Price'}, inplace = True)
    df.rename(columns = {'Customer_Id':'Transaction_Id'}, inplace = True)
    df.rename(columns = {'Timestamp of Purchase':'Transaction_Date_Time'}, inplace = True)
    items_df = df.iloc[:, [0,4,3,2,1]]
    print(items_df.head(10))
    with io.StringIO() as csv_buffer:
        items_df.to_csv(csv_buffer, index=False)
        response1 = s3_client.put_object(Bucket="deman4-group3", Key="transformed/chesterfield_basket_items_07-12-2022.csv", Body=csv_buffer.getvalue())
    print("Uploaded Basket items")

def normalize_transaction():
    response3 = s3_client.get_object(Bucket="deman4-group3", Key="extracted_chesterfield_07-12-2022.csv")
    df = pd.read_csv(response3.get("Body"))
    print('\nNormalize Transaction\n')
    to_drop = ["Basket Items (Name, Size & Price)", "Customer Name", "Card Number (Empty if Cash)"]
    df.drop(columns=to_drop, inplace=True)
    df.index = np.arange(1, len(df) + 1)
    df = df.reset_index()
    df.rename(columns = {'index':'Transaction_Id'}, inplace = True)
    df.rename(columns = {'Cash/Card':'Payment_Type'}, inplace = True)
    df.rename(columns = {'Store Name':'Store_Name'}, inplace = True)
    df.rename(columns = {'Timestamp of Purchase':'Transaction_Date_Time'}, inplace = True)
    df.rename(columns = {'Total Price':'Total_Price'}, inplace = True)
    transaction_df = df.iloc[:, [0,1,2,3,4]]
    print(transaction_df.head(10))
    with io.StringIO() as csv_buffer:
        transaction_df.to_csv(csv_buffer, index=False)
        response2 = s3_client.put_object(Bucket="deman4-group3", Key="transformed/chesterfield_transaction_07-12-2022.csv", Body=csv_buffer.getvalue())
    print("Uploaded Transaction")

def normalize_branch_sales():
    response3 = s3_client.get_object(Bucket="deman4-group3", Key="extracted_chesterfield_07-12-2022.csv")
    df = pd.read_csv(response3.get("Body"))
    print('\nNormalize Branch Sales\n')
    to_drop = ["Basket Items (Name, Size & Price)", "Timestamp of Purchase", "Cash/Card", "Customer Name", "Card Number (Empty if Cash)"]
    df.drop(columns=to_drop, inplace=True)
    df.rename(columns = {'Store Name':'Store_Name'}, inplace = True)
    df.head()
    total_spend = df.groupby(['Store_Name']).sum().rename(columns={"Total Price": "Total_Spend"})
    total_spend
    avg_spend = df.groupby(['Store_Name']).mean().rename(columns={"Total Price": "Average_Spend"})
    avg_spend
    customer_spend = avg_spend.merge(total_spend, on='Store_Name')
    df_branch = customer_spend
    print(df_branch)
    with io.StringIO() as csv_buffer:
        df_branch.to_csv(csv_buffer, index=False)
        response3 = s3_client.put_object(Bucket="deman4-group3", Key="transformed/chesterfield_branch_sales_07-12-2022.csv", Body=csv_buffer.getvalue())
    print('Successfully Uploaded!')

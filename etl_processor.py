import argparse
import json
import re
import requests
import configparser
import mysql.connector


# https://docs.python.org/3/library/argparse.html
# https://docs.python.org/3/library/configparser.html
# https://docs.python-requests.org/en/latest/
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
# https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
# https://ridb.recreation.gov/docs
# https://ridb.recreation.gov/docs#/Campsites/getCampsites

config = configparser.ConfigParser()
parser = argparse.ArgumentParser(description='ETL')
parser.add_argument('config', type=str, help='configuration file')
parser.add_argument('--limit', type=str, help='api request limit')


def extract(api_key: str, limit: str = 10) -> dict:
    endpoint: str = "https://ridb.recreation.gov/api/v1"
    resources: str = f"/campsites?limit={limit}"

    r = requests.get(f"{endpoint}{resources}", headers={'apikey': api_key})
    print(r.status_code)
    
    response: dict = r.json()
    return response


class RECREATIONGOV_COLUMNS:
    CAMPSITEID: str = "CampsiteID"
    FACILITYID: str = "FacilityID"
    CAMPSITENAME: str = "CampsiteName"
    CAMPSITETYPE: str = "CampsiteType"
    TYPEOFUSE: str = "TypeOfUse"
    CAMPSITEACCESSIBLE: str = "CampsiteAccessible"
    CAMPSITERESERVABLE: str = "CampsiteReservable"
    CAMPSITELONGITUDE: str = "CampsiteLongitude"
    CAMPSITELATITUDE: str = "CampsiteLatitude"


def transform(data: dict) -> list:
    recdata: list = data['RECDATA']
    transformed_data: list = []

    for record in recdata:
        transformed_data.append({
                RECREATIONGOV_COLUMNS.CAMPSITEID: record[RECREATIONGOV_COLUMNS.CAMPSITEID],
                RECREATIONGOV_COLUMNS.FACILITYID: record[RECREATIONGOV_COLUMNS.FACILITYID],
                RECREATIONGOV_COLUMNS.CAMPSITENAME: record[RECREATIONGOV_COLUMNS.CAMPSITENAME],
                RECREATIONGOV_COLUMNS.CAMPSITETYPE: record[RECREATIONGOV_COLUMNS.CAMPSITETYPE],
                RECREATIONGOV_COLUMNS.TYPEOFUSE: record[RECREATIONGOV_COLUMNS.TYPEOFUSE],
                RECREATIONGOV_COLUMNS.CAMPSITEACCESSIBLE: record[RECREATIONGOV_COLUMNS.CAMPSITEACCESSIBLE],
                RECREATIONGOV_COLUMNS.CAMPSITERESERVABLE: record[RECREATIONGOV_COLUMNS.CAMPSITERESERVABLE],
                RECREATIONGOV_COLUMNS.CAMPSITELONGITUDE: record[RECREATIONGOV_COLUMNS.CAMPSITELONGITUDE],
                RECREATIONGOV_COLUMNS.CAMPSITELATITUDE: record[RECREATIONGOV_COLUMNS.CAMPSITELATITUDE]
            }
        )
    return transformed_data


class DESTINATION_COLUMNS:
    CAMPSITEID: str = "campsite_id"
    FACILITYID: str = "facility_id"
    CAMPSITENAME: str = "campsite_name"
    CAMPSITETYPE: str = "campsite_type"
    TYPEOFUSE: str = "type_of_use"
    CAMPSITEACCESSIBLE: str = "campsite_accessible"
    CAMPSITERESERVABLE: str = "campsite_reservable"
    CAMPSITELONGITUDE: str = "campsite_longitude"
    CAMPSITELATITUDE: str = "campsite_latitude"


def load(mysql_config: dict, data: list):
    rows_inserted: int = 0
    destination_table: str = "recreationgov_base_v1"
    destination_columns: str = f"{destination_table}\
        ({DESTINATION_COLUMNS.CAMPSITEID}, \
        {DESTINATION_COLUMNS.FACILITYID}, \
        {DESTINATION_COLUMNS.CAMPSITENAME}, \
        {DESTINATION_COLUMNS.CAMPSITETYPE}, \
        {DESTINATION_COLUMNS.TYPEOFUSE}, \
        {DESTINATION_COLUMNS.CAMPSITEACCESSIBLE}, \
        {DESTINATION_COLUMNS.CAMPSITERESERVABLE}, \
        {DESTINATION_COLUMNS.CAMPSITELONGITUDE}, \
        {DESTINATION_COLUMNS.CAMPSITELATITUDE})"

    db = mysql.connector.connect(
        host=mysql_config['host'],
        user=mysql_config['user'],
        port=mysql_config['port'],
        password=mysql_config['password'],
        database=mysql_config['database']
    )
    cursor = db.cursor()

    sql: str = re.sub('\s+',' ',"INSERT INTO " + destination_columns + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    for record in data:
        values: tuple = tuple([x for x in record.values()])
        cursor.execute(sql, values)
        rows_inserted = cursor.rowcount + rows_inserted

    print(f"ROWS INSERTED: {rows_inserted}")    
    db.commit()


def etl(api_key: str,
        limit: str,
        mysql_config: dict):

    extracted_recreation_data: dict = extract(
        api_key=api_key,
        limit=limit
    )
    
    transformed_data_to_load: list = transform(data=extracted_recreation_data)
    
    load(
        mysql_config=mysql_config,
        data=transformed_data_to_load
    )


if __name__ == '__main__':
    args = parser.parse_args()
    config_file: str = args.config
    limit: str = None
    if args.limit:
        limit = args.limit
    else:
        limit = 10

    config.read(config_file)
    api_key: str = config['api']['key']
    mysql_config: dict = config['mysql']


    etl(
        api_key=api_key,
        limit=limit,
        mysql_config=mysql_config
    )
import requests
import json
import datetime
from connect import create_connection

conn = create_connection()
cursor = conn.cursor()


def get_items_to_scrape():
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return items


def get_price(item):
    item_id = item[0]
    url = item[1]
    html_target = item[2]
    html_identifier = item[3]
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

    r = requests.get(url, headers=headers)

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(r.content, features="html.parser")
    find = soup.find(id=html_identifier)
    price = json.loads(find.contents[0])['offers']['price']
    save_price(item_id, price)


def save_price(item_id, price):
    print_date = datetime.datetime.now()
    stmt = "INSERT INTO prices (itemId, date, price) VALUES (?, ?, ?)"
    data = (item_id, print_date, price)
    # cursor.execute(stmt, data)
    # conn.commit()


def compare_price(item):
    item_id = item[0]
    stmt = "SELECT price, date FROM prices WHERE itemId =:item_id ORDER BY date DESC LIMIT 2"
    data = {"item_id": item_id}
    cursor.execute(stmt, data)
    prices = cursor.fetchall()
    new_price = prices[0][0]
    old_price = prices[1][0]

    if new_price < old_price:
        print("Price Reduction")
    else:
        print("Price is the same or is higher")


def run():
    items = get_items_to_scrape()
    for item in items:
        get_price(item)
        compare_price(item)


run()

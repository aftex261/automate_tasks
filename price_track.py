# Two step verification required to be off and access to less secure apps should be on.
import requests
from bs4 import BeautifulSoup as bsoup
import smtplib
import time

# set the headers and user string
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
}

# send a request to fetch HTML of the page
action = requests.get('https://www.amazon.in/Apple-Watch-GPS-Cellular-44mm/dp/B07XWYCMQH/ref=sr_1_5'
                      '?crid=3DQZJI5SU8QSC&keywords=apple+watch+series+5&qid=1582128469&sprefix=apple%2Caps%2C368&sr=8-5'
    , headers=headers)

soup = bsoup(action.content, 'html.parser')

# change the encoding to utf-8
soup.encode('utf-8')


# function to check if the price has dropped below 60,000
def check_price():
    heading = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text().replace(',', '').replace('₹', '').replace(' ', '').strip()
    # print(price)

    # converting the string amount to float
    converted_price = float(price[0:5])
    print(converted_price)
    if converted_price < 60000:
        send_mail()

    # using strip to remove extra spaces in the title
    print(heading.strip())


# function that sends an email if the prices fell down
def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('gmail_id', 'password')

    subject = 'Price Fell Down'
    body = "Check the amazon link " \
           ":https://www.amazon.in/Apple-Watch-GPS-Cellular-44mm/dp/B07XWYCMQH/ref=sr_1_5" \
           "?crid=3DQZJI5SU8QSC&keywords=apple+watch+series+5&qid=1582128469&sprefix=apple%2Caps%2C368&sr=8-5"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'sender_email_id',
        'reciever_email_id',
        msg
    )
    # print a message to check if the email has been sent
    print('Hey Email has been sent')
    # quit the server
    server.quit()

# loop that allows the program to regularly check for prices
while True:
    check_price()
    time.sleep(60*60)


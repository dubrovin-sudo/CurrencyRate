import requests
from bs4 import BeautifulSoup
import time
import smtplib



class Currency:
    DOLLAR_RUB = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%9A%D0%A3%D0%A0%D0%A1+%D0%94%D0%9E%D0%9B%D0%9B%D0%90%D0%A0%D0%90+&aqs=chrome.1.0i271j0i512j69i57j0i512l7.8350j1j7&sourceid=chrome&ie=UTF-8'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

    current_converted_price = 0
    difference = 5

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price())

    def get_currency_price(self):
        full_page = requests.get(self.DOLLAR_RUB, headers=self.headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.findAll('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})
        return convert[0].text.replace(',', '.')

    def check_currency(self):
        currency = float(self.get_currency_price())
        if currency >= self.current_converted_price + self.difference:
            print('Курс сильно вырос, может пора что-то сделать?')
            # self.send_email()
        elif currency <= self.current_converted_price - self.difference:
            print('Курс сильно упал, может пора что-то сделать?')
            # self.send_email()
        print('Сейчас курс: 1 доллар=' + str(currency))
        time.sleep(3)
        self.check_currency()

    def send_email(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('name', 'login')

        subject = 'Курс валют'
        body = 'Курс доллара изменился!'
        message = f'Subject: {subject}\n\n{body}'

        server.sendmail(
            'admin@itproger.com',
            'xxxxx@gmail.com',
            message
        )
        server.quit()


if __name__ == '__main__':
    currency = Currency()
    currency.check_currency()



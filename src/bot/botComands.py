from telebot import types
import requests
from bs4 import BeautifulSoup

def start_command():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Погода', callback_data='weather'))
    markup.add(types.InlineKeyboardButton('Цены валют', callback_data='currency'))
    return markup

def cur():
    def get_currency(cur_name):
        pos = requests.get("https://www.cbr.ru/currency_base/daily/")
        soup = BeautifulSoup(pos.text, "html.parser")
        
        currency = soup.find("td", string=lambda text: cur_name in text)
        
        if currency :
            row = currency.find_parent('tr')
            if row:
                cells = row.find_all("td")
                if len(cells)>=5:
                    return{
                        "code_currency": cells[0].get_text(strip=True),
                        "code": cells[1].get_text(strip=True),
                        "name": cells[3].get_text(strip=True),
                        "rate": cells[4].get_text(strip=True)
                    }
        return None

    ctf = ["Доллар США", "Евро", "Тенге"]
    result = []

    for cur_name in ctf:
        rate_data = get_currency(cur_name)
        if rate_data:
            result.append(f"   {rate_data['name']} — {rate_data['rate']} руб.")
            
    return '\n \n'.join(result)
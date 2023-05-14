# მაგალითი_1


class Disease:
    def __init__(self, ID, disease):
        self.ID = ID
        self.disease = disease

    def __str__(self):
        return f"აიდი: {self.ID}, დაავადება: {self.disease}"


class Doctor:
    def __init__(self, doctor, department, patient=[]):
        self.doctor = doctor
        self.department = department
        self.patients = patient

    def __str__(self):
        return f"ექიმი: {self.doctor}, დეპარტამენტი: {self.department}, პაციენტები: {','.join(self.patients[0:-1])}"


class Patient:
    def __init__(self, personal_number, name, disease=[], doctor=None):
        self.personal_number = personal_number
        self.name = name
        self.diseases = disease
        self.doctor = doctor

    def __str__(self):
        return f"ფაციენტის პირადი ნომერი: {self.personal_number}, სახელი: {self.name}, დაავადება: {','.join(self.diseases[0:-1])}, ექიმი: {self.doctor}"

    def diagnose(self, disease, doctor=None):
        self.diseases.append(disease.disease)
        if doctor is not None:
            if len(doctor.patients) < 20:
                doctor.patients.append(doctor.patients)
                doctor.patient = self
                self.doctor = doctor.doctor
        else:
            return "ექიმის მიმაგრება ვერ მოხდება"

disease1 = Disease(7, "არითმია")
disease2 = Disease(2, "თავის ტკივილი")

doctor1 = Doctor("მანერგო", "სკოლის ექიმი", ['პაციენტი1', 'პაციენტი2'])
doctor2 = Doctor("ვაჟა", "კარდიოლოგი")

patient1 = Patient('62...8', "დავითი", ['დაავადება1', 'დაავადება2'])
patient2 = Patient("51...1", "თამარი")

patient1.diagnose(disease1, doctor1)
patient2.diagnose(disease2, doctor2)

print('\n', disease1, '\n', disease2, '\n', doctor1, '\n', doctor2, '\n', patient1, '\n', patient2)

# მაგალითი_2


import requests
import sqlite3
from bs4 import BeautifulSoup
from prettytable import PrettyTable

conn = sqlite3.connect('Crypto.sqlite')
cursor = conn.cursor()
conn.execute('''CREATE TABLE cryptomarket
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            crypto_name VARCAR(30),
            price VARCHAR(30),
            change VARCHAR(30),
            percent_change VARCHAR(30),
            market_cap VARCHAR(30));
            ''')


def parsing(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('body')
    app = body.find('div', id='app')
    render = app.find('div', id='render-target-default')
    margin = render.find('div', style='margin-top:175px')
    lead = margin.find('div', id='YDC-Lead')
    stack = lead.find('div', id='YDC-Lead-Stack')
    composite = stack.find('div', id='YDC-Lead-Stack-Composite')
    screener = composite.find('div', id='mrt-node-Lead-5-ScreenerResults')
    proxy = screener.find('div', id='Lead-5-ScreenerResults-Proxy')
    section = proxy.find('section', id='screener-results')
    fin = section.find('div', id='fin-scr-res-table')
    res = fin.find('div', id='scr-res-table')
    ovx = res.find('div', {'class': 'Ovx(a) Ovx(h)--print Ovy(h) W(100%)'})
    w_100 = ovx.find('table')
    tbody = w_100.find('tbody')
    all_data = tbody.find_all('tr')
    ls = []
    for i in all_data:
        crypto_name = i.find('td',
                             {'aria-label': 'Name'}).text
        price = i.find('td',
                       {'aria-label': 'Price (Intraday)'}).text
        change = i.find('td',
                        {'aria-label': 'Change'}).text
        percent_change = i.find('td',
                                {'aria-label': '% Change'}).text
        market_cap = i.find('td',
                            {'aria-label': 'Market Cap'}).text
        taply = (crypto_name, price, change, percent_change, market_cap)
        ls.append(taply)
    cursor.executemany("INSERT INTO cryptomarket(crypto_name, price, change, percent_change, market_cap) VALUES (?,?,?,?,?)", ls)


def formatting():
    info = cursor.execute('SELECT * FROM cryptomarket')
    ls = []
    headers = PrettyTable(['id','crypto_name', 'price', 'change', 'percent_change', 'market_cap'])
    for i in info:
        ls.append(list(i))
    for row in ls:
        headers.add_row(row)
    print(headers)


def main():
    parsing('https://finance.yahoo.com/crypto/')
    formatting()
    conn.commit()
    conn.close()


main()

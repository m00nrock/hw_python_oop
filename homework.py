import datetime as dt

date_format = '%d.%m.%Y'


class Record():
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        day_stats = 0
        for i in self.records:
            if i.date == dt.datetime.now().date():
                day_stats += i.amount
        return day_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.date.today()
        last_week = today - dt.timedelta(days=7)
        for i in self.records:
            if last_week <= i.date <= today:
                week_stats += i.amount
        return week_stats

    def balance(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories = self.balance()
        if calories <= 0:
            return "Хватит есть!"
        else:
            return ("Сегодня можно съесть что-нибудь ещё, "
                    f"но с общей калорийностью не более {calories} кКал")


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    EURO_RATE = 70.01
    USD_RATE = 60.01
    CURRENCIES = {
        'rub': ('руб', RUB_RATE),
        'eur': ('Euro', EURO_RATE),
        'usd': ('USD', USD_RATE)
    }

    def get_today_cash_remained(self, currency):
        free_cash = self.balance()
        currency_name, rate = self.CURRENCIES[currency]
        free_cash_currency = round(free_cash / rate, 2)
        if free_cash == 0:
            return "Денег нет, держись"
        elif free_cash > 0:
            return ("На сегодня "
                    f"осталось {abs(free_cash_currency)} {currency_name}")
        else:
            return ("Денег нет, держись: "
                    f"твой долг - {abs(free_cash_currency)} {currency_name}")

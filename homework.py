import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Record():
    def __init__(self, amount, comment, date=None) -> None:
        """Примет запись с указанными параметрами."""
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class Calculator:
    def __init__(self, limit: float) -> None:
        """Объявляет список записей и лимит."""
        self.limit = limit
        self.records = []

    def add_record(self, record: str) -> None:
        """Добавляет запись в список."""
        self.records.append(record)

    def get_today_stats(self) -> float:
        """Возвращает статистику за текущий день."""
        return sum(i.amount for i in self.records
                   if i.date == dt.date.today())

    def get_week_stats(self) -> float:
        """Возвращает статистику за неделю."""
        today = dt.date.today()
        last_week = today - dt.timedelta(days=7)
        return sum(i.amount for i in self.records
                   if last_week <= i.date <= today)

    def balance(self) -> float:
        """Возвращает свободный баланс."""
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    NO_CALORIES = "Хватит есть!"
    FREE_CALORIES = ("Сегодня можно съесть что-нибудь ещё, но с общей "
                     "калорийностью не более {calories} кКал")

    def get_calories_remained(self) -> str:
        """Считает можно ли получить ещё калорий и сколько."""
        calories = self.balance()
        if calories <= 0:
            return self.NO_CALORIES
        return self.FREE_CALORIES.format(calories=calories)


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    EURO_RATE = 70.01
    USD_RATE = 60.01
    CURRENCIES = {
        'rub': ('руб', RUB_RATE),
        'eur': ('Euro', EURO_RATE),
        'usd': ('USD', USD_RATE)
    }

    NO_MONEY = "Денег нет, держись"
    FREE_MONEY = "На сегодня осталось {money} {currency_name}"
    DEBT_MONEY = "Денег нет, держись: твой долг - {money} {currency_name}"
    NO_COMPATIBLE = ("Валюта {currency} не поддерживается. "
                     "Поддерживаемые валюты: {values}")

    def get_today_cash_remained(self, currency: str) -> str:
        """
        Считает сколько потрачено денег и возвращает один из трёх результатов.
        """
        if currency not in self.CURRENCIES:
            raise ValueError(
                self.NO_COMPATIBLE.format(
                    currency=currency,
                    values=', '.join(list(self.CURRENCIES.keys()))))

        free_cash = self.balance()
        currency_name, rate = self.CURRENCIES[currency]
        free_cash_currency = round(free_cash / rate, 2)

        if free_cash == 0:
            return self.NO_MONEY
        elif free_cash > 0:
            return self.FREE_MONEY.format(money=abs(free_cash_currency),
                                          currency_name=currency_name)
        else:
            return self.DEBT_MONEY.format(money=abs(free_cash_currency),
                                          currency_name=currency_name)

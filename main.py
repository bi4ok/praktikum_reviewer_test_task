import datetime as dt


class Record:
    # TODO К классу и методам, здесь и ниже, нужно добавить описание
    # TODO использовать для этого стоит докстринги
    # TODO В описании стоит указать общее назначение класса/метода
    # TODO А так же описать данные с которым работает объект.
    # TODO Проще говоря указать что объект ожидает получить на вход
    # TODO и что вернет на выходе.
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        # TODO сработает задумка верно, но было бы здорово записать её попроще
        # self.date = (<вариант-1> if <условие>
        #              else <вариант-2>)
        # TODO Таким образом у нас будет в целом меньше строк
        # TODO И при этом каждая строка будет соответствовать одному варианту
        # TODO Читать такой код будет легче
        self.comment = comment

    # TODO Если на данном этапе пройдены темы геттеров/сеттеров
    # TODO то стоит создать их здесь, указав на важность инкапсуляции


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        # TODO Если мы договорились работать только с записями типа Record
        # TODO то тут стоит выполнить проверку типа входящего объекта
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:
            # TODO по соглашению о стиле кода переменные нужно называть
            # TODO согласно стилю snake_case (по самому названию уже
            # TODO видны главные отличия - все буквы маленькие, а вместо
            # TODO пробелов используется символ "_")
            # TODO Исключениями могут быть константы, название которых
            # TODO полностью состоит из больших букв.
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
                # TODO в таких случаях удобно использовать вместо обычной
                # TODO операции сложения операцию +=
                # a = a + b --> a += b
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # TODO В записи условия ниже есть пара недостатков
            # TODO 1) когда нам надо проверить, что число лежит в неком
            #  диапазоне - мы можем использовать запись вида 1 < x < 10
            #  в этом случае я проверяю, что x одновременно (AND) больше 1 и
            #  меньше 10
            # TODO 2) В нашем случае PEP8 позволяет выполнить запись без
            #  дополнительных отступов (и скобок, если мы сократим условие)
            #  Примеры можно найти тут:
            #  https://www.python.org/dev/peps/pep-0008/#indentation
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # TODO Лучше создать полноценный комментарий через docstring
        x = self.limit - self.get_today_stats()
        # TODO х - плохой пример нэйминга
        # TODO попробуйте придумать полезное название, которое будет
        #  отражать смысл этой переменной (тех данных на которые она будет
        #  указывать)
        if x > 0:
            # TODO Не стоит применять \ для переноса
            # TODO Как вариант - можно использовать (), которые помогут
            #  пайтону понять, что эта строка продолжается на следующей
            # Пример: (f'Как прекрсано жить в мире '
            #          f'с красивыми переносами')
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')  # TODO Здесь можно обойтись без скобок


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # TODO Нет необходимости в создании параметров USD_RATE и EURO_RATE
        # TODO Вы можете обратиться к этим значениям через self
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00  # TODO у данной операции не будет эффекта
            # TODO (== - оператор сравнения, а результат сравнения вы нигде
            #  не используете). В целом эту операцию можно убрать.
            currency_type = 'руб'
        # TODO Кстати если курсов валют будет больше - можно задуматься над
        #  составлением словаря с курсами (в нём можно будет хранить
        #  дополнительную информацию по каждому курсу и получать её по ключу
        #  вместо написания множества if/elif/else конструкций
        # TODO примеры можно найти тут
        # TODO https://medium.com/swlh/3-alternatives-to-if-statements-to-make-your-python-code-more-readable-91a9991fb353
        # TODO А если тема интересна - можно ещё почитать про match/case
        #  конструкцию, которую ещё совсем недавно добавили в пайтон
        # TODO https://habr.com/ru/post/585216/
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
            # TODO Вместо переноса с \ - попробуйте использовать
            #   перенос при помощи скобок (), как я показывал это выше

    def get_week_stats(self):
        super().get_week_stats()
        # TODO Тут есть пара интересных моментов
        # TODO 1) Нам в целом нет нужды переопределять метод, если мы не
        #  хотим добавить в него какую-то дополнительную логику или изменить
        #  текущую
        # TODO 2) super().get_week_stats() по сути вызовет срабатывание
        #  родительского метода в данной строке, но как мы поступим с тем,
        #  что вернёт этот самый метод после работы? Т.к. return-а здесь
        #  нет, то метод всегда будет возвращать None, хоть при этом и будут
        #  выполнены все необходимые расчёты. Т.е. мы просто заставим пайтон
        #  сработать в холостую

# TODO Хоть замечаний и много, но большая их часть относится к стилю кода
# TODO Со временем вы привыкните и будете писать красивый код на автомате)
# TODO А сейчас вы уже неплохо постарались, т.к. основная логика расчётов
#  работает корректно!
import aiosqlite
import aiohttp
import logging

from dataclasses import dataclass
from typing import Optional, Union

from aiogram.utils.formatting import Bold, as_key_value, as_list, as_marked_section
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _

from core.const import CALC_DB_FILE
from bs4 import BeautifulSoup


geos = (
    ("Австралия", 5),
    ("Австрия", 3),
    ("Азербайджан", 2),
    ("Албания", 3),
    ("Алжир", 5),
    ("Ангилья", 5),
    ("Ангола", 5),
    ("Антигуа-Барбуда", 5),
    ("Антиллы нидерландские", 5),
    ("Аргентина", 5),
    ("Армения", 3),
    ("Аруба", 5),
   ("Афганистан", 4),
    ("Грузия", 3),
    ("Дания", 3),
    ("Джибути", 5),
    ("Доминика", 5),
    ("Доминиканская Республика", 5),
    ("Египет", 5),
    ("Замбия", 5),
    ("Зимбабве", 5),
    ("Йемен", 3),
    ("Израиль", 3),
    ("Индия", 3),
    ("Индонезия", 5),
    ("Иордания", 3),
    ("Малави", 5),
    ("Малайзия", 5),
    ("Мали", 5),
    ("Мальдивы", 5),
    ("Мальта", 3),
    ("Марокко", 5),
    ("Мартиника", 5),
    ("Мексика", 5),
    ("Мозамбик", 5),
    ("Молдова", 2),
    ("Монголия", 3),
    ("Монтсеррат", 5),
    ("Мьянма (Бирма)", 4),
    ("Сент-Винсент и гренадины", 5),
    ("Сент-Люсия", 5),
    ("Сербия", 3),
    ("Сингапур", 5),
    ("Сирия", 3),
    ("Словакия", 3),
    ("Словения", 3),
    ("Сомали", 5),
    ("Судан", 5),
    ("Суринам", 5),
    ("США", 4),
    ("Сьерра-Леоне", 5),
    ("Таджикистан", 1),
    ("Багамы", 5),
    ("Бангладеш", 4),
    ("Барбадос", 5),
    ("Бахрейн", 3),
    ("Беларусь", 2),
    ("Белиз", 5),
    ("Бельгия", 3),
    ("Бенин", 5),
    ("Бермуды", 5),
    ("Болгария", 3),
    ("Боливия", 5),
    ("Босния-Герцеговина", 3),
    ("Ботсвана", 5),
    ("Бразилия", 5),
    ("Бруней", 5),
    ("Буркина-Фасо", 5),
    ("Бурунди", 5),
    ("Бутан", 4),
    ("Вануату", 5),
    ("Ватикан", 3),
    ("Великобритания", 3),
    ("Венгрия", 3),
    ("Венесуэла", 5),
    ("Виргиния британская", 5),
    ("Вьетнам", 4),
    ("Габон", 5),
    ("Гайана", 5),
    ("Гайана Французская", 5),
    ("Гаити", 5),
    ("Гамбия", 5),
    ("Гана", 5),
    ("Гваделупа", 5),
    ("Гватемала", 5),
    ("Гвинея", 5),
    ("Гвинея-Бисау", 5),
    ("Германия", 3),
    ("Гибралтар", 3),
    ("Гондурас", 5),
    ("Гонконг (Китай)", 4),
    ("Гренада", 5),
    ("Греция", 3),
    ("Ирак", 3),
    ("Иран", 3),
    ("Ирландия", 3),
    ("Исландия", 3),
    ("Испания", 3),
    ("Италия", 3),
    ("Кабо-Верде", 5),
    ("Кайманы", 5),
    ("Камбоджа", 4),
    ("Камерун", 5),
    ("Канада", 4),
    ("Катар", 3),
    ("Кения", 5),
    ("Кипр", 3),
    ("Кирибати", 5),
    ("Китай", 3),
    ("Колумбия", 5),
    ("Конго", 5),
    ("Конго (дР)", 5),
    ("Корея северная", 3),
    ("Корея южная", 3),
    ("Коста-Рика", 5),
    ("Кот дИвуар", 5),
    ("Куба", 5),
    ("Кувейт", 3),
    ("Кыргызстан", 1),
    ("Кюрасао", 5),
    ("Лаос", 4),
    ("Латвия", 3),
    ("Лесото", 5),
    ("Либерия", 5),
    ("Ливан", 3),
    ("Ливия", 5),
    ("Литва", 3),
    ("Люксембург", 3),
    ("Маврикий", 5),
    ("Мавритания", 5),
    ("Мадагаскар", 5),
    ("Майотта", 5),
    ("Макао (Китай)", 4),
    ("Македония", 3),
    ("Намибия", 5),
    ("Науру", 5),
    ("Непал", 3),
    ("Нигер", 5),
    ("Нигерия", 5),
    ("Нидерланды", 3),
    ("Никарагуа", 5),
    ("Новая Зеландия", 5),
    ("Новая Каледония", 5),
    ("Норвегия", 3),
    ("о.Вознесения", 5),
    ("о.Коморские", 5),
    ("о.Св.Елены", 5),
    ("о.Соломоновы", 5),
    ("ОАЭ", 3),
    ("о-ва Аландские", 3),
    ("Оман", 3),
    ("Пакистан", 4),
    ("Палестина", 3),
    ("Панама", 5),
    ("Папуа-Новая гвинея", 5),
    ("Парагвай", 5),
    ("Перу", 5),
    ("Питкэрн", 5),
    ("Полинезия французкая", 5),
    ("Польша", 3),
    ("Португалия", 3),
    ("Реюньон", 5),
    ("Россия", 2),
    ("Руанда", 5),
    ("Румыния", 3),
    ("Сальвадор", 5),
    ("Самоа", 5),
    ("Сан-Томе и Принсипи", 5),
    ("Саудовская Аравия", 3),
    ("Свазиленд", 5),
    ("Сейшелы", 5),
    ("Сенегал", 5),
    ("Сен-Мартен", 5),
    ("Сен-Пьер и Микелон", 5),
    ("Сент Китс", 5),
    ("Таиланд", 4),
    ("Танзания", 5),
    ("Тимор-Лешти", 5),
    ("Того", 5),
    ("Тонга", 5),
    ("Тринид и Тобаго", 5),
    ("Тристан да Кунья", 5),
    ("Тувалу", 5),
    ("Тунис", 5),
    ("Туркменистан", 1),
    ("Туркс и Кайкос", 5),
    ("Турция", 3),
    ("Уганда", 5),
    ("Узбекистан", 1),
    ("Украина", 2),
    ("Уоллис и Футуна", 5),
    ("Уругвай", 5),
    ("Фиджи", 5),
    ("Филиппины", 5),
    ("Финляндия", 3),
    ("Фолклендские о.", 5),
    ("Франция", 3),
    ("Хорватия", 3),
    ("ЦАР", 5),
    ("Чад", 5),
    ("Черногория", 3),
    ("Чехия", 3),
    ("Чили", 5),
    ("Чили -о.Пасхи", 5),
    ("Швейцария", 3),
    ("Швеция", 3),
    ("Шри-ланка", 5),
    ("Эквадор", 5),
    ("Экваториальная гвинея", 5),
    ("Эритрея", 5),
    ("Эстония", 3),
    ("Эфиопия", 5),
    ("ЮАР", 5),
    ("Южный Судан", 5),
    ("Ямайка", 5),
    ("Япония", 3),
)
g = [x[0] for x in geos]
res = [g[x:] for x in range(0, len(g), 50)]
good = [res[x][:50] for x in range(len(res))]

first = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000]
second = [10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 75000, 80000, 85000, 90000, 95000, 100000]
third = [100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 550000, 600000, 650000, 700000, 750000, 850000, 900000, 950000, 1000000]
four = [1000000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000, 4500000, 5000000, 5500000, 6000000, 6500000, 7000000, 7500000, 8000000, 8500000, 9000000, 9500000, 10000000]
item_prices = [first, second ,third, four]


@dataclass
class Category():
    category_name: str # Имя категории
    category_number: int # Номер категории
    percent: Union[int, float] # Процент за категорию
    sub_procent: Optional[Union[int, float]] = None # Процент за категорию если превышает сумму
    international_fee: Union[int, float] = 1.3 # Международный сбор
    final_coast_fee: Union[int, float] = 0.40 # Окончательный сбор с товара
    vat_fee: Union[int, float] = 12 # НДС

    def calc(self, item_price: Union[int, float], threeshold: Optional[Union[int, float]] = None):
        if threeshold:
            if item_price < threeshold:
                category_fee = item_price / 100 * self.percent
                international_fee = item_price / 100 * self.international_fee
                final_coast_fee = self.final_coast_fee
                vat = (category_fee + international_fee + final_coast_fee) / 100 * self.vat_fee
                result = category_fee + international_fee + vat
                return round(float(result), 2)
            else:
                category_fee = item_price / 100 * self.percent
                sub_category_fee = item_price / 100 * self.sub_procent
                international_fee = item_price / 100 * self.international_fee
                final_coast_fee = self.final_coast_fee
                vat = (category_fee + international_fee + final_coast_fee) / 100 * self.vat_fee
                result = category_fee + sub_category_fee + international_fee + vat
                return round(result, 2)
        else:
            category_fee = item_price / 100 * self.percent
            international_fee = item_price / 100 * self.international_fee
            final_coast_fee = self.final_coast_fee
            vat = (category_fee + international_fee + final_coast_fee) / 100 * self.vat_fee
            result = category_fee + international_fee + vat
            return round(result, 2)


most_category = Category(
    category_name="Большинство категорий",
    category_number=1,
    percent=13.25,
    sub_procent=2.35
)

book = Category(
    category_name="Книги и журналы",
    category_number=2,
    percent=14.95,
    sub_procent=2.25
)

coins_and_papers = Category(
    category_name="Монеты, банкноты, слитки",
    category_number=3,
    percent=13.25,
    sub_procent=7
)

clothing = Category(
    category_name="Одежда, обувь и аксессуары",
    category_number=4,
    percent=15,
    sub_procent=9
)

jewerly_and_watches = Category(
    category_name="Украшения и часы",
    category_number=5,
    percent=15,
    sub_procent=9
)

jewerly_and_watches_and_parts = Category(
    category_name="Часы, запчасти и аксессуары",
    category_number=6,
    percent=15,
    sub_procent=6.5
)

nft = Category(
    category_name="Искусство NFT",
    category_number=7,
    percent=5
)

buisness_and_industry = Category(
    category_name="Отдельные подкатегории в Бизнес и промышленность",
    category_number=8,
    percent=3,
    sub_procent=0.5
)

musical_gear = Category(
    category_name="Музыкальные инструменты",
    category_number=9,
    percent=6.35,
    sub_procent=2.35
)

other_category = Category(
    category_name="Отдельные подкатегории в Одежда, обувь и аксессуары",
    category_number=10,
    percent=13.25,
    sub_procent=8
)


async def parse() -> Union[int, float]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://mig.kz/') as res:
                html = await res.text()
                soap = BeautifulSoup(html, "lxml")
                el = soap.find('div', class_='col-xs-12 col-sm-4 col-sm-push-4')
                table = el.find_next('tr').text.split('\n')
                nice = [x for x in table if x != '']
                last_el = float(nice[-1])
                return round(last_el, 2) if last_el else 450
        except Exception as e:
            logging.exception(e)
            return 450
        

async def get_data_from_finish_state(
    geo: str, 
    transport_type: str, 
    category_number: int, 
    item_weight: int, 
    item_price: int):

    usd = await parse()

    shipping_price = 0
    ttype = 'Наземным транспортом' if transport_type == 'combined' else 'Воздушным транспортом'
    category_name = ''

    async with aiosqlite.connect(CALC_DB_FILE) as db:
        cursor = await db.cursor()

        if item_weight > 10:
            query1 = f"""
            select * from countries, logistic
            where name == '{geo}' and type == '{transport_type}' and kg == 10;
            """
            execute = await cursor.execute(query1)
            res = await execute.fetchone() # ('Судан', 5, 10, 'air', 26900, 42250, 47600, 58100, 80400)

            query2 = f"""
            select * from logistic
            where type == '{transport_type}' and kg == 11;
            """
            execute2 = await cursor.execute(query2)
            res2 = await execute2.fetchone() # (11, 'air', 2250, 3650, 4150, 5280, 7550)

            zone = int(res[1])
            prices = [*res[4:]]
            prices2 = [*res2[2:]]
            shipping_price += int(prices[zone - 1])

            for _ in range(item_weight - 10):
                shipping_price += int(prices2[zone - 1])

        else:
            query = f"""
            select * from countries, logistic
            where name =='{geo}' and type == '{transport_type}' and kg == '{item_weight}';
            """
            execute = await cursor.execute(query)
            res = await execute.fetchone() # ('США', 4, 2, 'combined', 7700, 10950, 10700, 10700, 12600)

            zone = int(res[1])
            prices = [*res[4:]]
            shipping_price += int(prices[zone - 1])

        shipping_usd_price = round(shipping_price / usd, 2)
        item_usd_price = round(item_price / usd, 2)

        if category_number == 1:
            total_ebay_fee_usd = most_category.calc(item_usd_price, 7500)
            category_name += most_category.category_name
        if category_number == 2:
            total_ebay_fee_usd = book.calc(item_usd_price, 7500)
            category_name += book.category_name
        if category_number == 3:
            total_ebay_fee_usd = coins_and_papers.calc(item_usd_price, 7500)
            category_name += coins_and_papers.category_name
        if category_number == 4:
            total_ebay_fee_usd = clothing.calc(item_usd_price, 2000)
            category_name += clothing.category_name
        if category_number == 5:
            total_ebay_fee_usd = jewerly_and_watches.calc(item_usd_price, 5000)
            category_name += jewerly_and_watches.category_name
        if category_number == 6:
            total_ebay_fee_usd = jewerly_and_watches_and_parts.calc(item_usd_price, 7500)
            category_name += jewerly_and_watches_and_parts.category_name
        if category_number == 7:
            total_ebay_fee_usd = nft.calc(item_usd_price)
            category_name += nft.category_name
        if category_number == 8:
            total_ebay_fee_usd = buisness_and_industry.calc(item_usd_price, 15000)
            category_name += buisness_and_industry.category_name
        if category_number == 9:
            total_ebay_fee_usd = musical_gear.calc(item_usd_price, 7500)
            category_name += musical_gear.category_name
        if category_number == 10:
            total_ebay_fee_usd = other_category.calc(item_usd_price, 150)
            category_name += other_category.category_name

        total_ebay_fee_kzt = round(total_ebay_fee_usd * usd, 2)

        total_kzt = round(item_price - (shipping_price + total_ebay_fee_kzt), 2)
        total_usd = round(item_usd_price - (shipping_usd_price + total_ebay_fee_usd), 2)

        content = as_list(
            as_marked_section(
                Bold(__("Итого️")),
                as_key_value(__("Страна назначения"), geo),
                as_key_value(__("Тип транспортировки"), ttype),
                as_key_value(__("Обший вес товара"), f"{item_weight} кг"),
                as_key_value(__("Категория товара"), category_name),
                as_key_value(__("Курс доллара"), usd),
                as_key_value(__("Цена товара"), f"{item_price} KZT | {item_usd_price} $"),
                as_key_value(__("Сборы Ebay"), f"{total_ebay_fee_kzt} KZT | {total_ebay_fee_usd} $"),
                as_key_value(__("Цена доставки"), f"{shipping_price} KZT | {shipping_usd_price} $"),
                as_key_value(__("Чистая прибыль"), f"{total_kzt} KZT | {total_usd} $"),
                marker=" - ",
            )
        )

        return content
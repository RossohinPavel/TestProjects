import requests


URL = 'https://search.wb.ru/exactmatch/ru/common/v5/search?ab_testing=false&appType=1&curr=rub&dest={}&query={}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false&uclusters=2&uiv=2&uv=sGWtma8zK6svfJF_sHkvRyR7KiUt4ynELJctW68wMU0koauwKsGlSq5-rbSrCrAPraanMqwFqpCjh6_FJ0egGim5JaCpUqNmLFaljKhAKEWrgLBBrHgpmCySoewvpC2GJnOqAC8vrJOuLjDerxcsFa8ipo6pUKejpTAn-SXkLoqtbSWqMdWvRKkappMwYyNjGUGr0RlKK9UybyhwpRUv5axmKRIqqqZWLzcmJSwdK4QvIKp6LB8wr6z-s78xLigKqHkwUTI2sNku6KxkLcIrJSwWsTeoCyyVrZweDi_Mrz6vM5_cLRCtjy8yHsGuDy9EJOEvgbGyJ6Up1imlqKOuuA'
MOSCOW_LOC = '-364001'


def _parser(response):
    """Парсит словарь"""
    data = response['data']['products'][:11]
    for obj in data:
        yield obj['name'], f'https://www.wildberries.ru/catalog/{obj['id']}/detail.aspx'


def parser(name: str) -> dict:
    """Делает запрос и формирует словарь"""
    r = requests.get(URL.format(MOSCOW_LOC, name)).json()
    return {k: v for k , v in _parser(r)}
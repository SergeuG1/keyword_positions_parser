import math
import time

import requests
from loguru import logger
from datetime import datetime, timedelta
from database import SessionLocal
from views.products import Product
from views.keywords import Keywords
from views.keyword_products import KeywordProducts
from views.keywords_positions import KeywordPositions
from parse import postion_products
from threading import Thread
import threading
from multiprocessing import Process


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0"  # noqa 501



def error_handler(exception: BaseException):

    BOT_TOKEN = '6217920753:AAEeWlLEbMZduA4uilPYS3VHEeFjgFIL5YI'
    CHAT_ID = -935052991
    file_name = datetime.now().strftime("%d_%m_%Y.log")

    data = {'chat_id': CHAT_ID, "caption": "🔴 КРИТИЧЕСКАЯ ОШИБКА\nМодуль: NiiN сбор позиций товара"}
    logger.stop()
    url = 'https://api.telegram.org/bot{}/sendDocument'.format(BOT_TOKEN)
    with open('logs/' + file_name, '') as f:
        files = {'document': f}
        # requests.post(url, data=data, files=files)


def send_log_to_tg():

    BOT_TOKEN = '6217920753:AAEeWlLEbMZduA4uilPYS3VHEeFjgFIL5YI'
    CHAT_ID = -935052991
    file_name = datetime.now().strftime("%d_%m_%Y.log")

    data = {'chat_id': CHAT_ID, "caption": "🟢 Отчёт по логам\nМодуль: NiiN сбор позиций товара"}
    logger.stop()
    url = 'https://api.telegram.org/bot{}/sendDocument'.format(BOT_TOKEN)
    with open('logs/' + file_name, 'rb') as f:
        files = {'document': f}
        # requests.post(url, data=data, files=files)


def get_product_pages(keywords, keywords_infos):
    for i, keyword in enumerate(keywords[::]): 

        logger.info(f"{threading.current_thread().getName()} i = {i} Сейчас собираеться ключевое слово {keyword.title}:  {i + 1} из {len(keywords)}")
        if keyword.title == '':
            logger.debug(f"keyword.title is none, id = {i} key = {keyword.title}")
            continue

        postions_product = postion_products(keyword.title)
        if postions_product is None:
            logger.debug("product is none")
            continue

        keywords_infos[keyword.title] = {_["id"] : idx + 1 for idx, _ in enumerate(postions_product)}  
        time.sleep(5)

        
def chunks(lst, n):
    arr_keys = []
    for i in range(0, len(lst), n):
        arr_keys.append(lst[i:i + n])

    return arr_keys


@logger.catch(
        onerror=error_handler
)
def start():
    with SessionLocal() as session:
        total = []
        keyword_products: list[KeywordProducts] = session.query(KeywordProducts).all()
        keywords = session.query(Keywords).filter(Keywords.id.in_([i.keyword_id for i in keyword_products])).all()
        products = session.query(Product).filter(Product.id.in_([i.product_id for i in keyword_products])).all()
        
        keywords = {i.id : i for i in keywords}
        products = {i.id : i for i in products}
        
        keywords_infos = {}
        n  = 30
        keys_temp = list(keywords.values())[::]
        keys_arr = chunks(keys_temp, math.ceil(len(keys_temp) / n))
        threads = [Thread(target=get_product_pages, args=(keys_arr[i], keywords_infos), daemon=True) for i in range(n)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        for i, kp in enumerate(keyword_products):
            product: Product = products[kp.product_id]
            keyword: Keywords = keywords[kp.keyword_id]
            if keyword.title == '':
                continue
            if keywords_infos.get(keyword.title) is None:
                continue
            keyword_info = keywords_infos[keyword.title] 


            position = keyword_info.get(product.wb_article, 0)
            page = "20+" if position == 0 else str((position // 100) + 1)

            new_keyword_position = KeywordPositions(
                    product_id=product.id,
                    keyword_id=keyword.id,
                    page= page, 
                    position= position % 100,
                    date=datetime.now(),
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    deleted_at=None,
                )
            total.append(new_keyword_position)
            


        try: 
            session.add_all(total)
            session.commit()
            logger.info(f"Были успешно добавлены данные о товарах и их позициях по ключевым словам в количестве {len(total)}")
        except Exception as e:
            session.rollback()
            logger.critical(f"Произошла ошибка при добавлении ключевых слов {e}")

        time.sleep(10)
    send_log_to_tg()


if __name__ == "__main__":

    logger.add(
        "logs/{}".format(datetime.now().strftime("%d_%m_%Y.log")),
        format="{time} {level} {message}",
        rotation="10 MB",
        level="DEBUG",
        compression="zip")
    start()


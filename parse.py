from time import sleep
import datetime
import psycopg2
import requests
import json
import urllib.parse
from typing import List
from typing import Any
from dataclasses import dataclass
import urllib.parse
from loguru import logger


def reload_request(url, headers):
    counter = 15
    while True:
        if counter == 0:
            return r
        try: 
            r = requests.get(
            url=url,
            headers=headers,
        )
        except Exception as e:
            logger.warning(e)
            continue

        if r.status_code == 200:
            break

        counter -= 1

    return r
     


def postion_products(keyword, page_limit:int = 20):

        search_key = urllib.parse.quote_plus(keyword)
        temp_key = []

        for page in range(1, page_limit+1):
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Origin': 'https://www.wildberries.ru',
                'Referer': f'https://www.wildberries.ru/catalog/0/search.aspx?search={search_key}',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Opera GX";v="100"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=waterfall_card_hybrid_ads&TestID=216&appType=1&page={page}&curr=rub&dest=-1257786&query={search_key}&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false'
            try:
                response = requests.get(
                    url=url,
                    headers=headers,
                )

            except Exception as e:
                logger.warning(f"Ошибка {response.status_code} key = {keyword} на странице {page}")
                logger.warning(f"Ошибка {e} key = {keyword} на странице {page}\n")
                response = reload_request(url, headers)

            if response.status_code in [401, 403, 429, 500]:
                logger.warning(f"Ошибка {response.status_code} key = {keyword} на странице {page}")
                sleep(2)
                response = reload_request(url, headers)

                if response.status_code != 200:
                    logger.warning(f"{response.status_code} данные по ключевому слову {keyword} на странице {page} не были загружены")
                    continue
                else:
                    logger.success(f"{response.status_code} данные по ключевому слову {keyword} на странице {page} были загружены")
                break

            data = response.json()
            if "merger" in data.values():
                continue

            try:
                temp = data['data']['products']
            except Exception as e:
                logger.warning(f"Ошибка {response.status_code} key = {keyword} на странице {page}")
                logger.warning(f"Ошибка {e} key = {keyword} на странице {page}\n")
                continue
            
            temp_key.extend(temp)

        return temp_key



# from time import sleep
# import datetime
# import psycopg2
# import requests
# import json
# import urllib.parse
# from typing import List
# from typing import Any
# from dataclasses import dataclass
# import urllib.parse
# from loguru import logger


# def postion_products(keyword, page_limit:int = 20):

#     try:
#         search_key = urllib.parse.quote_plus(keyword)
#         temp_key = []

#         for page in range(1, page_limit+1):
            
#             headers = {
#                 'Accept': '*/*',
#                 'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8',
#                 'Connection': 'keep-alive',
#                 'Origin': 'https://www.wildberries.ru',
#                 'Referer': f'https://www.wildberries.ru/catalog/0/search.aspx?search={search_key}',
#                 'Sec-Fetch-Dest': 'empty',
#                 'Sec-Fetch-Mode': 'cors',
#                 'Sec-Fetch-Site': 'cross-site',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0',
#                 'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Opera GX";v="100"',
#                 'sec-ch-ua-mobile': '?0',
#                 'sec-ch-ua-platform': '"Windows"',
#             }
#             url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=waterfall_card_hybrid_ads&TestID=216&appType=1&page={page}&curr=rub&dest=-1257786&query={search_key}&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false'
#             try:
#                 sleep(0.1)
#                 response = requests.get(
#                     url=url,
#                     headers=headers,
#                     timeout=5
#                 )

#             except requests.exceptions.Timeout as e:
#                 logger.warning(e)
#                 break
            

#             if response.status_code in [401, 403, 429, 500]:
#                 logger.warning(f"Ошибка {response.status_code} key = {keyword} на странице {page}")
#                 sleep(5)
#                 response = requests.get(
#                     url=url,
#                     headers=headers,
#                 )   
#                 if response.status_code != 200:
#                     logger.warning(f"{response.status_code} данные по ключевому слову {keyword} на странице {page} не были загружены")
#                     continue
#                 else:
#                     logger.success(f"{response.status_code} данные по ключевому слову {keyword} на странице {page} были загружены")
#                 break

#             data = response.json()
#             if "merger" in data.values():
#                 continue
            
#             temp = data['data']['products']
#             temp_key.extend(temp)


#         return temp_key

#     except Exception as e:
#         print(e)
#         logger.critical(f"Ошибка {e}")



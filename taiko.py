import requests
import time

# Прокси и ссылка для смены IP
PROXY_URL = 'http://xxx:x@aaa.ru:8278'
CHANGE_IP_LINK = 'http://aa.com/reser?id=100'

# ANSI-коды для выделения красным цветом
RED_TEXT = '\033[91m'
RESET_TEXT = '\033[0m'

# Заголовки для имитации браузерного запроса
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Функция для получения информации о кошельке
def get_wallet_info(wallet):
    url = f'https://trailblazer.mainnet.taiko.xyz/user/rank?address={wallet}'
    proxies = {
        'http': PROXY_URL,
        'https': PROXY_URL
    }
    
    try:
        response = requests.get(url, proxies=proxies, headers=HEADERS)  # Добавляем заголовки запроса
        
        # Логируем полный ответ для дебага
        # print(f"Ответ сервера для кошелька {wallet}: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, dict):
                rank = data.get('rank', 'N/A')
                score = data.get('score', 'N/A')
                blacklisted = data.get('blacklisted', False)
                return wallet, rank, score, blacklisted
            else:
                print(f"Неверный формат данных для кошелька {wallet}")
                return wallet, 'N/A', 'N/A', False
        else:
            print(f"Ошибка для кошелька {wallet}: статус {response.status_code}")
            return wallet, 'N/A', 'N/A', False
    except requests.RequestException as e:
        print(f"Ошибка при запросе для кошелька {wallet}: {e}")
        return wallet, 'N/A', 'N/A', False
    except ValueError as ve:
        print(f"Ошибка парсинга JSON для кошелька {wallet}: {ve}")
        return wallet, 'N/A', 'N/A', False

# Функция для смены IP через запрос к API
def change_ip():
    try:
        response = requests.get(CHANGE_IP_LINK)
        # Логируем ответ на запрос смены IP
        print(f"Ответ сервера при смене IP: {response.text}")
        if response.status_code == 200:
            print("IP-адрес успешно сменён")
        else:
            print(f"Ошибка при смене IP: статус {response.status_code}")
    except requests.RequestException as e:
        print(f"Ошибка при смене IP: {e}")

# Основная функция для обработки всех кошельков
def main():
    # Чтение списка кошельков из файла wallets.txt
    with open('wallets.txt', 'r') as f:
        wallets = [line.strip() for line in f.readlines()]

    with open('wallets_info.txt', 'w') as f_out:
        for wallet in wallets:
            # Получение информации о кошельке
            wallet, rank, score, blacklisted = get_wallet_info(wallet)

            # Если кошелек в черном списке, выводим "sybil" красным
            if blacklisted:
                blacklisted_text = f"{RED_TEXT}sybil{RESET_TEXT}"
                f_out.write(f"{wallet} : rank {rank}, score {score}, {blacklisted_text}\n")
                print(f"{wallet} : rank {rank}, score {score}, {blacklisted_text}")
            else:
                f_out.write(f"{wallet} : rank {rank}, score {score}\n")
                print(f"{wallet} : rank {rank}, score {score}")

            # Смена IP после обработки каждого кошелька
            change_ip()

            # Задержка, чтобы IP успел обновиться
            time.sleep(5)

# Запуск основной функции
if __name__ == '__main__':
    main()

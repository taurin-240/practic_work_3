import os
import re
import json
from collections import Counter
from bs4 import BeautifulSoup

#Для работы парсера, html файлы нужно сохранить в папку "1" в папке исполняемого файла

def sort_array(data: list, key: str):
    """Сортирует словарю по значениям конкретного поля"""   
    return sorted(data,key=lambda item: item[key] )

def get_street(start_word,end_word,word) -> str | None:
    """Функция получает только значение улицы из строки"""
    pattern = f"{start_word}(.*?){end_word}"
    street = re.search(pattern,word)
    return street.group(1).strip()
    

# Функция для извлечения данных из одного HTML файла
def parse_html_file(filename):
    data = {}
    with open(filename, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        # Город (первый тег <span>)
        city = soup.find('span')
        data['city'] = city.text.split(sep=":")[1].strip() if city else None

        # Строение (<h1> class="title")
        building = soup.find('h1', class_='title')
        data['build'] = building.text.split(':')[1].strip() if building else None

        # Улица (class="address-p")
        address = soup.find(class_='address-p')
        street = address.text.replace("\n","") if address else None
        data['street'] =  get_street("Улица:","Индекс",street)

        # Индекс (class="address-p" конец строки где улица)
        index = street
        data['index'] = index.strip()[-6:] if index else None

        # Этажи (тег <span> class="floors")
        floors = soup.find('span', class_='floors')
        data['floors'] = int(floors.text.split(":")[1].strip()) if floors else None

        # Возраст здания (тег <span> class="year")
        year = soup.find('span', class_='year')
        data['old'] = int(year.text.split("Построено в ")[1].strip()) if year else None
        
        # Паркинг 
        parking = soup.find('span', class_='year').find_next('span')
        parking = parking.text.split(":")[1].strip().lower() if parking else None
        if parking == "есть":
            data['parking'] = True
        else:
            data['parking'] = False
        
        # Ссылка на фото (тег <img>)
        image = soup.find('img')
        data['img'] = image['src'] if image and 'src' in image.attrs else None
        
        # Рейтинг 
        rating = soup.find('img').find_next('span')
        rating = float(rating.text.split(":")[1].strip())
        data['rating'] = rating if rating else None
        
        #Просмотры
        views = soup.find('img').find_next('span').find_next('span')
        data['views'] = int(views.text.split(":")[1].strip()) if views else None

    return data

# Главная функция для обработки всех файлов
def parse_html_files(start, end, sorted_field, output_file):
    all_data = []
    for i in range(start, end + 1):
        filename = f"1/{i}.html"
        if os.path.exists(filename):  # Проверяем, существует ли файл
            print(f"Обрабатываю файл: {i}.html")
            data = parse_html_file(filename)
            all_data.append(data)
        else:
            print(f"Файл {filename} не найден, пропускаю.")
            
    # Отсортировать массив по определенному полю
    all_data = sort_array(all_data,sorted_field)
    
            
    # Сохранение в JSON файл
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=4)
    print(f"Данные сохранены в файл {output_file}")
    
    
def statistics(filename):
    statistic = {}
    """Собирает статистику по числовым значениям"""
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)  
        
    # Получим максимальное значение поля views
    max_views = max(data,key=lambda dictionary: dictionary['views'])['views']
    statistic['max_views'] = max_views

    # Получим сумму все просмотров зданий
    summ_views = 0
    for item_data in data:
        summ_views += item_data['views']
    statistic['sum_views'] = summ_views

    # Получим среднее количество просмотров
    avg_views = summ_views / len(data)
    statistic['svg_views'] = avg_views

    # Записываем результат в файл statistics.json
    with open('statistics.json', 'w', encoding='utf-8') as file:
        json.dump(statistic, file, ensure_ascii=False, indent=2)

    # Частота городов
    city_frequency = Counter(dictionary['city'] for dictionary in data)
    city_frequency = [{city:count} for city,count in city_frequency.items()]
    with open('city_frequency.json','w',encoding='utf-8') as file:
        json.dump(city_frequency,file,ensure_ascii=False,indent=2)

# Запуск парсера
if __name__ == "__main__":
    # parse_html_files(2, 89,'old', 'result.json')
    # parse_html_files(2, 89,'city', 'result_sorted_city.json')
    statistics('result.json')

import json
from collections import Counter
from bs4 import BeautifulSoup

def handle_file(path):
    with open(path, "r", encoding="utf-8") as file:
        xml_file = file.read()

    clothings = BeautifulSoup(xml_file, "xml").find_all("clothing")
    items = []
    for clothing in clothings:
        item = {}
        item["id"] = int(clothing.id.get_text())
        item["name"] = clothing.find_all('name')[0].get_text().strip()
        item["category"] = clothing.category.get_text().strip()
        item['size'] = clothing.size.get_text().strip()
        item['color'] = clothing.color.get_text().strip()
        item['material'] = clothing.material.get_text().strip()
        item['price'] = float(clothing.price.get_text().strip())
        item['rating'] = float(clothing.rating.get_text().strip())
        item['reviews'] = int(clothing.reviews.get_text().strip())
        if clothing.sporty is not None:
            item['sporty'] = clothing.sporty.get_text().strip() == "yes"
        if clothing.new is not None:
            item["new"] = clothing.new.get_text().strip() == "+"
        if clothing.exclusive is not None:
            item["exclusive"] = clothing.exclusive.get_text().strip() == "yes"

        items.append(item)
    return items

data = []
file_paths = [f"4/{i}.xml" for i in range(1, 109)]
for file_path in file_paths:
    data.extend(handle_file(file_path))

with open("fourth_task_data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

sorted_by_price = sorted(data, key=lambda x: x["price"], reverse=True)
with open("fourth_task_sorted_by_price.json", "w", encoding="utf-8") as file:
    json.dump(sorted_by_price, file, ensure_ascii=False, indent=4)

filtered_by_category = [item for item in data if item["category"] == "Sweater"]
with open("fourth_task_filtered_by_category.json", "w", encoding="utf-8") as file:
    json.dump(filtered_by_category, file, ensure_ascii=False, indent=4)

prices = [item["price"] for item in data]
price_stats = {
    "sum": sum(prices),
    "min": min(prices),
    "max": max(prices),
    "average": sum(prices) / len(prices),
}

category_frequency = Counter(item["category"] for item in data)

print("Характеристики цены:")
print(f"Сумма: {price_stats['sum']}")
print(f"Минимум: {price_stats['min']}")
print(f"Максимум: {price_stats['max']}")
print(f"Среднее: {price_stats['average']:.2f}")

print("Частота меток категорий:")
for category, count in category_frequency.items():
    print(f"{category}: {count}")
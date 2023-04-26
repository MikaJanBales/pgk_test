import time
import random
from datetime import datetime, timedelta
from typing import List

from pgk_test.benchmark import timing


@timing
def get_current_dislocation() -> List:
    """
    Формирование текущей дислокации вагонов.
    Получаем список вагонов и их дату прибытия.
    Каждый вагон может быть привязан к одной и той же накладной!
    Для того, чтобы получить предсказанную дату прибытия, необходимо вызывать сервис 'get_predicted_dates'
    """
    locations = []
    arrivale_dates = [None, None, None, datetime.now() - timedelta(days=3), datetime.now()]
    time.sleep(2)

    for i in range(0, 20000):
        arrivale_date = random.choice(arrivale_dates)
        location = {
            "wagon": random.randint(10000, 90000),
            "invoice": f"{random.randint(1, 30000)}__HASH__",
            "arrivale_date": arrivale_date.strftime("%d.%m.%Y") if arrivale_date else None,
        }
        locations.append(location)
    return locations


@timing
def get_predicted_date_by_invoices(invoices: List) -> List:
    """
        На вход необходимо передать список из уникальных накладных.
        По каждой накладной будет сформировано время прибытия
        """
    time.sleep(1)
    predicted_results = []
    for invoice in invoices:
        predicted_date = datetime.now() + timedelta(days=random.randint(1, 5))
        data = {
            "invoice": invoice,
            "predicted_date": predicted_date.strftime("%d.%m.%Y")
        }
        predicted_results.append(data)

    return predicted_results


@timing
def api_call() -> List[dict]:
    """
    В качестве ответа должен выдаваться повагонный список из сервиса get_current_dislocation
    с обновленной датой прибытия вагона из сервиса get_predicted_dates
    только по вагоном, у которых она отсутствует
    """
    locations = get_current_dislocation()

    # Получить список уникальных накладных из текущей дислокации только по тем вагонам,
    # где arrivale_date = None
    invoices_set = set()
    for location in locations:
        if location["arrivale_date"] is None:
            invoices_set.add(location["invoice"])
    invoices = list(invoices_set)
    predicted_data = get_predicted_date_by_invoices(invoices)

    # Создать словарь, где ключом будет invoice, а значением - соответствующая predicted_date.
    predicted_dict = {predicted["invoice"]: predicted["predicted_date"] for predicted in predicted_data}

    # Обновить оригинальный список вагонов данными, которые прислал сервис get_predicted_dates().
    # Заменить вагоны, где arrivale_date = None на соответствующее поле predicted_date.
    for location in locations:
        if not location["arrivale_date"]:
            location["arrivale_date"] = predicted_dict[location["invoice"]]

    return locations

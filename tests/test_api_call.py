# не забудьте установить pytest
from datetime import datetime
from pgk_test.locations.dao import api_call


# Тест для проверки, что возвращается список
def test_api_call_returns_list():
    assert isinstance(api_call(), list)


# Тест для проверки, что в списке есть вагоны, у которых была проставлена дата прибытия
def test_api_call_arrivale_date_not_none():
    locations = api_call()
    for location in locations:
        assert location["arrivale_date"] is not None


# Тест для проверки, что формат даты прибытия соответствует ожидаемому
def test_api_call_arrivale_date_format():
    locations = api_call()
    for location in locations:
        if location["arrivale_date"] is not None:
            assert datetime.strptime(location["arrivale_date"], "%d.%m.%Y")


# Тест для проверки, что возвращаемый список не содержит отсутствующих данных (None) для каких-либо вагонов
def test_api_call_no_missing_data():
    for wagon in api_call():
        assert None not in wagon.values()

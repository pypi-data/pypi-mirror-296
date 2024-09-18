import pytest


@pytest.fixture
def get_order_data():
    def _make(
        ordernum: str = "123456",
    ):
        order_data = {
            "order_id": "RU12345",
            "ordernum": ordernum,
            "plan_delivery_moment": "2023-10-15T10:00:00",
            "order_combo_state": "В пути",
            "available_delivery_date": "2023-10-16T10:00:00",
            "parcel_department_id": 12467456,
            "parcel_state": "Доставлено",
            "plan_shipment_end_moment": "2023-10-14T18:00:00",
            "delivery_terminal_code": "Терминал 1",
            "consignee_address": "Улица Примерная, дом 1",
            "order_delivery_to_door": "1",
            "is_carrier_area": "1",
            "carrier_track_number": "ABC123456789",
            "business_dict_code": 12,
            "clientnom": 88005553535,
            "brand_client_tts": "Бренд A",
            "client_redelivery_pay": False,
            "reason_code": 82312,
            "consignee": "Иван Иванов",
            "cntmovepddbyerr": 0,
            "consignee_phone": "+70001234567",
            "is_map": True,
            "is_pps": False,
            "current_delivery_attempts": 1,
            "state_name": "Зарег",
            "order_last_state_reason_code": "ЛК123"
        }
        return order_data

    return _make

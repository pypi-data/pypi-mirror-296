from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class OrderState(BaseModel):
    order_id: str = Field(description="ID заказа")
    ordernum: str = Field(description="Номер заказа DPD")
    plan_delivery_moment: datetime = Field(description="Дата доставки в заказе на момент запроса")
    order_combo_state: str = Field(description="Статус заказа")
    available_delivery_date: datetime = Field(description="Ближ. возможная дата доставки")
    parcel_department_id: int = Field(description="Текущее местонахождение посылки - бренч код")
    parcel_state: str = Field(description="Статус посылки")
    plan_shipment_end_moment: datetime = Field(description="Плановая дата поступления на терминал доставки")
    delivery_terminal_code: str = Field(description="Терминал доставки - бренч")
    consignee_address: str = Field(description="Адрес доставки (если до двери)")
    order_delivery_to_door: str = Field(description="Тип доставки (дверь; самовывоз)")
    is_carrier_area: str = Field(description="Спецперевозчик (is carrier area)")
    carrier_track_number: Optional[str] = Field(default="", description="Трек спецперевозчик")
    business_dict_code: int = Field(description="Отрасль клиента (business dict code)")
    clientnom: int = Field(description="Клиентский номер (clientnom)")
    brand_client_tts: Optional[str] = Field(default="", description="brand client tts")
    client_redelivery_pay: bool = Field(description="Требуется ли согласование повторной платной доставки")
    reason_code: int = Field(description="КИ посылки (reason code)")
    consignee: str = Field(description="Получатель")
    cntmovepddbyerr: Optional[int] = Field( description="Счетчик вины DPD (cntmovepddbyerr)")
    consignee_phone: str = Field(description="Телефон получателя из заказа")
    delivery_department_map_id: Optional[str] = Field(default="", description="МАП")
    is_pps: bool = Field(description="Статус PPS")
    current_delivery_attempts: int = Field(description="Исчерапно кол-во попыток доставки")
    state_name: Optional[str] = Field(description="Зарег-на ПС")
    order_last_state_reason_code: Optional[str] = Field(description="КОД последней ПС в статусе зарег-на")


class Dialog(BaseModel):
    session_id: str = Field(alias="SessionId", description="ID сессии диалога")

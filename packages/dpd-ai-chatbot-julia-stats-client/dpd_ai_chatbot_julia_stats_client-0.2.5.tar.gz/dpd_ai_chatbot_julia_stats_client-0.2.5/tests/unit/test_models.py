from src.dpd_ai_chatbot_julia_stats_client.models import OrderState


def test_models(get_order_data):
    model = OrderState(**get_order_data())
    assert model.model_dump_json()

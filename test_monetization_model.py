from monetization_model import MonetizationModel


def test_revenue_streams_structure():
    model = MonetizationModel()
    streams = model.revenue_streams()

    assert "b2b_store_partnerships" in streams
    assert "b2c_user_revenue" in streams
    assert "b2b_mall_partnership" in streams

    b2b_store = streams["b2b_store_partnerships"]
    assert b2b_store["sponsored_quests"] == "$100-1000 per quest"

    b2c_user = streams["b2c_user_revenue"]
    assert b2c_user["vip_subscription"]["price"] == "$4.99/month"

    b2b_mall = streams["b2b_mall_partnership"]
    assert b2b_mall["licensing"] == "Revenue share 10-20%"

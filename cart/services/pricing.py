def calculate_delivery_fee(seller, items):
    base_fee = seller.base_delivery_fee  # e.g. 100
    item_count = sum(i.quantity for i in items)

    if item_count > 3:
        return base_fee + 50
    return base_fee

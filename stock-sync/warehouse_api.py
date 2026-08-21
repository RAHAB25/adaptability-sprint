# DEPRECATED (Day 4 pivot): polling replaced by webhook (see server.py /webhook/stock-update)
# Kept for Scope Delta Analysis reference — no longer imported or run.


import random


inventory = {
    "NR-1042": {"name": "Cast Iron Skillet, 10 inch", "stock": 24},
    "NR-2210": {"name": "Bamboo Cutting Board", "stock": 3},
    "NR-3399": {"name": "Ceramic Mug Set (4pk)", "stock": 0}
}

def get_warehouse_snapshot():
    for sku in inventory:
        change = random.choice([1, -1])
        inventory[sku]["stock"] = max(0, inventory[sku]["stock"] + change)
    return inventory
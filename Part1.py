import datetime

def read_manufacturer_list(filename):
    manufacturer_data = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            item_id = parts[0]
            manufacturer_data[item_id] = {
                'manufacturer': parts[1],
                'item_type': parts[2],
                'damaged': 'Yes' if len(parts) > 3 else 'No'
            }
    return manufacturer_data

def read_price_list(filename):
    price_data = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            item_id = parts[0]
            price_data[item_id] = {'price': parts[1]}
    return price_data

def read_service_dates(filename):
    service_data = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            item_id = parts[0]
            service_data[item_id] = {'service_date': parts[1]}
    return service_data

def merge_data(manufacturer_data, price_data, service_data):
    full_inventory = {}
    for item_id in manufacturer_data:
        full_inventory[item_id] = {
            **manufacturer_data[item_id],
            **price_data.get(item_id, {}),
            **service_data.get(item_id, {})
        }
    return full_inventory

def write_full_inventory(inventory):
    with open('FullInventory.txt', 'w') as file:
        for item in sorted(inventory.values(), key=lambda x: x['manufacturer']):
            file.write(f"{item['item_id']},{item['manufacturer']},{item['item_type']},{item['price']},{item['service_date']},{item['damaged']}\n")

def write_item_type_inventories(inventory):
    types = set(item['item_type'] for item in inventory.values())
    for t in types:
        with open(f"{t}Inventory.txt", 'w') as file:
            for item in sorted((item for item in inventory.values() if item['item_type'] == t), key=lambda x: x['item_id']):
                file.write(f"{item['item_id']},{item['manufacturer']},{item['price']},{item['service_date']},{item['damaged']}\n")

def write_past_service_date_inventory(inventory):
    today = datetime.datetime.now().date()
    with open('PastServiceDateInventory.txt', 'w') as file:
        for item in sorted((item for item in inventory.values() if datetime.datetime.strptime(item['service_date'], '%m/%d/%Y').date() < today), key=lambda x: datetime.datetime.strptime(x['service_date'], '%m/%d/%Y').date()):
            file.write(f"{item['item_id']},{item['manufacturer']},{item['item_type']},{item['price']},{item['service_date']},{item['damaged']}\n")

def write_damaged_inventory(inventory):
    with open('DamagedInventory.txt', 'w') as file:
        for item in sorted((item for item in inventory.values() if item['damaged'] == 'Yes'), key=lambda x: float(x['price']), reverse=True):
            file.write(f"{item['item_id']},{item['manufacturer']},{item['item_type']},{item['price']},{item['service_date']}\n")

def main():
    manufacturers = read_manufacturer_list('ManufacturerList.txt')
    prices = read_price_list('PriceList.txt')
    service_dates = read_service_dates('ServiceDatesList.txt')
    inventory = merge_data(manufacturers, prices, service_dates)
    
    write_full_inventory(inventory)
    write_item_type_inventories(inventory)
    write_past_service_date_inventory(inventory)
    write_damaged_inventory(inventory)

if __name__ == '__main__':
    main()

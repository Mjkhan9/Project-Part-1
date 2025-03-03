import datetime

def read_manufacturer_list(filename):
    manufacturer_data = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            item_id = parts[0]
            manufacturer_data[item_id] = {
                'manufacturer': parts[1],
                'type': parts[2],
                'damaged': 'damaged' in parts
            }
    return manufacturer_data

def read_price_list(filename):
    price_data = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            item_id = parts[0]
            price_data[item_id] = int(parts[1])
    return price_data

def read_service_dates(filename):
    service_data = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            item_id = parts[0]
            service_data[item_id] = datetime.datetime.strptime(parts[1], '%m/%d/%Y')
    return service_data

def combine_data(manufacturer_data, price_data, service_data):
    combined_data = {}
    for item_id in manufacturer_data:
        combined_data[item_id] = {
            'item_id': item_id,  # Include item_id in the dictionary
            **manufacturer_data[item_id],
            'price': price_data[item_id],
            'service_date': service_data[item_id]
        }
    return combined_data

def write_full_inventory(inventory):
    with open('FullInventory.txt', 'w') as file:
        for item_id in sorted(inventory.keys(), key=lambda id: inventory[id]['manufacturer']):
            item = inventory[item_id]
            file.write(f"{item['item_id']},{item['manufacturer']},{item['type']},{item['price']},{item['service_date'].strftime('%m/%d/%Y')},{item['damaged']}\n")

def write_item_type_inventories(inventory):
    types = {}
    for item in inventory.values():
        if item['type'] not in types:
            types[item['type']] = []
        types[item['type']].append(item)
    for item_type, items in types.items():
        with open(f'{item_type}Inventory.txt', 'w') as file:
            for item in sorted(items, key=lambda x: x['item_id']):
                file.write(f"{item['item_id']},{item['manufacturer']},{item['price']},{item['service_date'].strftime('%m/%d/%Y')},{item['damaged']}\n")

def write_past_service_date_inventory(inventory):
    with open('PastServiceDateInventory.txt', 'w') as file:
        past_service_items = [item for item in inventory.values() if item['service_date'] < datetime.datetime.now()]
        for item in sorted(past_service_items, key=lambda x: x['service_date']):
            file.write(f"{item['item_id']},{item['manufacturer']},{item['type']},{item['price']},{item['service_date'].strftime('%m/%d/%Y')},{item['damaged']}\n")

def write_damaged_inventory(inventory):
    with open('DamagedInventory.txt', 'w') as file:
        damaged_items = [item for item in inventory.values() if item['damaged']]
        for item in sorted(damaged_items, key=lambda x: x['price'], reverse=True):
            file.write(f"{item['item_id']},{item['manufacturer']},{item['type']},{item['price']},{item['service_date'].strftime('%m/%d/%Y')}\n")

def main():
    manufacturer_data = read_manufacturer_list('ManufacturerList.txt')
    price_data = read_price_list('PriceList.txt')
    service_data = read_service_dates('ServiceDatesList.txt')
    
    inventory = combine_data(manufacturer_data, price_data, service_data)
    
    write_full_inventory(inventory)
    write_item_type_inventories(inventory)
    write_past_service_date_inventory(inventory)
    write_damaged_inventory(inventory)

if __name__ == '__main__':
    main()

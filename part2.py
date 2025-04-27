# Name: Mohammad Khan
# Date: April 26, 2025
# Project: Inventory Management System (Part 2)
# Description: This script reads inventory data from files, writes inventory reports, and allows users to query items interactively.

import datetime

# Inventory class handles all inventory work
class Inventory:
    def __init__(self, manufacturer_file, price_file, service_file):
        self.manufacturer_data = self.get_manufacturer_data(manufacturer_file)
        self.price_data = self.get_price_data(price_file)
        self.service_data = self.get_service_data(service_file)
        self.inventory = self.combine_all_data()

    # Reads manufacturer list
    def get_manufacturer_data(self, filename):
        data = {}
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                item_id = parts[0]
                data[item_id] = {
                    'manufacturer': parts[1].strip(),
                    'type': parts[2].strip(),
                    'damaged': 'damaged' in [x.strip().lower() for x in parts]
                }
        return data

    # Reads price list
    def get_price_data(self, filename):
        data = {}
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                data[parts[0]] = int(parts[1])
        return data

    # Reads service dates
    def get_service_data(self, filename):
        data = {}
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                data[parts[0]] = datetime.datetime.strptime(parts[1], '%m/%d/%Y')
        return data

    # Combines all lists into one inventory
    def combine_all_data(self):
        combined = {}
        for item_id in self.manufacturer_data:
            combined[item_id] = {
                'item_id': item_id,
                **self.manufacturer_data[item_id],
                'price': self.price_data.get(item_id, 0),
                'service_date': self.service_data.get(item_id, datetime.datetime.min)
            }
        return combined

    # Writes full inventory file
    def write_full_inventory(self):
        with open('FullInventory.txt', 'w') as f:
            for item in sorted(self.inventory.values(), key=lambda x: x['manufacturer']):
                f.write(f"{item['item_id']},{item['manufacturer']},{item['type']},{item['price']},{item['service_date'].strftime('%m/%d/%Y')},{item['damaged']}\n")

    # Writes item type inventory files
    def write_type_inventory(self):
        types = {}
        for item in self.inventory.values():
            if item['type'] not in types:
                types[item['type']] = []
            types[item['type']].append(item)
        for item_type in types:
            with open(f'{item_type}Inventory.txt', 'w') as f:
                for item in sorted(types[item_type], key=lambda x: x['item_id']):
                    f.write(f"{item['item_id']},{item['manufacturer']},{item['price']},{item['service_date'].strftime('%m/%d/%Y')},{item['damaged']}\n")

    # Writes past service date inventory
    def write_past_service_inventory(self):
        with open('PastServiceDateInventory.txt', 'w') as f:
            today = datetime.datetime.now()
            past_service = [item for item in self.inventory.values() if item['service_date'] < today]
            for item in sorted(past_service, key=lambda x: x['service_date']):
                f.write(f"{item['item_id']},{item['manufacturer']},{item['type']},{item['price']},{item['service_date'].strftime('%m/%d/%Y')},{item['damaged']}\n")

    # Writes damaged inventory
    def write_damaged_inventory(self):
        with open('DamagedInventory.txt', 'w') as f:
            damaged_items = [item for item in self.inventory.values() if item['damaged']]
            for item in sorted(damaged_items, key=lambda x: x['price'], reverse=True):
                f.write(f"{item['item_id']},{item['manufacturer']},{item['type']},{item['price']},{item['service_date'].strftime('%m/%d/%Y')}\n")

    # User can search for items
    def user_query(self):
        while True:
            query = input("\nEnter manufacturer and item type (or 'q' to quit): ").lower()
            if query == 'q':
                break

            words = query.split()
            manufacturer = None
            item_type = None

            for word in words:
                for item in self.inventory.values():
                    if word == item['manufacturer'].lower():
                        manufacturer = word
                    if word == item['type'].lower():
                        item_type = word

            if not manufacturer or not item_type:
                print("No such item in inventory")
                continue

            available = [item for item in self.inventory.values()
                         if item['manufacturer'].lower() == manufacturer
                         and item['type'].lower() == item_type
                         and not item['damaged']
                         and item['service_date'] > datetime.datetime.now()]

            if not available:
                print("No such item in inventory")
                continue

            best_match = max(available, key=lambda x: x['price'])
            print(f"Your item is: {best_match['item_id']}, {best_match['manufacturer']}, {best_match['type']}, {best_match['price']}")

            other_options = [item for item in self.inventory.values()
                              if item['type'].lower() == item_type
                              and item['manufacturer'].lower() != manufacturer
                              and not item['damaged']
                              and item['service_date'] > datetime.datetime.now()]

            if other_options:
                closest = min(other_options, key=lambda x: abs(x['price'] - best_match['price']))
                print(f"You may, also, consider: {closest['item_id']}, {closest['manufacturer']}, {closest['type']}, {closest['price']}")

# Main function to run everything
def main():
    inv = Inventory('ManufacturerList.txt', 'PriceList.txt', 'ServiceDatesList.txt')
    inv.write_full_inventory()
    inv.write_type_inventory()
    inv.write_past_service_inventory()
    inv.write_damaged_inventory()
    inv.user_query()

if __name__ == '__main__':
    main()

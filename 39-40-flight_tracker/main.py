from data_manager import DataManager


# Get spreadsheet data, check iata codes and update them
data_manager = DataManager()
original_data = data_manager.get_spreadsheet_data()

print(original_data)
data_manager.update_iata_codes(original_data)
print(original_data)

# Get new prices
new_data = data_manager.get_new_prices(original_data)
print(new_data)

# Update prices on spreadsheet
if new_data.isna().all().all():
    raise ValueError("No new data")
else:
    data_manager.update_prices(original_data, new_data)
    print("ALl prices updated")

# Send email notification if price is lower than desired price
data_manager.check_desired_price(original_data, new_data)
print("________________________________________________________________")
print("DONE")

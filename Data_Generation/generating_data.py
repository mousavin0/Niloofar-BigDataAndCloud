# import random
# from datetime import datetime, timedelta
# import pandas as pd

# def generate_sales_data(num_records):
#     order_ids = [f"{random.randint(1000000000, 9999999999)}" for _ in range(num_records)]
#     categories = ['Set', 'Kurta', 'Top', 'Western Dress']
#     sizes = ['S', 'M', 'L', 'XL']
#     statuses = ['Shipped', 'Cancelled', 'Shipped - Delivered to Buyer', 'Returned']
#     fulfilments = ['Amazon', 'Merchant']
#     courier_statuses = ['In Transit', 'Delivered', 'Returned', 'Pending']
#     currencies = ['USD', 'INR', 'EUR', 'GBP']
    
#     # Define realistic B2B vs B2C differences
#     b2b_price_range = (500, 3000)  # Higher amounts for B2B
#     b2c_price_range = (50, 500)  # Lower amounts for B2C

#     sales_data = []
    
#     for i in range(num_records):
#         b2b_sale = random.choice([True, False])
#         price_range = b2b_price_range if b2b_sale else b2c_price_range
#         price = round(random.uniform(*price_range), 2)
#         qty = random.randint(1, 10) if b2b_sale else random.randint(1, 3)  # Higher quantity for B2B

#         # First create the sale record without the 'Courier Status'
#         sale_record = {
#             'Order ID': order_ids[i],
#             # 'Category': random.choice(categories),
#             'Size': random.choice(sizes),
#             'Date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
#             'Status': random.choice(statuses),
#             'Fulfilment': random.choice(fulfilments),
#             'Qty': qty,
#             'Price': price,
#             'Amount': round(price * qty, 2),  # Price * Quantity
#             'B2B': b2b_sale,
#             'Currency': 'INR' if random.choice(categories) == 'Kurta' else random.choice(currencies),
#         }

#         # Assign the 'Courier Status' based on the 'Status' field
#         if 'Delivered' in sale_record['Status']:
#             sale_record['Courier Status'] = 'Delivered'
#         elif 'Returned' in sale_record['Status']:
#             sale_record['Courier Status'] = 'Returned'
#         else:
#             sale_record['Courier Status'] = random.choice(courier_statuses)

#         # Add the sale record to the list
#         sales_data.append(sale_record)

#     # Convert the list of sale records into a DataFrame
#     sales_data = pd.DataFrame(sales_data)
#     return sales_data

# def generate_access_log_data(sales_data, engagement_ratio):
#     platforms = ['Android App', 'Chrome', 'Safari', 'Firefox', 'Other']
#     country_language_map = {
#         'USA': 'English', 'India': 'English', 'Germany': 'German', 
#         'UK': 'English', 'Australia': 'English', 'Other': random.choice(['English', 'Other'])
#     }
#     countries = list(country_language_map.keys())

#     access_log_data = []
    
#     for index, sale_record in sales_data.iterrows():
#         # Generate a random number of access logs based on the engagement ratio
#         num_logs = random.randint(1, engagement_ratio)  # Random logs per sale
#         non_zero_log_index = random.randint(0, num_logs - 1)  # Index for non-zero sales log
        
#         for log_index in range(num_logs):
#             country = random.choice(countries)
#             log_record = {
#                 'accessed_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S'),
#                 'duration_(secs)': random.randint(1, 3600),  # Random duration between 1 second to 1 hour
#                 'network_protocol': random.choice(['TCP', 'HTTP', 'Other']),
#                 'ip': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
#                 'bytes': random.randint(1000, 5000000),  # Random bytes between 1KB and 5MB
#                 'accessed_From': random.choice(platforms),
#                 'country': country,
#                 'language': country_language_map[country],
#                 'sales_amount': sale_record['Amount'] if log_index == non_zero_log_index else 0,  # Only one log has a non-zero sales amount
#                 'returned_amount': round(random.uniform(0, min(500, sale_record['Amount'])), 2),  # Random return amount not exceeding the sale amount
#                 'Order ID': sale_record['Order ID'],  # Link access log to the corresponding sale
#             }
#             access_log_data.append(log_record)

#     access_log_data = pd.DataFrame(access_log_data)
#     return access_log_data

# # Example usage
# num_sales = 1000
# engagement_ratio = 10  # Average of 5 access logs per sale

# # Generate sales and access logs
# sales_data = generate_sales_data(num_sales)
# access_log_data = generate_access_log_data(sales_data, engagement_ratio)

# # Print summary info
# print(f"\nTotal Sales Amount: {sales_data['Amount'].sum():.2f}")
# print(f"\nTotal Sales Amount: {access_log_data['sales_amount'].sum():.2f}")
# print(sales_data.info())
# print(access_log_data.info())

# # Save sales data to CSV and access log data to JSON
# sales_data.to_csv('sales_data.csv', index=False)
# access_log_data.to_json('access_log_data.json', orient='records', indent=4)




import random
import pandas as pd
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Read sales data from CSV file
def read_sales_data(file_path):
    try:
        # Read the CSV with low_memory set to False to avoid dtype warnings
        df = pd.read_csv(file_path, low_memory=False)

        # Inspect the columns in the DataFrame to check for correct names
        print("Columns in the CSV:", df.columns.tolist())
        
        # Here we assume 'SKU', 'Category', 'Amount', and 'Qty' are present
        sales_data = df[['SKU', 'Category', 'Amount', 'Qty']].to_dict(orient='records')

        for sale in sales_data:
            # Check if 'Amount' and 'Qty' are present
            sale['price'] = sale.pop('Amount')  # Rename Amount to price
            sale['quantity'] = sale.pop('Qty')   # Rename Qty to quantity
            sale['category'] = sale.pop('Category')  # Rename Category to category
            sale['product_name'] = f"Product {sale['SKU']}"  # Mock product name based on SKU

        return sales_data
    except Exception as e:
        print(f"Error reading sales data: {e}")
        return []

# Possible actions with weights for each
other_actions = ["visit_page", "view_product", "add_to_cart", "logout"]
action_weights = [0.5, 0.3, 0.15, 0.05]  # Adjusted probabilities for each action


# Function to generate user IDs
def generate_user_ids(num_users=10):
    return [f"user_{random.randint(1000, 9999)}" for _ in range(num_users)]

# Generate random XML logs including purchase data from sales_data
def generate_xml_logs(sales_data, num_extra_logs=30, num_users=100000):
    # Create the root element for XML
    root = ET.Element("logs")
    users = generate_user_ids(num_users)  # Generate random user IDs

    # First, add purchase logs corresponding to sales data
    for sale in sales_data:
        user_id = random.choice(users)
        
        # Set the start time
        start_time = datetime(2022, 4, 12)

        # Generate a random timedelta within 59 days (up to 84960 minutes)
        random_minutes = random.randint(0, 84960)  # Random number of minutes within 59 days
        timestamp = start_time + timedelta(minutes=random_minutes)


        log_entry = ET.SubElement(root, "log")
        ET.SubElement(log_entry, "timestamp").text = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        ET.SubElement(log_entry, "user_id").text = user_id
        ET.SubElement(log_entry, "action").text = "purchase"
        ET.SubElement(log_entry, "product_sku").text = sale["SKU"]
        ET.SubElement(log_entry, "product_name").text = sale["product_name"]
        ET.SubElement(log_entry, "category").text = sale["category"]
        ET.SubElement(log_entry, "quantity").text = str(sale["quantity"])
        ET.SubElement(log_entry, "amount").text = str(sale["price"] * sale["quantity"])
        ET.SubElement(log_entry, "currency").text = "INR"  # Assuming a default currency
        ET.SubElement(log_entry, "payment_method").text = random.choice(["Credit Card", "UPI", "Net Banking"])
        ET.SubElement(log_entry, "transaction_id").text = f"txn_{random.randint(100000, 999999)}"

        # Then, generate other random user actions
        for _ in range(num_extra_logs):
            user_id = random.choice(users)
            action = random.choices(other_actions, weights=action_weights, k=1)[0]  # Select based on weights

            random_minutes = random.randint(0, 84960)  # Random number of minutes within 59 days
            timestamp = start_time + timedelta(minutes=random_minutes)
            
            log_entry = ET.SubElement(root, "log")
            ET.SubElement(log_entry, "timestamp").text = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            ET.SubElement(log_entry, "user_id").text = user_id
            ET.SubElement(log_entry, "action").text = action

            if action == "visit_page":
                page = random.choice(["home", "products", "about", "contact"])
                referrer = random.choice(["google.com", "facebook.com", "direct"])
                ET.SubElement(log_entry, "page").text = page
                ET.SubElement(log_entry, "referrer").text = referrer

            elif action == "view_product":
                product = random.choice(sales_data)
                ET.SubElement(log_entry, "product_sku").text = product["SKU"]
                ET.SubElement(log_entry, "product_name").text = product["product_name"]
                ET.SubElement(log_entry, "category").text = product["category"]
                ET.SubElement(log_entry, "price").text = str(product["price"])
                ET.SubElement(log_entry, "currency").text = "INR"

            elif action == "add_to_cart":
                product = random.choice(sales_data)
                quantity = random.randint(1, 3)
                ET.SubElement(log_entry, "product_sku").text = product["SKU"]
                ET.SubElement(log_entry, "quantity").text = str(quantity)

    return root

# Function to pretty-print the XML
def pretty_print_xml(element):
    xml_string = ET.tostring(element, encoding='utf-8')
    parsed_xml = minidom.parseString(xml_string)
    return parsed_xml.toprettyxml(indent="    ")  # Using 4 spaces for indentation

# Main execution
if __name__ == "__main__":
    # Path to the sales data CSV file (adjust as needed)
    file_path = "Amazon Sale Report.csv"  # Use relative path for Linux (parent folder)
    
    sales_data = read_sales_data(file_path)
    print(pd.DataFrame(sales_data).info())

    if sales_data:  # Proceed only if sales data was read successfully
        xml_root = generate_xml_logs(sales_data, num_extra_logs=5, num_users=100000)  # Include sales data and 30 extra random logs with 10 unique users
        
        # Pretty-print and save logs to an XML file
        pretty_xml = pretty_print_xml(xml_root)
        with open("website_logs.xml", "w", encoding="utf-8") as xml_file:
            xml_file.write(pretty_xml)

        print("Log data generated and saved to 'website_logs.xml'")
    else:
        print("No sales data available to generate logs.")
https://storageaccountbigdata23.blob.core.windows.net/curated/sales/part-00000-d51be2bb-21b4-43d8-95dd-02f9d9db9081-c000.snappy.parquet
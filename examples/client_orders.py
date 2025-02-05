### Sample client code to fetch customer order history by email

import requests
import json

BASE_URL = "http://localhost:8000"

def find_customer(email=None):
    response = requests.get(f"{BASE_URL}/customer/", params={"email": email,})
    return response.json() if response.status_code == 200 else None

def fetch_customer_details(customer_id):
    response = requests.get(f"{BASE_URL}/customer/{customer_id}/")
    return response.json() if response.status_code == 200 else None

def fetch_customer_orders(customer_id):
    response = requests.get(f"{BASE_URL}/customer/{customer_id}/orders/")
    return response.json() if response.status_code == 200 else []

def fetch_customer_addresses(customer_id):
    response = requests.get(f"{BASE_URL}/customer/{customer_id}/addresses/")
    return response.json() if response.status_code == 200 else []

def fetch_order_details(order_id):
    response = requests.get(f"{BASE_URL}/order/{order_id}/")
    return response.json() if response.status_code == 200 else None

def fetch_order_items(order_id):
    response = requests.get(f"{BASE_URL}/order/{order_id}/items/")
    return response.json() if response.status_code == 200 else []

def assemble_order_history(customer_email):
    customer = find_customer(email=customer_email)
    if not customer:
        print("Customer not found.")
        return
    
    customer_id = customer["id"]
    customer_details = fetch_customer_details(customer_id)
    if not customer_details:
        print("Customer not found.")
        return
    
    orders = fetch_customer_orders(customer_id)
    addresses = {addr["id"]: addr for addr in fetch_customer_addresses(customer_id)}
    
    order_history = {
        "customer": {
            "id": customer["id"],
            "name": f"{customer['first_name']} {customer['last_name']}",
            "email": customer["email"],
            "phone": customer["phone"]
        },
        "orders": []
    }
    
    for order in orders:
        order_details = fetch_order_details(order["id"])
        if not order_details:
            continue
        
        order_info = {
            "id": order_details["id"],
            "billing_address": addresses.get(order_details["billing_address_id"], None),
            "items": []
        }
        
        order_items = fetch_order_items(order["id"])
        for item in order_items:
            item_info = {
                "description": item["description"],
                "quantity": item["quantity"],
                "is_in_store_pickup": item["is_in_store_pickup"],
                "shipping_address": addresses.get(item["address_id"], None)
            }
            order_info["items"].append(item_info)
        
        order_history["orders"].append(order_info)
    
    print(json.dumps(order_history, indent=4))

if __name__ == "__main__":
    customer_email = input("Enter customer email: ")
    assemble_order_history(customer_email)
from flask import Flask, render_template, request, jsonify, session
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'mummy'

# Define a dictionary to store product data
products = {
    1: {'name': 'Cocktail', 'sizes': { 'Large': 12}},
    2: {'name': 'Pineging', 'sizes': {'Small': 7, 'Large': 10}},
    3: {'name': 'Citruswave', 'sizes': {'Small': 7, 'Large': 10}},
    4: {'name': 'Tropifusion', 'sizes': {'Small': 7, 'Large': 10}},
    5: {'name': 'Waterpine', 'sizes': {'Small': 7, 'Large': 10}},
    6: {'name': 'Crimson Carrot', 'sizes': {'Large': 15}},
    7: {'name': 'Banapple', 'sizes': {'Small': 7, 'Large': 15}},
    8: {'name': 'Beetro-Pine', 'sizes': {'Large': 15}},
    9: {'name': 'Nutwave', 'sizes': {'Small': 10, 'Large': 15}},
}

currency_symbol = 'GHS'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/products')
def products_list():
    return render_template('products.html', products=products)


@app.route('/order')
def order():
    return render_template('order.html')


@app.route('/more')
def more():
    return render_template('more.html')


@app.route('/submit_order', methods=['POST'])
def submit_order():
    data = request.data
    parsed_data = json.loads(data)
    data_dict = parsed_data['data']
    customer_note = parsed_data['notes']
    
    msg = MIMEMultipart()
    msg['From'] = 'fruityrefresh27@gmail.com'
    msg['To'] = 'niisaki2016@gmail.com'
    msg['Subject'] = 'New Order'
    
    email_content = 'You have received a new order:\n\n'
    total_price = 0
    
    # Iterate over the products in the order
    for product_id, product_data in data_dict.items():
        product_name = products[int(product_id)]['name']
        email_content += f"Product: {product_name}\n"
    
        # Iterate over the items of each product
        for item in product_data:
            product_size = item['size']
            product_price = item['price']
            product_quantity = item['quantity']
    
            price_for_product_purchased = product_quantity * product_price
            total_price += price_for_product_purchased
    
            email_content += (
                f"Size: {product_size}, Quantity: {product_quantity}, "
                f"Price per Item: {currency_symbol} {product_price}\n"
            )
    
    # Include customer notes and total price in the email content
    email_content += f"\nCustomer Notes: {customer_note}\n"
    email_content += f"Total Order Price: {currency_symbol} {total_price}\n"
    
    msg.attach(MIMEText(email_content, 'plain'))
    try:
       
            smtp_host = 'smtp.gmail.com'
            smtp_port = 587
            sender_email = 'fruityrefresh27@gmail.com'
            sender_password = 'ibax fzyh hwws ntdt'
            recipient_email = 'yawasackey@gmail.com'
        
            # Establish a connection to the SMTP server
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
        
            # Create a message object
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = 'New Order'
            msg.attach(MIMEText(email_content, 'plain'))
        
            # Send the email
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
        
            return jsonify({'message': 'Order placed successfully'}), 200
    except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 500
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

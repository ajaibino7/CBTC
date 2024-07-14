import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def create_receipt(customer_name, items, total_amount, receipt_number):
    # Define the output directory
    output_directory = "receipts"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Define the PDF file name
    receipt_file = os.path.join(output_directory, f"receipt_{receipt_number}.pdf")
    pdf = SimpleDocTemplate(receipt_file, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("Payment Receipt", styles['Title']))
    
    # Customer Name
    elements.append(Paragraph(f"Customer Name: {customer_name}", styles['Normal']))
    
    # Receipt Number
    elements.append(Paragraph(f"Receipt Number: {receipt_number}", styles['Normal']))
    
    # Spacer
    elements.append(Spacer(1, 12))

    # Create the table data
    data = [['Item', 'Quantity', 'Price']]
    for item in items:
        data.append([item['name'], item['quantity'], item['price']])

    # Create a table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)

    # Total Amount
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Total Amount: {total_amount:.2f}/-", styles['Normal']))

    # Build the PDF
    pdf.build(elements)

    print(f"Receipt saved as {receipt_file}")

# Example usage
customer_name = input("Enter customer name: ")
items = []
while True:
    item_name = input("Enter item name (or 'Q' to finish): ")
    if item_name.lower() == 'q':
        break
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))
    items.append({'name': item_name, 'quantity': quantity, 'price': price})

total_amount = sum(item['quantity'] * item['price'] for item in items)
receipt_number = input("Enter receipt number: ")

create_receipt(customer_name, items, total_amount, receipt_number)

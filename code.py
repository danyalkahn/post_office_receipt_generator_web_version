from flask import Flask, render_template, request, send_file, redirect, url_for, Response
import sqlite3
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
import os
import tempfile
import sys
import csv
import chardet

app = Flask(__name__)
DATABASE_FILE = "customer_data.db"
PAKISTAN_POST_LOGO = "pakistan_post_logo.png"
TEXT_IMAGE = "text.jpg"
TABLE_NAME = "customer_data"

def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            city TEXT,
            phone TEXT,
            price TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

create_table()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'csv_file' in request.files:
            csv_file = request.files['csv_file']
            if csv_file.filename != '':
                try:
                    raw_data = csv_file.stream.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding']

                    csv_data = csv.reader(io.StringIO(raw_data.decode(encoding), newline=None))
                    header = next(csv_data)
                    conn = sqlite3.connect(DATABASE_FILE)
                    cursor = conn.cursor()
                    for row in csv_data:
                        cursor.execute(f"""
                            INSERT INTO {TABLE_NAME} (name, address, city, phone, price, timestamp)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, row)
                    conn.commit()
                    conn.close()
                except Exception as e:
                    print(f"Error importing CSV: {e}")
        else:
            name = request.form['name']
            address = request.form['address']
            city = request.form['city']
            phone = request.form['phone']
            price = request.form['price']
            timestamp = datetime.datetime.now().isoformat()

            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO {TABLE_NAME} (name, address, city, phone, price, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, address, city, phone, price, timestamp))
            conn.commit()
            conn.close()

        return redirect(url_for('index'))

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f"SELECT name, address, city, phone, price, timestamp FROM {TABLE_NAME}")
    data = cursor.fetchall()
    conn.close()

    return render_template('index.html', data=data)

def generate_pdf(data_to_print, filename):
    if not data_to_print:
        return None

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    new_box_height = 20
    new_box_width = 4 * 72
    start_x = 50
    start_y = height - 100
    logo_top_padding = 20
    start_y += logo_top_padding
    line_height = 14
    box_width = 250
    box_height = 110
    text_vertical_offset = 35
    box_spacing = 20

    for data in data_to_print:
        current_y = start_y
        c.drawImage(PAKISTAN_POST_LOGO, start_x, current_y, width=500, height=50)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(start_x + 5, current_y - 18, f"V.P.L Rs: {data[4]}")
        c.setStrokeColor(colors.black)

        box_y = current_y - 35 - box_height
        new_box_y = box_y + box_height + 10
        c.rect(start_x, new_box_y, new_box_width, new_box_height)
        c.rect(start_x, box_y, box_width, box_height)
        c.rect(start_x + box_width + box_spacing, box_y, box_width, box_height)

        c.setFont("Helvetica", 10)
        to_x = start_x + 10
        c.drawString(to_x, box_y + box_height - text_vertical_offset, "To:")
        c.drawString(to_x, box_y + box_height - text_vertical_offset - line_height, f"Name: {data[0]}")
        c.drawString(to_x, box_y + box_height - text_vertical_offset - 2 * line_height, f"Address: {data[1]}")
        c.drawString(to_x, box_y + box_height - text_vertical_offset - 3 * line_height, f"City: {data[2]}")
        c.drawString(to_x, box_y + box_height - text_vertical_offset - 4 * line_height, f"Phone: {data[3]}")

        from_x = start_x + box_width + box_spacing + 10
        from_y = box_y + box_height - text_vertical_offset
        c.setFont("Helvetica-Bold", 10)
        c.drawString(from_x, from_y, "From: WALI TRADER")
        c.setFont("Helvetica", 8)
        c.drawString(from_x, from_y - line_height, "CENTER HAYATABAD")
        c.drawString(from_x, from_y - 2 * line_height, "All Pakistan Online Cosmetic Delivery")
        c.drawString(from_x, from_y - 3 * line_height, "P/O Code: 25100")
        c.drawString(from_x, from_y - 4 * line_height, "Phone: 0307-7199782")

        image_path = TEXT_IMAGE
        image_width_inches = 3
        image_width = image_width_inches * 72
        image_height = image_width / 8.56
        image_x = (width - image_width) / 2
        image_y = box_y - 50
        c.drawImage(image_path, image_x, image_y, width=image_width, height=image_height, mask='auto')

        start_y -= box_height + 30 + 100
        if start_y < 100:
            c.showPage()
            start_y = height - 50

    c.save()
    buffer.seek(0)
    return buffer

@app.route('/export_csv')
def export_csv():
    def generate():
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        print("Connected to DB")

        cursor.execute(f"SELECT name, address, city, phone, price, timestamp FROM {TABLE_NAME}")
        data = cursor.fetchall()
        print(f"Data fetched: {data}")
        conn.close()

        csv_buffer = io.StringIO()  # Use StringIO for streaming text
        csv_writer = csv.writer(csv_buffer)

        csv_writer.writerow(['Name', 'Address', 'City', 'Phone', 'Price', 'Timestamp'])
        print("Header written")
        yield csv_buffer.getvalue()  # Yield the header

        csv_buffer = io.StringIO()  # Reset buffer for data rows
        for row in data:
            csv_writer = csv.writer(csv_buffer)
            csv_writer.writerow(row)
            yield csv_buffer.getvalue()  # Yield each row
            csv_buffer = io.StringIO()  # Reset buffer after each row

    return Response(generate(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=customer_data.csv'})

@app.route('/download_all')
def download_all():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f"SELECT name, address, city, phone, price, timestamp FROM {TABLE_NAME}")
    data = cursor.fetchall()
    conn.close()
    pdf_buffer = generate_pdf(data, "customer_data_all.pdf")

    if pdf_buffer:
        return send_file(pdf_buffer, as_attachment=True, download_name='customer_data_all.pdf', mimetype='application/pdf')
    else:
         return "No data to generate PDF!", 400

@app.route('/download_today')
def download_today():
    today = datetime.date.today()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f"SELECT name, address, city, phone, price, timestamp FROM {TABLE_NAME}")
    all_data = cursor.fetchall()
    conn.close()

    today_data = []
    for data in all_data:
        try:
            date_str = data[5].split('T')[0]
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            if date == today:
                today_data.append(data)
        except ValueError:
            print(f"Invalid date format: {data[5]}")
    
    pdf_buffer = generate_pdf(today_data, "customer_data_today.pdf")
    if pdf_buffer:
        return send_file(pdf_buffer, as_attachment=True, download_name='customer_data_today.pdf', mimetype='application/pdf')
    else:
        return "No data for today to generate PDF!", 400

if __name__ == '__main__':
    app.run(debug=True)

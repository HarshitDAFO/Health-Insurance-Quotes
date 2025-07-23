import base64
from flask import Flask, render_template, request, send_file, redirect, url_for
import pandas as pd
import io
import pdfkit

app = Flask(__name__)

# Load USP data
usp_df = pd.read_excel("Heath Insurance USP's.xlsx", skiprows=0)
usp_df = usp_df.rename(columns={usp_df.columns[3]: "USP"})

product_company = {
    "Elevate": "ICICI Lombard",
    "Reassure 2.0": "Niva Bupa",
    "Aspire": "Niva Bupa",
    "Optima Secure": "HDFC",
    "Medicare Premier": "TATA AIG",
    "Care Supreme": "Care Health Insurance"
}

submitted_data = {}

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    global submitted_data
    data = request.form

    name = data['doctor_name']
    mobile = data['doctor_mobile']
    specialization = data['specialization']
    age = data['age']
    ped = data['ped']
    ped_detail = data.get('ped_detail', '')
    product = data['product']
    company = product_company.get(product, "Unknown")

    premium_1y = float(data['premium_1y'])
    premium_2y = float(data['premium_2y'])
    premium_3y = float(data['premium_3y'])

    discount_1y = float(data['discount_1y'])
    discount_2y = float(data['discount_2y'])
    discount_3y = float(data['discount_3y'])

    final_1y = premium_1y - discount_1y
    final_2y = premium_2y - discount_2y
    final_3y = premium_3y - discount_3y

    usps = usp_df[['USP', product]].dropna()

    # Load images as base64
    with open("static/logo.png", "rb") as logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode("utf-8")

    with open("static/why-choose-coveryou.png", "rb") as file1:
        why_choose_base64 = base64.b64encode(file1.read()).decode("utf-8")

    with open("static/10-reasons-coveryou.png", "rb") as file2:
        ten_reasons_base64 = base64.b64encode(file2.read()).decode("utf-8")

    submitted_data = {
        "name": name,
        "mobile": mobile,
        "specialization": specialization,
        "age": age,
        "ped": ped,
        "ped_detail": ped_detail,
        "product": product,
        "company": company,
        "usps": usps,
        "logo_base64": logo_base64,
        "why_choose_base64": why_choose_base64,
        "ten_reasons_base64": ten_reasons_base64,
        "premium_1y": premium_1y,
        "premium_2y": premium_2y,
        "premium_3y": premium_3y,
        "discount_1y": discount_1y,
        "discount_2y": discount_2y,
        "discount_3y": discount_3y,
        "final_1y": final_1y,
        "final_2y": final_2y,
        "final_3y": final_3y
    }

    return render_template("result.html", **submitted_data)

@app.route('/download')
def download_pdf():
    global submitted_data
    if not submitted_data:
        return redirect(url_for('form'))

    rendered_html = render_template('result.html', **submitted_data)
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered_html, False, configuration=config)

    return send_file(io.BytesIO(pdf), download_name="Health_Quote_Summary.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

import base64
from weasyprint import HTML
from flask import Flask, render_template, request, send_file, redirect, url_for
import pandas as pd
import io

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
    product = data['product']
    company = product_company.get(product, "Unknown")
    premium = float(data['premium'])
    discount = float(data['discount'])
    final_premium = premium - discount

    usps = usp_df[['USP', product]].dropna()

    # Encode logo once and pass to both result and PDF
    with open("static/logo.png", "rb") as logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode("utf-8")

    submitted_data = {
        "name": name,
        "mobile": mobile,
        "specialization": specialization,
        "age": age,
        "ped": ped,
        "product": product,
        "company": company,
        "premium": premium,
        "discount": discount,
        "final_premium": final_premium,
        "usps": usps,
        "logo_base64": logo_base64
    }

    return render_template('result.html', **submitted_data)

@app.route('/download')
def download_pdf():
    global submitted_data
    if not submitted_data:
        return redirect(url_for('form'))

    rendered_html = render_template('result_pdf.html', **submitted_data)

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered_html, False, configuration=config)

    return send_file(io.BytesIO(pdf), download_name="Health_Quote_Summary.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

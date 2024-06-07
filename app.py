from flask import Flask, request, redirect, url_for, send_file, render_template
from PIL import Image
from fpdf import FPDF
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Fungsi untuk mengonversi gambar menjadi PDF
def convert_images_to_pdf(image_paths, output_path='output.pdf'):
    pdf = FPDF()
    for image_path in image_paths:
        cover = Image.open(image_path)
        width, height = cover.size

        # Convert pixel to mm (1px = 0.264583 mm)
        width, height = float(width * 0.264583), float(height * 0.264583)

        # A4 size (210x297 mm), we can add a new page and place the image
        pdf.add_page()

        # Centering the image on the page
        pdf.image(image_path, x=(210 - width) / 2, y=(297 - height) / 2, w=width, h=height)

    pdf.output(output_path, "F")
    return output_path

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('files[]')

    image_list = []
    for file in files:
        if file.filename == '':
            return redirect(request.url)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        image_list.append(file_path)

    output_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')
    convert_images_to_pdf(image_list, output_pdf_path)

    return send_file(output_pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

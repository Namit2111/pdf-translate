from flask import Flask, render_template, request, redirect, url_for
from PyPDF2 import PdfFileReader, PdfFileWriter
from googletrans import Translator
import os
import requests

app = Flask(__name__)

def translate_text(text, src='en', dest='hi'):
    translator = Translator()
    result = translator.translate(text, src=src, dest=dest)
    return result.text

def split_pdf(filename):
    reader = PdfFileReader(filename)
    num_pages = reader.getNumPages()
    files = []
    for i in range(num_pages):
        writer = PdfFileWriter()
        writer.addPage(reader.getPage(i))
        output_filename = f"page_{i+1}.pdf"
        with open(output_filename, "wb") as output:
            writer.write(output)
            files.append(output_filename)
    return files

def process_page(input_filename):
    filename = input_filename
    reader = PdfFileReader(filename)
    page = reader.getPage(0)
    pagecontent = page.extractText()
    translated_data = translate_text(pagecontent)

    with open("translated.txt", 'a', encoding="utf-8") as translated_file:
        translated_file.write(translated_data+"\n\n\n\n\n\n\n\n\n")
    os.remove(filename)
    return translated_data



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['pdf']
        if file.filename == '':
            return redirect(request.url)

        file.save(file.filename)
        files = split_pdf(file.filename)
        translated_text = []
        for idx, file in enumerate(files, start=1):
            translated_page = process_page(file)
            translated_text.append(translated_page)
        return render_template('result.html', translated_text=translated_text)

    return render_template('index.html')

if __name__ == '__main__':


    app.run(host='0.0.0.0',port=5000,use_reloader=True,debug=True)

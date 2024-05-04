from flask import Flask, render_template, request, send_file
from enum import Enum
from io import BytesIO
import pypdf
from pypdf import PdfReader, PdfWriter
app = Flask(__name__)

PDFSizeParam = [
    ("PX_72DPI_A7", (210, 268)),
    ("PX_72DPI_A6", (298, 420)),
    ("PX_72DPI_A5", (420, 595)),
    ("PX_72DPI_A4", (595, 847)),
    ("PX_72DPI_A3", (842, 1191)),
    ("PX_72DPI_A2", (1191, 1684)),
    ("PX_72DPI_A1", (1684, 2384)),
    ("PX_72DPI_A0", (2384, 3370)),
    ("PX_72DPI_B7", (258, 363)),
    ("PX_72DPI_B6", (363, 516)),
    ("PX_72DPI_B5", (516, 729)),
    ("PX_72DPI_B4", (729, 1032)),
    ("PX_72DPI_B3", (1032, 1460)),
    ("PX_72DPI_B2", (1460, 2064)),
    ("PX_72DPI_B1", (2064, 2920)),
    ("PX_72DPI_B0", (2920, 4127)),
    ("PX_300DPI_A7", (874, 1240)),
    ("PX_300DPI_A6", (1240, 1748)),
    ("PX_300DPI_A5", (1748, 2480)),
    ("PX_300DPI_A4", (2480, 3508)),
    ("PX_300DPI_A3", (3508, 4961)),
    ("PX_300DPI_A2", (4961, 7016)),
    ("PX_300DPI_A1", (7016, 9933)),
    ("PX_300DPI_A0", (9933, 14043)),
    ("PX_300DPI_B7", (1075, 1512)),
    ("PX_300DPI_B6", (1512, 2150)),
    ("PX_300DPI_B5", (2150, 3035)),
    ("PX_300DPI_B4", (3035, 4299)),
    ("PX_300DPI_B3", (4299, 6083)),
    ("PX_300DPI_B2", (6083, 8598)),
    ("PX_300DPI_B1", (8598, 12165)),
    ("PX_300DPI_B0", (12165, 17197))
]


value_map = {
    'A7':1/8,
    'A6':2/8,
    'A5':3/8,
    'A4':4/8,
    'A3':5/8,
    'A2':6/8,
    'A1':7/8,
    'A0':8/8,
    'B7':9/8,
    'B6':10/8,
    'B5':11/8,
    'B4':12/8,
    'B3':13/8,
    'B2':14/8,
    'B1':15/8,
    'B0':16/8,
}

def scale_pdf_to(pdf_path: str, scale_to = PDFSizeParam[19][1]) -> bytes:
    with open(pdf_path, 'rb') as file:
        pdf_bytes = file.read()
    
    reader = PdfReader(BytesIO(pdf_bytes))
    num_pages = len(reader.pages)
    pages = [reader.pages[i] for i in range(num_pages)]
    [page.scale_to(scale_to.value[0], scale_to.value[1]) for page in pages]
    writer: PdfWriter = PdfWriter()
    [writer.add_page(page) for page in pages]
    temp_pdf: BytesIO = BytesIO()
    writer.write(temp_pdf)
    temp_pdf.seek(0)
    return temp_pdf.read()

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/upload", methods=["POST"])
def sendFile():
  if 'file' not in request.files:
    return jsonify({'error': 'ファイルがアップロードされていません'}), 400
  uploaded_file = request.files["file"]
  pdf_size_param = request.form.get("pdfSize")
  dpi_size_param = request.form.get("dpiSize")
  plusAlpha = 0
  if dpi_size_param == 300:
      plusAlpha = 16
  # if uploaded_file == '':
  #   return jsonify({'error': 'ファイルがアップロードされていません'}), 400
  output_filename = "output.pdf"
  uploaded_file_path = "temp.pdf"
  uploaded_file.save(uploaded_file_path)
  output_pdf_bytes = scale_pdf_to(uploaded_file_path, PDFSizeParam[plusAlpha + 8 * value_map[pdf_size_param]][1])
  with open(output_filename, "wb") as output_file:
    output_file.write(output_pdf_bytes)
  return send_file(output_filename, as_attachment=True)


if __name__ == "__main__":
  app.run()

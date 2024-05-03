from flask import Flask, render_template, request, send_file
from pypdf import PdfReader, PdfWriter
import fitz
import os
app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
  if request.method == "POST":
    #ファイルがアップロードされた場合の処理
    uploaded_file = request.files["file"]
    #一時ファイルを保存する
    uploaded_file_path = "temp.pdf"
    uploaded_file.save(uploaded_file_path)
    #ここでファイルを処理するロジックを実装する
    reader = PdfReader(uploaded_file)
    #出力サイズを指定
    a4_width_pt = 595.27
    a4_height_pt = 841.89
    doc = fitz.open(uploaded_file_path)
    
    
    #出力先のPDFファイルを用意
    writer = PdfWriter()
    
    #読み込んだPDFファイルのすべてのページのサイズを変更
    for index, page in enumerate(reader.pages):
        # 元のページのサイズを取得
        original_width_pt = doc[index].rect.width#幅
        original_height_pt = doc[index].rect.height#高さ
        # original_width_pt, original_height_pt = PageDataArr[index]
        #ページの縦横比を維持しながら、A4サイズにスケーリング
        if original_width_pt > original_height_pt:
            scale_factor = min(a4_width_pt / original_width_pt, a4_height_pt / original_height_pt)
        else:
            scale_factor = min(a4_width_pt / original_height_pt, a4_height_pt / original_width_pt)
        new_width_pt = original_width_pt * scale_factor
        new_height_pt = original_height_pt * scale_factor
        #余白を計算してA4サイズに調整
        margin_x = (a4_width_pt - new_width_pt) / 2
        margin_y = (a4_height_pt - new_height_pt) / 2
        new_x0 = margin_x
        new_y0 = margin_y
        new_x1 = a4_width_pt - margin_x
        new_y1 = a4_height_pt - margin_y
        # ページのサイズを変更して出力ファイルに追加
        page.scale_to(new_width_pt, new_height_pt)
        writer.add_page(page)
          
    # 出力ファイル名を設定
    output_filename = "output.pdf"
        
    # PDFファイルとして書き出し
    writer.write(output_filename)
    writer.close()
        
    # 処理が完了したことをユーザーに通知
    return send_file(output_filename, as_attachment=True)
    # #ここでは単純にファイル名を返す
    # return f"File '{uploaded_file.filename}' uploaded successfully."

if __name__ == "__main__":
  app.run(debug=True)

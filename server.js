const express = require('express');
const multer = require('multer');
const pdfParse = require('pdf-parse');
const fs = require('fs')

const app = express();
const port = process.env.PORT || 5000;

// ファイルのアップロードを行うための設定
const upload = multer({ dest: 'uploads/' });

// index.htmlの提供
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// ファイルのアップロードを処理するエンドポイント
app.post('/upload', upload.single('pdfFile'), (req, res) => {
    if (!req.file) {
        return res.status(400).send('ファイルがアップロードされていません');
    }

    // アップロードされたPDFファイルを読み込む
    const pdfFilePath = req.file.path;
    const pdfFileContent = fs.readFileSync(pdfFilePath);

    // PDFの解析
    pdfParse(pdfFileContent).then(data => {
        // 解析結果をコンソールに表示
        console.log(data.text);
        // 解析結果をクライアントに送信する場合は、ここで送信処理を行う
        res.send('PDFファイルを解析しました');
    }).catch(error => {
        console.error('PDFの解析中にエラーが発生しました:', error);
        res.status(500).send('PDFの解析中にエラーが発生しました');
    });
});

app.listen(port, () => {
    console.log(`サーバーがポート${port}で起動しました`);
});

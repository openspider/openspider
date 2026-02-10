const fs = require('fs');
const PDFParser = require('pdf2json');

const filePath = '/root/clawd/downloads/Suboya Classical Wisdom Translation in an AI Educator & Empirical Research on the  Truth-Goodness-Beauty-Spirit  Curriculum_1770714094491.pdf';

const pdfParser = new PDFParser(this, 1);

pdfParser.on('pdfParser_dataError', (err) => {
  console.error('Parse Error:', err.parserError);
});

pdfParser.on('pdfParser_dataReady', (pdfData) => {
  console.log('PDF parsed successfully');
  
  // Extract text from pages
  let fullText = '';
  let charCount = 0;
  
  if (pdfData.Pages) {
    pdfData.Pages.forEach((page, idx) => {
      console.log(`Page ${idx + 1}:`);
      
      if (page.Texts) {
        page.Texts.forEach((text, textIdx) => {
          if (text.R) {
            text.R.forEach((r) => {
              try {
                let decoded = decodeURIComponent(r.T);
                fullText += decoded;
                charCount += decoded.length;
              } catch (e) {
                // 如果解码失败，使用原始文本
                fullText += r.T;
                charCount += r.T.length;
              }
            });
          }
        });
      }
    });
  }
  
  console.log('Total Content Length:', charCount);
  console.log('');
  console.log('=== PDF Content (First 20000 chars) ===');
  console.log(fullText.substring(0, 20000));
});

pdfParser.loadPDF(filePath);

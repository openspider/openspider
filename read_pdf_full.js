const fs = require('fs');
const PDFParser = require('pdf2json');

const filePath = '/root/clawd/downloads/Suboya Classical Wisdom Translation in an AI Educator & Empirical Research on the Truth-Goodness-Beauty-Spirit  Curriculum_1770714094491.pdf';

const pdfParser = new PDFParser(this, 1);

pdfParser.on('pdfParser_dataError', (err) => {
  console.error('Parse Error:', err.parserError);
});

pdfParser.on('pdfParser_dataReady', (pdfData) => {
  console.log('PDF parsed successfully');
  
  let fullText = '';
  let charCount = 0;
  
  if (pdfData.Pages) {
    pdfData.Pages.forEach((page, idx) => {
      console.log(`Page ${idx + 1} processing...`);
      
      if (page.Texts) {
        page.Texts.forEach((text) => {
          if (text.R) {
            text.R.forEach((r) => {
              try {
                let decoded = decodeURIComponent(r.T);
                fullText += decoded + ' ';
                charCount += decoded.length;
              } catch (e) {
                fullText += r.T;
                charCount += r.T.length;
              }
            });
          }
        });
      }
    });
  }
  
  console.log(`\nTotal Content: ${charCount} characters`);
  
  // 保存完整内容
  fs.writeFileSync('/root/.openclaw/workspace/boya_paper_full.txt', fullText);
  console.log('Saved to boya_paper_full.txt');
  
  // 输出完整内容
  console.log('\n=== FULL PDF CONTENT ===');
  console.log(fullText);
});

pdfParser.loadPDF(filePath);

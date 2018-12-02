# DocumentSimilarityChecker
Implementation of Cosine Document Distance algorithm.





*****Required Libraries*****

1) For Simple Pdfs:
   a) Import pdfToTxt from pdfReader
   b) pdfminer.six

2) For Scanned Pdfs(OCR to text):
   a) PIL
   b) wand
   c) pyocr
   d) tesseract-ocr
   e) ImageMagick 6.9.9-37 (magic using pip and software through official site)
   f) GhostScript
   
   Installation Tutorial : http://xiaofeima1990.github.io/2016/12/19/extract-text-from-sanned-pdf/

3) For Word Documents:
   a) python-docx

4) Additional Libraries:
  a) ntlk



****Usage****

1) Place the Documents in same directory as program

The output is not acccurate as it implements the cosine document distance algo
(processing over word frequencies)

Algorithm Reference:
https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-fall-2011/lecture-videos/MIT6_006F11_lec02.pdf


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 10:10:35 2020

@author: otuniyio
"""


#install poppler and tesseract also needed
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path


startmark = b'\xff\xd8\xff'
startfix = 0
endmark = b"\xff\xd9\r\n"
endfix = 2
figures = 0
njpg = 0


sample_pdf_path = 'sample.pdf'
reference = []
figure_name = []
name_length = len(sample_pdf_path)-4

pages = convert_from_path(sample_pdf_path, 500)

image_counter = 1

#screenshots
for page in pages:
    filename = sample_pdf_path[:name_length]+'_pdf_page_'+str(image_counter)+'.jpg'
    page.save(filename, 'JPEG')

    image_counter = image_counter +1

filelimit = image_counter-1

outfile= sample_pdf_path[:name_length]+'_pdf_text.txt'

#text
f = open(outfile, 'a')
for i in range(1, filelimit + 1):
    filename = sample_pdf_path[:name_length]+'_pdf_page_'+str(i)+".jpg"
    text = str(((pytesseract.image_to_string(Image.open(filename)))))
    text= text.replace('-\n','')
    f.write(text)
f.close()

pdf = open(sample_pdf_path, 'rb').read()

#figures
while True:
    istream = pdf.find(b"stream", figures)
    if istream < 0:
        break
    istart = pdf.find(startmark, istream, istream+20)
    if istart < 0:
        figures = istream+20
        continue
    iend = pdf.find(b"endstream", istart)
    if iend < 0:
        raise Exception("Didn't find end of stream!")
    iend = pdf.find(endmark, iend-20)
    if iend < 0:
        raise Exception("Didn't find end of JPG!")

    istart += startfix
    iend += endfix
    print ("IMAAGE %d from %d to %d" % (njpg, istart, iend))
    jpg = pdf[istart:iend]
    jpgfile = open("fig%d.jpg" % njpg, "wb")
    jpgfile.write(jpg)
    jpgfile.close()

    njpg += 1
    figures = iend
    print('Found: istream ='+ str(istream), 'istart = '+ str(istart), 'figures ='+ str(figures), 'iend ='+ str(iend))

#refrences





from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

title = "IMSTIT"
codes = ["lclUY", "BbL04", "99L59", "IbFOS", "t3Fvz", "GFsOS", "2HZY3", "fYjNR", "ixY48", "xzSko"]

page = canvas.Canvas(title + ".pdf") #Oppretter et tomt dokument
width, height = A4 #Importer arkstørrelsen

font = "Courier"
size = [24, 18, 10] #Skriftstørrelsen på tittelen, teksten og undertittelen

margin = [50, 35, 2] #Avstanden fra toppen, tittlen og undertittelen
spacing = [100, 60] #Horisontal og vertikal mellomrom

page.setFont(font + "-Bold", size[0]) #Definerer tittelskriften
title_width = stringWidth(title, font + "-Bold", size[0]) / 2 #Finner bredden på tittelen for sentrering

page.drawString(width / 2 - title_width, height - (margin[0] + size[0]), title) #Legger til tittelen i dokumentet

for candidate, code in enumerate(codes):
    column = candidate % 5
    row = candidate // 5
    
    page.setFont(font, size[1]) #Definerer tekstskriften
    text_width = stringWidth(code, font, size[1]) / 2 #Finner bredden på teksten for sentrering
    
    #Finner tekstplassering basert på kolonne og rad
    cell_center = margin[0] + column * spacing[0] + spacing[0] / 2
    cell_height = height - (margin[0] + margin[1] + size[0] + size[2]) - row * spacing[1]
    
    page.drawString(cell_center - text_width, cell_height - (size[1] + margin[2]), code) #Legger til undertittelen i dokumentet
    
    page.setFont(font, size[2]) #Definerer undertittelen
    small_width = stringWidth(title, font, size[2]) / 2  #Finner bredden på undertittelen for sentrering
    
    page.drawString(cell_center - small_width, cell_height, title) #Legger til undertittelen i dokumentet
    
page.save()

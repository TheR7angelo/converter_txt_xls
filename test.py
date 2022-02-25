import os
import pathlib
import openpyxl
import re

link = r'G:\16- MULTISERVICES\Affaires\2022\Orange\- 11 CEM\AMEL 47\3 Suivi travaux\Sainte Bazeille\03-RETOUR TRAVAUX\05-D2\PMZ_28941 PA_32163\Dossier D2 PMZ 28941 PA 32163 SAINTE BAZEILLE\REFLECTOMETRIE'
extension = '*\\*.txt'

files = list(pathlib.Path(link).glob(extension))

for file in files:
    file = str(file)

    dossier, fichier = os.path.split(file)
    fichier = fichier.split('.')[0]

    with open(file) as f:
        lines = f.readlines()

    for row in range(len(lines)):
        lines[row] = lines[row].rstrip("\n")
        lines[row] = re.sub('  +', '\t', lines[row]).replace('\t\t', '\t')
        lines[row] = lines[row].split('\t')
        for col in range(len(lines[row])):
            lines[row][col] = lines[row][col].strip()

    workbook = openpyxl.Workbook()
    workbook.properties.creator = os.getenv("USERNAME")
    worksheet = workbook.worksheets[0]

    for row in range(len(lines)):
        for col in range(len(lines[row])):
            worksheet.cell(row=row+1, column=col+1).value = lines[row][col]

    file_name = f"{fichier}_{dossier.split(os.path.sep)[-1]}.xls"
    workbook.save(f'{dossier}/{file_name}')
    workbook.close()

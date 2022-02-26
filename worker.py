import datetime
import os

from re import sub
from openpyxl import Workbook

from PySide6.QtCore import QObject, Signal, QRunnable


class WorkerSignals(QObject):
    start = Signal(bool)
    progress = Signal(int)
    data = Signal(dict)
    error = Signal(str)


class Worker(QRunnable):
    """
    Worker thread
    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.
    """

    signals = WorkerSignals()

    def __init__(self, files, extension: str):
        super().__init__()
        self.files = files
        self.extension = extension

        self.is_killed = False

    def run(self):

        self.signals.start.emit(True)

        try:
            for file in self.files:
                file = str(file)
                dossier, fichier = os.path.split(file)
                fichier = fichier.split('.')[0]

                with open(file) as f:
                    lines = f.readlines()

                for row in range(len(lines)):
                    lines[row] = lines[row].rstrip("\n")
                    lines[row] = sub('  +', '\t', lines[row]).replace('\t\t', '\t')
                    lines[row] = lines[row].split('\t')
                    for col in range(len(lines[row])):
                        lines[row][col] = lines[row][col].strip()

                workbook = Workbook()
                workbook.properties.creator = os.getenv("USERNAME")
                worksheet = workbook.worksheets[0]

                for row in range(len(lines)):
                    for col in range(len(lines[row])):
                        worksheet.cell(row=row + 1, column=col + 1).value = lines[row][col]

                file_name = f"{fichier}_{dossier.split(os.path.sep)[-1]}.xls"
                workbook.save(f'{dossier}/{file_name}')
                workbook.close()

        except Exception as error:
            self.signals.error.emit(error)

            date = datetime.datetime.now().strftime('%d-%m-%Y %H-%M-%S')
            file = os.path.basename(__file__).replace('.py', '')
            directory = 'crash-log\\'

            os.makedirs(directory, exist_ok=True)
            with open(f'{directory}{file}_{date}.txt', 'w') as crash_report:
                crash_report.write(str(error))

        self.signals.start.emit(False)

    def kill(self):
        self.is_killed = True
        return

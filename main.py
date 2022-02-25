import datetime
import sys
import os

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import QSize, QPropertyAnimation
from PySide6.QtGui import Qt, QFont, QScreen, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

from Module.Widget.SideGrip import SideGrip

from mainWindow import Ui_MainWindow

WINDOW_SIZE = 0


class mainWindow(QMainWindow, Ui_MainWindow):
    clickPosition = None
    _gripSize = 8
    titre = 'Template'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation = None
        self.setupUi(self)

        self.setup()
        self.setup_connection_button()
        self.setup_programme()

        # Connection des bouton change interface

        # Connection des boutons pour réduire/agrandir/fermer le logiciel
        self.minimizeButton.clicked.connect(lambda: self.showMinimized())
        self.closeButton.clicked.connect(lambda: self.close())
        self.restoreButton.clicked.connect(lambda: self.restore_or_maximize_window())

        def moveWindow(e):
            if not self.isMaximized():  # Not maximized
                # Move window only when window is normal size
                # ###############################################
                # if left mouse button is clicked (Only accept left mouse button clicks)
                if e.buttons() == Qt.LeftButton:
                    # Move window
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()

            e.accept()

        self.main_header.mouseMoveEvent = moveWindow
        # self.left_menu_toggle_btn.clicked.connect(lambda: self.slideLeftMenu())
        self.show()

    def setup_connection_button(self):
        self.but_file_path.clicked.connect(self.select_dir)

        self.but_xls.clicked.connect(lambda: self.extension(self.but_xls.objectName()))
        self.but_xlsx.clicked.connect(lambda: self.extension(self.but_xlsx.objectName()))

    def setup_programme(self):
        self.file_path.setPlaceholderText('Glisser déposer un dossier  ou cliquer sur le bouton "Dossier"')

        self.but_run.clicked.connect(self.start_prog)

    def setup(self):

        def titre(self):
            font = QFont()
            font.setBold(True)

            # title = 'Extracteur photo'
            self.setWindowTitle(self.titre)

            self.title.setText(self.titre)
            self.title.setFont(font)

        def interface(self):
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

            self.sideGrips = [
                SideGrip(self, QtCore.Qt.Edge.LeftEdge),
                SideGrip(self, QtCore.Qt.Edge.TopEdge),
                SideGrip(self, QtCore.Qt.Edge.RightEdge),
                SideGrip(self, QtCore.Qt.Edge.BottomEdge),
            ]

            self.cornerGrips = [QtWidgets.QSizeGrip(self) for _ in range(4)]

        def buttonFont(self):
            font = QFont()
            font.setBold(True)
            listButton = self.left_side_menu.findChildren(QPushButton) + self.main_header.findChildren(QPushButton)
            for button in listButton:
                button.setFont(font)
                button.setFlat(True)
                button.setCheckable(True)
                button.setChecked(False)

        def activeHover(self):
            style = 'QPushButton{' \
                    'padding: 5px 10px;' \
                    'border: none;' \
                    'border-radius: 10px;' \
                    'background-color: transparent;' \
                    '}' \
                    'QPushButton:hover{' \
                    'background-color: rgb(0, 92, 157);' \
                    '}' \
                    'QPushButton:checked{' \
                    'background-color: rgb(112, 150, 70);' \
                    '}'
            self.left_side_menu.setStyleSheet(style)
            self.main_header.setStyleSheet(style)

        def connection_button_change_interface(self):
            listButton = self.left_side_menu.findChildren(QPushButton)
            for button in listButton:
                button.clicked.connect(lambda state=False, text=button.objectName(): self.interface_change(text))

        titre(self)
        # buttonFont(self)
        interface(self)
        # activeHover(self)
        # connection_button_change_interface(self)

    def extension(self, widget):
        list_widget = [self.but_xls, self.but_xlsx]

        widget = getattr(self, widget)
        for but in list_widget:
            if but != widget:
                but.setChecked(False)

    def start_prog(self):
        if self.file_path.text() != '':
            path = self.file_path.text()
            print(path)
        else:
            # message(self, "Le chemin du dossier n'a pas étais remplit", "Erreur", "Critique")
            print("Le chemin du dossier n'a pas étais remplit")

    def select_dir(self):
        if self.file_path.text() != '':
            path = self.file_path.text()
        else:
            path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        dossier = QFileDialog.getExistingDirectory(self, "Merci de choisir un dossier", path)
        if dossier != '':
            self.file_path.setText(dossier)

    def center(self):
        # Get Screen geometry
        SrcSize = QScreen.availableGeometry(QApplication.primaryScreen())
        # Set X Position Center
        frmX = (SrcSize.width() - self.width()) / 2
        # Set Y Position Center
        frmY = (SrcSize.height() - self.height()) / 2
        # Set Form's Center Location
        self.move(frmX, frmY)

    def interface_change(self, interface, option=None):

        widget = getattr(self, interface)
        liste_widget = self.left_menu_top_buttons.findChildren(QPushButton)

        if widget in liste_widget:
            for button in liste_widget:
                if button == widget:
                    button.setChecked(True)
                else:
                    button.setChecked(False)

        interface = f'page_{interface}'
        try:
            page = getattr(self, interface)
            self.stackedWidget.setCurrentWidget(page)
        except AttributeError:
            pass

    def mousePressEvent(self, event):
        # ###############################################
        # Get the current position of the mouse
        self.clickPosition = event.globalPos()
        # We will use this value to move the window
        # ###############################################

    def mouseDoubleClickEvent(self, event):

        if event.button() == QtCore.Qt.LeftButton:
            self.restore_or_maximize_window()

            if not self.isMaximized():
                self.center()

        if event.button() == QtCore.Qt.RightButton:
            print('hey')

    def mouseReleaseEvent(self, event):
        if self.pos().y() <= 0 and WINDOW_SIZE == 0:
            self.restore_or_maximize_window()

    # Restore or maximize your window
    def restore_or_maximize_window(self):
        # Global windows state
        global WINDOW_SIZE  # The default value is zero to show that the size is not maximized
        win_status = WINDOW_SIZE

        icon = QIcon()

        if win_status == 0:
            # If the window is not maximized
            WINDOW_SIZE = 1  # Update value to show that the window has been maximized
            self.showMaximized()

            # Update button icon  when window is maximized
            # self.restoreButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-restore.png"))  # Show minimized icon
            icon.addFile(u":/menu/Ressources/Asset/restore.svg", QSize(), QIcon.Normal, QIcon.Off)
        else:
            # If the window is on its default size
            WINDOW_SIZE = 0  # Update value to show that the window has been minimized/set to normal size (which is 800 by 400)
            self.showNormal()

            # Update button icon when window is minimized
            # self.restoreButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-maximize.png"))  # Show maximize icon
            icon.addFile(u":/menu/Ressources/Asset/maximize.svg", QSize(), QIcon.Normal, QIcon.Off)

        self.restoreButton.setIcon(icon)
        # function.resizePropre(self)

    ########################################################################
    # Slide left menu
    ########################################################################
    def slideLeftMenu(self, affichage=True):
        # Get current left menu width
        width = self.left_side_menu.width()

        # If minimized
        if width == 50 and affichage:
            # Expand menu
            newWidth = 182
        # If maximized
        else:
            # Restore menu
            newWidth = 50

        # Animate the transition
        self.animation = QPropertyAnimation(self.left_side_menu, b"minimumWidth")  # Animate minimumWidth
        self.animation.setDuration(250)
        self.animation.setStartValue(width)  # Start value is the current menu width
        self.animation.setEndValue(newWidth)  # end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        # self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
                                  -self.gripSize, -self.gripSize)

        # top left
        self.cornerGrips[0].setGeometry(
            QtCore.QRect(outRect.topLeft(), inRect.topLeft()))
        # top right
        self.cornerGrips[1].setGeometry(
            QtCore.QRect(outRect.topRight(), inRect.topRight()).normalized())
        # bottom right
        self.cornerGrips[2].setGeometry(
            QtCore.QRect(inRect.bottomRight(), outRect.bottomRight()))
        # bottom left
        self.cornerGrips[3].setGeometry(
            QtCore.QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        # left edge
        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())
        # top edge
        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)
        # right edge
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(),
            inRect.top(), self.gripSize, inRect.height())
        # bottom edge
        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(),
            inRect.width(), self.gripSize)

        [grip.raise_() for grip in self.sideGrips + self.cornerGrips]

    def resizeEvent(self, event):
        if WINDOW_SIZE == 0:
            QtWidgets.QMainWindow.resizeEvent(self, event)
            self.updateGrips()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # SPL_Pixmap = QtGui.QPixmap(u":/Asset/Ressources/Asset/logo.png")
    # splash = QtWidgets.QSplashScreen(SPL_Pixmap, QtCore.Qt.WindowStaysOnTopHint)
    # splash.show()

    locale = QtCore.QLocale.system().name()
    translator = QtCore.QTranslator()
    reptrad = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    translator.load("qtbase_" + locale, reptrad)  # qtbase_fr.qm
    app.installTranslator(translator)

    window = mainWindow()
    # splash.finish(window)
    window.show()
    sys.exit(app.exec())

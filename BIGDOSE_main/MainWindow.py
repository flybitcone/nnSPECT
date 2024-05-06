import sys
from PyQt6.QtWidgets import QApplication,QMainWindow, QFileDialog,QLineEdit
from PyQt6.QtGui import QValidator, QIntValidator,QDoubleValidator
from PyQt6 import uic
from ImageRead import ImageRead

class Ui(QMainWindow):
    patient_info = {
        "weight": 0,
        "height": 0,
        "age": 0,
        "id": 0,
    }
    def __init__(self, parent=None):
        super(Ui,self).__init__(parent)
        uic.loadUi("./界面.ui", self)  # Load the .ui file and pass self to bind components
        self.show()

        # 对输入进行限制
        self.patient_age.setValidator(QIntValidator())
        self.patient_weight.setValidator(QDoubleValidator())
        self.patient_height.setValidator(QDoubleValidator())

        # Connect ComboBox signal
        self.comboBox_3.currentIndexChanged.connect(self.onComboBoxIndexChanged)

        # 读取文件名称，并将名称填到一个TextLine中
        self.pushButton.clicked.connect(lambda: self.loadDataFile(5))
        self.pushButton_2.clicked.connect(lambda: self.loadDataFile(6))
        self.pushButton_3.clicked.connect(lambda: self.loadDataFile(7))
        self.pushButton_4.clicked.connect(lambda: self.loadDataFile(8))
        self.pushButton_5.clicked.connect(lambda: self.loadDataFile(9))
        self.pushButton_6.clicked.connect(lambda: self.loadDataFile(10))
        self.pushButton_7.clicked.connect(lambda: self.loadDataFile(11))
        self.pushButton_8.clicked.connect(lambda: self.loadDataFile(12))
        self.pushButton_9.clicked.connect(lambda: self.loadDataFile(13))
        self.pushButton_10.clicked.connect(lambda: self.loadDataFile(14))

        self.Tc99mAArun.clicked.connect(self.Tc99dose())
        self.Y90run.clicked.connect(self.Tc99dose())

    def setupPreviousData(self):
        self.patient_info["weight"] = self.patient_weight.text
        self.patient_info["height"] = self.patient_height.text
        self.patient_info['age'] = self.patient_age.text
        self.patient_info['id'] = self.patient_id.text
    def loadDataFile(self, index):
        path = self.loadDataPath()
        line_edit = getattr(self, f"lineEdit_{index}")
        line_edit.setText(path)
    def loadDataPath(self):
        filename = QFileDialog.getOpenFileName(
            filter="Image files (*.nii *.nii.gz *.mhd *.nrrd *.dcm)")
        # Prevent Crash for does not select file in file dialog
        if len(filename[0]) < 1:
            return ""
        return filename[0]
    # density correction选项变化
    def onComboBoxIndexChanged(self, index):
        # Get the current selected item
        current_text = self.comboBox_3.currentText()
        if current_text == "Customize":
            self.Custumize_density.setEnabled(True)
            self.density_a_1.setEnabled(True)
            self.density_a_2.setEnabled(True)
            self.density_b_1.setEnabled(True)
            self.density_b_2.setEnabled(True)

        if current_text != "Customize":
            self.Custumize_density.setEnabled(False)
            self.Density_a_1.setEnabled(False)
            self.Density_a_2.setEnabled(False)
            self.Density_b_1.setEnabled(False)
            self.Density_b_2.setEnabled(False)
        # print("Selected item:", current_text)
    def Tc99dose(self):
        return
    def Y90dose(self):
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui()
    sys.exit(app.exec())
#!/usr/bin/python

from PyQt4 import QtCore, QtGui
import os, glob


class whonix_repository_Settings():
  # default
  WHONIX_REPOSITORY_ENABLED = True
  WHONIX_REPOSITORY = '"wheezy"'

  # read Whonix Repository settings.
  def read(self):
    if os.path.exists('/root/.whonix.d/'):
      files = sorted(glob.glob('/root/.whonix.d/*'))
      if  files:
        for conf in files:
          if not conf.endswith('~') and conf.count('.dpkg-') == 0:
            with open(conf) as f:
              for line in f:
                if line.startswith('WHONIX_APT_REPOSITORY_DISTRUST_CONFIG'):
                  k, value = line.split('=')
                  self.WHONIX_REPOSITORY_ENABLED = value.strip() == '"0"'
                if line.startswith('WHONIX_APT_REPOSITORY_DISTRIBUTION_CONFIG'):
                  k, value = line.split('=')
                  self.WHONIX_REPOSITORY = value.strip()

  def write(self):
    print self.WHONIX_REPOSITORY_ENABLED
    print self.WHONIX_REPOSITORY


class whonix_repository_Dialog(QtGui.QDialog):
  def __init__(self):
    super(whonix_repository_Dialog, self).__init__()
    self.settings = whonix_repository_Settings()
    self.initUI()

  def initUI(self):
    self.resize(599, 360)
    self.setWindowTitle("Whonix Repository")

    self.buttonBox = QtGui.QDialogButtonBox(self)
    self.buttonBox.setGeometry(QtCore.QRect(425, 330, 159, 25))
    self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
    self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    self.buttonBox.accepted.connect(self.OK_Pressed)
    self.buttonBox.rejected.connect(self.reject)

    message = """<p><B>Automatically install updates from the Whonix team?</B></p><p>\n
Whonix News (via whonixcheck) will notify you of available updates.</p>
<p>When you run</p><blockquote>sudo apt-get dist-upgrade</blockquote>
<p>updates from the Whonix team will be AUTOMATICALLY downloaded and installed,
along with updates from the Debian team. Please read <a href=https://www.whonix.org/wiki/Trust>https://www.whonix.org/wiki/Trust</a> to understand the risks. </p>
<p>You can always start the Whonix Repository Tool again by running:</p><blockquote>sudo whonix_repository</blockquote>
"""
    self.label = QtGui.QLabel(self)
    self.label.setGeometry(QtCore.QRect(14, 4, 560, 155))
    #self.label.setFrameShape(QtGui.QFrame.Panel)
    self.label.setTextFormat(QtCore.Qt.RichText)
    self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
    self.label.setWordWrap(True)
    self.label.setText(message)

    self.enableGroup = QtGui.QGroupBox(self)
    self.enableGroup.setGeometry(QtCore.QRect(14, 160, 570, 60))
    self.enableButton = QtGui.QRadioButton(self.enableGroup)
    self.enableButton.setGeometry(QtCore.QRect(14, 10, 430, 21))
    self.enableButton.clicked.connect(self.enableButton_clicked)
    self.enableButton.setText("Yes. Automatically install updates from the Whonix team.")
    self.disableButton = QtGui.QRadioButton(self.enableGroup)
    self.disableButton.setGeometry(QtCore.QRect(14, 30, 430, 21))
    self.disableButton.setText("No. I will manually update from source code.")
    self.disableButton.clicked.connect(self.disableButton_clicked)

    self.repoGroup = QtGui.QGroupBox(self)
    self.repoGroup.setGeometry(QtCore.QRect(14, 230, 571, 90))
    self.repoGroup.setTitle('Repository (Most users should select the Stable repository)')
    self.stabeOption = QtGui.QRadioButton(self.repoGroup)
    self.stabeOption.setGeometry(QtCore.QRect(14, 22, 300, 21))
    self.stabeOption.setText('Whonix Stable Repository')
    self.testersOption = QtGui.QRadioButton(self.repoGroup)
    self.testersOption.setGeometry(QtCore.QRect(14, 42, 300, 21))
    self.testersOption.setText('Whonix Testers Repository')
    self.devOption = QtGui.QRadioButton(self.repoGroup)
    self.devOption.setGeometry(QtCore.QRect(14, 62, 300, 21))
    self.devOption.setText('Whonix Developpers Repository')

    self.settings.read()
    # set the GUI to the current settings.
    if self.settings.WHONIX_REPOSITORY_ENABLED:
      self.enableButton.setChecked(True)
      self.disableButton.setChecked(False)
    else:
      self.enableButton.setChecked(False)
      self.disableButton.setChecked(True)
      self.repoGroup.setEnabled(False)
    if self.settings.WHONIX_REPOSITORY == '"wheezy"':
      self.stabeOption.setChecked(True)
    elif self.settings.WHONIX_REPOSITORY == '"testers"':
      self.testersOption.setChecked(True)
    elif self.settings.WHONIX_REPOSITORY == '"developers"':
      self.devOption.setChecked(True)

    self.exec_()

  # toggle repository options enabled/disabled
  def enableButton_clicked(self):
    self.repoGroup.setEnabled(True)
  def disableButton_clicked(self):
    self.repoGroup.setEnabled(False)

  def OK_Pressed(self):
    # set user settings
    if self.enableButton.isChecked():
      self.settings.WHONIX_REPOSITORY_ENABLED = True
    elif self.disableButton.isChecked():
      self.settings.WHONIX_REPOSITORY_ENABLED = False
    if self.stabeOption.isChecked():
      self.settings.WHONIX_REPOSITORY = '"whezzy"'
    elif self.testersOption.isChecked():
      self.settings.WHONIX_REPOSITORY = '"testers"'
    elif self.devOption.isChecked():
      self.settings.WHONIX_REPOSITORY = '"developers"'

    self.close()
    self.settings.write()


def main():
  import sys
  app = QtGui.QApplication(sys.argv)
  dialog = whonix_repository_Dialog()
  sys.exit()

if __name__ == "__main__":
  main()

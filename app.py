from mainwindow import Ui_MainWindow
from PySide6.QtGui import QIcon
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import QSize
from PySide6.QtWidgets import QMessageBox
from pytube import YouTube, Playlist
import os
import sys
import moviepy.editor as mp #to convert the mp4 to wavv then mp3
import re
from os import path, rename
from pathlib import Path


class GUI_cont(QMainWindow, Ui_MainWindow): #Ui_MainWindow é a herança da class ui_mainwindow.py
    def __init__(self):
        super(GUI_cont, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Youtube Downloader")
        self.btn_baixar.clicked.connect(self.yt_downloader)
        self.setWindowIcon(QtGui.QIcon('imgs/icon.ico')) ##PASTA LÁ DE CIMA
        self.label

        self.file = ''
    
    
        

    def yt_downloader(self):

        
        video_url = self.txt_path.text()
        formato = ""
        

        #Para Audio-MP3
        if self.rb_mp3.isChecked():
            Musicas_MP3 = Path.home() /'Desktop'/'Musicas_MP3'
            Musicas_MP3.mkdir(exist_ok=True)

            video = YouTube(video_url).streams.first()
            downloaded_file = video.download(Musicas_MP3)
            base, ext = path.splitext(downloaded_file)
            new_file = base + '.mp3'
            rename(downloaded_file, new_file)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Audio baixado com sucesso!")
            msg.exec_()

        #Para Video - MP4
            
        elif self.rb_mp4.isChecked():
            Video = Path.home() /'Desktop'/'Video_Baixado'
            Video.mkdir(exist_ok=True)

            YouTube(video_url).streams.get_highest_resolution().download(Video)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Video baixado com sucesso!\n O vídeo está salvo na área de trabalho!")
            msg.exec_()
           
        #Para playlist
        
        elif self.rb_playlist.isChecked():
            playlist_baixadas = Path.home()/'Desktop'/'Playlist_mp3'
            playlist_baixadas.mkdir(exist_ok=True)

            playlist = Playlist(video_url)
            playlist.video_urls
        for url in playlist:
            print(url)
        for vid in playlist.videos:
            print(vid)
        for url in playlist:
            YouTube(url).streams.filter(only_audio=True).first().download(playlist_baixadas)
            
 
        for file in os.listdir(playlist_baixadas):
            if re.search('mp4', file):
                print("Converting : " + file)
                mp4_path = os.path.join(playlist_baixadas,file)
                mp3_path = os.path.join(playlist_baixadas,os.path.splitext(file)[0]+'.mp3')
                new_file = mp.AudioFileClip(mp4_path)
                new_file.write_audiofile(mp3_path)
                os.remove(mp4_path)

         
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Playlist baixada com sucesso! ")
        msg.exec_()
        

        ################################################################################
if __name__ == '__main__':
    qt = QApplication(sys.argv)

    window = GUI_cont()
    window.show()

    qt.exec()

    
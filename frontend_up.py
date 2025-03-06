from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QStackedWidget, QHBoxLayout,QVBoxLayout,QFrame,QScrollArea,QCheckBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import tempfile
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
import numpy as np
from backend import moving_averages_list, build_segment_tree_sum, call_data, convert_to_dictionary,ema_list,MACD,historical_volatility_list,VWAP_list,RSI,gains_list,loss_list,bollinger_bands

data_dict_ibm= call_data("IBM_Daily.db")
data_dict_walmart= call_data("Walmart_Daily.db")
data_dict_ms= call_data("Microsoft_Daily.db")
data_dict_nvidia= call_data("NVIDIA_Daily.db")
data_dict_Netflix= call_data("Netflix_Daily.db")

from helper import *


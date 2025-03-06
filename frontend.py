# Run this program for the project display:

# Run the following command in terminal to download all required libraries, modules, etc.
# pip install -r requirements.txt

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QStackedWidget, QHBoxLayout,QVBoxLayout,QFrame,QScrollArea,QCheckBox,QPushButton
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
data_dict_apple= call_data("Apple_Daily.db")
data_dict_Adobe= call_data("Adobe_Daily.db")
data_dict_Tesla= call_data("Tesla_Daily.db")

def movng_av(data_dict):
    dates_in_api = list(data_dict.keys())
    dates_in_api = dates_in_api[::-1]
    dates_dict = convert_to_dictionary(dates_in_api)

    start_date = dates_in_api[0]
    end_date = dates_in_api[-1]

    closings = []
    volumes = []
    volume_x_close = []
    open = []
    
    # Putting values from API to lists:
    for date in dates_in_api:

        closings.append(float(data_dict[date]["4. close"]))
        open.append(float(data_dict[date]["1. open"]))
        volumes.append(int(data_dict[date]["5. volume"]))
        volume_x_close.append((float(data_dict[date]["4. close"])) * (float(data_dict[date]["5. volume"])))
 
    segment_tree_closings_sum = build_segment_tree_sum(closings)
    data, lst = moving_averages_list(segment_tree_closings_sum, 10, dates_dict[start_date], dates_dict[end_date])
    return(data,lst)

def movng_ema(data_dict):
    dates_in_api = list(data_dict.keys())
    dates_in_api = dates_in_api[::-1]
    dates_dict = convert_to_dictionary(dates_in_api)
    
    start_date = dates_in_api[0]
    end_date = dates_in_api[-1]

    closings = []
    volumes = []
    volume_x_close = []
    open = []

    # Putting values from API to lists:
    for date in dates_in_api:

        closings.append(float(data_dict[date]["4. close"]))
        open.append(float(data_dict[date]["1. open"]))
        volumes.append(int(data_dict[date]["5. volume"]))
        volume_x_close.append((float(data_dict[date]["4. close"])) * (float(data_dict[date]["5. volume"])))
  
    segment_tree_closings_sum = build_segment_tree_sum(closings)
    data, lst =ema_list(closings, segment_tree_closings_sum, 12, dates_dict[start_date], dates_dict[end_date])
    return(data,lst)

def macd(data_dict):
    dates_in_api = list(data_dict.keys())
    dates_in_api = dates_in_api[::-1]
    dates_dict = convert_to_dictionary(dates_in_api)

    start_date = dates_in_api[0]
    end_date = dates_in_api[-1]

    closings = []
    volumes = []
    volume_x_close = []
    open = []

    # Putting values from API to lists:
    for date in dates_in_api:

        closings.append(float(data_dict[date]["4. close"]))
        open.append(float(data_dict[date]["1. open"]))
        volumes.append(int(data_dict[date]["5. volume"]))
        volume_x_close.append((float(data_dict[date]["4. close"])) * (float(data_dict[date]["5. volume"])))
   
    segment_tree_closings_sum = build_segment_tree_sum(closings)
    dates_in_api, macd_line, signal_line, macd_histogram= MACD(closings, segment_tree_closings_sum, dates_dict[start_date], dates_dict[end_date])
    return (dates_in_api, macd_line, signal_line, macd_histogram)

def hv(data_dict):
    dates_in_api = list(data_dict.keys())
    dates_in_api = dates_in_api[::-1]
    dates_dict = convert_to_dictionary(dates_in_api)

    start_date = dates_in_api[0]
    end_date = dates_in_api[-1]

    closings = []
    volumes = []
    volume_x_close = []
    open = []

    # Putting values from API to lists:
    for date in dates_in_api:

        closings.append(float(data_dict[date]["4. close"]))
        open.append(float(data_dict[date]["1. open"]))
        volumes.append(int(data_dict[date]["5. volume"]))
        volume_x_close.append((float(data_dict[date]["4. close"])) * (float(data_dict[date]["5. volume"])))
   
    segment_tree_closings_sum = build_segment_tree_sum(closings)
    data, lst = historical_volatility_list(closings, segment_tree_closings_sum, 20, dates_dict[start_date], dates_dict[end_date])
    return (data,lst)

def vwap(data_dict):
    dates_in_api = list(data_dict.keys())
    dates_in_api = dates_in_api[::-1]
    dates_dict = convert_to_dictionary(dates_in_api)

    start_date = dates_in_api[0]
    end_date = dates_in_api[-1]

    closings = []
    volumes = []
    volume_x_close = []
    open = []

    # Putting values from API to lists:
    for date in dates_in_api:

        closings.append(float(data_dict[date]["4. close"]))
        open.append(float(data_dict[date]["1. open"]))
        volumes.append(int(data_dict[date]["5. volume"]))
        volume_x_close.append((float(data_dict[date]["4. close"])) * (float(data_dict[date]["5. volume"])))
        
    segment_tree_volumes_sum = build_segment_tree_sum(volumes)
    segment_tree_volume_x_close_sum = build_segment_tree_sum(volume_x_close)
    data, lst = VWAP_list(segment_tree_volumes_sum, segment_tree_volume_x_close_sum, 10, dates_dict[start_date], dates_dict[end_date])
    return (data,lst)

def rsi(data_dict):
    
    dates_in_api = list(data_dict.keys())
    dates_in_api = dates_in_api[::-1]
    dates_dict = convert_to_dictionary(dates_in_api)

    start_date = dates_in_api[0]
    end_date = dates_in_api[-1]

    closings = []
    volumes = []
    volume_x_close = []
    open = []
    
    # Putting values from API to lists:
    for date in dates_in_api:

        closings.append(float(data_dict[date]["4. close"]))
        open.append(float(data_dict[date]["1. open"]))
        volumes.append(int(data_dict[date]["5. volume"]))
        volume_x_close.append((float(data_dict[date]["4. close"])) * (float(data_dict[date]["5. volume"])))
        
    gains = gains_list(closings, dates_dict[start_date], dates_dict[end_date])
    loss = loss_list(closings, dates_dict[start_date], dates_dict[end_date])
    segment_tree_gains = build_segment_tree_sum(gains)
    segment_tree_loss = build_segment_tree_sum(loss)
    data, lst = RSI(segment_tree_gains, segment_tree_loss, gains, loss, 14, dates_dict[start_date], dates_dict[end_date])
    return (data,lst)

def boulinder(data_dict):
    
    dates_in_api = list(data_dict.keys())
    dates_in_api = dates_in_api[::-1]
    dates_dict = convert_to_dictionary(dates_in_api)

    start_date = dates_in_api[0]
    end_date = dates_in_api[-1]

    closings = []
    volumes = []
    volume_x_close = []
    open = []

    # Putting values from API to lists:
    for date in dates_in_api:

        closings.append(float(data_dict[date]["4. close"]))
        open.append(float(data_dict[date]["1. open"]))
        volumes.append(int(data_dict[date]["5. volume"]))
        volume_x_close.append((float(data_dict[date]["4. close"])) * (float(data_dict[date]["5. volume"])))
 
    segment_tree_closings_sum = build_segment_tree_sum(closings)
    data, high,low = bollinger_bands(closings, segment_tree_closings_sum, dates_dict[start_date], dates_dict[end_date])
    return (data,high,low)

class Simple_moving(QWidget):
    def __init__(self, parent=None,frame=None,call=None):
        super().__init__(parent)
        # Create a Plotly figure

        # Load data
        if call =="sma":
            ibm_date,ibm_lst = movng_av(data_dict_ibm)
            meta_date,meta_lst = movng_av(data_dict_walmart)
            ms_date,ms_lst = movng_av(data_dict_ms)
            n_date,n_lst = movng_av(data_dict_nvidia)
            net_date,net_lst = movng_av(data_dict_Netflix)
            net_date,ap_lst = movng_av(data_dict_apple)
            net_date,ad_lst = movng_av(data_dict_Adobe)
            net_date,tes_lst = movng_av(data_dict_Tesla)
            
        elif call =="ema":
            ibm_date,ibm_lst = movng_ema(data_dict_ibm)
            meta_date,meta_lst = movng_ema(data_dict_walmart)
            ms_date,ms_lst = movng_ema(data_dict_ms)
            n_date,n_lst = movng_ema(data_dict_nvidia)
            net_date,net_lst = movng_ema(data_dict_Netflix)
            net_date,ap_lst = movng_ema(data_dict_apple)
            net_date,ad_lst = movng_ema(data_dict_Adobe)
            net_date,tes_lst = movng_ema(data_dict_Tesla)
            
        elif call =="hv":
            ibm_date,ibm_lst = hv(data_dict_ibm)
            meta_date,meta_lst =hv(data_dict_walmart)
            ms_date,ms_lst = hv(data_dict_ms)
            n_date,n_lst = hv(data_dict_nvidia)
            net_date,net_lst = hv(data_dict_Netflix)
            net_date,ap_lst = hv(data_dict_apple)
            net_date,ad_lst = hv(data_dict_Adobe)
            net_date,tes_lst = hv(data_dict_Tesla)
            
        elif call =="vwap":
            ibm_date,ibm_lst = vwap(data_dict_ibm)
            meta_date,meta_lst =vwap(data_dict_walmart)
            ms_date,ms_lst = vwap(data_dict_ms)
            n_date,n_lst = vwap(data_dict_nvidia)
            net_date,net_lst = vwap(data_dict_Netflix)
            net_date,ap_lst = vwap(data_dict_apple)
            net_date,ad_lst = vwap(data_dict_Adobe)
            net_date,tes_lst = vwap(data_dict_Tesla)

        elif call =="rsi":
            ibm_date,ibm_lst = rsi(data_dict_ibm)
            meta_date,meta_lst =rsi(data_dict_walmart)
            ms_date,ms_lst = rsi(data_dict_ms)
            n_date,n_lst = rsi(data_dict_nvidia)
            net_date,net_lst = rsi(data_dict_Netflix)
            net_date,ap_lst = rsi(data_dict_apple)
            net_date,ad_lst = rsi(data_dict_Adobe)
            net_date,tes_lst = rsi(data_dict_Tesla)
            
        # Create figure
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x = ibm_date, y = ibm_lst))

        fig.add_trace(
            go.Scatter(x=meta_date, y=meta_lst, visible=False))

        fig.add_trace(
            go.Scatter(x=ms_date, y=ms_lst, visible=False))
        
        fig.add_trace(
            go.Scatter(x=n_date, y=n_lst, visible=False))
        
        fig.add_trace(
            go.Scatter(x=net_date, y=net_lst, visible=False))
        
        fig.add_trace(
            go.Scatter(x=net_date, y=ap_lst, visible=False))
        fig.add_trace(
            go.Scatter(x=net_date, y=ad_lst, visible=False))
        fig.add_trace(
            go.Scatter(x=net_date, y=tes_lst, visible=False))
        # Set title
        fig.update_layout(
            title_text="Time series with range slider and selectors"
        )

        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
        updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="IBM",
                     method="update",
                     args=[{"visible": [True, False, False, False,False,False, False,False]}]),
                dict(label="Walmart",
                     method="update",
                     args=[{"visible": [False, True, False, False,False,False, False,False]},
                           ]),
                dict(label="MICROSOFT",
                     method="update",
                     args=[{"visible": [False, False, True, False,False,False, False,False]}
                           ]),
                dict(label="NVDIA",
                     method="update",
                     args=[{"visible": [False, False, False, True,False,False, False,False]}]),
                     
                dict(label="Netflix",
                     method="update",
                     args=[{"visible": [False, False, False, False,True,False, False,False]}]),
                dict(label="Apple",
                     method="update",
                     args=[{"visible": [False, False, False, False,False,True, False,False]}]),
                dict(label="Adobe",
                     method="update",
                     args=[{"visible": [False, False, False, False,False,False, True,False]}]),
                dict(label="Tesla",
                     method="update",
                     args=[{"visible": [False, False, False, False,False,False, False,True]}]),
            ]),
            x = 0.4,
            y= 1.12,
            direction = "right",
        )
    
    ])
        if call=="ema":
            fig.update_layout(template="ggplot2")
        if call=="hv":
            fig.update_layout(template="presentation")
        if call=="vwap":
             fig.update_layout(template="xgridoff")
        # Save the plot to a temporary HTML file
        temp_file_path = tempfile.NamedTemporaryFile(suffix='.html', delete=True).name
        fig.write_html(temp_file_path)

        # Create a Qt widget to display the Plotly HTML
        self.plot_widget = QWebEngineView(frame)
        self.plot_widget.setUrl(QtCore.QUrl.fromLocalFile(temp_file_path))

        self.plot_widget.setGeometry(10,350,1100,600)

class exponential_moving_company(QWidget):
    
    def __init__(self, parent=None,frame=None,call=None,geo=None):
        
        super().__init__(parent)
        # Create a Plotly figure
        fig = go.Figure()
        # Load data
        if call =="IMB":
            ibm_date,ibm_lst = movng_ema(data_dict_ibm)
            fig.add_trace(
            go.Scatter(x = ibm_date, y = ibm_lst))

        elif call=="WMT":
            meta_date,meta_lst = movng_ema(data_dict_walmart)
            fig.add_trace(go.Scatter(x=meta_date, y=meta_lst))
            
        elif call == 'MSFT':
            ms_date,ms_lst = movng_ema(data_dict_ms)
            fig.add_trace(
            go.Scatter(x=ms_date, y=ms_lst)) 
            
        elif call=="NVDA":
            n_date,n_lst = movng_ema(data_dict_nvidia)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        
        elif call=="NFL": 
            n_date,n_lst = movng_ema(data_dict_Netflix)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
                    
        elif call=='ap':
            n_date,n_lst = movng_ema(data_dict_apple)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        elif call=='ad':
            n_date,n_lst = movng_ema(data_dict_Adobe)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        elif call=="tes":
            n_date,n_lst = movng_ema(data_dict_Tesla)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
                    
        # Set title
        fig.update_layout(
            title_text="Time series with range slider and selectors"
        )
        
        fig.update_layout(template="ggplot2")
        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
        updatemenus=[
    ])

        # Save the plot to a temporary HTML file
        temp_file_path = tempfile.NamedTemporaryFile(suffix='.html', delete=True).name
        fig.write_html(temp_file_path)

        # Create a Qt widget to display the Plotly HTML
        self.plot_widget = QWebEngineView(frame)
        self.plot_widget.setUrl(QtCore.QUrl.fromLocalFile(temp_file_path))

        self.plot_widget.setGeometry(geo[0],geo[1],geo[2],geo[3])

class Simple_moving_company(QWidget):
    
    def __init__(self, parent=None,frame=None,call=None,geo=None):
        
        super().__init__(parent)
        # Create a Plotly figure
        fig = go.Figure()
        # Load data
        if call =="IMB":
            ibm_date,ibm_lst = movng_av(data_dict_ibm)
            fig.add_trace(
            go.Scatter(x = ibm_date, y = ibm_lst))

        elif call=="WMT":
            meta_date,meta_lst = movng_av(data_dict_walmart)
            fig.add_trace(go.Scatter(x=meta_date, y=meta_lst))
            
        elif call == 'MSFT':
            ms_date,ms_lst = movng_av(data_dict_ms)
            fig.add_trace(
            go.Scatter(x=ms_date, y=ms_lst)) 
            
        elif call=="NVDA": 
            n_date,n_lst = movng_av(data_dict_nvidia)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
            
        elif call=="NFL": 
            n_date,n_lst = movng_av(data_dict_Netflix)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
                    
        elif call=='ap':
            n_date,n_lst = movng_av(data_dict_apple)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        elif call=='ad':
            n_date,n_lst = movng_av(data_dict_Adobe)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        elif call=="tes":
            n_date,n_lst = movng_av(data_dict_Tesla)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
            
        # Set title
        fig.update_layout(
            title_text="Time series with range slider and selectors"
        )

        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
        updatemenus=[
    ])

        # Save the plot to a temporary HTML file
        temp_file_path = tempfile.NamedTemporaryFile(suffix='.html', delete=True).name
        fig.write_html(temp_file_path)

        # Create a Qt widget to display the Plotly HTML
        self.plot_widget = QWebEngineView(frame)
        self.plot_widget.setUrl(QtCore.QUrl.fromLocalFile(temp_file_path))

        self.plot_widget.setGeometry(geo[0],geo[1],geo[2],geo[3])

class hv_company(QWidget):
    
    def __init__(self, parent=None,frame=None,call=None,geo=None):
        
        super().__init__(parent)
        # Create a Plotly figure
        fig = go.Figure()
        # Load data
        if call =="IMB":
            ibm_date,ibm_lst = hv(data_dict_ibm)
            fig.add_trace(
            go.Scatter(x = ibm_date, y = ibm_lst))

        elif call=="WMT":
            meta_date,meta_lst = hv(data_dict_walmart)
            fig.add_trace(go.Scatter(x=meta_date, y=meta_lst))
            
        elif call == 'MSFT':
            ms_date,ms_lst = hv(data_dict_ms)
            fig.add_trace(
            go.Scatter(x=ms_date, y=ms_lst)) 
            
        elif call=="NVDA": 
            n_date,n_lst = hv(data_dict_nvidia)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
            
        elif call=="NFL": 
            n_date,n_lst = hv(data_dict_Netflix)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
                    
        elif call=='ap':
            n_date,n_lst = hv(data_dict_apple)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        elif call=='ad':
            n_date,n_lst = hv(data_dict_Adobe)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        elif call=="tes":
            n_date,n_lst = hv(data_dict_Tesla)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        # Set title
        fig.update_layout(
            title_text="Time series with range slider and selectors"
        )
        
        fig.update_layout(template="presentation")
        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
        updatemenus=[
    ])

        # Save the plot to a temporary HTML file
        temp_file_path = tempfile.NamedTemporaryFile(suffix='.html', delete=True).name
        fig.write_html(temp_file_path)

        # Create a Qt widget to display the Plotly HTML
        self.plot_widget = QWebEngineView(frame)
        self.plot_widget.setUrl(QtCore.QUrl.fromLocalFile(temp_file_path))

        self.plot_widget.setGeometry(geo[0],geo[1],geo[2],geo[3])

class vwap_company(QWidget):
    
    def __init__(self, parent=None,frame=None,call=None,geo=None):
        
        super().__init__(parent)
        # Create a Plotly figure
        fig = go.Figure()
        # Load data
        if call =="IMB":
            ibm_date,ibm_lst = vwap(data_dict_ibm)
            fig.add_trace(
            go.Scatter(x = ibm_date, y = ibm_lst))

        elif call=="WMT":
            meta_date,meta_lst = vwap(data_dict_walmart)
            fig.add_trace(go.Scatter(x=meta_date, y=meta_lst))
            
        elif call == 'MSFT':
            ms_date,ms_lst = vwap(data_dict_ms)
            fig.add_trace(
            go.Scatter(x=ms_date, y=ms_lst)) 
            
        elif call=="NVDA": 
            n_date,n_lst = vwap(data_dict_nvidia)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
            
        elif call=="NFL": 
            n_date,n_lst = vwap(data_dict_Netflix)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        
        elif call=='ap':
            n_date,n_lst = vwap(data_dict_apple)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        elif call=='ad':
            n_date,n_lst = vwap(data_dict_Adobe)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        elif call=="tes":
            n_date,n_lst = vwap(data_dict_Tesla)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        # Set title
        fig.update_layout(
            title_text="Time series with range slider and selectors"
        )
        fig.update_layout(template="xgridoff")
        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
        updatemenus=[
    ])

        # Save the plot to a temporary HTML file
        temp_file_path = tempfile.NamedTemporaryFile(suffix='.html', delete=True).name
        fig.write_html(temp_file_path)

        # Create a Qt widget to display the Plotly HTML
        self.plot_widget = QWebEngineView(frame)
        self.plot_widget.setUrl(QtCore.QUrl.fromLocalFile(temp_file_path))

        self.plot_widget.setGeometry(geo[0],geo[1],geo[2],geo[3])

class rsi_company(QWidget):
    
    def __init__(self, parent=None,frame=None,call=None,geo=None):
        
        super().__init__(parent)
        # Create a Plotly figure
        fig = go.Figure()
        # Load data
        if call =="IMB":
            ibm_date,ibm_lst = rsi(data_dict_ibm)
            fig.add_trace(
            go.Scatter(x = ibm_date, y = ibm_lst))

        elif call=="WMT":
            meta_date,meta_lst = rsi(data_dict_walmart)
            fig.add_trace(go.Scatter(x=meta_date, y=meta_lst))
            
        elif call == 'MSFT':
            ms_date,ms_lst = rsi(data_dict_ms)
            fig.add_trace(
            go.Scatter(x=ms_date, y=ms_lst)) 
            
        elif call=="NVDA": 
            n_date,n_lst = rsi(data_dict_nvidia)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
            
        elif call=="NFL": 
            n_date,n_lst = rsi(data_dict_Netflix)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
                    
        elif call=='ap':
            n_date,n_lst = rsi(data_dict_apple)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        elif call=='ad':
            n_date,n_lst = rsi(data_dict_Adobe)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        elif call=="tes":
            n_date,n_lst = rsi(data_dict_Tesla)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
        # Set title
        fig.update_layout(
            title_text="Time series with range slider and selectors"
        )
        fig.update_layout(template="xgridoff")
        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
        updatemenus=[
    ])

        # Save the plot to a temporary HTML file
        temp_file_path = tempfile.NamedTemporaryFile(suffix='.html', delete=True).name
        fig.write_html(temp_file_path)

        # Create a Qt widget to display the Plotly HTML
        self.plot_widget = QWebEngineView(frame)
        self.plot_widget.setUrl(QtCore.QUrl.fromLocalFile(temp_file_path))

        self.plot_widget.setGeometry(geo[0],geo[1],geo[2],geo[3])

class boulinder_company(QWidget):
    
    def __init__(self, parent=None,frame=None,call=None,geo=None):
        
        super().__init__(parent)
        # Create a Plotly figure
        fig = go.Figure()
        # Load data
        if call =="IMB":
            ibm_date,ibm_lst ,ibm_sig= boulinder(data_dict_ibm)
            fig.add_trace(
            go.Scatter(x = ibm_date, y = ibm_lst))
            fig.add_trace(
            go.Scatter(x = ibm_date, y = ibm_sig))
            
        elif call=="WMT":
            meta_date,meta_lst ,meta_sig= boulinder(data_dict_walmart)
            fig.add_trace(go.Scatter(x=meta_date, y=meta_lst))
            fig.add_trace(go.Scatter(x=meta_date, y=meta_sig))
            
        elif call == 'MSFT':
            ms_date,ms_lst,ms_sig = boulinder(data_dict_ms)
            fig.add_trace(
            go.Scatter(x=ms_date, y=ms_lst)) 
            fig.add_trace(
            go.Scatter(x=ms_date, y=ms_sig)) 
            
        elif call=="NVDA": 
            n_date,n_lst,n_sig = boulinder(data_dict_nvidia)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
            fig.add_trace(
            go.Scatter(x=n_date, y=n_sig))
            
        elif call=="NFL": 
            n_date,n_lst,n_sig = boulinder(data_dict_Netflix)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
            fig.add_trace(
            go.Scatter(x=n_date, y=n_sig))
        elif call=="ap": 
            n_date,n_lst,n_sig = boulinder(data_dict_apple)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
            fig.add_trace(
            go.Scatter(x=n_date, y=n_sig))
            
        elif call=="ad": 
            n_date,n_lst,n_sig = boulinder(data_dict_Adobe)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
            fig.add_trace(
            go.Scatter(x=n_date, y=n_sig))
            
        elif call=="tes": 
            n_date,n_lst,n_sig = boulinder(data_dict_Tesla)
            fig.add_trace(
            go.Scatter(x=n_date, y=n_lst))
            fig.add_trace(
            go.Scatter(x=n_date, y=n_sig))
        # Set title
        fig.update_layout(
            title_text="Time series with range slider and selectors"
        )
        fig.update_layout(template="xgridoff")
        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
        updatemenus=[
    ])

        # Save the plot to a temporary HTML file
        temp_file_path = tempfile.NamedTemporaryFile(suffix='.html', delete=True).name
        fig.write_html(temp_file_path)

        # Create a Qt widget to display the Plotly HTML
        self.plot_widget = QWebEngineView(frame)
        self.plot_widget.setUrl(QtCore.QUrl.fromLocalFile(temp_file_path))

        self.plot_widget.setGeometry(geo[0],geo[1],geo[2],geo[3])


class MCAD_company(QWidget):
    
    def __init__(self, parent=None,frame=None,call=None,geo=None):
        
        super().__init__(parent)
        # Create a Plotly figure
        fig = go.Figure()

        if call =="IMB":
            ibm_date,ibm_lst ,ibm_sig,imb_his= macd(data_dict_ibm)
            fig.add_trace(go.Bar(x=ibm_date, y = imb_his,name ="histogram"))
            fig.add_trace(
                go.Scatter(x = ibm_date, y = ibm_lst,name='MACD line'))
            fig.add_trace(
                go.Scatter(x = ibm_date, y = ibm_sig,name="signal line"))
            
        elif call == "WMT":
            meta_date,meta_lst ,meta_sig,meta_his= macd(data_dict_walmart)
            fig.add_trace(
                go.Scatter(x=meta_date, y=meta_lst))
            fig.add_trace(
                go.Scatter(x =meta_date, y = meta_sig,name="signal line"))
            fig.add_trace(go.Bar(x=meta_date, y = meta_his,name ="histogram"))

        elif call == "MSFT":
            ms_date,ms_lst,ms_sig,ms_his = macd(data_dict_ms)
            fig.add_trace(
                go.Scatter(x=ms_date, y=ms_lst))
            fig.add_trace(
                go.Scatter(x =ms_date, y = ms_sig,name="signal line"))
            fig.add_trace(go.Bar(x=ms_date, y = ms_his,name ="histogram"))

        elif call=="NVDA":
            n_date,n_lst,n_sig,n_his = macd(data_dict_nvidia)
            fig.add_trace(
                go.Scatter(x=n_date, y=n_lst))
            fig.add_trace(
                go.Scatter(x =n_date, y = n_sig,name="signal line"))
            fig.add_trace(go.Bar(x=n_date, y = n_his,name ="histogram"))
            
        elif call=="NFL":
            net_date,net_lst,net_sig,net_his = macd(data_dict_Netflix)
            fig.add_trace(
                go.Scatter(x=net_date, y=net_lst))
            fig.add_trace(
                go.Scatter(x =net_date, y = net_sig,name="signal line"))
            fig.add_trace(go.Bar(x=net_date, y = net_his,name ="histogram"))
            
        elif call=="ap":
            n_date,n_lst,n_sig,n_his = macd(data_dict_apple)
            fig.add_trace(
                go.Scatter(x=n_date, y=n_lst))
            fig.add_trace(
                go.Scatter(x =n_date, y = n_sig,name="signal line"))
            fig.add_trace(go.Bar(x=n_date, y = n_his,name ="histogram"))
            
        elif call=="ad":
            net_date,net_lst,net_sig,net_his = macd(data_dict_Adobe)
            fig.add_trace(
                go.Scatter(x=net_date, y=net_lst))
            fig.add_trace(
                go.Scatter(x =net_date, y = net_sig,name="signal line"))
            fig.add_trace(go.Bar(x=net_date, y = net_his,name ="histogram"))
        elif call=="tes":
            net_date,net_lst,net_sig,net_his = macd(data_dict_Tesla)
            fig.add_trace(
                go.Scatter(x=net_date, y=net_lst))
            fig.add_trace(
                go.Scatter(x =net_date, y = net_sig,name="signal line"))
            fig.add_trace(go.Bar(x=net_date, y = net_his,name ="histogram"))
        # Set title
        fig.update_layout(
            title_text="Time series with range slider and selectors"
        )

        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ))
        fig.update_layout(template="seaborn")

        # Save the plot to a temporary HTML file
        temp_file_path = tempfile.NamedTemporaryFile(suffix='.html', delete=True).name
        fig.write_html(temp_file_path)

        # Create a Qt widget to display the Plotly HTML
        self.plot_widget = QWebEngineView(frame)
        self.plot_widget.setUrl(QtCore.QUrl.fromLocalFile(temp_file_path))

        self.plot_widget.setGeometry(geo[0],geo[1],geo[2],geo[3])

class Simple_moving_animate(QWidget):
    def __init__(self, parent=None,frame=None,pivot_df=None,val=None,Name=None, choice=[0,1],range_x=[0,400]):# Val is list containg list of vla
        super().__init__(parent)
        # Create a Plotly figure
        numOfRows = len(choice) # No of Countries
        numOfCols = len(pivot_df) # No of years + one column for a country
        numOfFrames = numOfCols -1
        xaxis_range = [0,numOfFrames + 2]
        # While, testing the code, test with low numbers:
        # Initial State of the data
        # First we are just seeing it for afghanistan

        x_init = np.array([1])


        initial_data = []
        for cont_ind in choice:
            y_axis = np.array(val[cont_ind][0])
            initial_data.append(go.Scatter(x =x_init, y = y_axis,mode = "lines",name = Name[cont_ind]))
        initial_max = 600

        # Frames
        frames = []
        for f in range(1,numOfFrames+1,10):
            x_axis = np.arange(1,f+1)
            curr_data = []
            title_names = []
            start = "For " + str(pivot_df[f-1])
            for cont_ind in choice:

                curr_country = Name[cont_ind]
                y_axis = np.array(val[cont_ind][1:f+1])
                curr_data.append(go.Scatter(x = x_axis, y = y_axis,mode = "lines", name = curr_country,text=str(pivot_df[f-1])))
    
            curr_frame = go.Frame(data = curr_data, layout = {"title":"Animating_graph"})
            frames.append(curr_frame)
        
        figure = go.Figure(
            data = initial_data,
            layout = {
                "title":"Line Chart Race",
                "xaxis":{"range":xaxis_range, "visible":True, "showline":True},
                "yaxis":{"range":range_x, "visible":True, "showline":True,}
                },
            frames = frames,)
            
        figure["layout"]["updatemenus"] = [
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 0, "redraw": False},
                                        "fromcurrent": True, "transition": {"duration": 0,
                                                                            "easing": "quadratic-in-out"}}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate",
                                        "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }
        ]

        figure.update_layout(template='plotly_dark')
        # Save the plot to a temporary HTML file
        temp_file_path = tempfile.NamedTemporaryFile(suffix='.html', delete=True).name
        figure.write_html(temp_file_path)

        # Create a Qt widget to display the Plotly HTML
        self.plot_widget = QWebEngineView(frame)
        self.plot_widget.setUrl(QtCore.QUrl.fromLocalFile(temp_file_path))

        self.plot_widget.setGeometry(10,1100,1100,600)
        
class boulinder_graph(QWidget):
    
    def __init__(self, parent=None,frame=None,visible=True):
        
        super().__init__(parent)
        # Create a Plotly figure
        
        ibm_date,ibm_lst ,ibm_sig= boulinder(data_dict_ibm)
        meta_date,meta_lst ,meta_sig= boulinder(data_dict_walmart)
        ms_date,ms_lst,ms_sig = boulinder(data_dict_ms)
        n_date,n_lst,n_sig = boulinder(data_dict_nvidia)
        net_date,net_lst,net_sig = boulinder(data_dict_Netflix)
        # Load data
        # Create figure
        fig = go.Figure()
            
        fig.add_trace(
            go.Scatter(x = ibm_date, y = ibm_lst,name='High'))
        fig.add_trace(
            go.Scatter(x = ibm_date, y = ibm_sig,name="Low"))
        
        fig.add_trace(
            go.Scatter(x=meta_date, y=meta_lst, visible=False,name="High"))
        fig.add_trace(
            go.Scatter(x =meta_date, y = meta_sig,name="Low",visible=False))
        
        fig.add_trace(
            go.Scatter(x=ms_date, y=ms_lst, visible=False,name="High"))
        fig.add_trace(
            go.Scatter(x =ms_date, y = ms_sig,name="Low",visible=False))
        
        fig.add_trace(
            go.Scatter(x=n_date, y=n_lst, visible=False,name="High"))
        fig.add_trace(
            go.Scatter(x =n_date, y = n_sig,name="Low",visible=False))
        
        fig.add_trace(
            go.Scatter(x=n_date, y=net_lst, visible=False,name="High"))
        fig.add_trace(
            go.Scatter(x =n_date, y = net_sig,name="Low",visible=False))
        
        # Set title
        fig.update_layout(
            title_text="Time series with range slider and selectors"
        )
        fig.update_layout(template="seaborn")
        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
        updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="IBM",
                     method="update",
                     args=[{"visible": [True,True,False,False,False,False,False ,False,False ,False]}]),
                dict(label="WALLMART",
                     method="update",
                     args=[{"visible": [False, False,True,True,False,False, False, False,False ,False]},
                           ]),
                dict(label="MICROSOFT",
                     method="update",
                     args=[{"visible": [False ,False, False,False,True,True,False ,False,False ,False]}
                           ]),
                dict(label="NVIDIA",
                     method="update",
                     args=[{"visible": [False, False,False, False, False,False,True,True,False ,False]}]),
                dict(label="NETFLIX",
                     method="update",
                     args=[{"visible": [False, False,False, False, False,False,False ,False,True,True]}]),
            ]),
            x = 0.4,
            y= 1.12,
            direction = "right",
        )
    ])

        # Save the plot to a temporary HTML file
        temp_file_path = tempfile.NamedTemporaryFile(suffix='.html', delete=True).name
        fig.write_html(temp_file_path)

        # Create a Qt widget to display the Plotly HTML
        self.plot_widget = QWebEngineView(frame)
        self.plot_widget.setUrl(QtCore.QUrl.fromLocalFile(temp_file_path))

        self.plot_widget.setGeometry(10,300,1100,600)


class MCAD(QWidget):
    
    def __init__(self, parent=None,frame=None,visible=True):
        
        super().__init__(parent)
        # Create a Plotly figure
        
        ibm_date,ibm_lst ,ibm_sig,imb_his= macd(data_dict_ibm)
        meta_date,meta_lst ,meta_sig,meta_his= macd(data_dict_walmart)
        ms_date,ms_lst,ms_sig,ms_his = macd(data_dict_ms)
        n_date,n_lst,n_sig,n_his = macd(data_dict_nvidia)
        n_date,net_lst,net_sig,net_his = macd(data_dict_Netflix)
        n_date,ap_lst,ap_sig,ap_his = macd(data_dict_apple)
        n_date,ad_lst,ad_sig,ad_his = macd(data_dict_Adobe)
        n_date,tes_lst,tes_sig,tes_his = macd(data_dict_Tesla)
        # Load data
        # Create figure
        fig = go.Figure()
        fig.add_trace(go.Bar(x=ibm_date, y = imb_his,name ="histogram"))
           
        fig.add_trace(
            go.Scatter(x = ibm_date, y = ibm_lst,name='MACD line'))
        fig.add_trace(
            go.Scatter(x = ibm_date, y = ibm_sig,name="signal line"))
        
        fig.add_trace(
            go.Scatter(x=meta_date, y=meta_lst, visible=False))
        fig.add_trace(
            go.Scatter(x =meta_date, y = meta_sig,name="signal line",visible=False))
        fig.add_trace(go.Bar(x=meta_date, y = meta_his,visible=False,name ="histogram"))


        fig.add_trace(
            go.Scatter(x=ms_date, y=ms_lst, visible=False))
        fig.add_trace(
            go.Scatter(x =ms_date, y = ms_sig,name="signal line",visible=False))
        fig.add_trace(go.Bar(x=ms_date, y = ms_his,visible=False,name ="histogram"))
        
        fig.add_trace(
            go.Scatter(x=n_date, y=n_lst, visible=False))
        fig.add_trace(
            go.Scatter(x =n_date, y = n_sig,name="signal line",visible=False))
        fig.add_trace(go.Bar(x=n_date, y = n_his,visible=False,name ="histogram"))

        fig.add_trace(
            go.Scatter(x=n_date, y=net_lst, visible=False))
        fig.add_trace(
            go.Scatter(x =n_date, y = net_sig,name="signal line",visible=False))
        fig.add_trace(go.Bar(x=n_date, y = net_his,visible=False,name ="histogram"))
        #apple
        fig.add_trace(
            go.Scatter(x=n_date, y=ap_lst, visible=False))
        fig.add_trace(
            go.Scatter(x =n_date, y =ap_sig,name="signal line",visible=False))
        fig.add_trace(go.Bar(x=n_date, y =ap_his,visible=False,name ="histogram"))
        #adobe
        fig.add_trace(
            go.Scatter(x=n_date, y=ad_lst, visible=False))
        fig.add_trace(
            go.Scatter(x =n_date, y =ad_sig,name="signal line",visible=False))
        fig.add_trace(go.Bar(x=n_date, y =ad_his,visible=False,name ="histogram"))
        #tesla
        fig.add_trace(
            go.Scatter(x=n_date, y=tes_lst, visible=False))
        fig.add_trace(
            go.Scatter(x =n_date, y =tes_sig,name="signal line",visible=False))
        fig.add_trace(go.Bar(x=n_date, y =tes_his,visible=False,name ="histogram"))


        
        # Set title
        fig.update_layout(
            title_text="Time series with range slider and selectors"
        )
        fig.update_layout(template="seaborn")
        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
        updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="IBM",
                     method="update",
                     args=[{"visible": [True,True,True,False,False,False,False ,False, False,False, False, False,False, False, False,False, False, False,False, False, False,False, False, False]}]),
                dict(label="WALLMART",
                     method="update",
                     args=[{"visible": [False ,False, False,True,True,True,False, False, False,False ,False, False,False, False, False,False, False, False,False, False, False,False, False, False]},
                           ]),
                dict(label="MICROSOFT",
                     method="update",
                     args=[{"visible": [False, False, False,False ,False, False,True,True,True,False ,False, False,False, False, False,False, False, False,False, False, False,False, False, False]}
                           ]),
                dict(label="NVIDIA",
                     method="update",
                     args=[{"visible": [False, False, False,False ,False, False,False, False, False,True,True,True,False, False, False,False, False, False,False, False, False,False, False, False]}]),
                dict(label="NETFLIX",
                     method="update",
                     args=[{"visible": [False, False, False,False ,False, False,False, False, False,False, False, False,True,True,True,False, False, False,False, False, False,False, False, False]}]),
                dict(label="APPLE",
                     method="update",
                     args=[{"visible": [False, False, False,False ,False, False,False, False, False,False, False, False,False, False, False,True,True,True,False, False, False,False, False, False]}]),
                dict(label="ADOBE",
                     method="update",
                     args=[{"visible": [False, False, False,False ,False, False,False, False, False,False, False, False,False, False, False,False, False, False,True,True,True,False, False, False]}]),
                dict(label="TESLA",
                     method="update",
                     args=[{"visible": [False, False, False,False ,False, False,False, False, False,False, False, False,False, False, False,False, False, False,False, False, False,True,True,True]}]),
            ]),
            x = 0.4,
            y= 1.12,
            direction = "right",
        )
    ])

        # Save the plot to a temporary HTML file
        temp_file_path = tempfile.NamedTemporaryFile(suffix='.html', delete=True).name
        fig.write_html(temp_file_path)

        # Create a Qt widget to display the Plotly HTML
        self.plot_widget = QWebEngineView(frame)
        self.plot_widget.setUrl(QtCore.QUrl.fromLocalFile(temp_file_path))

        self.plot_widget.setGeometry(10,300,1100,600)
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Stock Market Analysis')
        self.setGeometry(0, 0, 1410, 720)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.font = QFont()
        self.font.setPointSize(12)  # Adjust the font size as needed
        self.font.setWeight(QFont.Normal)  # Adjust the font weight as needed
        
        self.font1 = QFont()
        self.font1.setPointSize(25)  # Adjust the font size as needed
        self.font1.setWeight(QFont.Normal)
        # Create a central widget
        self.widget = QWidget(self)
        self.widget.setGeometry(250, -2, 1175, 720)
        
        # Create a horizontal layout for the central widget
        self.central_layout = QHBoxLayout(self.widget)
        # Create the side menu list
        self.side_menu = QListWidget(self)
        # Style sheet for side menu: set background color, text color, padding, and font size
        self.side_menu.setStyleSheet(
            "QListView::item:hover{background :rgb(194, 214, 214);}"
            "QListView::item:selected{background :rgb(194, 214, 214);}"

            "QListWidget"
                                  "{"
                        
                                  "background : black;color:white"
                                  "}"
            
        
        )

        self.side_menu.setFixedWidth(260)  # Set width of the side menu
        self.side_menu.setGeometry(-2,0,260,720)
        # Add headings and items to the side menu
        self.add_heading('\n Metrics')
        self.add_item('     Simple Moving Average', 'sma')
        self.add_item('     Exponential Moving Average', 'ema')
        self.add_item('     MACD', 'macd')
        self.add_item('     Historical Volatility', 'hv')
        self.add_item('     VWAP', 'vwap')
        self.add_item('     Relative Strength Index', 'rsi')
        self.add_item('     Bollinger Bands', 'bands')
        self.add_heading('\nCompanies')
        self.add_item('     IBM', 'company_a')
        self.add_item('     Microsoft', 'company_c')
        self.add_item('     Walmart', 'company_f')        
        self.add_item('     Nvidia', 'company_i')
        self.add_item('     Netflix', 'company_h')
        self.add_item('     Apple', 'company_b')        
        self.add_item('     Adobe', 'company_j')
        self.add_item('     Tesla', 'company_e')
        # Create a stacked widget to hold the different pages
        self.stacked_widget = QStackedWidget(self)
        self.sma_text = "<b>Simple Moving Average (SMA)<b>"
        self.sma_discription = "A simple moving average (SMA) calculates the average of a selected range of prices, usually closing prices, by the number of periods in that range.A simple moving average (SMA) is an arithmetic moving average calculated by adding recent prices and then dividing that figure by the number of time periods in the calculation average. For example, one could add the closing price of a security for a number of time periods and then divide this total by that same number of periods. Short-term averages respond quickly to changes in the price of the underlying security, while long-term averages are slower to react."

        self.ema_text='<b>Exponential Moving Average (EMA)<b>'
        self.ema_discription = "An exponential moving average (EMA) is a type of moving average (MA) that places a greater weight and significance on the most recent data points.\nThe exponential moving average is also referred to as the exponentially weighted moving average. An exponentially weighted moving average reacts\nmore significantly to recent price changes than a simple moving average simple moving average (SMA), which applies an equal weight to all\nobservations in the period."
        # Create pages for each option
        self.hv_text = "<b>Historical Volatility (HV)<b>"
        self.hv_discription = "Historical volatility (HV) is a statistical measure of the dispersion of returns for a given security or market index over a given period of time. Generally, this measure is calculated by determining the average deviation from the average price of a financial instrument in the given time period. Using standard deviation is the most common, but not the only, way to calculate historical volatility. The higher the historical volatility value,the riskier the security. However, that is not necessarily a bad result as risk works both ways—bullish and bearish. Historical volatility is also used in all types of risk valuations. Stocks with a high historical volatility usually require a higher risk tolerance."
        self.vwap_text = '<b>Volume-Weighted Average Price (VWAP)<b>'
        self.vwap_description = "The volume-weighted average price (VWAP) is a technical analysis indicator used on intraday charts that resets at the start of every new trading session. It's a trading benchmark that represents the average price a security has traded at throughout the day, based on both volume and price. VWAP is important because it provides traders with pricing insight into both the trend and value of a security.VWAP is used in different ways by traders. Traders may use VWAP as a trend confirmation tool and build trading rules around it. For instance, they may consider stocks with prices below VWAP as undervalued and those with prices above it as overvalued."

        self.rsi_text = '<b>Relative Strength Index (RSI)<b>'
        self.rsi_description = "The relative strength index (RSI) is a momentum indicator used in technical analysis. RSI measures the speed and magnitude of a security's recent price changes to evaluate overvalued or undervalued conditions in the price of that security.The RSI is displayed as an oscillator (a line graph) on a scale of zero to 100. The RSI can do more than point to overbought and oversold securities. It can also indicate securities that may be primed for a trend reversal or corrective pullback in price. It can signal when to buy and sell. Traditionally, an RSI reading of 70 or above indicates an overbought situation. A reading of 30 or below indicates an oversold condition."

        self.boulinder_text = '<b>Bollinger Bands<b>'
        self.bolinder_description = "Bollinger Bands, a popular tool among investors and traders, helps gauge the volatility of stocks and other securities to determine if they are over or undervalued. Developed in the 1980s by financial analyst John Bollinger, the bands appear on stock charts as three lines that move with the price. The center line is the stock price's 20-day simple moving average (SMA). The upper and lower bands are set at a certain number of standard deviations, usually two, above and below the middle line. The bands widen when a stock's price becomes more volatile and contract when it is more stable."
        self.create_page('sma', '<b>Simple Moving Average (SMA)<b>',"A simple moving average (SMA) calculates the average of a selected range of prices, usually closing prices, by the number of periods in that range.A simple moving average (SMA) is an arithmetic moving average calculated by adding recent prices and then dividing that figure by the number of time periods in the calculation average. For example, one could add the closing price of a security for a number of time periods and then divide this total by that same number of periods. Short-term averages respond quickly to changes in the price of the underlying security, while long-term averages are slower to react.",[0,1],'sma')
        self.create_page('ema', '<b>Exponential Moving Average (EMA)<b>',"An exponential moving average (EMA) is a type of moving average (MA) that places a greater weight and significance on the most recent data points. The exponential moving average is also referred to as the exponentially weighted moving average. An exponentially weighted moving average reacts more significantly to recent price changes than a simple moving average simple moving average (SMA), which applies an equal weight to all observations in the period.",[0,1],'ema')
        self.create_page('macd', "<b>Moving average convergence/divergence<b>", "(MACD) is a technical indicator to help investors identify price trends, measure trend momentum, and identify market entry points for buying or selling. Moving average convergence/divergence (MACD) is a trend-following momentum indicator that shows the relationship between two exponential moving averages (EMAs) of a security’s price. MACD was developed in the 1970s by Gerald Appel. The MACD line is calculated by subtracting the 26-period EMA from the 12-period EMA. The calculation creates the MACD line. A nine-day EMA of the MACD line is called the signal line, plotted on top of the MACD line, which can function as a trigger for buy or sell signals.",None,"macd",show=True)
        self.create_page('hv', '<b>Historical Volatility (HV)<b>',"Historical volatility (HV) is a statistical measure of the dispersion of returns for a given security or market index over a given period of time. Generally, this measure is calculated by determining the average deviation from the average price of a financial instrument in the given time period. Using standard deviation is the most common, but not the only, way to calculate historical volatility. The higher the historical volatility value,the riskier the security. However, that is not necessarily a bad result as risk works both ways—bullish and bearish. Historical volatility is also used in all types of risk valuations. Stocks with a high historical volatility usually require a higher risk tolerance.",graph='hv',head_2=[0,1])
        self.create_page('vwap', '<b>Volume-Weighted Average Price (VWAP)<b>',"The volume-weighted average price (VWAP) is a technical analysis indicator used on intraday charts that resets at the start of every new trading session. It's a trading benchmark that represents the average price a security has traded at throughout the day, based on both volume and price. VWAP is important because it provides traders with pricing insight into both the trend and value of a security.VWAP is used in different ways by traders. Traders may use VWAP as a trend confirmation tool and build trading rules around it. For instance, they may consider stocks with prices below VWAP as undervalued and those with prices above it as overvalued.",graph="vwap",head_2=[0,1])
        self.create_page('rsi', '<b>Relative Strength Index (RSI)<b>',"The relative strength index (RSI) is a momentum indicator used in technical analysis. RSI measures the speed and magnitude of a security's recent price changes to evaluate overvalued or undervalued conditions in the price of that security.The RSI is displayed as an oscillator (a line graph) on a scale of zero to 100. The RSI can do more than point to overbought and oversold securities. It can also indicate securities that may be primed for a trend reversal or corrective pullback in price. It can signal when to buy and sell. Traditionally, an RSI reading of 70 or above indicates an overbought situation. A reading of 30 or below indicates an oversold condition.",graph="rsi",head_2=[0,1])
        self.create_page('bands', '<b>Bollinger Bands<b>',"Bollinger Bands, a popular tool among investors and traders, helps gauge the volatility of stocks and other securities to determine if they are over or undervalued. Developed in the 1980s by financial analyst John Bollinger, the bands appear on stock charts as three lines that move with the price. The center line is the stock price's 20-day simple moving average (SMA). The upper and lower bands are set at a certain number of standard deviations, usually two, above and below the middle line. The bands widen when a stock's price becomes more volatile and contract when it is more stable.",graph="bands",head_2=[0,1])

        
        self.create_page('company_a', '<b>International Business Machines Corporation<b>',"IBM, or International Business Machines Corporation, is a global technology and consulting company headquartered in Armonk, New York. Known for its innovations in hardware, software, and services, IBM has been a major player in the IT industry for over a century. The company is also a leader in cloud computing, AI, and data analytics, serving businesses worldwide.",graph = "IMB")
        self.create_page('company_c', '<b>Microsoft Corp<b>',"Microsoft is a leading global technology company based in Redmond, Washington, known for its software, hardware, and cloud services. The company is famous for its Windows operating system, Microsoft Office suite, and Azure cloud platform. Microsoft also develops consumer electronics, including the Xbox gaming console and Surface devices. The company is a major player in artificial intelligence and business solutions, serving a wide range of industries and customers worldwide.",graph="MSFT")
        self.create_page('company_f', '<b>Walmart Inc<b>',"Walmart Inc. (WMT) is a global retail corporation headquartered in Bentonville, Arkansas, known for its large discount department stores, supercenters, and e-commerce presence. The company offers a wide range of products including groceries, electronics, clothing, and household goods at competitive prices. Walmart is recognized for its vast supply chain network and commitment to everyday low prices for its customers.",graph="WMT")        
        self.create_page('company_i', '<b>NVIDIA Corp<b>',"NVIDIA Corporation (NVDA) is a leading technology company based in Santa Clara, California, known for its advanced graphics processing units (GPUs) and AI computing technology. The company’s GPUs are widely used in gaming, data centers, and professional visualization. NVIDIA is a major player in AI research and development, providing key technologies for machine learning, autonomous vehicles, and high-performance computing applications.",graph="NVDA")
        self.create_page('company_h', '<b>Netflix Inc<b>',"Netflix, Inc. (NFLX) is a leading global streaming entertainment service that provides a wide range of TV shows, movies, documentaries, and original content to millions of subscribers worldwide. Based in Los Gatos, California, Netflix is known for its innovative content production and data-driven approach to audience preferences. The company has significantly impacted the entertainment industry, transforming how people watch and consume media.",graph="NFL")
        self.create_page('company_b', '<b>Apple Inc<b>',"Apple Inc. is a global technology company based in Cupertino, California, known for its innovative consumer electronics, software, and services. Its popular products include the iPhone, iPad, Mac computers, and Apple Watch, which have become iconic in the industry. Apple emphasizes sleek design and user-friendly interfaces, and its services include iCloud, Apple Music, and Apple TV+.",graph="ap")
        self.create_page('company_j', '<b>Adobe Inc<b>',"Adobe Inc. (ADBE) is a global software company headquartered in San Jose, California, known for its creative and digital solutions. The company's flagship products include Adobe Photoshop, Illustrator, and Premiere Pro, which are industry standards for digital media creation and editing. Adobe also offers a suite of cloud-based services, such as Adobe Creative Cloud and Adobe Document Cloud, enabling professionals and businesses to create, manage, and deliver digital content efficiently.",graph="ad")
        self.create_page('company_e', '<b>Tesla Inc<b>',"Tesla, Inc. (TSLA) is an American electric vehicle (EV) and clean energy company based in Palo Alto, California. It is known for its innovative EVs, such as the Model S, Model 3, and Model Y, which feature cutting-edge technology and autonomous driving capabilities. Tesla also produces solar panels, energy storage solutions, and operates a growing network of Supercharger stations worldwide. The company is recognized for its commitment to sustainability and its goal of accelerating the global transition to renewable energy.",graph='tes')
        # Add the side menu and stacked widget to the central layout
        self.central_layout.addWidget(self.stacked_widget)

        #Connect the side menu selection changed signal to a slot function
        self.side_menu.currentItemChanged.connect(self.on_item_clicked)

        # Display the first page initially
        self.side_menu.setCurrentRow(0)
        self.show_page('pe_ratio')

    def add_heading(self, heading):
        # Create a QListWidgetItem for the heading
        item = QListWidgetItem(heading)
        # Set the flags to prevent selection and clicking
        self.side_menu.addItem(item)
        item.setFont(self.font1)

    def add_item(self, text, data):
        # Create a QListWidgetItem for the item
        item = QListWidgetItem(text)
        item.setData(Qt.UserRole, data)  # Store data to identify the item
        item.setSizeHint(QSize(0, 40))  # Adjust height for padding
        self.side_menu.addItem(item)
        item.setFont(self.font)

    def create_page(self, page_id, title,data,head_2 = None,graph=None,show=None):
        stylesheet = """
QCheckBox {
    background-color: transparent;
    color: #14C7F4; /* Text color */
    font-size: 16px; /* Text size */
    padding: 10px; /* Padding around the checkbox */
}

QCheckBox::indicator {
    width: 20px; /* Size of the checkbox */
    height: 20px;
    border: 2px solid #000000 ; /* Border around the checkbox */
}

QCheckBox::indicator:checked {
    background-color:#d3d3d3; /* Background color when checked */
}

QCheckBox::indicator:hover {
    border: 2px solid #d3d3d3; /* Border color on hover */
}
"""
        page = QWidget()
        page.setGeometry(0, 0, 1400, 1600)
        page.setStyleSheet("background-color: white")
        
        # Create a layout for the page
        layout = QVBoxLayout(page)
        
        # Create a scroll area
        scroll_area = QScrollArea(page)
        scroll_area.setGeometry(0,0,1400,720)
        scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its content
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Set vertical scroll bar policy
        
        # Create a frame to hold the content
        frame = QFrame(page)
        frame.setGeometry(0,0,1280,720)
        frame.setStyleSheet("background-color: white")
        
        # Create a layout for the frame

        # Add the content to the frame
        label = QLabel(frame)
        label.setText(title)
        label.setAlignment(Qt.AlignLeft)  

        label.setGeometry(20,20,1200, 100)
        # label.setFont(self.font1)  # Assuming self.font1 is defined elsewhere
        label.setFont(self.font1)# Align the label to the center
        line = QLabel(frame)
        line.setStyleSheet("background-color: black;")
        line.setFixedHeight(3)
        line.setGeometry(0,110,1280, 3)  # Set the width and height of the line
        # line.setStyleSheet("background-color: black;")  # Set the background color of the line

        label1 = QLabel(frame)
        label1.setText(data)
        # label1.setFont(self.font)  # Assuming self.font is defined elsewhere
        label1.setFont(self.font)# Align the label to the center
        label1.setGeometry(13,120,1100, 150)
        label1.setWordWrap(True)

        
        # Set the minimum size for the frame
        if page_id[:-2] == "company":
            frame.setMinimumSize(1000, 5000)
        else:
            frame.setMinimumSize(1000, 1700)
        
        # Set the frame as the widget for the scroll area
        scroll_area.setWidget(frame)
        
        layout.addWidget(scroll_area)  # Add the scroll area to the layout
        page.setLayout(layout)
        if graph =="sma":
            val=head_2
            Simple_moving(None, frame,call="sma")
            button = QPushButton(parent=frame,text='Animate')
            button.setStyleSheet('''
                QPushButton {
                    background-color: #14C7F4;
                    border-style: solid;
                    border-radius: 5px;
                    border-width: 2px;
                    border-color: #0E94C1;
                    color: white;
                    padding: 10px 20px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #0E94C1;
                }
                QPushButton:pressed {
                    background-color: #0A728C;
                    border-color: #095E73;
                }
            ''')
            button.setGeometry(350,1020,100,50)
            b1 = QCheckBox(parent=frame,text="IBM")
            b1.setGeometry(30,900,150,80)
            b2 = QCheckBox(parent=frame,text="WALLMART")
            b2.setGeometry(190,900,150,80)
            b4 = QCheckBox(parent=frame,text="NVIDIA")
            b4.setGeometry(495,900,150,80)
            b3 = QCheckBox(parent=frame,text="MICROSOFT")
            b3.setGeometry(340,900,150,80)
            b5 = QCheckBox(parent=frame,text="NETFLIX")
            b5.setGeometry(660,900,150,80)
            b6 = QCheckBox(parent=frame,text="APPLE")
            b6.setGeometry(810,900,150,80)
            b7 = QCheckBox(parent=frame,text="ADOBE")
            b7.setGeometry(30,1000,150,80)
            b8 = QCheckBox(parent=frame,text="TESLA")
            b8.setGeometry(190,1000,150,80)
            b1.setStyleSheet(stylesheet)
            b2.setStyleSheet(stylesheet)
            b3.setStyleSheet(stylesheet)
            b4.setStyleSheet(stylesheet)
            b5.setStyleSheet(stylesheet)
            b6.setStyleSheet(stylesheet)
            b7.setStyleSheet(stylesheet)
            b8.setStyleSheet(stylesheet)
            if 0 in val:
                b1.setChecked(True)
            else:
                b1.setChecked(False)
            if 1 in val:
                b2.setChecked(True)
            else:
                b2.setChecked(False)
            if 2 in val:
                b3.setChecked(True)
            else:
                b3.setChecked(False)
            if 3 in val:
                b4.setChecked(True)
            else:
                b4.setChecked(False)
            if 4 in val:
                b5.setChecked(True)
            else:
                b5.setChecked(False)
            if 5 in val:
                b6.setChecked(True)
            else:
                b6.setChecked(False)
            if 6 in val:
                b7.setChecked(True)
            else:
                b7.setChecked(False)
            if 7 in val:
                b8.setChecked(True)
            else:
                b8.setChecked(False)
            
            b1.stateChanged.connect(lambda:self.b1_(val,b1,"sma"))
            b2.stateChanged.connect(lambda:self.b2_(val,b2,"sma"))
            b3.stateChanged.connect(lambda:self.b3_(val,b3,"sma"))
            b4.stateChanged.connect(lambda:self.b4_(val,b4,"sma"))
            b5.stateChanged.connect(lambda:self.b5_(val,b5,"sma"))
            b6.stateChanged.connect(lambda:self.b6_(val,b6,"sma"))
            b7.stateChanged.connect(lambda:self.b7_(val,b7,"sma"))
            b8.stateChanged.connect(lambda:self.b8_(val,b8,"sma"))
            button.clicked.connect(lambda:self.bt_(val,"sma"))
            ibm_date,ibm_lst = movng_av(data_dict_ibm)
            meta_date,meta_lst = movng_av(data_dict_walmart)
            ms_date,ms_lst = movng_av(data_dict_ms)
            n_date,n_lst = movng_av(data_dict_nvidia)
            net_date,net_lst = movng_av(data_dict_Netflix)
            net_date,ap_lst = movng_av(data_dict_apple)
            net_date,ad_lst = movng_av(data_dict_Adobe)
            net_date,tes_lst = movng_av(data_dict_Tesla)
            Simple_moving_animate(None,frame=frame,pivot_df=ibm_date,val=[ibm_lst,meta_lst,ms_lst,n_lst,net_lst,ap_lst,ad_lst,tes_lst],Name=['IBM',"WALMART","MICROSOFT","NVIDIA","NETFLIX","APPLE","ADOBE","TESLA"],choice=val)
            
        if graph =="ema":
            val=head_2
            Simple_moving(None, frame,call="ema")
            button = QPushButton(parent=frame,text='Animate')
            button.setStyleSheet('''
                QPushButton {
                    background-color: #14C7F4;
                    border-style: solid;
                    border-radius: 5px;
                    border-width: 2px;
                    border-color: #0E94C1;
                    color: white;
                    padding: 10px 20px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #0E94C1;
                }
                QPushButton:pressed {
                    background-color: #0A728C;
                    border-color: #095E73;
                }
            ''')
            button.setGeometry(350,1020,100,50)
            b1 = QCheckBox(parent=frame,text="IBM")
            b1.setGeometry(30,900,150,80)
            b2 = QCheckBox(parent=frame,text="WALLMART")
            b2.setGeometry(190,900,150,80)
            b4 = QCheckBox(parent=frame,text="NVIDIA")
            b4.setGeometry(495,900,150,80)
            b3 = QCheckBox(parent=frame,text="MICROSOFT")
            b3.setGeometry(340,900,150,80)
            b5 = QCheckBox(parent=frame,text="NETFLIX")
            b5.setGeometry(660,900,150,80)
            b6 = QCheckBox(parent=frame,text="APPLE")
            b6.setGeometry(810,900,150,80)
            b7 = QCheckBox(parent=frame,text="ADOBE")
            b7.setGeometry(30,1000,150,80)
            b8 = QCheckBox(parent=frame,text="TESLA")
            b8.setGeometry(190,1000,150,80)
            b1.setStyleSheet(stylesheet)
            b2.setStyleSheet(stylesheet)
            b3.setStyleSheet(stylesheet)
            b4.setStyleSheet(stylesheet)
            b5.setStyleSheet(stylesheet)
            b6.setStyleSheet(stylesheet)
            b7.setStyleSheet(stylesheet)
            b8.setStyleSheet(stylesheet)
            if 0 in val:
                b1.setChecked(True)
            else:
                b1.setChecked(False)
            if 1 in val:
                b2.setChecked(True)
            else:
                b2.setChecked(False)
            if 2 in val:
                b3.setChecked(True)
            else:
                b3.setChecked(False)
            if 3 in val:
                b4.setChecked(True)
            else:
                b4.setChecked(False)
            if 4 in val:
                b5.setChecked(True)
            else:
                b5.setChecked(False)
            if 5 in val:
                b6.setChecked(True)
            else:
                b6.setChecked(False)
            if 6 in val:
                b7.setChecked(True)
            else:
                b7.setChecked(False)
            if 7 in val:
                b8.setChecked(True)
            else:
                b8.setChecked(False)
    
            b1.stateChanged.connect(lambda:self.b1_(val,b1,"ema"))
            b2.stateChanged.connect(lambda:self.b2_(val,b2,"ema"))
            b3.stateChanged.connect(lambda:self.b3_(val,b3,"ema"))
            b4.stateChanged.connect(lambda:self.b4_(val,b4,"ema"))
            b5.stateChanged.connect(lambda:self.b5_(val,b5,"ema"))
            b6.stateChanged.connect(lambda:self.b6_(val,b6,"ema"))
            b7.stateChanged.connect(lambda:self.b7_(val,b7,"ema"))
            b8.stateChanged.connect(lambda:self.b8_(val,b8,"ema"))
            button.clicked.connect(lambda:self.bt_(val,"ema"))
            ibm_date,ibm_lst = movng_ema(data_dict_ibm)
            meta_date,meta_lst = movng_ema(data_dict_walmart)
            ms_date,ms_lst = movng_ema(data_dict_ms)
            n_date,n_lst = movng_ema(data_dict_nvidia)
            net_date,net_lst = movng_ema(data_dict_Netflix)
            net_date,ap_lst = movng_ema(data_dict_apple)
            net_date,ad_lst = movng_ema(data_dict_Adobe)
            net_date,tes_lst = movng_ema(data_dict_Tesla)
            Simple_moving_animate(None,frame=frame,pivot_df=ibm_date,val=[ibm_lst,meta_lst,ms_lst,n_lst,net_lst,ap_lst,ad_lst,tes_lst],Name=['IBM',"WALMART","MICROSOFT","NVIDIA","NETFLIX","APPLE","ADOBE","TESLA"],choice=val)
       
        if graph =="macd":
            MCAD(None,frame=frame,visible=show)
            
        if graph =='hv':
            val=head_2
            Simple_moving(None, frame,call="hv")
            button = QPushButton(parent=frame,text='Animate')
            button.setStyleSheet('''
                QPushButton {
                    background-color: #14C7F4;
                    border-style: solid;
                    border-radius: 5px;
                    border-width: 2px;
                    border-color: #0E94C1;
                    color: white;
                    padding: 10px 20px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #0E94C1;
                }
                QPushButton:pressed {
                    background-color: #0A728C;
                    border-color: #095E73;
                }
            ''')
            button.setGeometry(350,1020,100,50)
            b1 = QCheckBox(parent=frame,text="IBM")
            b1.setGeometry(30,900,150,80)
            b2 = QCheckBox(parent=frame,text="WALLMART")
            b2.setGeometry(190,900,150,80)
            b4 = QCheckBox(parent=frame,text="NVIDIA")
            b4.setGeometry(495,900,150,80)
            b3 = QCheckBox(parent=frame,text="MICROSOFT")
            b3.setGeometry(340,900,150,80)
            b5 = QCheckBox(parent=frame,text="NETFLIX")
            b5.setGeometry(660,900,150,80)
            b6 = QCheckBox(parent=frame,text="APPLE")
            b6.setGeometry(810,900,150,80)
            b7 = QCheckBox(parent=frame,text="ADOBE")
            b7.setGeometry(30,1000,150,80)
            b8 = QCheckBox(parent=frame,text="TESLA")
            b8.setGeometry(190,1000,150,80)
            b1.setStyleSheet(stylesheet)
            b2.setStyleSheet(stylesheet)
            b3.setStyleSheet(stylesheet)
            b4.setStyleSheet(stylesheet)
            b5.setStyleSheet(stylesheet)
            b6.setStyleSheet(stylesheet)
            b7.setStyleSheet(stylesheet)
            b8.setStyleSheet(stylesheet)
            if 0 in val:
                b1.setChecked(True)
            else:
                b1.setChecked(False)
            if 1 in val:
                b2.setChecked(True)
            else:
                b2.setChecked(False)
            if 2 in val:
                b3.setChecked(True)
            else:
                b3.setChecked(False)
            if 3 in val:
                b4.setChecked(True)
            else:
                b4.setChecked(False)
            if 4 in val:
                b5.setChecked(True)
            else:
                b5.setChecked(False)
            if 5 in val:
                b6.setChecked(True)
            else:
                b6.setChecked(False)
            if 6 in val:
                b7.setChecked(True)
            else:
                b7.setChecked(False)
            if 7 in val:
                b8.setChecked(True)
            else:
                b8.setChecked(False)

            b1.stateChanged.connect(lambda:self.b1_(val,b1,"hv"))
            b2.stateChanged.connect(lambda:self.b2_(val,b2,"hv"))
            b3.stateChanged.connect(lambda:self.b3_(val,b3,"hv"))
            b4.stateChanged.connect(lambda:self.b4_(val,b4,"hv"))
            b5.stateChanged.connect(lambda:self.b5_(val,b5,"hv"))
            b6.stateChanged.connect(lambda:self.b6_(val,b6,"hv"))
            b7.stateChanged.connect(lambda:self.b7_(val,b7,"hv"))
            b8.stateChanged.connect(lambda:self.b8_(val,b8,"hv"))
            button.clicked.connect(lambda:self.bt_(val,"hv"))
            ibm_date,ibm_lst = hv(data_dict_ibm)
            meta_date,meta_lst = hv(data_dict_walmart)
            ms_date,ms_lst = hv(data_dict_ms)
            n_date,n_lst = hv(data_dict_nvidia)
            net_date,net_lst = hv(data_dict_Netflix)
            net_date,ap_lst = hv(data_dict_apple)
            net_date,ad_lst = hv(data_dict_Adobe)
            net_date,tes_lst = hv(data_dict_Tesla)
            Simple_moving_animate(None,frame=frame,pivot_df=ibm_date,val=[ibm_lst,meta_lst,ms_lst,n_lst,net_lst,ap_lst,ad_lst,tes_lst],Name=['IBM',"WALMART","MICROSOFT","NVIDIA","NETFLIX","APPLE","ADOBE","TESLA"],choice=val)

        if graph =="vwap":
            val=head_2
            Simple_moving(None, frame,call="vwap")
            button = QPushButton(parent=frame,text='Animate')
            button.setStyleSheet('''
                QPushButton {
                    background-color: #14C7F4;
                    border-style: solid;
                    border-radius: 5px;
                    border-width: 2px;
                    border-color: #0E94C1;
                    color: white;
                    padding: 10px 20px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #0E94C1;
                }
                QPushButton:pressed {
                    background-color: #0A728C;
                    border-color: #095E73;
                }
            ''')
            button.setGeometry(350,1020,100,50)
            b1 = QCheckBox(parent=frame,text="IBM")
            b1.setGeometry(30,900,150,80)
            b2 = QCheckBox(parent=frame,text="WALLMART")
            b2.setGeometry(190,900,150,80)
            b4 = QCheckBox(parent=frame,text="NVIDIA")
            b4.setGeometry(495,900,150,80)
            b3 = QCheckBox(parent=frame,text="MICROSOFT")
            b3.setGeometry(340,900,150,80)
            b5 = QCheckBox(parent=frame,text="NETFLIX")
            b5.setGeometry(660,900,150,80)
            b6 = QCheckBox(parent=frame,text="APPLE")
            b6.setGeometry(810,900,150,80)
            b7 = QCheckBox(parent=frame,text="ADOBE")
            b7.setGeometry(30,1000,150,80)
            b8 = QCheckBox(parent=frame,text="TESLA")
            b8.setGeometry(190,1000,150,80)
            b1.setStyleSheet(stylesheet)
            b2.setStyleSheet(stylesheet)
            b3.setStyleSheet(stylesheet)
            b4.setStyleSheet(stylesheet)
            b5.setStyleSheet(stylesheet)
            b6.setStyleSheet(stylesheet)
            b7.setStyleSheet(stylesheet)
            b8.setStyleSheet(stylesheet)
            if 0 in val:
                b1.setChecked(True)
            else:
                b1.setChecked(False)
            if 1 in val:
                b2.setChecked(True)
            else:
                b2.setChecked(False)
            if 2 in val:
                b3.setChecked(True)
            else:
                b3.setChecked(False)
            if 3 in val:
                b4.setChecked(True)
            else:
                b4.setChecked(False)
            if 4 in val:
                b5.setChecked(True)
            else:
                b5.setChecked(False)
            if 5 in val:
                b6.setChecked(True)
            else:
                b6.setChecked(False)
            if 6 in val:
                b7.setChecked(True)
            else:
                b7.setChecked(False)
            if 7 in val:
                b8.setChecked(True)
            else:
                b8.setChecked(False)
         
            b1.stateChanged.connect(lambda:self.b1_(val,b1,"vwap"))
            b2.stateChanged.connect(lambda:self.b2_(val,b2,"vwap"))
            b3.stateChanged.connect(lambda:self.b3_(val,b3,"vwap"))
            b4.stateChanged.connect(lambda:self.b4_(val,b4,"vwap"))
            b5.stateChanged.connect(lambda:self.b5_(val,b5,"vwap"))
            b6.stateChanged.connect(lambda:self.b6_(val,b6,"vwap"))
            b7.stateChanged.connect(lambda:self.b7_(val,b7,"vwap"))
            b8.stateChanged.connect(lambda:self.b8_(val,b8,"vwap"))
            button.clicked.connect(lambda:self.bt_(val,"vwap"))
            ibm_date,ibm_lst = vwap(data_dict_ibm)
            meta_date,meta_lst = vwap(data_dict_walmart)
            ms_date,ms_lst = vwap(data_dict_ms)
            n_date,n_lst = vwap(data_dict_nvidia)
            net_date,net_lst =vwap(data_dict_Netflix)
            net_date,ap_lst =vwap(data_dict_apple)
            net_date,ad_lst = vwap(data_dict_Adobe)
            net_date,tes_lst = vwap(data_dict_Tesla)
            Simple_moving_animate(None,frame=frame,pivot_df=ibm_date,val=[ibm_lst,meta_lst,ms_lst,n_lst,net_lst,ap_lst,ad_lst,tes_lst],Name=['IBM',"WALMART","MICROSOFT","NVIDIA","NETFLIX","APPLE","ADOBE","TESLA"],choice=val)
        
        if graph =="rsi":
            val=head_2
            Simple_moving(None, frame,call="rsi")
            button = QPushButton(parent=frame,text='Animate')
            button.setStyleSheet('''
                QPushButton {
                    background-color: #14C7F4;
                    border-style: solid;
                    border-radius: 5px;
                    border-width: 2px;
                    border-color: #0E94C1;
                    color: white;
                    padding: 10px 20px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #0E94C1;
                }
                QPushButton:pressed {
                    background-color: #0A728C;
                    border-color: #095E73;
                }
            ''')
            button.setGeometry(350,1020,100,50)
            b1 = QCheckBox(parent=frame,text="IBM")
            b1.setGeometry(30,900,150,80)
            b2 = QCheckBox(parent=frame,text="WALLMART")
            b2.setGeometry(190,900,150,80)
            b4 = QCheckBox(parent=frame,text="NVIDIA")
            b4.setGeometry(495,900,150,80)
            b3 = QCheckBox(parent=frame,text="MICROSOFT")
            b3.setGeometry(340,900,150,80)
            b5 = QCheckBox(parent=frame,text="NETFLIX")
            b5.setGeometry(660,900,150,80)
            b6 = QCheckBox(parent=frame,text="APPLE")
            b6.setGeometry(810,900,150,80)
            b7 = QCheckBox(parent=frame,text="ADOBE")
            b7.setGeometry(30,1000,150,80)
            b8 = QCheckBox(parent=frame,text="TESLA")
            b8.setGeometry(190,1000,150,80)
            b1.setStyleSheet(stylesheet)
            b2.setStyleSheet(stylesheet)
            b3.setStyleSheet(stylesheet)
            b4.setStyleSheet(stylesheet)
            b5.setStyleSheet(stylesheet)
            b6.setStyleSheet(stylesheet)
            b7.setStyleSheet(stylesheet)
            b8.setStyleSheet(stylesheet)
            if 0 in val:
                b1.setChecked(True)
            else:
                b1.setChecked(False)
            if 1 in val:
                b2.setChecked(True)
            else:
                b2.setChecked(False)
            if 2 in val:
                b3.setChecked(True)
            else:
                b3.setChecked(False)
            if 3 in val:
                b4.setChecked(True)
            else:
                b4.setChecked(False)
            if 4 in val:
                b5.setChecked(True)
            else:
                b5.setChecked(False)
            if 5 in val:
                b6.setChecked(True)
            else:
                b6.setChecked(False)
            if 6 in val:
                b7.setChecked(True)
            else:
                b7.setChecked(False)
            if 7 in val:
                b8.setChecked(True)
            else:
                b8.setChecked(False)

            b1.stateChanged.connect(lambda:self.b1_(val,b1,"rsi"))
            b2.stateChanged.connect(lambda:self.b2_(val,b2,"rsi"))
            b3.stateChanged.connect(lambda:self.b3_(val,b3,"rsi"))
            b4.stateChanged.connect(lambda:self.b4_(val,b4,"rsi"))
            b5.stateChanged.connect(lambda:self.b5_(val,b5,"rsi"))
            b6.stateChanged.connect(lambda:self.b6_(val,b6,"rsi"))
            b7.stateChanged.connect(lambda:self.b7_(val,b7,"rsi"))
            b8.stateChanged.connect(lambda:self.b8_(val,b8,"rsi"))
            button.clicked.connect(lambda:self.bt_(val,"rsi"))
            ibm_date,ibm_lst = rsi(data_dict_ibm)
            meta_date,meta_lst = rsi(data_dict_walmart)
            ms_date,ms_lst = rsi(data_dict_ms)
            n_date,n_lst = rsi(data_dict_nvidia)
            net_date,net_lst =rsi(data_dict_Netflix)
            net_date,ap_lst = rsi(data_dict_apple)
            net_date,ad_lst = rsi(data_dict_Adobe)
            net_date,tes_lst = rsi(data_dict_Tesla)
            Simple_moving_animate(None,frame=frame,pivot_df=ibm_date,val=[ibm_lst,meta_lst,ms_lst,n_lst,net_lst,ap_lst,ad_lst,tes_lst],Name=['IBM',"WALMART","MICROSOFT","NVIDIA","NETFLIX","APPLE","ADOBE","TESLA"],choice=val)
            # Simple_moving_animate(None,frame=frame,pivot_df=ibm_date,val=[ibm_lst,meta_lst,ms_lst,n_lst,net_lst],Name=['IBM',"WALMART","MICROSOFT","NVIDIA","NETFLIX"],choice=val)
        
        if graph =="bands":
            val=head_2
            boulinder_graph(None, frame)
            button = QPushButton(parent=frame,text='Animate')
            button.setStyleSheet('''
                QPushButton {
                    background-color: #14C7F4;
                    border-style: solid;
                    border-radius: 5px;
                    border-width: 2px;
                    border-color: #0E94C1;
                    color: white;
                    padding: 10px 20px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #0E94C1;
                }
                QPushButton:pressed {
                    background-color: #0A728C;
                    border-color: #095E73;
                }
            ''')
            button.setGeometry(350,1020,100,50)
            b1 = QCheckBox(parent=frame,text="IBM")
            b1.setGeometry(30,900,150,80)
            b2 = QCheckBox(parent=frame,text="WALLMART")
            b2.setGeometry(190,900,150,80)
            b4 = QCheckBox(parent=frame,text="NVIDIA")
            b4.setGeometry(495,900,150,80)
            b3 = QCheckBox(parent=frame,text="MICROSOFT")
            b3.setGeometry(340,900,150,80)
            b5 = QCheckBox(parent=frame,text="NETFLIX")
            b5.setGeometry(660,900,150,80)
            b6 = QCheckBox(parent=frame,text="APPLE")
            b6.setGeometry(810,900,150,80)
            b7 = QCheckBox(parent=frame,text="ADOBE")
            b7.setGeometry(30,1000,150,80)
            b8 = QCheckBox(parent=frame,text="TESLA")
            b8.setGeometry(190,1000,150,80)
            b1.setStyleSheet(stylesheet)
            b2.setStyleSheet(stylesheet)
            b3.setStyleSheet(stylesheet)
            b4.setStyleSheet(stylesheet)
            b5.setStyleSheet(stylesheet)
            b6.setStyleSheet(stylesheet)
            b7.setStyleSheet(stylesheet)
            b8.setStyleSheet(stylesheet)
            if 0 in val:
                b1.setChecked(True)
            else:
                b1.setChecked(False)
            if 1 in val:
                b2.setChecked(True)
            else:
                b2.setChecked(False)
            if 2 in val:
                b3.setChecked(True)
            else:
                b3.setChecked(False)
            if 3 in val:
                b4.setChecked(True)
            else:
                b4.setChecked(False)
            if 4 in val:
                b5.setChecked(True)
            else:
                b5.setChecked(False)
            if 5 in val:
                b6.setChecked(True)
            else:
                b6.setChecked(False)
            if 6 in val:
                b7.setChecked(True)
            else:
                b7.setChecked(False)
            if 7 in val:
                b8.setChecked(True)
            else:
                b8.setChecked(False)
                
            b1.stateChanged.connect(lambda:self.b1_(val,b1,"bands"))
            b2.stateChanged.connect(lambda:self.b2_(val,b2,"bands"))
            b3.stateChanged.connect(lambda:self.b3_(val,b3,"bands"))
            b4.stateChanged.connect(lambda:self.b4_(val,b4,"bands"))
            b5.stateChanged.connect(lambda:self.b5_(val,b5,"bands"))
            b6.stateChanged.connect(lambda:self.b6_(val,b6,"bands"))
            b7.stateChanged.connect(lambda:self.b7_(val,b7,"bands"))
            b8.stateChanged.connect(lambda:self.b8_(val,b8,"bands"))
            button.clicked.connect(lambda:self.bt_(val,"bands"))
            ibm_date,ibm_lst ,ibm_sig= boulinder(data_dict_ibm)
            meta_date,meta_lst ,meta_sig= boulinder(data_dict_walmart)
            ms_date,ms_lst,ms_sig = boulinder(data_dict_ms)
            n_date,n_lst,n_sig = boulinder(data_dict_nvidia)
            n_date,net_lst,n_sig = boulinder(data_dict_Netflix)
            net_date,ap_lst,ap_sig, = boulinder(data_dict_apple)
            net_date,ad_lst,ad_sig= boulinder(data_dict_Adobe)
            net_date,tes_lst,tes_sig= boulinder(data_dict_Tesla)
            Simple_moving_animate(None,frame=frame,pivot_df=ibm_date,val=[ibm_lst,meta_lst,ms_lst,n_lst,net_lst,ap_lst,ad_lst,tes_lst],Name=['IBM',"WALMART","MICROSOFT","NVIDIA","NETFLIX","APPLE","ADOBE","TESLA"],choice=val)

        if graph =="IMB":
            self.create_label(frame,"<b>Simple Moving average<b>",self.font,(10,255,1100, 50))
            Simple_moving_company(None, frame,call=graph,geo=(10,300,1100,600))
            self.create_label(frame,"<b>Exponentional Moving average<b>",self.font,(10,920,1100, 50))
            exponential_moving_company(None, frame,call=graph,geo=(10,965,1100,600))
            self.create_label(frame,"<b>MACD<b>",self.font,(10,1585,1100, 50))
            MCAD_company(None, frame,call=graph,geo=(10,1625,1100,600))
            self.create_label(frame,"<b>Historical Volatility <b>",self.font,(10,2250,1100, 50))
            hv_company(None, frame,call=graph,geo=(10,2285,1100,600))
            self.create_label(frame,"<b>Volume-Weighted Average Price<b>",self.font,(10,2925,1100, 50))
            vwap_company(None, frame,call=graph,geo=(10,2960,1100,600))
            self.create_label(frame,"<b>Relative Strength Index (RSI)<b>",self.font,(10,3600,1100, 50))
            rsi_company(None, frame,call=graph,geo=(10,3640,1100,600))
            self.create_label(frame,"<b>Bollinger Bands<b>",self.font,(10,4300,1100, 50))
            boulinder_company(None,frame,call=graph,geo=(10,4340,1100,600))
            
        if graph =="MSFT":
            self.create_label(frame,"<b>Simple Moving average<b>",self.font,(10,255,1100, 50))
            Simple_moving_company(None, frame,call=graph,geo=(10,300,1100,600))
            self.create_label(frame,"<b>Exponentional Moving average<b>",self.font,(10,920,1100, 50))
            exponential_moving_company(None, frame,call=graph,geo=(10,965,1100,600))
            self.create_label(frame,"<b>MACD<b>",self.font,(10,1585,1100, 50))
            MCAD_company(None, frame,call=graph,geo=(10,1625,1100,600))
            self.create_label(frame,"<b>Historical Volatility <b>",self.font,(10,2250,1100, 50))
            hv_company(None, frame,call=graph,geo=(10,2285,1100,600))
            self.create_label(frame,"<b>Volume-Weighted Average Price<b>",self.font,(10,2925,1100, 50))
            vwap_company(None, frame,call=graph,geo=(10,2960,1100,600))
            self.create_label(frame,"<b>Relative Strength Index (RSI)<b>",self.font,(10,3600,1100, 50))
            rsi_company(None, frame,call=graph,geo=(10,3640,1100,600))
            self.create_label(frame,"<b>Bollinger Bands<b>",self.font,(10,4300,1100, 50))
            boulinder_company(None,frame,call=graph,geo=(10,4340,1100,600))
            
        if graph =="NVDA":
            self.create_label(frame,"<b>Simple Moving average<b>",self.font,(10,255,1100, 50))
            Simple_moving_company(None, frame,call=graph,geo=(10,300,1100,600))
            self.create_label(frame,"<b>Exponentional Moving average<b>",self.font,(10,920,1100, 50))
            exponential_moving_company(None, frame,call=graph,geo=(10,965,1100,600))
            self.create_label(frame,"<b>MACD<b>",self.font,(10,1585,1100, 50))
            MCAD_company(None, frame,call=graph,geo=(10,1625,1100,600))
            self.create_label(frame,"<b>Historical Volatility <b>",self.font,(10,2250,1100, 50))
            hv_company(None, frame,call=graph,geo=(10,2285,1100,600))
            self.create_label(frame,"<b>Volume-Weighted Average Price<b>",self.font,(10,2925,1100, 50))
            vwap_company(None, frame,call=graph,geo=(10,2960,1100,600))
            self.create_label(frame,"<b>Relative Strength Index (RSI)<b>",self.font,(10,3600,1100, 50))
            rsi_company(None, frame,call=graph,geo=(10,3640,1100,600))
            self.create_label(frame,"<b>Bollinger Bands<b>",self.font,(10,4300,1100, 50))
            boulinder_company(None,frame,call=graph,geo=(10,4340,1100,600))

        if graph =="WMT":
            self.create_label(frame,"<b>Simple Moving average<b>",self.font,(10,255,1100, 50))
            Simple_moving_company(None, frame,call=graph,geo=(10,300,1100,600))
            self.create_label(frame,"<b>Exponentional Moving average<b>",self.font,(10,920,1100, 50))
            exponential_moving_company(None, frame,call=graph,geo=(10,965,1100,600))
            self.create_label(frame,"<b>MACD<b>",self.font,(10,1585,1100, 50))
            MCAD_company(None, frame,call=graph,geo=(10,1625,1100,600))
            self.create_label(frame,"<b>Historical Volatility <b>",self.font,(10,2250,1100, 50))
            hv_company(None, frame,call=graph,geo=(10,2285,1100,600))
            self.create_label(frame,"<b>Volume-Weighted Average Price<b>",self.font,(10,2925,1100, 50))
            vwap_company(None, frame,call=graph,geo=(10,2960,1100,600))
            self.create_label(frame,"<b>Relative Strength Index (RSI)<b>",self.font,(10,3600,1100, 50))
            rsi_company(None, frame,call=graph,geo=(10,3640,1100,600))
            self.create_label(frame,"<b>Bollinger Bands<b>",self.font,(10,4300,1100, 50))
            boulinder_company(None,frame,call=graph,geo=(10,4340,1100,600))
            
        if graph =="NFL":
            self.create_label(frame,"<b>Simple Moving average<b>",self.font,(10,255,1100, 50))
            Simple_moving_company(None, frame,call=graph,geo=(10,300,1100,600))
            self.create_label(frame,"<b>Exponentional Moving average<b>",self.font,(10,920,1100, 50))
            exponential_moving_company(None, frame,call=graph,geo=(10,965,1100,600))
            self.create_label(frame,"<b>MACD<b>",self.font,(10,1585,1100, 50))
            MCAD_company(None, frame,call=graph,geo=(10,1625,1100,600))
            self.create_label(frame,"<b>Historical Volatility <b>",self.font,(10,2250,1100, 50))
            hv_company(None, frame,call=graph,geo=(10,2285,1100,600))
            self.create_label(frame,"<b>Volume-Weighted Average Price<b>",self.font,(10,2925,1100, 50))
            vwap_company(None, frame,call=graph,geo=(10,2960,1100,600))
            self.create_label(frame,"<b>Relative Strength Index (RSI)<b>",self.font,(10,3600,1100, 50))
            rsi_company(None, frame,call=graph,geo=(10,3640,1100,600))
            self.create_label(frame,"<b>Bollinger Bands<b>",self.font,(10,4300,1100, 50))
            boulinder_company(None,frame,call=graph,geo=(10,4340,1100,600))
        if graph =="ap":
            self.create_label(frame,"<b>Simple Moving average<b>",self.font,(10,255,1100, 50))
            Simple_moving_company(None, frame,call=graph,geo=(10,300,1100,600))
            self.create_label(frame,"<b>Exponentional Moving average<b>",self.font,(10,920,1100, 50))
            exponential_moving_company(None, frame,call=graph,geo=(10,965,1100,600))
            self.create_label(frame,"<b>MACD<b>",self.font,(10,1585,1100, 50))
            MCAD_company(None, frame,call=graph,geo=(10,1625,1100,600))
            self.create_label(frame,"<b>Historical Volatility <b>",self.font,(10,2250,1100, 50))
            hv_company(None, frame,call=graph,geo=(10,2285,1100,600))
            self.create_label(frame,"<b>Volume-Weighted Average Price<b>",self.font,(10,2925,1100, 50))
            vwap_company(None, frame,call=graph,geo=(10,2960,1100,600))
            self.create_label(frame,"<b>Relative Strength Index (RSI)<b>",self.font,(10,3600,1100, 50))
            rsi_company(None, frame,call=graph,geo=(10,3640,1100,600))
            self.create_label(frame,"<b>Bollinger Bands<b>",self.font,(10,4300,1100, 50))
            boulinder_company(None,frame,call=graph,geo=(10,4340,1100,600))
        if graph =="ad":
            self.create_label(frame,"<b>Simple Moving average<b>",self.font,(10,255,1100, 50))
            Simple_moving_company(None, frame,call=graph,geo=(10,300,1100,600))
            self.create_label(frame,"<b>Exponentional Moving average<b>",self.font,(10,920,1100, 50))
            exponential_moving_company(None, frame,call=graph,geo=(10,965,1100,600))
            self.create_label(frame,"<b>MACD<b>",self.font,(10,1585,1100, 50))
            MCAD_company(None, frame,call=graph,geo=(10,1625,1100,600))
            self.create_label(frame,"<b>Historical Volatility <b>",self.font,(10,2250,1100, 50))
            hv_company(None, frame,call=graph,geo=(10,2285,1100,600))
            self.create_label(frame,"<b>Volume-Weighted Average Price<b>",self.font,(10,2925,1100, 50))
            vwap_company(None, frame,call=graph,geo=(10,2960,1100,600))
            self.create_label(frame,"<b>Relative Strength Index (RSI)<b>",self.font,(10,3600,1100, 50))
            rsi_company(None, frame,call=graph,geo=(10,3640,1100,600))
            self.create_label(frame,"<b>Bollinger Bands<b>",self.font,(10,4300,1100, 50))
            boulinder_company(None,frame,call=graph,geo=(10,4340,1100,600))
        if graph =="tes":
            self.create_label(frame,"<b>Simple Moving average<b>",self.font,(10,255,1100, 50))
            Simple_moving_company(None, frame,call=graph,geo=(10,300,1100,600))
            self.create_label(frame,"<b>Exponentional Moving average<b>",self.font,(10,920,1100, 50))
            exponential_moving_company(None, frame,call=graph,geo=(10,965,1100,600))
            self.create_label(frame,"<b>MACD<b>",self.font,(10,1585,1100, 50))
            MCAD_company(None, frame,call=graph,geo=(10,1625,1100,600))
            self.create_label(frame,"<b>Historical Volatility <b>",self.font,(10,2250,1100, 50))
            hv_company(None, frame,call=graph,geo=(10,2285,1100,600))
            self.create_label(frame,"<b>Volume-Weighted Average Price<b>",self.font,(10,2925,1100, 50))
            vwap_company(None, frame,call=graph,geo=(10,2960,1100,600))
            self.create_label(frame,"<b>Relative Strength Index (RSI)<b>",self.font,(10,3600,1100, 50))
            rsi_company(None, frame,call=graph,geo=(10,3640,1100,600))
            self.create_label(frame,"<b>Bollinger Bands<b>",self.font,(10,4300,1100, 50))
            boulinder_company(None,frame,call=graph,geo=(10,4340,1100,600))            
        self.stacked_widget.addWidget(page)  # Add the page to the stacked widget
        page.setObjectName(page_id)

    def create_label(self,frame,data,font,geo):
        label1 = QLabel(frame)
        label1.setText(data)
        # label1.setFont(self.font)  # Assuming self.font is defined elsewhere
        label1.setFont(font)# Align the label to the center
        label1.setGeometry(geo[0],geo[1],geo[2],geo[3])
        
    def button_show(self,b1):
        if  b1.isChecked():
            self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
            self.create_page('macd', '<b>Moving Average Convergence/Divergence (MACD)<b>',"Moving average convergence/divergence (MACD) is a technical indicator to help investors identify price trends, measure trend momentum, and\nidentify market entry points for buying or selling. Moving average convergence/divergence (MACD) is a trend-following momentum indicator that\nshows the relationship between two exponential moving averages (EMAs) of a security’s price. MACD was developed in the 1970s by Gerald Appel.\nThe MACD line is calculated by subtracting the 26-period EMA from the 12-period EMA. The calculation creates the MACD line. A nine-day EMA of\nthe MACD line is called the signal line, plotted on top of the MACD line, which can function as a trigger for buy or sell signals.",None,"macd",show=True)
            self.show_page('macd')
            
        else:
            self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
            self.create_page('macd', '<b>Moving Average Convergence/Divergence (MACD)<b>',"Moving average convergence/divergence (MACD) is a technical indicator to help investors identify price trends, measure trend momentum, and\nidentify market entry points for buying or selling. Moving average convergence/divergence (MACD) is a trend-following momentum indicator that\nshows the relationship between two exponential moving averages (EMAs) of a security’s price. MACD was developed in the 1970s by Gerald Appel.\nThe MACD line is calculated by subtracting the 26-period EMA from the 12-period EMA. The calculation creates the MACD line. A nine-day EMA of\nthe MACD line is called the signal line, plotted on top of the MACD line, which can function as a trigger for buy or sell signals.",None,"macd",show=False)
            self.show_page('macd')


    def bt_(self,ar,call):
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
        if call == 'sma':
            self.create_page('sma', self.sma_text,self.sma_discription,ar,'sma')
            self.show_page('sma')
        elif call =="ema":
            self.create_page('ema', self.ema_text,self.ema_discription,ar,'ema')
            self.show_page('ema')
        elif call =="hv":
            self.create_page('hv', self.hv_text,self.hv_discription,ar,'hv')
            self.show_page('hv')    
        elif call=='vwap':
            self.create_page('vwap', self.hv_text,self.hv_discription,ar,'vwap')
            self.show_page('vwap') 
        elif call=='rsi':
            self.create_page('rsi', self.rsi_text,self.rsi_description,ar,'rsi')
            self.show_page('rsi') 
        elif call=='bands':
            self.create_page('bands', self.boulinder_text,self.bolinder_description,ar,'bands')
            self.show_page('bands')

    def b1_(self,ar,b1,call):
        if  b1.isChecked():
            if 0 not in ar:
                ar.append(0)
        else:
            if 0 in ar:
                ar.pop(0) 

        
             
    def b2_(self,ar,b2,call):
        if  b2.isChecked():
            if 1 not in ar:
                ar.append(1)
        else:
            if 1 in ar:
                ar.pop(1)
            
    def b3_(self,ar,b3,call):
        if  b3.isChecked():
            if 2 not in ar:
                ar.append(2)
        else:
            if 2 in ar:
                ar.pop(2)
            
    def b4_(self,ar,b4,call):
        if  b4.isChecked():
            if 3 not in ar:
                ar.append(3)
        else:
            if 3 in ar:
                ar.pop(3)

    def b5_(self,ar,b5,call):
        if  b5.isChecked():
            if 4 not in ar:
                ar.append(4)
        else:
            if 4 in ar:
                ar.pop(4)

    def b6_(self,ar,b6,call):
        if  b6.isChecked():
            if 5 not in ar:
                ar.append(5)
        else:
            if 5 in ar:
                ar.pop(5)

    def b7_(self,ar,b7,call):
        if  b7.isChecked():
            if 6 not in ar:
                ar.append(6)
        else:
            if 6 in ar:
                ar.pop(6)

    def b8_(self,ar,b8,call):
        if  b8.isChecked():
            if 7 not in ar:
                ar.append(7)
        else:
            if 7 in ar:
                ar.pop(7)
 
    def on_item_clicked(self, current, previous):
        
        if current is not None:
            # Get the data from the selected item
            page_id = current.data(Qt.UserRole)
            # Display the corresponding page
            self.show_page(page_id)

    def show_page(self, page_id):
        # Find the page widget by its object name (page_id) and display it
        for i in range(self.stacked_widget.count()):
            page = self.stacked_widget.widget(i)
            if page.objectName() == page_id:
                self.stacked_widget.setCurrentWidget(page)
                break

# Run the application
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

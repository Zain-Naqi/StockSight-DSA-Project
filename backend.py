import math 
import sqlite3

# Calling data from the database:
def call_data(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.execute("SELECT * FROM data")
    data_dict={}
    for row in cursor:
        data_dict[row[1]] = {"1. open": row[2], "2. high": row[3],"3. low" : row[4],  "4. close": row[5],"5. volume": row[6]}
    return data_dict

data_dict = call_data("Walmart_Daily.db")

dates_in_api = list(data_dict.keys())
dates_in_api = dates_in_api[::-1]

def convert_to_dictionary(dates_in_api):
    date_dict = {}
    count = 0
    for date in dates_in_api:
        date_dict[date] = count
        count += 1
    return date_dict

dates_dict = convert_to_dictionary(dates_in_api)

closings = []
volumes = []
volume_x_close = []
open = []

for date in dates_in_api:
    closings.append(float(data_dict[date]["4. close"]))
    open.append(float(data_dict[date]["1. open"]))
    volumes.append(int(data_dict[date]["5. volume"]))
    volume_x_close.append((float(data_dict[date]["4. close"])) * (float(data_dict[date]["5. volume"])))

# Segment Tree for Sum Calculation:
def build_tree_sum(arr, tree, node, start, end):
    
    if start == end:
        tree[node] = arr[start]  
        
    else:
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
    
        build_tree_sum(arr, tree, left_child, start, mid)
        build_tree_sum(arr, tree, right_child, mid + 1, end)
        
        tree[node] = tree[left_child] + tree[right_child]

# Query function for segment tree:
def query_sum(tree, node, start, end, query_start, query_end):
    
    if query_end < start or query_start > end:
        return 0
    
    elif query_start <= start and query_end >= end:
        return tree[node]
    
    else:
        mid = (start + end) // 2
        
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        left_sum = query_sum(tree, left_child, start, mid, query_start, query_end)
        right_sum = query_sum(tree, right_child, mid + 1, end, query_start, query_end)
        
        return left_sum + right_sum

# Building the segment tree skeleton:
def build_segment_tree_sum(arr):
    
    n = len(arr)
    tree = [0] * (4 * n)
    build_tree_sum(arr, tree, 0, 0, n - 1)
    return tree

segment_tree_closings_sum = build_segment_tree_sum(closings)
segment_tree_open_sum = build_segment_tree_sum(open)
segment_tree_volumes_sum = build_segment_tree_sum(volumes)
segment_tree_volume_x_close_sum = build_segment_tree_sum(volume_x_close)

start_date = dates_in_api[0]
end_date = dates_in_api[-1]

# Function to calculate list of simple moving average. Simple Moving Average: Given a list of five integers arr=[1, 2, 3, 7, 9] and we need to calculate moving averages of the list with window size specified as 3. We will first calculate average of first 3 elements and that will be stored as first moving average. Then window will be shifted one position to the right and again average of elements present in the window will be calculated and stored in the list. Similarly, the process will repeat till the window reaches the last element of the array. 
def moving_averages_list(segment_tree, window_size, start_date, end_date):
    
    moving_averages = []
    n = len(segment_tree) // 4

    for i in range(start_date, end_date + 1):

        sum = query_sum(segment_tree, 0, 0, n - 1, i - window_size + 1, i)
        moving_average = sum / window_size
        moving_averages.append(moving_average)
    
    return (dates_in_api, moving_averages)

# Function to calculate moving average at some specific date:
def moving_average(segment_tree, window_size, date):
    
    n = len(segment_tree) // 4
    sum = query_sum(segment_tree, 0, 0, n - 1, date - window_size + 1, date + 1)
    moving_average = sum / window_size
    return moving_average

# Function to return the list of Exponential Moving Averages:
def ema_list(closings, segment_tree, window_size, start_date, end_date):
    
    previous_day_ema = moving_average(segment_tree, window_size, start_date)
    multiplier = 2 / (1 + window_size)
    ema_list = []
    
    for i in range(start_date, end_date + 1):
        
        close = closings[i]
        ema = ((close - previous_day_ema) * multiplier) + previous_day_ema
        ema_list.append(round(ema, 2))
        previous_day_ema = ema
       
    return(dates_in_api, ema_list)

def MACD(closings, segment_tree, start_date, end_date, short_window=12, long_window=26, signal_window=9):
    
    # Calculate the Short Term Exponential Moving Average
    dates, short_ema = ema_list(closings, segment_tree, short_window, start_date, end_date)
    
    # Calculate the Long Term Exponential Moving Average
    dates, long_ema = ema_list(closings, segment_tree, long_window, start_date, end_date)
    
    # Calculate MACD Line
    macd_line = []
    for i in range(len(short_ema)):
        macd_line.append(short_ema[i] - long_ema[i])
    
    # Calculate Signal Line
    macd_segment_tree = build_segment_tree_sum(macd_line)
    dates, signal_line = ema_list(macd_line, macd_segment_tree, signal_window, 0, len(macd_line)-1)
    
    # Calculate MACD Histogram
    macd_histogram = []
    for i in range(len(macd_line)):
        macd_histogram.append(macd_line[i] - signal_line[i])
    
    return (dates_in_api, macd_line, signal_line, macd_histogram)

# Function that returns a list of historiacal volatilites for a given dates range:
def historical_volatility_list(closings, segment_tree, window_size, start_date, end_date):
    
    volatalities = []
    n = len(segment_tree) // 4
    
    for i in range(start_date, end_date):
        
        total = query_sum(segment_tree, 0, 0, n - 1, i - window_size + 1, i)
        mean = total / window_size
        difference = []
        
        for j in range(i - window_size + 1, i + 1):
            difference.append((closings[j] - mean) ** 2)
                
        standard_deviation = math.sqrt(sum(difference) / window_size)
        volatalities.append(standard_deviation)
        
    return (dates_in_api, volatalities)

# Function that return historical volatility for a given date:
def historical_volatility(segment_tree, closings, window_size, date):
    
    n = len(segment_tree) // 4
    total = query_sum(segment_tree, 0, 0, n - 1, date - window_size + 1, date)
    mean = total / window_size
    difference = []
    
    for j in range(date - window_size + 1, date + 1):
        
        if closings[j] == 0:
            difference.append(0)
        else:
            difference.append((closings[j] - mean) ** 2)
            
    standard_deviation = math.sqrt(sum(difference) / window_size)
    return standard_deviation

# Function that returns a list containing VWAPs for some specific date ranges:
def VWAP_list(segment_tree_volumes, segment_tree_volume_x_close, window_size, start_date, end_date):
    
    VWAP_list = []
    n = len(segment_tree_volumes) // 4
    
    for i in range(start_date, end_date):
        
        sum_volumes = query_sum(segment_tree_volumes, 0, 0, n - 1, i - window_size + 1, i + 1)
        sum_volume_x_close = query_sum(segment_tree_volume_x_close, 0, 0, n - 1, i - window_size + 1, i + 1)
        VWAP_list.append(round(sum_volume_x_close / sum_volumes, 2))
        
    return (dates_in_api, VWAP_list)

# Function that returns the list of gains for a date range:
def gains_list(closings, start_date, end_date):
    
    gains = []
    
    for i in range(start_date, end_date + 1):
        if closings[i] > closings[i - 1]:
            gains.append(closings[i] - closings[i - 1])
        else:
            gains.append(0)
            
    return gains


# Function that returns the list of loss for a date range:
def loss_list(closings, start_date, end_date):
    
    loss = []
    for i in range(start_date, end_date + 1):
        if closings[i] < closings[i - 1]:
            loss.append(closings[i - 1] - closings[i])
        else:
            loss.append(0)
            
    return loss

gains = gains_list(closings, dates_dict[start_date], dates_dict[end_date])
loss = loss_list(closings, dates_dict[start_date], dates_dict[end_date])
segment_tree_gains = build_segment_tree_sum(gains)
segment_tree_loss = build_segment_tree_sum(loss)


# Function which returns a list of Relative Strength Index over a given date range:
def RSI(segment_tree_gains, segment_tree_loss, gains, loss, window_size, start_date, end_date):
    
    average_gains = []
    n = len(segment_tree_gains) // 4
    total_gain = query_sum(segment_tree_gains, 0, 0, n - 1, start_date - window_size + 1, start_date + 1)
    average_gain = total_gain / window_size
    average_gains.append(average_gain)
    
    average_losses = []
    l = len(segment_tree_loss) // 4
    total_loss = query_sum(segment_tree_loss, 0, 0, l - 1, start_date - window_size + 1, start_date + 1)
    average_loss = total_loss / window_size
    average_losses.append(average_loss)
    
    
    for i in range(start_date + 1, end_date + 1):
        
        average_gain = ((average_gain * (window_size - 1)) + gains[i]) / window_size
        average_gains.append(average_gain)
        
        average_loss = ((average_loss * (window_size - 1)) + loss[i]) / window_size
        average_losses.append(average_loss)
        
    RSI = []
    
    for i in range(len(average_gains)):
        
        RSI.append(100 - (100 / (1 + (average_gains[i] / average_losses[i]))))
    
    return (dates_in_api,RSI)

def bollinger_bands(closings, segment_tree, start_date, end_date):
    high_band = []
    low_band = []
    
    for i in range(start_date, end_date + 1):
        # Calculate the simple moving average (SMA)
        sma = moving_average(segment_tree, window_size=20, date=i)
        
        # Calculate the standard deviation
        std_dev = historical_volatility(segment_tree, closings, window_size=20, date=i)
        
        # Calculate upper and lower bands
        upper_band = sma + (2 * std_dev)
        lower_band = sma - (2 * std_dev)
        
        high_band.append(upper_band)
        low_band.append(lower_band)
    
    return (dates_in_api,high_band, low_band)




















       

        
    
    
    
    
    
    
    
    
    



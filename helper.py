

from backend import moving_averages_list, build_segment_tree_sum, call_data, convert_to_dictionary,ema_list,MACD,historical_volatility_list,VWAP_list,RSI,gains_list,loss_list,bollinger_bands

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
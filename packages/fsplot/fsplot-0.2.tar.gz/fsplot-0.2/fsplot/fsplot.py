import svgwrite
import numpy as np

def plot_line(data_array, width=150, height=100):
    """
    Plot a line chart based on an input array of values.
    
    Parameters:
        data_array (list or numpy array): Array of y-values to be plotted.
        width (int, optional): The width of the SVG canvas. Default is 150.
        height (int, optional): The height of the SVG canvas. Default is 100.
    
    Returns:
        str: SVG string representing the line chart.
    """
    # Extracting data from array
    x_values = np.arange(len(data_array))
    y_values = np.array(data_array)  # Ensure data_array is a numpy array

    # Normalize y values to fit within the SVG canvas
    y_min = y_values.min()
    y_max = y_values.max()
    normalized_y_values = [(y - y_min) / (y_max - y_min) * height for y in y_values]

    # Scale x values to fit within the specified width
    scaled_x_values = [(x / len(data_array)) * width for x in x_values]

    # Create SVG drawing
    dwg = svgwrite.Drawing(size=(width, height))

    # Draw lines connecting data points
    for i in range(len(scaled_x_values) - 1):
        x1 = scaled_x_values[i]
        y1 = height - normalized_y_values[i]
        x2 = scaled_x_values[i + 1]
        y2 = height - normalized_y_values[i + 1]
        dwg.add(dwg.line((round(x1, 2), round(y1, 2)), (round(x2, 2), round(y2, 2)), stroke='black'))

    # Return SVG string
    return dwg.tostring()

def plot_candlestick(data_dict, width=150, height=100):
    """
    Plot a candlestick chart based on an input dictionary of values.
    
    Parameters:
        data_dict (dict): Dictionary with keys 'Open', 'High', 'Low', and 'Close' containing corresponding lists of values.
        width (int, optional): The width of the SVG canvas. Default is 150.
        height (int, optional): The height of the SVG canvas. Default is 100.
    
    Returns:
        str: SVG string representing the candlestick chart.
    """
    # Extracting data from the dictionary
    x_values = np.arange(len(data_dict['Open']))
    y_values_open = np.array(data_dict['Open'])
    y_values_high = np.array(data_dict['High'])
    y_values_low = np.array(data_dict['Low'])
    y_values_close = np.array(data_dict['Close'])

    # Normalize y values to fit within the SVG canvas
    y_min = min(y_values_low.min(), y_values_open.min(), y_values_close.min())
    y_max = max(y_values_high.max(), y_values_open.max(), y_values_close.max())
    normalized_y_values_open = [(y - y_min) / (y_max - y_min) * height for y in y_values_open]
    normalized_y_values_high = [(y - y_min) / (y_max - y_min) * height for y in y_values_high]
    normalized_y_values_low = [(y - y_min) / (y_max - y_min) * height for y in y_values_low]
    normalized_y_values_close = [(y - y_min) / (y_max - y_min) * height for y in y_values_close]

    # Scale x values to fit within the specified width
    scaled_x_values = [(x / len(data_dict['Open'])) * width for x in x_values]

    # Create SVG drawing
    dwg = svgwrite.Drawing(size=(width, height))

    # Draw candlesticks
    for x, open_, high, low, close in zip(scaled_x_values, normalized_y_values_open, normalized_y_values_high, normalized_y_values_low, normalized_y_values_close):
        if open_ < close:
            body_color = 'green'
            stroke_color = 'green'
        else:
            body_color = '#cc0022'
            stroke_color = '#cc0022'
        # Flip the y-axis coordinates by subtracting from the specified height
        dwg.add(dwg.rect((round(x - 1, 2), round(height - max(open_, close), 2)), (2, round(abs(close - open_), 2)), fill=body_color, stroke=stroke_color))
        dwg.add(dwg.line((round(x, 2), round(height - high, 2)), (round(x, 2), round(height - low, 2)), stroke=body_color))

    # Return SVG string
    return dwg.tostring()


def plot_candlestick_trendline(data, width=150, height=100):
    """
    Plot a candlestick chart along with support and resistance trendlines.

    Parameters:
        data (dict): A dictionary containing the following keys:
            'Open' (list or array): The opening prices.
            'High' (list or array): The highest prices.
            'Low' (list or array): The lowest prices.
            'Close' (list or array): The closing prices.
            'support_first_value' (float): The first value for the support line.
            'support_gradient' (float): The gradient of the support line.
            'resistance_first_value' (float): The first value for the resistance line.
            'resistance_gradient' (float): The gradient of the resistance line.
        width (int, optional): The width of the SVG canvas. Default is 150.
        height (int, optional): The height of the SVG canvas. Default is 100.

    Returns:
        str: An SVG string representing the candlestick chart with trendlines.
    """
    
    # Extract data from the input dictionary
    open_values = data['Open']
    high_values = data['High']
    low_values = data['Low']
    close_values = data['Close']
    support_first_value = data['support_first_value']
    support_gradient = data['support_gradient']
    resistance_first_value = data['resistance_first_value']
    resistance_gradient = data['resistance_gradient']

    x_values = np.arange(len(open_values))

    # Normalize y values to fit within the SVG canvas
    y_min = min(low_values.min(), open_values.min(), close_values.min(), 
                support_first_value, resistance_first_value)
    y_max = max(high_values.max(), open_values.max(), close_values.max(), 
                support_first_value + support_gradient * (len(open_values) - 1), 
                resistance_first_value + resistance_gradient * (len(open_values) - 1))
                
    normalized_y_values_open = [(y - y_min) / (y_max - y_min) * height for y in open_values]
    normalized_y_values_high = [(y - y_min) / (y_max - y_min) * height for y in high_values]
    normalized_y_values_low = [(y - y_min) / (y_max - y_min) * height for y in low_values]
    normalized_y_values_close = [(y - y_min) / (y_max - y_min) * height for y in close_values]

    # Scale x values to fit within the specified width
    scaled_x_values = [(x / len(open_values)) * width for x in x_values]

    # Create SVG drawing
    dwg = svgwrite.Drawing(size=(width, height))

    # Draw candlesticks
    for x, open_, high, low, close in zip(scaled_x_values, normalized_y_values_open, normalized_y_values_high, normalized_y_values_low, normalized_y_values_close):
        if open_ < close:
            body_color = 'green'
            stroke_color = 'green'
        else:
            body_color = '#cc0022'
            stroke_color = '#cc0022'
        # Flip the y-axis coordinates by subtracting from the specified height
        dwg.add(dwg.rect((round(x - 1, 2), round(height - max(open_, close), 2)), 
                         (2, round(abs(close - open_), 2)), fill=body_color, stroke=stroke_color))
        dwg.add(dwg.line((round(x, 2), round(height - high, 2)), 
                         (round(x, 2), round(height - low, 2)), stroke=stroke_color))

    # Draw the support and resistance trendlines
    start_x = scaled_x_values[0]
    end_x = scaled_x_values[-1]

    # Calculate the y-coordinates for the support line
    support_start_y = (support_first_value - y_min) / (y_max - y_min) * height
    support_end_y = (support_first_value + support_gradient * (len(open_values) - 1) - y_min) / (y_max - y_min) * height

    # Calculate the y-coordinates for the resistance line
    resistance_start_y = (resistance_first_value - y_min) / (y_max - y_min) * height
    resistance_end_y = (resistance_first_value + resistance_gradient * (len(open_values) - 1) - y_min) / (y_max - y_min) * height

    # Draw support trend line
    dwg.add(dwg.line((round(start_x, 2), round(height - support_start_y, 2)), 
                     (round(end_x, 2), round(height - support_end_y, 2)), 
                     stroke='black', stroke_width=1))

    # Draw resistance trend line
    dwg.add(dwg.line((round(start_x, 2), round(height - resistance_start_y, 2)), 
                     (round(end_x, 2), round(height - resistance_end_y, 2)), 
                     stroke='black', stroke_width=1))

    # Return SVG string
    return dwg.tostring()

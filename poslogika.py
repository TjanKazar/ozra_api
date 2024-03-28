import datetime

def convert_to_proper_case(name):
    parts = name.split('_')
    for part in parts:
        part.lower()    
    proper_name = ' '.join(part.capitalize() for part in parts)
    return proper_name

def get_shortest_time(rows):
    min_time = float('inf')
    min_time_entry = None

    for row in rows:
        overall_time_str = row['overall']
        
        try:
            overall_time = datetime.datetime.strptime(overall_time_str, '%H:%M:%S')
        except ValueError:
            continue

        total_seconds = overall_time.hour * 3600 + overall_time.minute * 60 + overall_time.second
        
        if total_seconds < min_time:
            min_time = total_seconds
            min_time_entry = row

    return min_time_entry

def get_shortest_time_run(rows):
    min_time = float('inf')
    min_time_entry = None

    for row in rows:
        overall_time_str = row['run']
        
        try:
            overall_time = datetime.datetime.strptime(overall_time_str, '%H:%M:%S')
        except ValueError:
            continue

        total_seconds = overall_time.hour * 3600 + overall_time.minute * 60 + overall_time.second
        
        if total_seconds < min_time:
            min_time = total_seconds
            min_time_entry = row

    return min_time_entry

def get_shortest_time_swim(rows):
    min_time = float('inf')
    min_time_entry = None

    for row in rows:
        overall_time_str = row['swim']
        
        try:
            overall_time = datetime.datetime.strptime(overall_time_str, '%H:%M:%S')
        except ValueError:
            continue

        total_seconds = overall_time.hour * 3600 + overall_time.minute * 60 + overall_time.second
        
        if total_seconds < min_time:
            min_time = total_seconds
            min_time_entry = row

    return min_time_entry

def get_shortest_time_bike(rows):
    min_time = float('inf')
    min_time_entry = None

    for row in rows:
        overall_time_str = row['bike']
        
        try:
            overall_time = datetime.datetime.strptime(overall_time_str, '%H:%M:%S')
        except ValueError:
            continue

        total_seconds = overall_time.hour * 3600 + overall_time.minute * 60 + overall_time.second
        
        if total_seconds < min_time:
            min_time = total_seconds
            min_time_entry = row

    return min_time_entry
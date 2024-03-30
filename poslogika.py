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

def get_top_swimmers(rows):
    swim_times = {}
    for row in rows:
        rezultat_id = row[0]
        swim_time = row[1]
        if swim_time != '---':
            swim_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(swim_time.split(':'))))
            swim_times[rezultat_id] = swim_seconds
    
    shortest_swim_times = sorted(swim_times.items(), key=lambda item: item[1])[:3]
    
    top_3_swimmers = []
    for swimmer_id, _ in shortest_swim_times:
        top_3_swimmers.append(swimmer_id)

    return top_3_swimmers

def get_top_runners(rows):
    run_times = {}
    for row in rows:
        rezultat_id = row[0]
        run_time = row[1]
        if run_time != '---':
            run_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(run_time.split(':'))))
            run_times[rezultat_id] = run_seconds
    
    shortest_run_times = sorted(run_times.items(), key=lambda item: item[1])[:3]
    
    top_3_runners = []
    for runner_id, _ in shortest_run_times:
        top_3_runners.append(runner_id)

    return top_3_runners

def get_top_bikers(rows):
    bike_times = {}
    for row in rows:
        rezultat_id = row[0]
        bike_time = row[1]
        if bike_time != '---':
            bike_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(bike_time.split(':'))))
            bike_times[rezultat_id] = bike_seconds
    
    shortest_bike_times = sorted(bike_times.items(), key=lambda item: item[1])[:3]
    
    top_3_bikers = []
    for biker_id, _ in shortest_bike_times:
        top_3_bikers.append(biker_id)

    return top_3_bikers
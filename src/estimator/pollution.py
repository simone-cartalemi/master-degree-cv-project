from config.defaults import EMISSION_COEFFICIENTS, RATIO_FOR_DIESEL_FLEET, RATIO_FOR_PETROL_FLEET


def calculate_pollution(speed: float, coefficients: tuple) -> float:
    """
    Calculate esmission polinomial formula
    """
    if speed <= 1:
        return 0
    if not isinstance(speed, float):
        speed = float(speed)
    a, b, c, d, e, f, g = coefficients
    numerator = a + b*speed + c*speed**2 + d*speed**3 + e*speed**4 + f*speed**5 + g*speed**6
    return numerator / speed

def pollution_trend(all_estimation_data):
    '''
    Create pollution trend from speed estimations and count vehicles
    '''
    cumulation = []
    cumulation_frame = {}
    vehicle_count_frame = {}
    last_frame = 0
    for vehicle in all_estimation_data:
        min_f, max_f, estimation_speed = vehicle
        last_frame = max(last_frame, max_f)
        for i in range(min_f, max_f + 1):
            y_d = calculate_pollution(estimation_speed, EMISSION_COEFFICIENTS["diesel"])
            y_b = calculate_pollution(estimation_speed, EMISSION_COEFFICIENTS["petrol"])
            if i not in cumulation_frame:
                cumulation_frame[i] = 0
                vehicle_count_frame[i] = 0
            cumulation_frame[i] += RATIO_FOR_DIESEL_FLEET * y_d + RATIO_FOR_PETROL_FLEET * y_b
            vehicle_count_frame[i] += 1

    actual_emitted = 0
    for i in range(last_frame):
        actual_emitted += cumulation_frame.get(i, 0.0)
        count = vehicle_count_frame.get(i, 0)
        cumulation.append((count, actual_emitted))
    return cumulation

def rearrange_speed_results(lines: list, all_estimation_data: dict = {}) -> dict:
    '''
    Adapt speed results for pollution estimatio functions
    '''
    for line in lines:
        file_video_name, min_f, max_f, cls, estimation_speed, benchmarking_speed = line
        if file_video_name not in all_estimation_data:
            all_estimation_data[file_video_name] = []
        all_estimation_data[file_video_name].append([int(min_f), int(max_f), float(estimation_speed)])
    return all_estimation_data

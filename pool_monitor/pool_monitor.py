import json

def load_language_strings(lang='en'):
    with open('/etc/pool_monitor/strings.json', 'r') as f:
        strings = json.load(f)
    return strings.get(lang, strings['en'])

def calculate_free_chlorine(orp, ph, temp, salinity, tds):
    return round((orp - 500) * 0.01 - (ph - 7) * 0.05 + (temp - 25) * 0.02 + (salinity - 1000) * 0.001 - (tds - 1000) * 0.0005, 2)

def calculate_total_chlorine(free_chlorine, additional_factor=1.5):
    return round(free_chlorine + additional_factor, 2)

def calculate_combined_chlorine(total_chlorine, free_chlorine):
    return round(total_chlorine - free_chlorine, 2)

def calculate_cya_level(orp, ph, temp, salinity, tds, orp_constant=700, cya_constant=0.057):
    temperature_factor = (temp - 25) * 0.02
    ph_factor = (ph - 7.5) * 0.03
    salinity_factor = (salinity - 1000) * 0.01
    tds_factor = (tds - 1000) * 0.005
    adjusted_orp = orp - (orp_constant + temperature_factor + ph_factor + salinity_factor + tds_factor)
    cya = adjusted_orp / cya_constant
    return round(cya, 0)

def generate_pool_recommendations(ph, free_chlorine, salinity, cya, volume, strings):
    recommendations = []

    if free_chlorine < 1.5:
        chlorine_needed = round((1.5 - free_chlorine) * volume * 0.5)
        recommendations.append(strings['add_chlorine'].format(amount=chlorine_needed))

    if ph < 7.2:
        acid_amount = round((7.2 - ph) * volume * 0.1, 2)
        recommendations.append(strings['add_acid'].format(amount=acid_amount))
    elif ph > 7.8:
        soda_ash_amount = round((ph - 7.8) * volume * 0.1, 2)
        recommendations.append(strings['add_soda_ash'].format(amount=soda_ash_amount))

    water_refresh_reasons = []
    if cya > 50:
        water_refresh_reasons.append("High cyanuric acid level")
    if salinity > 1300:
        water_refresh_reasons.append("High salinity (above 1300 ppm)")
    elif salinity < 800:
        water_refresh_reasons.append("Low salinity (below 800 ppm)")
    if ph < 6.8:
        water_refresh_reasons.append("Very low pH (below 6.8)")
    elif ph > 8.0:
        water_refresh_reasons.append("Very high pH (above 8.0)")
    if free_chlorine < 1.0:
        water_refresh_reasons.append("Very low free chlorine (below 1.0 ppm)")
    elif free_chlorine > 3.0:
        water_refresh_reasons.append("Very high free chlorine (above 3.0 ppm)")

    if water_refresh_reasons:
        recommendations.append(strings['refresh_water'].format(reasons=', '.join(water_refresh_reasons)))

    if not recommendations:
        return "-"
    return ', '.join(recommendations)

# Load the configuration from the JSON file
try:
    with open('/etc/pool_monitor/config.json', 'r') as f:
        config = json.load(f)

    # Load language strings
    lang = config.get('language', 'en')
    strings = load_language_strings(lang)

    # Get sensor values from configuration
    orp = float(config.get('sensor_orp', 0))
    ph = float(config.get('sensor_ph', 0))
    temp = float(config.get('sensor_temp', 0))
    salinity = float(config.get('sensor_salinity', 0))
    tds = float(config.get('sensor_tds', 0))
    volume = float(config.get('pool_volume_liters', 50000))

    # Calculate sensor values
    free_chlorine = calculate_free_chlorine(orp, ph, temp, salinity, tds)
    total_chlorine = calculate_total_chlorine(free_chlorine)
    combined_chlorine = calculate_combined_chlorine(total_chlorine, free_chlorine)
    cya_level = calculate_cya_level(orp, ph, temp, salinity, tds)
    pool_recommendations = generate_pool_recommendations(ph, free_chlorine, salinity, cya_level, volume, strings)

    # Output calculated values
    print(f"{strings['free_chlorine']}: {free_chlorine} ppm")
    print(f"{strings['total_chlorine']}: {total_chlorine} ppm")
    print(f"{strings['combined_chlorine']}: {combined_chlorine} ppm")
    print(f"{strings['cya_level']}: {cya_level} ppm")
    print(f"{strings['pool_recommendations']}: {pool_recommendations}")

except Exception as e:
    print(f"Error occurred: {e}")

# Smart keyword groups with flexible matching using regex
KEYWORD_GROUPS = {
    # Overheating hours and related terms
    "Overheating Hours": [
        r"overheating hour[s]?",      # "overheating hour" or "overheating hours"
        r"overheat",                  # Matches "overheat" and "overheating"
        r"discomfort hour[s]?",       # "discomfort hour" or "discomfort hours"
    ],
    
    # Overheating degree terms
    "Overheating Degree": [
        r"indoor overheating degree",   # Indoor Overheating Degree
        r"overheating degree",          # General Overheating Degree
    ],

    # Degree hours or degree days
    "Degree Hours or Degree Days": [
        r"degree hour[s]?",             # "degree hour" or "degree hours"
        r"cooling degree hour[s]?",     # Cooling Degree Hours
        r"unmet degree hour[s]?",       # Unmet Degree-Hours (UDH)
        r"degree day[s]?",              # "degree day" or "degree days"
        r"heating degree day[s]?",      # Heating Degree Days (HDD)
        r"cooling degree day[s]?",      # Cooling Degree Days (CDD)
    ],

    # PMV (Predicted Mean Vote) and PPD (Predicted Percentage of Dissatisfied)
    "Thermal Comfort (PMV, PPD)": [
        r"pmv",                         # Matches "PMV"
        r"ppd",                         # Matches "PPD"
        r"predicted mean vote",         # Full "Predicted Mean Vote"
        r"predicted percentage of dissatisfied",  # Full "Predicted Percentage of Dissatisfied"
    ],

    # Expanded Temperature-related terms
    "Temperature": [
        r"temperature",                 # General temperature
        r"mean operative temperature",  # Mean Operative Temperature
        r"peak temperature",            # Peak Temperature
        r"average temperature",         # Average Temperature
        r"maximum temperature",         # Maximum Temperature
        r"daily temperature",           # Daily Temperature
        r"operative temperature",       # Operative Temperature
        r"minimum temperature",         # Minimum Temperature
        r"extreme temperature",         # Extreme Temperature
        r"ambient temperature",         # Ambient Temperature
    ],

    # Humidity and related
    "Humidity": [
        r"humidity",                    # General Humidity
        r"wet bulb globe temperature",  # Wet Bulb Globe Temperature
    ],

    # Heat index and related terms
    "Heat Index": [
        r"heat index",                  # Heat Index
    ],

    # Thermal autonomy and Ambient Warmness Degree (AWD)
    "Thermal Autonomy and AWD": [
        r"thermal autonomy",            # Thermal Autonomy
        r"ambient warmness degree",     # AWD - Ambient Warmness Degree
    ],

    # CIBSE Guide A
    "CIBSE Guide A": [
        r"cibse guide a",               # CIBSE Guide A
        r"cibse guide a static",        # CIBSE Guide A Static
    ],

    # Overheating Escalation Factor
    "Overheating Escalation Factor": [
        r"overheating escalation factor"  # Overheating Escalation Factor
    ],

    # Climate change overheating resistivity and related terms
    "Climate Change and Overheating Resistivity": [
        r"climate change overheating resistivity",  # CCOR
        r"climate change",                          # General Climate Change
    ],

    # Overheating criteria (CIBSE/EN/ISO)
    "Overheating Criteria (CIBSE/EN/ISO)": [
        r"cibse tm52",                  # CIBSE TM52
        r"cibse tm59",                  # CIBSE TM59
        r"en 15251",                    # EN 15251
        r"en 16798",                    # EN 16798
        r"iso 17772",                   # ISO 17772
    ],

    # Givoni Bioclimatic Index
    "Givoni Bioclimatic Index": [
        r"givoni bioclimatic index",    # Givoni Bioclimatic Index
    ],

    # Discomfort Index and related metrics
    "Discomfort Index": [
        r"discomfort index",            # Discomfort Index
    ]
}

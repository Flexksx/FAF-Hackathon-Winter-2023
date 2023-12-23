def custom_round(value):
    if value == 0.9375:
        return 1
    elif value == 0.46875:
        return 0.5
    elif value == 1.40625:
        return 1.5
    elif value == 1.875:
        return 2
    elif value == 1.125:
        # Handle the case of 1.125 according to your requirements
        # For example, you can round it to 1 or 1.5 based on your preference
        return 1.5
    else:
        # For other values, you can use the default rounding behavior
        return round(value)

def apply_subject_round(df):
    df["theory"] = (df["theory"]/32).apply(custom_round)
    df["seminar"] = (df["seminar"]/32).apply(custom_round)
    df["lab"] = (df["lab"]/32).apply(custom_round)
    return df
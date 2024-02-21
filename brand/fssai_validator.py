# fssai_validator.py
def break_into_parts(digits):
    parts = [digits[i:i+1] for i in range(0, len(digits), 1)]
    return parts

def check_state_code(state_code, state_list):
    if state_code in state_list:
        return True
    else:
        return False

def validate_fssai(fssai_number, user_state, user_year):
    state_codes = {
        "00": "Central License",
        "01": "Andhra Pradesh",
        "02": "Arunachal Pradesh",
        "03": "Assam",
        "04": "Bihar",
        "05": "Chhattisgarh",
        "06": "Goa",
        "07": "Gujarat",
        "08": "Haryana",
        "09": "Himachal Pradesh",
        "10": "Jammu & Kashmir",
        "11": "Jharkhand",
        "12": "Karnataka",
        "13": "Kerala",
        "14": "Madhya Pradesh",
        "15": "Maharashtra",
        "16": "Manipur",
        "17": "Meghalaya",
        "18": "Mizoram",
        "19": "Nagaland",
        "20": "Odisha",
        "21": "Punjab",
        "22": "Rajasthan",
        "23": "Sikkim",
        "24": "Tamil Nadu",
        "25": "Tripura",
        "26": "Uttarakhand",
        "27": "Uttar Pradesh",
        "28": "West Bengal",
        "29": "Andaman & Nicobar Islands",
        "30": "Chandigarh",
        "31": "Dadra & Nagar Haveli",
        "32": "Daman & Diu",
        "33": "Delhi",
        "34": "Lakshadweep",
        "35": "Puducherry"
    }

    valid_codes = state_codes.keys()

    if len(fssai_number) != 14 or not fssai_number.isdigit():
        return False, "Please enter a valid FASSAI number."
    elif fssai_number[0] not in ['1', '2']:
        return False, "Invalid FASSAI number."
    elif fssai_number[1:3] not in valid_codes:
        return False, "Invalid state code."
    else:
        state_code = fssai_number[1:3]
        if not check_state_code(state_code, valid_codes):
            return False, "Invalid state code."
        else:
            if state_codes[state_code] != user_state:
                return False, "The FASSAI number does not match the provided state."
            elif user_year[-2:] != fssai_number[3:5]:
                return False, "The FASSAI number does not match the provided year."
            else:
                return True, "The FASSAI number is correct."

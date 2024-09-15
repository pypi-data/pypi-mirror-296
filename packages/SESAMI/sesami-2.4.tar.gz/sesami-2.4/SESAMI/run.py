import numpy as np
import pandas as pd
import csv

def calculation_bet(csv_file, columns=["Pressure","Loading"],
                    adsorbate="N2", p0=1e5, T=77,
                    R2_cutoff=0.9995, R2_min=0.998,
                    font_size=12, font_type="DejaVu Sans",
                    legend=True, dpi=600, save_fig=True):
    
    from .bet import BETAn

    setting = {}
    minlinelength = 4
    if adsorbate != 'N2' and adsorbate != 'Ar' :
        setting["custom saturation pressure"] = float(p0)
        setting["custom temperature"] = float(T)
        setting['custom adsorbate'] = 'No'
        gas = 'Custom'
        temperature = float(T)
    elif adsorbate == 'N2':
        setting["custom saturation pressure"] = float(1e5)
        setting["custom temperature"] = float(77)
        setting["gas"] = 'Nitrogen'
        temperature = 77
        gas = 'Nitrogen'
    elif adsorbate == 'Ar':
        setting["custom saturation pressure"] = float(1e5)
        setting["gas"] = 'Argon'
        temperature = 87
        gas = 'Argon'

    setting["font size"] = int(font_size)
    setting["R2 cutoff"] = float(R2_cutoff)
    setting["R2 min"] = float(R2_min)
    setting["dpi"] = float(dpi)
    setting["font type"] = font_type
    setting["save fig"] = save_fig

    if legend:
        setting["legend"] = "Yes"
    else:
        setting["legend"] = "No"
   
    b = BETAn(gas, temperature, minlinelength, setting)
    data = pd.read_csv(csv_file, usecols=columns)
    if data["Pressure"].iloc[0] == 0:
        data.loc[0, 'Pressure'] = data["Pressure"].iloc[1] / 2
    data = b.prepdata(data, p0=p0)
    BET_dict, BET_ESW_dict = b.generatesummary(data, setting)

    print("*"*75)
    print("BET result")
    print("-"*75)
    print("BET Suface Area:",BET_dict["A_BET"],"mm2/g")
    print("Fitting points:",BET_dict["length_linear_region"])
    print("Fitting parameter","C:",BET_dict["C"],"qm:",BET_dict["qm"])
    print("Fitting region","C:","low region: ",BET_dict["low_P_linear_region"],"Pa", "high regio:",BET_dict["high_P_linear_region"],"Pa")
    print("con3:",BET_dict["con3"],"con4:",BET_dict["con4"])
    print("Fitting R2",BET_dict["R2_linear_region"])
    print("*"*75)
    print("BET + ESW result")
    print("-"*75)
    print("BET Suface Area:",BET_ESW_dict["A_BET"],"mm2/g")
    print("Fitting points:",BET_ESW_dict["length_linear_region"])
    print("Fitting parameter","C:",BET_ESW_dict["C"],"qm:",BET_ESW_dict["qm"])
    print("Fitting region","C:","low region: ",BET_ESW_dict["low_P_linear_region"],"Pa", "high regio:",BET_ESW_dict["high_P_linear_region"],"Pa")
    print("con3:",BET_ESW_dict["con3"],"con4:",BET_ESW_dict["con4"])
    print("Fitting R2",BET_ESW_dict["R2_linear_region"])
    print("-"*75)
    # return BET_dict, BET_ESW_dict




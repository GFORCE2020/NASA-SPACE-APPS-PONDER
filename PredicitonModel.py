import requests
import geocoder
import os
from wwo_hist import retrieve_hist_data
import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt
import json
import string
from instabot import Bot
import time

g = geocoder.ip('me')
latlong = g.latlng



#  getting temperature from open weather map
openWeatherMapAPI_key = "471498c3b83189f779be26b6f21e6b4c"
openWeatherMapBase_url = "http://api.openweathermap.org/data/2.5/onecall?"

latitude =str(latlong[0])
longitude =str(latlong[1])


Final_url = openWeatherMapBase_url + "appid=" + openWeatherMapAPI_key  + "&lat=" + latitude + "&lon=" + longitude + "&exclude=hourly,minutely,alerts"
#Final_url = https://api.openweathermap.org/data/2.5/onecall?lat=33.441792&lon=-94.037689&exclude=hourly,daily&appid=%7BAPI key}
weather_data = requests.get(Final_url).json()
#print("\nWeather Data By Geograhic Coordinates :" )
#pprint(weather_data)
json_obj = json.dumps(weather_data)
python_obj = json.loads(json_obj)
#print(python_obj)
temp_kel = python_obj["current"]["temp"]
temp_cel = temp_kel-273.15
print("temperature in degrees celcius = ", temp_cel)
daily = python_obj["daily"]
today_daily = daily[0]

today_rain = today_daily["rain"]
print(today_rain)

'''os.chdir('E:/Python/Nasa hackathon')
FREQUENCY = 3
START_DATE = '25-JUN-2020'
END_DATE = '25-SEPT-2020'
API_KEY = 'f572ce4b15674fa6b6a71330200310'
LOCATION_LIST = ['Mumbai']
hist_weather_data = retrieve_hist_data(API_KEY,
                                LOCATION_LIST,
                                START_DATE,
                                END_DATE,
                                FREQUENCY,
                                location_label = False,
                                export_csv = True,
                                store_df = True)'''
df = pd.read_csv('Mumbai.csv')
precip = np.array(df['precipMM'])
precip_final = []
for n in precip:
    precip_final.append(n)
precip_final.append(today_rain)
precip_final.sort(reverse= False)
print(precip_final)
total_values = sum(1 for row in precip_final)
lower_quartile = (total_values + 1)/4
val_1_lower = math.ceil(lower_quartile)
val_2_lower = math.floor(lower_quartile)
lower_quartile_value_1 = precip_final[val_1_lower]
lower_quartile_value_2 = precip_final[val_2_lower]
average_lower = (lower_quartile_value_1 + lower_quartile_value_2)/2

upper_quartile = 3*lower_quartile
val_1_upper = math.ceil(upper_quartile)
val_2_upper = math.floor(upper_quartile)
upper_quartile_value_1 = precip_final[val_1_upper]
upper_quartile_value_2 = precip_final[val_2_upper]
average_upper = (upper_quartile_value_1 + upper_quartile_value_2)/2
print('lower quartile = ', average_lower, '\nupper quartile = ', average_upper)

TooMuch = []
TooLess = []
acceptable= []
for n in precip_final:
    if n > average_upper:
        TooMuch.append(n)
    elif n < average_lower:
        TooLess.append(n)
    elif n > average_lower and n < average_upper:
        acceptable.append(n)
print('too much rain = ',TooMuch)
print('too less rain = ',TooLess)
print('acceptable amount = ', acceptable)
value_for_excess = sum(1 for row in TooMuch)
value_for_acceptable = sum(1 for row in acceptable)
value_for_lacking = sum(1 for row in TooLess)
print('frequency of too much = ', value_for_excess)
print('frequency for acceptable amount = ', value_for_acceptable)
print('frequency for too less = ', value_for_lacking)
data = {'Rainfall':['too much', 'okay', 'too less'], 'frequency':[value_for_excess, value_for_acceptable, value_for_lacking]}
df_2 = pd.DataFrame(data)
sns.set()
sns.barplot(x = 'Rainfall', y = 'frequency',data = df_2)
plt.savefig('this years rainfall.jpg')

frequency = []
if today_rain < average_lower:
    frequency.append(today_rain)
value_f = sum(1 for row in frequency)
if value_f > 10:
    print('WARNING: Rainfall is low use water vigilantly')

mean_position = (total_values + 1)/2
mean_val_1 = math.ceil(mean_position)
mean_val_2 = math.floor(mean_position)
mean_value_1 = precip_final[mean_val_1]
mean_value_2 = precip_final[mean_val_2]
average_mean = (mean_value_1 + mean_value_2)/2
print('average amount of rainfall =',average_mean)

with open("Lake_capacity.json") as json_file:
    data1 = json.load(json_file)

with open("Lake_overflow.json") as json_file:
    data2 = json.load(json_file)

#making a dataframe for capacity
val1C = data1['Modak Sagar  (Lower Vaitarna)']
val2C = data1['Tansa Lake']
val3C = data1['Vihar Lake']
val4C = data1['Tulsi Lake']
val5C = data1['Upper Vaitarana']
val6C = data1['Bhatsa']
val7C = data1['Middle Vaitarna [4]']

data_C = {'lakes': ['Modak Sagar  (Lower Vaitarna)', 'Tansa Lake','Vihar Lake', 'Tulsi Lake', 'Upper Vaitarana', 'Bhatsa', 'Middle Vaitarna [4]'],
          'capacity': [val1C, val2C, val3C, val4C, val5C, val6C, val7C]}
dfC = pd.DataFrame(data_C)
Capacity = dfC['capacity']

#making a dataframe for overflow
val1O = data2['Modak Sagar  (Lower Vaitarna)']
val2O = data2['Tansa Lake']
val3O = data2['Vihar Lake']
val4O = data2['Tulsi Lake']
val5O = data2['Upper Vaitarana']
val6O = data2['Bhatsa']
val7O = data2['Middle Vaitarna [4]']
data_O = {'lakes': ['Modak Sagar  (Lower Vaitarna)', 'Tansa Lake','Vihar Lake', 'Tulsi Lake', 'Upper Vaitarana', 'Bhatsa', 'Middle Vaitarna [4]'],
          'overflow': [val1O, val2O, val3O, val4O, val5O, val6O, val7O]}
dfO = pd.DataFrame(data_O)

with open('river_areas.json') as json_file:
    data3 = json.load(json_file)
area_tansa = data3['tansa']
area_vihar =data3['vihar']
area_tulsi =data3['tulsi']
area_upperV =data3['upperV']
area_bhatsa =data3['Bhatsa']
area_modak =data3['modaksagar']
area_middle =data3['middleV']
def tansa():
    area_m2 = area_tansa*10**6
    average_rainfall = average_mean*92
    total_volume_filled_mean = (average_rainfall*area_m2*0.8)/1000
    total_volume_wasted= total_volume_filled_mean - val2C
    total_volume_filled_daily = (today_rain*area_m2*0.8)/1000
    return (total_volume_wasted, total_volume_filled_daily)
volume_meanta, volume_dailyta = tansa()
def vihar():
    area_m2 = area_vihar*10**6
    average_rainfall = average_mean*92
    total_volume_filled_mean = (average_rainfall*area_m2*0.8)/1000
    total_volume_wasted = total_volume_filled_mean - val3C
    total_volume_filled_daily = (today_rain*area_m2*0.8)/1000
    return (total_volume_wasted, total_volume_filled_daily)
volume_meanv, volume_dailyv = vihar()
def tulsi():
    area_m2 = area_tulsi*10**6
    average_rainfall = average_mean*92
    total_volume_filled_mean = (average_rainfall*area_m2*0.8)/1000
    total_volume_wasted = total_volume_filled_mean - val2C
    total_volume_filled_daily = (today_rain*area_m2*0.8)/1000
    return (total_volume_wasted, total_volume_filled_daily)
volume_meant, volume_dailyt = tulsi()
def upperV():
    area_m2 = area_upperV*10**6
    average_rainfall = average_mean*92
    total_volume_filled_mean = (average_rainfall*area_m2*0.8)/1000
    total_volume_wasted = total_volume_filled_mean - val4C
    total_volume_filled_daily = (today_rain*area_m2*0.8)/1000
    return (total_volume_wasted, total_volume_filled_daily)
volume_meanu, volume_dailyu = upperV()
def bhatsa():
    area_m2 = area_bhatsa*10**6
    average_rainfall = average_mean*92
    total_volume_filled_mean = (average_rainfall*area_m2*0.8)/1000
    total_volume_wasted = total_volume_filled_mean - val6C
    total_volume_filled_daily = (today_rain*area_m2*0.8)/1000
    return (total_volume_wasted, total_volume_filled_daily)
volume_meanb, volume_dailyb = bhatsa()
def Modak():
    area_m2 = area_modak*10**6
    average_rainfall = average_mean*92
    total_volume_filled_mean = (average_rainfall*area_m2*0.8)/1000
    total_volume_wasted = total_volume_filled_mean - val1C
    total_volume_filled_daily = (today_rain*area_m2*0.8)/1000
    return (total_volume_wasted, total_volume_filled_daily)
volume_meanm, volume_dailym = Modak()
def Middle():
    area_m2 = area_middle*10**6
    average_rainfall = average_mean*92
    total_volume_filled_mean = (average_rainfall*area_m2*0.8)/1000
    total_volume_wasted = total_volume_filled_mean - val7C
    total_volume_filled_daily = (today_rain*area_m2*0.8)/1000
    return (total_volume_wasted, total_volume_filled_daily)
volume_meanM, volume_dailyM = Middle()


total_volume_daily = volume_dailyb + volume_dailyt + volume_dailyu + volume_dailyv + volume_dailyta + volume_dailym + volume_dailyM
print('volume of water recieved today =',total_volume_daily)


total_volume_monsoon = volume_meanb + volume_meant + volume_meanta + volume_meanu + volume_meanv + volume_meanm + volume_meanM
total_volume_season = total_volume_monsoon*1000000
print('volume of water being wasted =',total_volume_season)

#125 litres per day
#population of distribution zones

dfP = pd.read_csv('WARDS_POPULATION (1).csv')
population = np.array(dfP['population'])
clean_population = []
for n in population:
    cl = n.translate(str.maketrans('','',string.punctuation))
    cle = int(cl)
    clean_population.append(cle)
total = sum(clean_population)
consumption_average =[]
for n in clean_population:
    consumption_val = n*125
    consumption_average.append(consumption_val)

total_volume_filt = sum(Capacity)*1000000
print('volume of water in the reservoir =',total_volume_filt)
total_volume = (total_volume_filt + total_volume_daily)
print('total volume of water in the reservoir =',total_volume)
data_average = []
x = 0
n = False
number_of_days = []
volume = []
while n is False:
    total = sum(consumption_average)
    reservoir = total_volume - total
    if reservoir < 0:
        n = True
    else:
        data_average.append(reservoir)
        total_volume = reservoir
        x = x + 1
        number_of_days.append(x)
        volume.append(reservoir)
Xs = number_of_days
Ys = []
for n in volume:
    m3 = n/1000
    Ys.append(m3)
plt.plot(Xs,Ys,c = 'b')
plt.xlabel('number of days')
plt.ylabel('volume of water in m^3')
plt.savefig('at current rate.jpg')
print('number of days water will last at current rate =',x)

def save_need():
    totalPop = sum(clean_population)
    total_volume_needed = 62*totalPop #62 -> detremined by iit researchers
    volume_present = total_volume_filt + total_volume_daily
    y = 0
    n_new = False
    number_days_final = []
    volume_final = []
    while n_new is False:
        reservoir_final = volume_present - total_volume_needed
        if reservoir_final < 0:
            n_new = True
        else:
            volume_present = reservoir_final
            y = y + 1
            number_days_final.append(y)
            volume_final.append(reservoir_final)
    return number_days_final ,volume_final

def save_by_10():
    totalPop = sum(clean_population)
    total_volume_needed = 115*totalPop
    volume_present = total_volume_filt + total_volume_daily
    y = 0
    n_new = False
    number_days_final = []
    volume_final = []
    while n_new is False:
        reservoir_final = volume_present - total_volume_needed
        if reservoir_final < 0:
            n_new = True
        else:
            volume_present = reservoir_final
            y = y + 1
            number_days_final.append(y)
            volume_final.append(reservoir_final)
    return number_days_final ,volume_final

number_save_10, save_10 = save_by_10()
n_save_10 = sum(1 for row in number_save_10)
number_save_need, save_need = save_need()
n_save_need = sum(1 for row in number_save_need)
print('by cutting water use by 10 litres we can last for = ', n_save_10)
print('by cutting down usage to what we need we can last for = ', n_save_need)
in_m310 = []
for n in save_10:
    calc = n/1000
    in_m310.append(calc)
plt.subplot(3,3,1)
plt.plot(number_save_10, in_m310, 'r')
plt.title('consumption reduced by 10 litres')
plt.xlabel('days')
plt.ylabel('volume in m^3')

in_m3save = []
for n in save_need:
    new_calc = n/1000
    in_m3save.append(new_calc)
plt.subplot(3,3,6)
plt.plot(number_save_need, in_m3save, 'g')
plt.title('consumption of 62 litres')
plt.xlabel('days')
plt.ylabel('volume in m^3')

def save_by_method(num1):
    totalPop = sum(clean_population)
    num2 = 125 - num1
    total_volume_needed = num2*totalPop
    volume_present = total_volume_filt + total_volume_daily
    y = 0
    n_new = False
    number_days_final = []
    volume_final = []
    while n_new is False:
        reservoir_final = volume_present - total_volume_needed
        if reservoir_final < 0:
            n_new = True
        else:
            volume_present = reservoir_final
            y = y + 1
            number_days_final.append(y)
            volume_final.append(reservoir_final)
    return number_days_final ,volume_final
print('Flushing down useful clean water \n– insert 500 ml to 1000 ml bottle in flush tank to save that much amount of water \nwith each flush amounting to saving 3 litres per person per day clean water',
      '\nselect option A to see the effect of the following\n')
print('Taking long showers without using a low flow showerhead. Reducing your shower \ntime by just 1-2 minutes can save up to 700 gallons per month.\n'
      'Using a low flow showerhead can save up to 800 gallons of water per month.', '\nselect option B to see the effect of the following\n')
options = {'A':3,'B':15}
input_val = input('Enter the option you want to select =')
data_val = options[input_val]
save_method_days, save_method_volume = save_by_method(data_val)
value_method = sum(1 for rows in save_method_days)
print('by cutting down usage, we can last for =', value_method)

in_m3method = []
for n in save_method_volume:
    calc_method = n/1000
    in_m3method.append(calc_method)
plt.subplot(3,3,7)
plt.plot(save_method_days, save_method_volume, 'b')
plt.title('reducing shower time')
plt.xlabel('days')
plt.ylabel('volume in m^3')
plt.savefig('graphs.jpg')

bot = Bot()
bot.login(username = "gforce2142",  password = "OmotecGforce2020")
#bot.upload_photo("E:/Python/Nasa hackathon/this years rainfall.jpg", caption = "this years rain")
#bot.upload_photo("E:/Python/Nasa hackathon/at current rate.jpg", caption = "at our current average usage of water per day, our lakes will last for 899 days before drying up.")
bot.upload_photo("E:/Python/Nasa hackathon/graphs.jpg", caption = "Taking long showers without using a low flow showerhead. Reducing your shower time by just 1-2 minutes can save up to 700 gallons per month. Using a low flow showerhead can save up to 800 gallons of water per month. The following shows the effects of reducing water usage. By decreasing your time in the shower by two minutes our lakes can last for 1022 days before drying up. As you can see, this small change has increased the life of our lakes by several days.")




























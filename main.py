import tweepy
import schedule
import time
import requests
import datetime
import settings

'''
Project: TwitterCityBot
Description: TwitterCityBot finds over 107 United States cities with the highest and lowest temperatures and publishes a tweet every four hours
Version 1.0.0
Author: Adi Bhan
'''

class TwitterBot():
    
    ''' Creating TwitterBot Class'''
    
    def __init__(self):
        
        self.client = tweepy.Client(consumer_key = settings.CONSUMER_KEY,
                                    consumer_secret = settings.CONSUMER_SECRET,
                                    access_token = settings.ACCESS_TOKEN,
                                    access_token_secret = settings.ACCESS_TOKEN_SECRET)
    
    def Tweet(self):
        
        ''' Tweet Method composes the tweet'''
      
        url2 = settings.BASE_URL + "appid=" + settings.API_KEY + "&q=" + Coldest_City   
        response2 = requests.get(url2).json()
        
        Temp_Coldest_City = response2['main']['temp'] 
        Temp_Coldest_City -= 273  
        
        Temp_Coldest_City_F = ((Temp_Coldest_City) * (9/5)) + 32
            
        url3 = settings.BASE_URL + "appid=" + settings.API_KEY + "&q=" + Hottest_City
        response3 = requests.get(url3).json()
        
        Temp_Hottest_City = response3['main']['temp']   
        Temp_Hottest_City -= 273
        
        Temp_Hottest_City_F = ((Temp_Hottest_City) * (9/5)) + 32
      
        Date  = datetime.datetime.now()
        self.tweet = self.client.create_tweet(text = 'OUT OF ' + str(self.City_Counter()) + ' CITIES\n\n' + 'Hottest City: ' + Hottest_City + ' ☀️' + '\n • Temperature: ' + str(round(Temp_Hottest_City,2)) +
                                            "° C │"  + str(round(Temp_Hottest_City_F,2)) + "° F\n\n" + 'Coldest City: ' + Coldest_City +  ' ❄️' + '\n • Temperature: ' + str(round(Temp_Coldest_City,2)) + "° C │" + str(round(Temp_Coldest_City_F,2)) + "° F"
                                            + "\n\n * as of " + str(Date) + "*")
    def City_Counter(self):
        
        ''' City Counter Method counts the number of cities in the list'''
    
        self.Cities_List = open(r'C:\Testing\TwitterTesting\us_cities_sample.txt','r')
        self.Cities_Count = 1
    
        for lines in self.Cities_List:
            self.Cities_Count += 1
            
        self.Cities_List.close()
        return self.Cities_Count     
       
def City_List_Getter():
    
    ''' Function gets each City and temperature from city dataset and stores it into list'''
    
    global Cities
    Cities = []
    
    Cities_List = open(r'C:\Testing\TwitterTesting\us_cities_sample.txt','r')
    
    for lines in Cities_List:
    
         New_City = lines.split()
         
         kelvin_city_temp = Temp_Finder(New_City)
         
         celsius_city_temp = kelvin_city_temp - 273
         
         Combo = New_City + [celsius_city_temp]
         
         Cities += Combo
    
    Cities_List.close()
    List_To_Dict_Converter(Cities)  
   

def List_To_Dict_Converter(listname):
    
    ''' Function converts List to Dictionary'''
    
    iterate = iter(listname)
    dictionary_city_list = dict(zip(iterate, iterate))
   
    Find_Max_Min_City(dictionary_city_list)
  
    
def Find_Max_Min_City(cities):
    
    ''' Method finds hottest and coolest city in the dictionary by finding 
        highest and lowest values of the key value pairs in the dictionary'''
    
    global Hottest_City
    Hottest_City = max(cities, key=cities.get)
    
    global Coldest_City
    Coldest_City = min(cities, key=cities.get)
   
def Temp_Finder(CityName):
    
    ''' Using WeatherAPI, finds temperature of each city'''
    
    # Converting list to string
    City = ''.join(CityName)

    url = settings.BASE_URL + "appid=" + settings.API_KEY + "&q=" + City
    response = requests.get(url).json()
    
    temp_min = response['main']['temp']
    
    return int(temp_min)

def RUNProgram():
    
    ''' Function starts the program '''
    
    City_List_Getter()
    Bot = TwitterBot()
    Bot.Tweet()
    
RUNProgram()

# Schedule Library allows us to run the program every 4 hours
schedule.every().hour.do(RUNProgram)
while True:
    schedule.run_pending()
    time.sleep(1)

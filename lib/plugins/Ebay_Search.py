#!/usr/bin/env python3
import requests, logging, os, re, datetime, plugins.common.General as General, json
from ebaysdk.finding import Connection

Plugin_Name = "Ebay"
The_File_Extension = ".html"

def Load_Configuration():
    File_Dir = os.path.dirname(os.path.realpath('__file__'))
    Configuration_File = os.path.join(File_Dir, 'plugins/common/configuration/config.json')
    logging.info(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " Loading configuration data.")

    try:

        with open(Configuration_File) as JSON_File:  
            Configuration_Data = json.load(JSON_File)

            for Ebay_Details in Configuration_Data[Plugin_Name.lower()]:

                if Ebay_Details['access_key']:
                    return Ebay_Details['access_key']

                else:
                    return None

    except:
        logging.warning(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " Failed to load location details.")

def Search(Query_List, Task_ID, **kwargs):
    Data_to_Cache = []
    Cached_Data = []

    if kwargs.get('Limit'):

        if int(kwargs["Limit"]) > 0:
            Limit = kwargs["Limit"]

    else:
        Limit = 10

    Directory = General.Make_Directory(Plugin_Name.lower())

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    Log_File = General.Logging(Directory, Plugin_Name.lower())
    handler = logging.FileHandler(os.path.join(Directory, Log_File), "w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    Ebay_API_Key = Load_Configuration()
    Cached_Data = General.Get_Cache(Directory, Plugin_Name)

    if not Cached_Data:
        Cached_Data = []

    Query_List = General.Convert_to_List(Query_List)

    for Query in Query_List:

        try:
            API_Request = Connection(appid=Ebay_API_Key, config_file=None)
            API_Response = API_Request.execute('findItemsAdvanced', {'keywords': Query})
            JSON_Output_Response = json.dumps(API_Response.dict(), indent=4, sort_keys=True)
            JSON_Response = json.dumps(API_Response.dict())
            JSON_Response = json.loads(JSON_Response)
            General.Main_File_Create(Directory, Plugin_Name, JSON_Output_Response, Query, ".json")

            if JSON_Response["ack"] == "Success":
                Current_Step = 0

                for JSON_Line in JSON_Response['searchResult']['item']:
                    Ebay_Item_URL = JSON_Line['viewItemURL']

                    if Ebay_Item_URL not in Cached_Data and Ebay_Item_URL not in Data_to_Cache and Current_Step < int(Limit):
                        Ebay_Item_Regex = re.search(r"http\:\/\/www\.ebay\.com\/itm\/([\w\d\-]+)\-\/\d+", Ebay_Item_URL)
                        headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0', 'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5'}
                        Ebay_Item_Response = requests.get(Ebay_Item_URL, headers=headers).text
                        Output_file = General.Create_Query_Results_Output_File(Directory, Query, Plugin_Name, Ebay_Item_Response, Ebay_Item_Regex.group(1), The_File_Extension)

                        if Output_file:
                            General.Connections(Output_file, Query, Plugin_Name, Ebay_Item_URL, "ebay.com", "Data Leakage", Task_ID, General.Get_Title(Ebay_Item_URL), Plugin_Name.lower())

                        Data_to_Cache.append(Ebay_Item_URL)
                        Current_Step += 1

            else:
                logging.warning(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " No results found.")

        except:
            logging.info(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " Failed to make API call.")

    if Cached_Data:
        General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "a")

    else:
        General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "w")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime, os, logging, re, requests, urllib, json, plugins.common.Connectors as Connectors
from bs4 import BeautifulSoup

Bad_Characters = ["|", "/", "&", "?", "\\", "\"", "\'", "[", "]", ">", "<", "~", "`", ";", "{", "}", "%", "^"]
Configuration_File = os.path.join('plugins/common/config', 'config.json')

def Date():
    return str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def Logging(Directory, Plugin_Name):

    try:
        Main_File = Plugin_Name + "-log-file.log"
        General_Directory_Search = re.search(r"(.*)\/\d{4}\/\d{2}\/\d{2}", Directory)

        if General_Directory_Search:
            Complete_File = os.path.join(General_Directory_Search.group(1), Main_File)
            return Complete_File

    except:
        logging.warning(Date() + " Failed to initialise logging.")


def Get_Cache(Directory, Plugin_Name):
    Main_File = Plugin_Name + "-cache.txt"
    General_Directory_Search = re.search(r"(.*)\/\d{4}\/\d{2}\/\d{2}", Directory)

    if General_Directory_Search:
        Complete_File = os.path.join(General_Directory_Search.group(1), Main_File)

        try:

            if os.path.exists(Complete_File):
                File_Input = open(Complete_File, "r")
                Cached_Data = File_Input.read()
                File_Input.close()
                return Cached_Data

            else:
                logging.info(Date() + " No cache file found, caching will not be used for this session.")

        except:
            logging.warning(Date() + " Failed to read file.")

    else:
        logging.warning(Date() + " Failed to regex directory. Cache not read.")

def Write_Cache(Directory, Data_to_Cache, Plugin_Name, Open_File_Type):
    Main_File = Plugin_Name + "-cache.txt"
    General_Directory_Search = re.search(r"(.*)\/\d{4}\/\d{2}\/\d{2}", Directory)

    if General_Directory_Search:
        Complete_File = os.path.join(General_Directory_Search.group(1), Main_File)

        try:
            File_Output = open(Complete_File, Open_File_Type)
            Current_Output_Data = "\n".join(Data_to_Cache) + "\n"
            File_Output.write(Current_Output_Data)
            File_Output.close()

        except:
            logging.warning(Date() + " Failed to create file.")

    else:
        logging.warning(Date() + " Failed to regex directory. Cache not written.")

def Convert_to_List(String):

    try:

        if ', ' in String:
            List = String.split(', ')
            return List

        elif ',' in String:
            List = String.split(',')
            return List

        else:
            List = [String]
            return List

    except:
        logging.warning(Date() + " Failed to convert the provided query to a list.")

class Connections():

    def __init__(self, Input, Plugin_Name, Domain, Result_Type, Task_ID, Concat_Plugin_Name):

        try:
            self.Plugin_Name = str(Plugin_Name)
            self.Domain = str(Domain)
            self.Result_Type = str(Result_Type)
            self.Task_ID = str(Task_ID)
            self.Input = str(Input)
            self.Concat_Plugin_Name = str(Concat_Plugin_Name)

        except:
            logging.warning(Date() + " Error setting initial variables.")

    def Output(self, Complete_File, Link, DB_Title, **kwargs):

        try:

            if "Dump_Types" in kwargs:
                self.Dump_Types = kwargs["Dump_Types"]
                self.Title = "Data for input: " + self.Input + ", found by Scrummage plugin " + self.Plugin_Name + ".\nData types include: " + ", ".join(Dump_Types) + ".\nAll data is stored in " + Complete_File + "."
                self.Ticket_Subject = "Scrummage " + self.Plugin_Name + " results for query " + self.Input + "."
                self.Ticket_Text = "Results were identified for the search " + self.Input + " performed by the Scrummage plugin " + self.Plugin_Name + ".\nThe following types of sensitive data were found:\n - " + "\n - ".join(Dump_Types) + ". Please ensure these results do not pose a threat to your organisation, and take the appropriate action necessary if they pose a security risk. The result data is stored in a file located at " + Complete_File + "."

            else:
                self.Title = "Data for input: " + self.Input + ", found by Scrummage plugin " + self.Plugin_Name + ".\nAll data is stored in " + Complete_File + "."
                self.Ticket_Subject = "Scrummage " + self.Plugin_Name + " results for query " + self.Input + "."
                self.Ticket_Text = "Results were identified for the search " + self.Input + " performed by the Scrummage plugin " + self.Plugin_Name + ". Please ensure these results do not pose a threat to your organisation, and take the appropriate action necessary if they pose a security risk. The result data is stored in a file located at " + Complete_File + "."

        except:
            logging.warning(Date() + " Error setting unique variables.")

        Connectors.Scumblr_Main(self.Input, DB_Title, self.Title)
        Connectors.RTIR_Main(self.Ticket_Subject, self.Ticket_Text)
        Connectors.JIRA_Main(self.Ticket_Subject, self.Ticket_Text)
        Connectors.Email_Main(self.Ticket_Subject, self.Ticket_Text)
        Connectors.Slack_Main(self.Ticket_Text)
        Relative_File = Complete_File.replace(os.path.dirname(os.path.realpath('__file__')), "")
        logging.info(Date() + " Adding item to Scrummage database.")

        if DB_Title:
            Connectors.Main_Database_Insert(DB_Title, self.Plugin_Name, self.Domain, Link, self.Result_Type, Relative_File, self.Task_ID)
            Connectors.Elasticsearch_Main(DB_Title, self.Plugin_Name, self.Domain, Link, self.Result_Type, Relative_File, self.Task_ID, self.Concat_Plugin_Name)
            Connectors.CSV_Output(DB_Title, self.Plugin_Name, self.Domain, Link, self.Result_Type, Relative_File, self.Task_ID)
            Connectors.DOCX_Output(DB_Title, self.Plugin_Name, self.Domain, Link, self.Result_Type, Relative_File, self.Task_ID)
            Connectors.Defect_Dojo_Output(DB_Title, self.Ticket_Text)

        else:
            Connectors.Main_Database_Insert(self.Plugin_Name, self.Plugin_Name, self.Domain, Link, self.Result_Type, Relative_File, self.Task_ID)
            Connectors.Elasticsearch_Main(self.Plugin_Name, self.Plugin_Name, self.Domain, Link, self.Result_Type, Relative_File, self.Task_ID, self.Concat_Plugin_Name)
            Connectors.CSV_Output(self.Plugin_Name, self.Plugin_Name, self.Domain, Link, self.Result_Type, Relative_File, self.Task_ID)
            Connectors.DOCX_Output(self.Plugin_Name, self.Plugin_Name, self.Domain, Link, self.Result_Type, Relative_File, self.Task_ID)
            Connectors.Defect_Dojo_Output(self.Plugin_Name, self.Ticket_Text)

def Main_File_Create(Directory, Plugin_Name, Output, Query, Main_File_Extension):
    Main_File = "Main-file-for-" + Plugin_Name + "-query-" + Query + Main_File_Extension
    Complete_File = os.path.join(Directory, Main_File)
    Appendable_Output_Data = []

    try:

        if not os.path.exists(Complete_File):
            File_Output = open(Complete_File, "w")
            File_Output.write(Output)
            File_Output.close()
            logging.info(Date() + " Main file created.")

        else:

            if not Main_File_Extension == ".json":
                File_Input = open(Complete_File, "r")
                Cache_File_Input = File_Input.read()
                File_Input.close()
                
                for Temp_Scrape in Cache_File_Input:

                    if not Temp_Scrape in Cache_File_Input:
                        Appendable_Output_Data.append(Temp_Scrape)

                if Appendable_Output_Data:
                    logging.info(Date() + " New data has been discovered and will be appended to the existing file.")
                    Appendable_Output_Data_String = "\n".join(Appendable_Output_Data)
                    File_Output = open(Complete_File, "a")
                    File_Output.write("\n" + Appendable_Output_Data_String)
                    File_Output.close()
                    logging.info(Date() + " Main file appended.")

                else:
                    logging.info(Date() + " No new data has been discovered, no point continuing.")

            else:
                File_Output = open(Complete_File, "w")
                File_Output.write(Output)
                File_Output.close()
                logging.info(Date() + " Main file created.")

        return Complete_File

    except:
        logging.warning(Date() + " Failed to create file.")

def Data_Type_Discovery(Data_to_Search):
    # Function responsible for determining the type of data found. Examples: Hash_Type, Credentials, Email, or URL.

    try:
        Dump_Types = []
        Hash_Types = [["MD5","([a-fA-F0-9]{32})\W"],["SHA1","([a-fA-F0-9]{40})\W"],["SHA256","([a-fA-F0-9]{64})\W"]]

        for Hash_Type in Hash_Types: # Hash_Type identification
            Hash_Regex = re.search(Hash_Type[1], Data_to_Search)

            if Hash_Regex:
                Hash_Type_Line = Hash_Type[0] + " hash"

                if not Hash_Type_Line in Dump_Types:
                    Dump_Types.append(Hash_Type_Line)

            else:
                pass

        Credential_Regex = re.search(r"[\w\d\.\-\_]+\@[\w\.]+\:.*", Data_to_Search)

        if Credential_Regex: # Credentials identification

            if not "Credentials" in Dump_Types:
                Dump_Types.append("Credentials")

        else:
            EmailRegex = re.search("[\w\d\.\-\_]+\@[\w\.]+", Data_to_Search)
            URLRegex = re.search("(https?:\/\/(www\.)?)?([-a-zA-Z0-9:%._\+#=]{2,256})(\.[a-z]{2,6}\b([-a-zA-Z0-9:%_\+.#?&//=]*))", Data_to_Search)

            if EmailRegex: # Email Identification

                if not "Email" in Dump_Types:
                    Dump_Types.append("Email")

            if URLRegex: # URL Indentification

                if not "URL" in Dump_Types:
                    Dump_Types.append("URL")

        return Dump_Types

    except:
        logging.warning(Date() + " Failed to determine data type.")

def Create_Query_Results_Output_File(Directory, Query, Plugin_Name, Output_Data, Query_Result_Name, The_File_Extension):

    for Character in Bad_Characters:

        if Character in Query:
            Query = Query.replace(Character, "")

    try:
        The_File = Plugin_Name + "-Query-" + Query + "-" + Query_Result_Name + The_File_Extension
        Complete_File = os.path.join(Directory, The_File)

        if not os.path.exists(Complete_File):

            with open(Complete_File, 'w') as Current_Output_file:
                Current_Output_file.write(Output_Data)

            logging.info(Date() + " File: " + Complete_File + " created.")

        else:
            logging.info(Date() + " File already exists, skipping creation.")

        return Complete_File

    except:
        logging.warning(Date() + " Failed to create file.")

def Create_Scrape_Results_File(Directory, Plugin_Name, Output_Data, ID, The_File_Extension):

    try:
        The_File = Plugin_Name + "-" + ID + The_File_Extension
        Complete_File = os.path.join(Directory, The_File)

        if not os.path.exists(Complete_File):

            with open(Complete_File, 'w') as Current_Output_file:
                Current_Output_file.write(Output_Data)

            logging.info(Date() + " File: " + Complete_File + " created.")
            return Complete_File

        else:
            logging.info(Date() + " File already exists, skipping creation.")

    except:
        logging.warning(Date() + " Failed to create file.")

def Load_Location_Configuration():
    Valid_Locations = ['ac', 'ac', 'ad', 'ae', 'af', 'af', 'ag', 'ag', 'ai', 'ai', 'al', 'am', 'am', 'ao', 'aq', 'ar', 'as', 'at', 'au', 'az', 'ba', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bi', 'bj', 'bn', 'bo', 'bo', 'br', 'bs', 'bt', 'bw', 'by', 'by', 'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'cn', 'co', 'co', 'co', 'cr', 'cu', 'cv', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ec', 'ee', 'eg', 'es', 'et', 'eu', 'fi', 'fj', 'fm', 'fr', 'ga', 'ge', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gp', 'gp', 'gr', 'gr', 'gt', 'gy', 'gy', 'gy', 'hk', 'hk', 'hn', 'hr', 'ht', 'ht', 'hu', 'hu', 'id', 'id', 'ie', 'il', 'im', 'im', 'in', 'in', 'io', 'iq', 'iq', 'is', 'it', 'je', 'je', 'jm', 'jo', 'jo', 'jp', 'jp', 'ke', 'kg', 'kh', 'ki', 'kr', 'kw', 'kz', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'ma', 'md', 'me', 'mg', 'mk', 'ml', 'mm', 'mn', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'mx', 'my', 'mz', 'na', 'ne', 'nf', 'ng', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nr', 'nu', 'nz', 'om', 'pa', 'pe', 'pe', 'pf', 'pg', 'ph', 'pk', 'pk', 'pl', 'pl', 'pn', 'pr', 'ps', 'ps', 'pt', 'py', 'qa', 'qa', 're', 'ro', 'rs', 'rs', 'ru', 'ru', 'rw', 'sa', 'sb', 'sc', 'se', 'sg', 'sh', 'si', 'sk', 'sl', 'sl', 'sm', 'sn', 'so', 'sr', 'st', 'sv', 'sy', 'td', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tt', 'tz', 'ua', 'ua', 'ug', 'uk', 'us', 'us', 'uy', 'uz', 'uz', 'vc', 've', 've', 'vg', 'vi', 'vn', 'vu', 'ws', 'za', 'zm', 'zw']

    try:

        with open(Configuration_File) as JSON_File:  
            Configuration_Data = json.load(JSON_File)

            for General_Details in Configuration_Data['general']:
                Location = General_Details['location']

            if (len(Location) > 2) or (Location not in Valid_Locations):
                logging.warning(Date() + " An invalid location has been specified, please provide a valid location in the config.json file.")

            else:
                logging.info(Date() + " Country code " + Location + " selected.")
                return Location

    except:
        logging.warning(Date() + " Failed to load location details.")

def Make_Directory(Plugin_Name):
    Today = datetime.datetime.now()
    Year = str(Today.year)
    Month = str(Today.month)
    Day = str(Today.day)

    if len(Month) == 1:
        Month = "0" + Month

    if len(Day) == 1:
        Day = "0" + Day

    File_Path = os.path.dirname(os.path.realpath('__file__'))
    Directory = File_Path + "/static/protected/output/" + Plugin_Name + "/" + Year + "/" + Month + "/" + Day

    try:
        os.makedirs(Directory)
        logging.info(Date() + " Using directory: " + Directory + ".")
        return Directory

    except:
        logging.warning(Date() + " Using directory: " + Directory + ".")
        return Directory

def Get_Latest_URLs(Pull_URL, Scrape_Regex_URL):
    Scrape_URLs = []
    Content = ""
    Content_String = ""

    try:
        Content = requests.get(Pull_URL).text
        Content_String = str(Content)

    except:
        logging.warning(Date() + " Failed to connect, if you are using the Tor network, please make sure you're running the Tor proxy and are connected to it.")

    try:
        Scrape_URLs_Raw = re.findall(Scrape_Regex_URL, Content_String)

        for Temp_URL_Extensions in Scrape_URLs_Raw:

            if not Temp_URL_Extensions in Scrape_URLs:
                Scrape_URLs.append(Temp_URL_Extensions)

    except:
        logging.warning(Date() + " Failed to regex URLs.")

    return Scrape_URLs

def Get_Title(URL):

    try:

        if 'file:/' not in URL:
            Soup = BeautifulSoup(urllib.request.urlopen(URL), features="lxml")
            return Soup.title.text

        else:
            logging.warning(Date() + " this function does not work on files.")

    except:
        logging.warning(Date() + " failed to get title.")
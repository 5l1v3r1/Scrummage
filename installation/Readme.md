[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# Installation

**This tool currently supports Debian, RHEL, and SUSE based linux distributions.**

Clone this repository to the location where you want to run the web application from.

    1. git clone https://github.com/matamorphosis/Scrummage

Navigate to the installation directory.

    2. cd installation

Run the dependencies.sh bash script with root privileges, to install all necessary dependencies.

    3. sudo bash dependencies.sh

As part of this script it will install all python dependencies in the python_requirements.txt file and run the Create_Tables.py script to create all necessary tables in the backend database. If you want to change the default username and database, which are both set to “Scrummage”, change the following lines in the script:

DATABASE="scrummage"  
USER="scrummage"

When the script finishes, it should print out the username and database it has created; furthermore, a randomly generated password used. Please retain this information and update the config.json file located in the bin/plugins/common/configuration/ directory. Provide the details under "postgresql". If you would like to create a new user, use the "Create_User.py" script located in the installation directory. The command is as follows:
    
    4. python3 Create_User.py --username/-u Username --password/-p Password --admin/-a [True | False] --blocked/-b [True | False]

Next navigate to the parent directory and then to the bin directory and start the server.

    5. cd ../bin
    6. python3 main.py


# Tasks and APIs  
Here is listed the currently supported tasks and the requirements for each task:
Note: All provided input is santised by the server-side code, please create an issue if you can find anyway to bypass it :).
Each task has been provided with a test query to verify the plugin is working. All test queries are case-sensitive, or reference something you can use to test. While the provided test queries may appear random, they are queries that will generate a bounty of results.
Tasks are provided to allow users to search various corners of the web for a given query.
Multiple queries can be provided when creating a task, simply use a comma to separate the values.
Any files that need to be editted, can be found in the “bin/plugins/common/configuration” directory.

**GENERAL:**  
Several of the plugins use location to assist in providing more relevant results, please ensure you set this in the config.json file, under “general”:

  	"general": [
		{
		      "location": "au"
		}
	],
  

**Ahmia Darkweb Search**  
This task requires no API keys, and works by performing a search for both Tor and I2P sites on the provided query.

*Test query: test*


**Blockchain Search**  
This task doesn’t require an API key, and contains 2 subtasks, 1 for searching blockchain addresses and the other for search tasks. Furthermore, these tasks currently search for Bitcoin, Bitcoin Cash, and Ethereum. Therefore, in the web app there are 6 options:
* Blockchain Bitcoin Address Search
* Blockchain Bitcoin Cash Address Search
* Blockchain Ethereum Address Search
* Blockchain Bitcoin Transaction Search
* Blockchain Bitcoin Cash Transaction Search
* Blockchain Ethereum Transaction Search


**Certificate Transparency**  
This task requires an API key, and works by performing an API search against the sslmate.com website. Registration is free and easy. After obtaining the API key, please add it to the config.json file, under “sslmate”:

  	"sslmate": [
		{
		      "api_key": "",
		      "search_subdomain": "true or false"
		}
	],

*Test query: google.com*

*API Link: https://sslmate.com/help/api/rest*


**Craigslist Search**  
This task doesn’t require an API key, and works by performing a search against the craigslist website. However, because Craigslist works based on a city location this will need to be prespecified in the configuration file.

  	"craigslist": [
		{
		      "city": "Sydney"
		}
	],

*Test query: love*


**Domain Fuzzer**  
This task doesn’t require an API key, and works by attempting to resolve a provided list of domains. There are 4 different domain fuzzer tasks within this tool:
* *Character Switcher* – This a unique tool works by calling a custom library called “Rotor.py” and uses it to generate every possible combination of the given domain’s body using phoenetic, greek, and cyrillic alphabets. For example of your domain contains the letter “a”, it will itertate through the word using each of the following characters in the letters place:
  * a, а, à, á, â, ã, ä, å, ā, ă, ą - While the first 2 characters look the same, they have different unicode values and therefore you could have 2 facebook.com domains with 2 different unicode characters that look like a, which to anyone would make the domain look legitimate. While the other characters are a lot more obvious, the program takes the liberty to check for them anyway. A practical example can be seen in the following screenshot:
  *![Char Switch](/installation/char_switch.png)
  * After each combination has been generated this tool iterates through each one and attempts to resolve it to an IP address, if it does a result is created for that domain.
  * The ultimate use case of this would be to identity domain spoofs which use domains similar to your domain or identical to the naked eye.
  * FYI this can be a slow plugin depending on the length and the amount of domains it attempts to resolve. 1 short domain such as google.com shouldn’t take too long – around 1-2 minutes.

* *Regular Extensions / Suffixes* – This tool works by simply switching out the domain extension with other common extensions. Such as .com, .net, .gov. After this the tool iterates through each generated domain and attempts to resolve it to an IP address, if it does a result is created for that domain.

* *Global Extensions / Suffixes* – This tool works by simply switching out the domain extension with the extension of every country. Such as .com.au, .co.nz, etc. After this the tool iterates through each generated domain and attempts to resolve it to an IP address, if it does a result is created for that domain.

* *All Extensions / Suffixes* – This tool works by simply switching out the domain extension with the extension of every country for each regular extension. Such as .com.au, .net.au, .gov.au, etc. After this the tool iterates through each generated domain and attempts to resolve it to an IP address, if it does a result is created for that domain. FYI this is a slow plugin due to the amount of domains it attempts to resolve.

*Test query: google.com*


**Ebay Search**  
This task requires an API key, and works by performing an API search against the ebay.com website. Registration is free and easy. After obtaining the API key, please add it to the config.json file, under “ebay”:

	"ebay": [
		{
		      "access_key": ""
		}
	],

*Test query: computer*

*API Link: https://developer.ebay.com/*


**Google Play Store Search**  
This task requires no API keys, and works by querying the play.google.com site.

*Test query: whatsapp*


**Google Search**  
This task requires an API key, and works by performing an API search against the google.com website. Registration is free and easy. After obtaining the API key and Custom Search Engine (CSE) details, please add it to the config.json file, under “google”:

  	"google": [
		{
		      "cx": "",
		      "application_name": "",
		      "application_version": "",
		      "developer_key": ""
		}
	],

*Test query: chrome*

*API Links: https://console.developers.google.com/apis/dashboard, https://developers.google.com/apis-explorer/#p/*


**Have I Been Pwned Search**  
This task requires no API keys, and works by performing a search against the haveibeenpwned.com site. There are 4 kinds of search options represented by four options in the web application:
* Email Search – Gets pastes affecting a given email address.
* Breach Search – Use this to search for a public data breach.
*Test query: Adobe*
* Account Search – Use this to search for email addresses in data breaches.
*Test query: [YOUR EMAIL]*
* Password Search – Use this to see if your password has been found in any data breaches.
*Test query: password*


**Instagram Search**  
This task requires no API keys, and works by performing a search against the instagram.com site. There are 4 kinds of search options represented by four options in the web application:
* User Search – Use this to search for an instagram user.
*Test query: [Your username]*
* Tag Search – Use this to search for an instagram tag.
*Test query: cat*
* Location Search – Use this to search for email addresses in data breaches.
*Test query: 7226110 (This number represents Tokyo, Japan.)*
* Media Search – Use this to see if your password has been found in any data breaches.
*Test query: BFRO_5WBQfc (This is just a random instagram promo video from a few years back)*


**iTunes Store Search**  
This task requires no API keys, and works by performing a search against the itunes.apple.com site.

*Test query: jack johnson*


**Pinterest Search**  
This task requires an API key, and works by performing a search against the pinterest.com site. There are 2 kinds of search options available, represented by 2 options in the web application:
* Pin Search - Searches for a pin based on a given pin id.
*Test query: 509258670361306287*
* Board Search - Searches for pins on a board based on a given board id.
*Test query: 509258739053404977*

After obtaining the API details and oauth token, please add the appropriate details to the config.json file, under "pinterest":
  
  	"pinterest": [
		{
		      "oauth_token": ""
		}
	],


*API Link: https://developers.pinterest.com/docs/api/overview/?*


**Phishtank Search**  
This task requires no API keys, and works by performing a search against the phishtank.com site for known phishing attacks against a company, this search has a predefined list and won’t search for just any domain. However, a lot of well-known companies are in the list whether you work for one or one is a client of your companies, this search may come in handy.

*Test query: [Refer to the predefined list in the web app.]*


**Reddit Search**  
This task requires an API key, and works by performing an API search against the reddit.com website. Registration is free and easy. After obtaining the API key and other details, please add it to the config.json file, under “reddit”:
  
  	"reddit": [
		{
		      "client_id": "",
		      "client_secret": "",
		      "user_agent": "",
		      "username": "",
		      "password": "",
		      "subreddits": "all"
		}
	],

*Test query: cooking*

*API Link: https://www.reddit.com/dev/api/*


**RSS Feed Search**  
This task requires no API keys, and works by performing a search against a pre-specified list of RSS feeds for a given query. To add or remove RSS feeds from this list you will need to edit the “RSS_Feeds.txt” file. The file by default contains 34 common, well-known RSS feeds.

*Test query: [Refer to the predefined list in the web app.]*


**Twitter Search**  
This task requires an API key, and works by performing an API search against the twitter.com website. Registration is free and easy. After obtaining the API key and other details, please add it to the config.json file, under “twitter”:

	"twitter": [
		{
			"CONSUMER_KEY": "",
			"CONSUMER_SECRET": "",
			"ACCESS_KEY": "",
			"ACCESS_SECRET": ""
		}
	],

*Test query: BarackObama*

*API Link: https://developer.twitter.com/en/docs.html*

**Vehicle Registration Search**  
  
*Note: This search only supports Australian registration numbers.*  
  
This task doesn't require any API keys, and works by performing an API search against a publicly available car insurance site to obtain the details of the vehicle that matches the query provided which should be a valid registration plate number. For this search to work a valid Australian state/territory must be provided in the config.json file, under "vehicle-registration-search":

	"vehicle-registration-search": [
		{
			"state": "NSW, QLD, VIC, etc."
		}
	]

*Test query: [any australian license plate]*

**Vulners Search**  
This task requires an API, and works by performing an API search against the vulners.com site, which uses the vulners database that contains exploits and vulnerabilities, to find such items that are similar to the provided query. After obtaining the API key and other details, please add it to the config.json file, under “vulners”:

	"vulners": [
		{
			"api_key": ""
		}
	]

*Test query: hikvision*

*API Link: https://vulners.com*

**Windows Store Search**  
This task requires no API keys, and works by querying the microsoft.com site.

*Test query: david*


**YouTube Search**  
This task requires an API key, and works by performing an API search against the youtube.com website. Registration is free and easy. After obtaining the API key and other details, please add it to the config.json file, under “youtube”:

	"youtube": [
		{
			"developer_key": "",
			"application_name": "",
			"application_version": "",
			"location": "37.42307,-122.08427",
			"location_radius": "5km"
		}
	],
  
*Test query: beauty*

*API Link: https://developers.google.com/youtube/v3/*

FYI: Please use google maps or similar to get your location in a format similar to the location above; furthermore, feel free to change location_radius, but please remember to use kilometres (km) after the integer.

# Output Alert Options  
By default, Scrummage stores all output data in 1 of 4 main output formats:
* .html
* .json
* .csv
* .txt (Not used by current plugins)

When Scrummage creates a result it creates refences to the result link, domain, and output file; furthermore, functionality is provided to create a screenshot for a result, through the link. So essentially you will most of the time end up with an output file and a screenshot which act as evidence.
!! Warning !!  -  Deleting a result will delete the output and screenshot files too.

On top of this Scrummage provides an additional 5 ways of alerting the user when a result is created. Please note each alert you enable will create an alert for each result. For example if you have slack channel notifications and email enabled. An email will be sent alongside a Slack channel notification for every result found by a plugin.

**Scumblr Database Output**  
The Scrummage team is well aware another open-source tool called Scumblr, developed by Netflix, performs some of the same functionality as Scrummage; furthermore, those who follow Scumblr know it currently is deprecated, and has been looking for a new developer for the last 6 months. The github repo can be found at https://github.com/Netflix-Skunkworks/Scumblr. Scrummage provides this functionality to current users of Scumblr by providing results to the Scumblr database so they dont have to view results in two different web applications, but can still benefit from both. To enable this, enter Scumblr’s backend postgresql database details to the config.json file, under “scumblr”:

    "scumblr": [
        {
            "host": "",
            "port": 5432,
            "database": "",
            "user": "",
            "password": ""
        }
    ],

**Request Tracker for Incident Response (RTIR) Ticket Alert**  
In the world of Incident Response, RTIR is a bit of a veteran program; therefore, functionality has been provided for RTIR. Currently, this method only supports Cookie-Based authentication, while there is a python library for RTIR, the library is old and doesn’t support python3. Rather than attempting to rewrite it, the Scrummage developers decided to go with cookie-based auth as it is very common, and used requests to handle it. To enable this mode, enter the RTIR details into the config.json file, under “RTIR”:

    "rtir": [
        {
            "service": "http",
            "host": "",
            "port": 80,
            "user": "",
            "password": "",
            "authenticator": ""
        }
    ],

Some teams that use RTIR use it’s SMTP functionality and for those teams, they could leverage the email output functionality below to achieve the same result.

**Atlassian JIRA Ticket Alert**  
While JIRA is typically used for software development projects, for tracking bugs and tasks, in the event a user wishes to use it for tracking incidents, it is available. To enable this mode, enter the JIRA details into the config.json file, under “JIRA”:

    "JIRA": [
        {
            "project_key": "",
            "address": "",
            "username": "",
            "password": "",
            "ticket_type": ""
        }
    ],

**Elasticsearch Output**  
Currently Elasticsearch is rapidly growing in popularity and therefore is included as an output option. To enable this mode, please enter the details in config.json under “elasticsearch”:

    "elasticsearch": [
        {
            "service": "http://",
            "host": "",
            "port": 9200
        }
    ],

**Email Alerts**  
Email alerts have been included, where the user specifies both the from address and the to address. The from address will also the user to specify the username and password of the from email address. To enable this mode, please enter the details in config.json under “email”:

    "email": [
        {
            "smtp_server": "",
            "smtp_port": 25,
            "from_address": "",
            "from_password": "",
            "to_address": ""
        }
    ],

**Slack Channel Notifications**  
Slack channel notifications work by having a message sent to a slack channel . To enable this mode, enter the Slack Channel details into the config.json file, under “slack”:

    "slack": [
        {
            "token": "",
            "channel": ""
        }
    ],

# Setting up your first task

**Limits**  
All tasks have a limit option available except for the following:
* Certificate Transparency
* Domain Fuzzer - All Extensions
* Domain Fuzzer - Alpha-Linguistic Character Switcher
* Domain Fuzzer - Global Domain Suffixes
* Domain Fuzzer - Regular Domain Suffixes
* Have I Been Pwned - Email Search
* Have I Been Pwned - Breach Search
* Have I Been Pwned - Password Search
* Instagram Media Search
* Pinterest Pin Search
* Vehicle Registration Search

All tasks that have a limit have their default limit set to 10; therefore, if you don’t specify a limit it’ll be autoset to 10.


**Frequency / Cron Jobs**  
Frequency has been provided as an option when creating a task. The syntax for frequency is exactly the same as linux cron jobs and this is verified on input. When a frequency is added or updated, a cronjob will appear when you check crontab. Furthermore, it will be removed if the user updates the task to not use a frequency or deletes the task.
Creating a task with a frequency:  
![Char Switch](/installation/task_1.png)

Verifying the task has been created:  
![Char Switch](/installation/task_2.png)

Verifying the cronjob has been created:  
![Char Switch](/installation/task_3.png)

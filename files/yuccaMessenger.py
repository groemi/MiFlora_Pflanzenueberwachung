everythingOk = "Hallo Welt, es ist ein wunderschöner Tag und mir geht es gut"
infoText = "Ich möchte gerne "
warnText = "Ich muss "
critText = "Ich muss unbedingt "

#alertTexts for Telegram Messages
#yout can customize them as you want 
moistureText = "durchdringend gegossen werden"
batteryText = "eine neue Batterie bekommen"

import requests
from influxdb_client import InfluxDBClient

url = "http://myInfluxURL"
org = "my-org"
bucket = "_monitoring"
token = "myToken"

query_BatteryStatus = 'from(bucket: "_monitoring")\
  |> range(start: -1h)\
  |> filter(fn: (r) => r["_measurement"] == "statuses")\
  |> filter(fn: (r) => r["_check_id"] == "06de6697a6b2a000")\
  |> filter(fn: (r) => r["_check_name"] == "Battery")\
  |> filter(fn: (r) => r["_field"] == "_message")\
  |> last()'

query_MoistureStatus = 'from(bucket: "_monitoring")\
  |> range(start: -1h)\
  |> filter(fn: (r) => r["_measurement"] == "statuses")\
  |> filter(fn: (r) => r["_check_id"] == "06de80192772a000")\
  |> filter(fn: (r) => r["_check_name"] == "Moisture")\
  |> filter(fn: (r) => r["_field"] == "_message")\
  |> last()'

#establish a connection
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

def queryStatus(query):
    result = client.query_api().query(org=org, query=query)

    results = []
    for table in result:
        for record in table.records:
            results.append((record.values.get('_level')))

    return(results[0])


def telegram_bot_sendtext(bot_message):
    
    bot_token = 'botToken'
    bot_chatID = 'chatID'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    print("message sent")
    return response.json()
    
    

greeting = telegram_bot_sendtext(everythingOk)
print(greeting)



def buildAndSendMessageString(alertLvl, alertText):
    if alertLvl == 'info':
        telegram_bot_sendtext(infoText+alertText)
    elif alertLvl == 'warn':
        telegram_bot_sendtext(warnText+alertText)
    elif alertLvl == 'crit': 
        telegram_bot_sendtext(critText+alertText)


buildAndSendMessageString(queryStatus(query_BatteryStatus),batteryText)
buildAndSendMessageString(queryStatus(query_MoistureStatus),moistureText)
print(queryStatus(query_MoistureStatus))
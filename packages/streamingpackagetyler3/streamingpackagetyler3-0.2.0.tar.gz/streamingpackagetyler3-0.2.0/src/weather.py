import requests
from bs4 import BeautifulSoup
import time as t
import pandas as pd
import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import json
def weather_streaming():
    def getdata(city):
        #creating url and request instance
        url="https://www.google.com/search?q="+"weather"+city
        html=requests.get(url).content

        #getting raw data
        soup= BeautifulSoup(html,'html.parser')
        temp=soup.find('div',attrs={'class':'BNeawe iBp4i AP7Wnd'}).text
        str=soup.find('div',attrs={'class':'BNeawe tAd8D AP7Wnd'}).text

        #forematting data
        data=str.split('\n')  
        time=data[0]
        sky=data[1] 

        #printing all data
        t.sleep(60)
        dataframe=pd.DataFrame([[temp,time,sky]],columns=['temperature','time','skycondition'])
        dataframe=dataframe.to_json(orient='records', lines=True)
        
        return dataframe

    getdata('New York')

    async def run():
        while True:
            await asyncio.sleep(5)
            producer=EventHubProducerClient.from_connection_string(conn_str='Endpoint=sb://streamingdata-demo-dev.servicebus.windows.net/;SharedAccessKeyName=weatherdata-policy;SharedAccessKey=y8tGytHlo6RMIIIyWSzJRONpl5wvr42Xn+AEhDyJg34=;EntityPath=weatherdata-streaming-demo-dev',eventhub_name='weatherdata-streaming-demo-dev')
            async with producer:
                #Create a batch.
                event_data_batch=await producer.create_batch()
                d=getdata('New York')
                d = json.loads(d)
                #Add events to the batch
                event_data_batch.add(EventData(json.dumps(d)))

                #send the batch of events to the event hub
                await producer.send_batch(event_data_batch)
                t.sleep(3)
                print(d)
                print('Data sent successfully to eventhubs!!')
            
    loop=asyncio.get_event_loop()
    try:
        asyncio.ensure_future(run())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print('CloseingloopNow!!')
        loop.close()

if __name__=="__main__":
    weather_streaming()




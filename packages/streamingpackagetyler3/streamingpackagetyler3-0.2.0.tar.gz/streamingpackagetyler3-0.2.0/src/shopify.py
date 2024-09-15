import os 
import json 
from google.cloud import pubsub_v1
import time as t
import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData


subscription_name='projects/wired-victor-432822-p3/subscriptions/demo1-sub'
creds='demoCredential.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=creds


def shopify_streamingdata_functin():
    def callback(message):
        order_data=json.loads(message.data)
        keep = ['id','cancel_reason','cancelled_at','checkout_id','created_at','customer_locale','financial_status','presentment_currency','processed_at','subtotal_price','billing_address','line_items']
        order_data = json.dumps({key: order_data[key] for key in keep})
        order_data=json.loads(order_data)
        async def run():
                producer=EventHubProducerClient.from_connection_string(conn_str='Endpoint=sb://streamingdata-demo-dev.servicebus.windows.net/;SharedAccessKeyName=weatherdata-policy;SharedAccessKey=y8tGytHlo6RMIIIyWSzJRONpl5wvr42Xn+AEhDyJg34=;EntityPath=weatherdata-streaming-demo-dev',eventhub_name='weatherdata-streaming-demo-dev')
                async with producer:
                    #Create a batch.
                    event_data_batch=await producer.create_batch()
                    #Add events to the batch
                    event_data_batch.add(EventData(json.dumps(order_data)))

                    #send the batch of events to the event hub
                    await producer.send_batch(event_data_batch)
                    t.sleep(3)
                    print(order_data)
                    print('Data sent successfully to eventhubs!!')
        asyncio.run(run())
        message.ack() 

    subscriber=pubsub_v1.SubscriberClient()
    future=subscriber.subscribe(subscription_name,callback=callback)

    with subscriber:
        future.result()


if __name__=="__main__":
    shopify_streamingdata_functin()




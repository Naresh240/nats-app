from flask import Flask, jsonify
from nats.aio.client import Client as NATS, Msg
import asyncio
import os
import threading

app = Flask(__name__)

def get_nats_url():
    nats_chart_name = os.environ.get("NATS_CHART_NAME", "default-nats-chart")
    namespace = os.environ.get("NAMESPACE", "default-namespace")
    nats_url = f"nats://{nats_chart_name}-nats.{namespace}.svc.cluster.local:4222"
    return nats_url

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

received_message = None
lock = threading.Lock()

async def publish_message():
    try:
        nc = NATS()
        nats_url = get_nats_url()
        print(f"Connecting to: {nats_url}")
        await nc.connect(servers=[nats_url])

        subject = "example_subject"
        message = "Hello, NATS!"

        await nc.publish(subject, message.encode())
        await nc.flush()
        await nc.close()

    except Exception as e:
        print(f"Error publishing message: {e}")

## Receive Message
async def message_handler(msg: Msg):
    global received_message
    subject = msg.subject
    data = msg.data.decode()
    with lock:
        received_message = f'Received a message on {subject}: {data}'

async def subscribe_message():
    global received_message

    try:
        nc = NATS()
        nats_url = get_nats_url()
        print(f"Connecting to: {nats_url}")
        await nc.connect(servers=[nats_url])
        subject = "example_subject"
        await nc.subscribe(subject, cb=message_handler)
        await asyncio.sleep(10)
        await nc.close()

    except Exception as e:
        print(f"Error subscribing to message: {e}")

@app.route('/')
def send_message():
    try:
        loop.run_until_complete(publish_message())
    except Exception as e:
        print(f"Error in sending message: {e}")

    return jsonify({"status": "Message sent to NATS!"})

@app.route('/receive')  
def run_subscribe_message():
    try:
        loop.run_until_complete(subscribe_message())
    except Exception as e:
        print(f"Error in subscribing to messages: {e}")

    return jsonify({"status": "Subscribed to NATS messages!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

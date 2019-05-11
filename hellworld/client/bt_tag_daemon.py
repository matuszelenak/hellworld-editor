from bluepy.btle import Scanner

import requests
import os

QUERY_URL = 'https://hellworld-editor.herokuapp.com/people/tags'
SUBMIT_URL = 'https://hellworld-editor.herokuapp.com/pandemic/bluetooth_tag/'

DEFAULT_RSSI = -100
HISTORY_LENGTH = 3
REQUIRED_AVG_RSSI = -80
SUBMIT_COOLDOWN_CYCLES = 5


def submit_tag_presence(address):
    try:
        response = requests.post(
            url=SUBMIT_URL,
            json={
                'address': address,
                'target': os.environ.get('HELLWORLD_TEAM_ID', 1)
            })
        if response.status_code == 200:
            return response.json()['result'] == 'infected'
    except Exception:
        pass
    return False


def get_registered_tags():
    try:
        return requests.get(QUERY_URL).json()
    except Exception:
        pass
    return []


scanner = Scanner()
device_rssi_history = {}
submission_history = {}

registered_tags = get_registered_tags()

while True:
    devices = scanner.scan(5.0)

    discovered = {dev.addr: dev.rssi for dev in devices if dev.addr in registered_tags}

    # If a device wasn't found, its history is erased
    device_rssi_history = {addr: v for addr, v in device_rssi_history.items() if addr in discovered}

    for addr in submission_history:
        submission_history[addr] = max(submission_history[addr] - 1, 0)

    for addr, rssi in discovered.items():

        # If the device doesn't have a history yet, create it with default RSSI
        if addr not in device_rssi_history:
            device_rssi_history[addr] = [DEFAULT_RSSI for _ in range(HISTORY_LENGTH - 1)]

        device_rssi_history[addr].append(rssi)

        # Cut off the device history so only HISTORY_LENGTH events remain
        device_rssi_history[addr] = device_rssi_history[addr][-HISTORY_LENGTH:]

        # Calculate the average RSSI of the device over the last HISTORY_LENGTH events
        device_avg_rssi = sum(device_rssi_history[addr]) / HISTORY_LENGTH

        print("Device %s, avg RSSI=%d dB" % (addr, device_avg_rssi))

        if device_avg_rssi > REQUIRED_AVG_RSSI and submission_history.get(addr, 0) == 0:
            print("Submitting addr {}".format(addr))
            if submit_tag_presence(addr):
                submission_history[addr] = SUBMIT_COOLDOWN_CYCLES

        print("Device %s, RSSI=%d dB" % (addr, rssi))
    print()

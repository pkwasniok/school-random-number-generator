from flask import Flask
from flask_cors import CORS
import json
import random
import time
import _datetime

# Loading config file
config = json.load(open("./config.json"))

api = Flask(__name__)
cors = CORS(api, resources={r"/*": {"origins": "*"}})


def config_save(data):
    with open('./config.json', 'w') as outfile:
        json.dump(data, outfile)


@api.route('/', methods=['GET'])
def home():
    # Load config from file
    config = json.load(open("./config.json"))

    # Generate new numbers array if empty
    if(len(config['numbers']) < 2):
        # Generating and shuffling numbers
        numbers = list(range(config['min-number'], config['max-number']+1))
        random.shuffle(numbers)

        # Delete excluded numbers
        for number in config['excluded-numbers']:
            numbers.remove(number)

        # Update config object
        config['numbers'] = numbers

    # Check number od days from last number generation
    date_last = _datetime.datetime.strptime(config['last-new-number-date'], "%Y-%m-%d")
    date_now = _datetime.datetime.now()
    if((date_now - date_last).days >= config['new-number-generation-period']):
        # Extract 2 numbers and delete them from array
        numbers = config['numbers']
        numbers.pop(0)
        numbers.pop(0)
        config['numbers'] = numbers
        config['last-new-number-date'] = date_now.strftime("%Y-%m-%d")

    # Save config file
    config_save(config)

    # Get numbers from array
    numbers = config['numbers']

    # Response to get request
    return str([numbers[0], numbers[1]])


""" @api.route('/datetime', methods=['GET'])
def datetime():
    a = _datetime.datetime.strptime(config['last-new-number-date'], "%Y-%m-%d")
    b = _datetime.datetime.now()
    return str((b-a).days) """


if __name__ == '__main__':
    api.run()

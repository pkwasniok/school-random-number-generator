from flask import Flask
from flask_cors import CORS
import json
import random

# Loading config file
config = json.load(open("./config.json"))

api = Flask(__name__)
cors = CORS(api, resources={r"/*": {"origins": "*"}})


def config_save():
    with open('./config.json', 'w') as outfile:
        json.dump(config, outfile)


@api.route('/', methods=['GET'])
def home():
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

    # Extract 2 numbers and delete them from array
    numbers = config['numbers']
    num1 = numbers.pop(0)
    num2 = numbers.pop(0)
    config['numbers'] = numbers

    # Save config file
    config_save()

    # Response to get request
    # return str([num1, num2])
    return str([num1, num2])


if __name__ == '__main__':
    api.run()

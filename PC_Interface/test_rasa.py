from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# from rasa_nlu.converters import load_data
from pprint import pprint

import os
import pymongo
from rasa_nlu.training_data import load_data

from rasa_nlu.config import RasaNLUModelConfig
# from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer, Metadata, Interpreter
from rasa_nlu import config

myclient = pymongo.MongoClient(os.getenv('MONGO_CLIENT'))
pc_db = myclient[os.getenv('MONGO_DB')]


def train(data, config_file, model_dir):
    training_data = load_data(data)
    configuration = config.load(config_file)
    trainer = Trainer(configuration)
    trainer.train(training_data)
    model_directory = trainer.persist(model_dir, fixed_model_name='chat')


def run(line):
    interpreter = Interpreter.load('./models/nlu/default/chat')
    print(line + "\n")
    pprint(interpreter.parse(line))
    # pprint(interpreter.parse(line)["intent_ranking"][:2])
    # pprint(interpreter.parse('use data manipulation library'))
    # pprint(interpreter.parse('using multidimensional array operator'))
    # pprint(interpreter.parse('use Random Forrest '))


def get_pseudocode_from_db():
    coll_name = pc_db["pseudocodes"]
    records = list(coll_name.find({}))
    lines = []
    for x in records:
        lines.append(x['PseudoCode'])

    return lines


if __name__ == '__main__':
    pc_lines = get_pseudocode_from_db()[147]
    # train('./training_data.json', './config.yml', './models/nlu')
    # run()
    for line in pc_lines:
        run(line)

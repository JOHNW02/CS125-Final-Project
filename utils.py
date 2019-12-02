import json
import logging
import os
import torch
import shutil

class Params():
    def __init__(self, dir):
        with open(dir) as f:
            params = json.load(f)
            self.__dict__.update(params)

    def save(self, json_path):
        with open(json_path, 'w') as f:
            json.dump(self.__dict__, f, indent= 4)

    def update(self, json_path):
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    @property
    def dict(self):
        return self.__dict__


class RunningAverage():
    def __init__(self):
        self.steps = 0
        self.total = 0

    def update(self, value):
        self.steps += 1
        self.total += value

    def __call__(self):
        return self.total/self.steps


def set_logger(log_path):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(stream_handler)

def save_dict_to_json(dic, json_path):
    with open(json_path, 'w') as f:
        dic = {k : float(y) for k, y in dic.items()}
        json.dump(dic, f, indent=4)

def save_checkpoint(state, is_best, checkpoint):
    filepath = os.path.join(checkpoint, 'last.pth.tar')
    if not os.path.exists(checkpoint):
        print("Checkpoint directory does not exist! Creating {}".format(checkpoint))
        os.mkdir(checkpoint)
    else:
        print("Found checkpoint")
    torch.save(state, filepath)
    if is_best:
        shutil.copyfile(filepath, os.path.join(checkpoint,'best.pth.tar'))

def load_checkpoint(checkpoint, model, optimizer = None):
    if not os.path.exists(checkpoint):
        raise("Checkpoint directory {} does not exist").format(checkpoint)
    checkpoint = torch.load(checkpoint)
    model.load_state_dict(checkpoint['state_dict'])
    if optimizer:
        optimizer.load_state_dict(checkpoint['optim_dict'])
    return checkpoint

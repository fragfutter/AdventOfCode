#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
import re
import sys

INPUT = 'input_10.txt'
PATTERN = re.compile(r'(.*?)\((\d+)x(\d+)\)(.*)')
data = open(INPUT, 'r').readlines()
# data = '(27x12)(20x12)(13x14)(7x10)(1x12)A'
# data = 'X(8x2)(3x3)ABCY'


class Bot(object):
    bots = {}
    outputs = {}

    def __init__(self, number):
        self.number = number
        self.instructions = None
        self.chips = []

    @classmethod
    def bot(cls, number):
        try:
            result = cls.bots[number]
            return result
        except KeyError:
            result = Bot(number)
            cls.bots[number] = result
            return result

    @classmethod
    def output(cls, number, value):
        try:
            cls.outputs[number].append(value)
        except KeyError:
            cls.outputs[number] = [value]

    def chip(self, data):
        logging.debug('%d receives %s', self.number, data)
        self.chips.append(int(data))
        self.action()

    def instruction(self, data):
        self.instructions = data
        self.action()

    def action(self):
        if len(self.chips) != 2:
            logging.debug('%d has not enough chips', self.number)
            return
        if self.instructions is None:
            logging.debug('%d has no instruction', self.number)
            return
        logging.info('bot %d processes %s with %s', self.number, self.instructions, self.chips)
        low = min(self.chips)
        high = max(self.chips)
        self.chips = []
        if low == 17 and high == 61:
            logging.info('%d processeses 17,61', self.number)
        """low to bot 73 and high to output 5"""
        data = self.instructions
        self.ship(data[2], int(data[3]), low)
        self.ship(data[7], int(data[8]), high)

    def ship(self, target, number, value):
        if target == 'bot':
            b = self.bot(number)
            b.chip(value)
        else:
            self.output(number, value)


for line in data:
    d = line.strip().split(' ')
    if d[0] == 'value':
        bot = Bot.bot(int(d[5]))
        bot.chip(int(d[1]))
    else:
        bot = Bot.bot(int(d[1]))
        bot.instruction(d[3:])

logging.info(
    Bot.outputs[0][0] *
    Bot.outputs[1][0] *
    Bot.outputs[2][0])

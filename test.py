# 載入需要的模組
from __future__ import unicode_literals
import os
import sys
import configparser
#from dotenv import load_dotenv

from test_fsm import TocMachine


machine = TocMachine(
    states=[
        'choice',
        'input_age',
        'convert_age',
        'send_picture'
    ],
    transitions=[
        {'trigger': 'advance', 'source': 'user', 'dest': 'choice', 'conditions': 'is_going_to_choice'},
        {'trigger': 'advance', 'source': 'choice', 'dest': 'input_age', 'conditions': 'is_going_to_input_age'},
        {'trigger': 'advance', 'source': 'choice', 'dest': 'send_picture', 'conditions': 'is_going_to_send_picture'},
        {'trigger': 'advance', 'source': 'input_age', 'dest': 'convert_age', 'conditions': 'is_going_to_convert_age'},
        {
            'trigger': 'go_back',
            'source': [
                'choice',
                'input_age',
                'convert_age',
                'send_picture'
            ],
            'dest': 'user'
        },
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True
)       


def main():
    response = machine()
    
if __name__ == '__main__':
    main()

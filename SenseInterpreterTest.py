from interpreter import *
interp({
    'Pages': [ {
            'Name': 'Main',
            'Nodes': [ {
                            'Type': 'SenseHat',
                            'Command': 'set_rotation',
                            'Params': [ {
                                'Type': 'Constant',
                                'Value': 0,
                            } ]
                        }, { 
                            'Type': 'SenseHat',
                            'Command': 'show_message',
                            'Params': [ {
                                'Type': 'Constant',
                                'Value': 'Hello'
                            } ] 
                        }, {
                            'Type': 'If',
                            'Condition': {
                                'Type': 'Expression',
                                'Op': '>',
                                'Left': {
                                    'Type': 'SenseHat',
                                    'Command': 'get_temperature',
                                    'Params': []
                                },
                                'Right': {
                                    'Type': 'Constant',
                                    'Value': 20
                                }
                            },
                            'Page': 'If1'
                        }
            ] }, {
                'Name': 'If1',
                'Nodes': [ {
                        'Type': 'SenseHat',
                        'Command': 'show_message',
                        'Params': [ {
                                'Type': 'Format',
                                'Text': 'It\'s {} C',
                                'Params': [ {
                                    'Type': 'SenseHat',
                                    'Command': 'get_temperature',
                                    'Params': []
                                } ]
                            }, {
                                'Type': 'Constant',
                                'Value': .1
                            }, {
                                'Type': 'Constant',
                                'Value': [255, 0, 0]
                            } ]
                        } ]
            } ]
})

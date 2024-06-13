class LabExConfigs:
    def __init__(self):
        '''
            URL
        '''
        self.robot_standard_url = 'http://34.87.82.163/node-red/api/'
        self.robot_config_url = {
            'controller1': self.robot_standard_url + 'controller1',
            'command_robot1': self.robot_standard_url + 'controlrobot1',
            'controller2' : self.robot_standard_url + 'controller2',
            'command_robot2' : self.robot_standard_url +  'controlrobot2',
            'controller3' : self.robot_standard_url + 'controller3',
            'command_robot3' : self.robot_standard_url + 'controlrobot3'
        }

        '''
            x-api-key
        '''
        self.post_controller = '2H4Co8KfxPxYwbc7vKygj254kqi6WXcA'
        self.post_command = 'zVfbUErBN8YWFH8wV6jafQ87nfiX5VNC'

labex_config = LabExConfigs()
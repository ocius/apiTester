#!/usr/bin/python3.7
'''
Tests the Ocius live drone API
'''

import requests

def test_API_online(response):
    ''' Tests the API is online '''
    if not response.status_code == 200:
        return ('API Online', 'script recevied a {response.status_code} response')
    return ('API Online', 'PASSED')

def test_drone_basic(drone):
    ''' Tests each drone contains basic information about the drone '''
    keys = set(['Name', 'Timestamp', 'Status'])
    if not keys.issubset(drone.keys()):
        return ('Basic', f'Missing {keys - set(drone.keys())}')
    return ('Basic', 'PASSED')

def test_drone_coordinates(drone):
    ''' Tests coordinates have '''
    if not 'Props' in drone:
        return ('Coordinates', 'Missing props in drone')
    if not 'Coordinates' in drone['Props']['Location']:
        return ('Coordinates', 'Missing coordinates in props location')
    if not 'Lon' in drone['Props']['Location']['Coordinates']:
        return ('Coordinates', 'Missing Lon field in location Coordinates')
    if not 'Lat' in drone['Props']['Location']['Coordinates']:
        return ('Coordinates', 'Missing Lat field in location Coordinates')
    return ('Coordinates', 'PASSED')

def test_drone_camera(drone):
    if not 'Props' in drone:
        return ('Coordinates', 'Missing props in drone')
    if not 'Cameras' in drone['Props']:
        return ('Cameras', 'Missing Cameras in props')
    if len(drone['Props']['Cameras']) < 1:
        return ('Cameras', 'No available Cameras')
    return ('Cameras', 'PASSED')

def run_tests():
    response = requests.get('https://api.ocius.com.au/drones')
    tests = [test_API_online(response)]
    for drone in response.json():
        if 'Name' in drone:
            tests.append(('Name', f'{drone["Name"]}'))
        else:
            tests.append(('Name', 'Unknown'))
        tests.append(test_drone_basic(drone))
        tests.append(test_drone_coordinates(drone))
        tests.append(test_drone_camera(drone))
    return tests


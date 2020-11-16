#!/usr/bin/python3.7
'''
Tests the Ocius live drone API
'''
from APIConstants import *
import requests
import xml.etree.ElementTree as ElementTree


def test_verify_active_drones(live_api, list_robots) -> tuple:
    ''' verifies the API data matches up with the source API '''
    list_robots = ElementTree.fromstring(list_robots.text)
    drone_ids = [drone.get('robotid') for drone in list_robots.findall(
        'robot') if drone.get('robotid') in SUPPORTED_DRONES]

    if len(live_api.json()) < len(drone_ids):
        return ('Number of USVs', 'api data mismatch')

    return ('Number of USVs', 'PASSED')


def test_list_robots_online(list_robots) -> tuple:
    if list_robots.status_code != 200:
        return ('LIST ROBOTS API', f'received HTTP {list_robots.status_code}')
    return ('listrobots online?', 'PASSED')


def test_verify_API_data(live_api) -> list:
    ''' Tests that data from the API matches with source API'''
    test_results = []

    list_robots = requests.get(LIST_ROBOTS_ENDPOINT)
    test_results.append(test_list_robots_online(list_robots))
    if test_results[-1][1] != 'PASSED':
        return test_results

    test_results.append(test_verify_active_drones(live_api, list_robots))
    return test_results


def test_API_online(response) -> tuple:
    ''' Tests the API is online '''
    if not response.status_code == 200:
        return ('API Online', 'script recevied a {response.status_code} response')
    return ('API Online', 'PASSED')


def test_drone_basic(drone) -> tuple:
    ''' Tests each drone contains basic information about the drone '''
    keys = set(['Name', 'Timestamp', 'Status'])
    if not keys.issubset(drone.keys()):
        return ('Basic', f'Missing {keys - set(drone.keys())}')
    for key in drones:
        if drones[key] == None:
            return (f'{key}', 'null')
    return ('Basic', 'PASSED')


def test_drone_coordinates(drone) -> tuple:
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


def test_drone_camera(drone) -> tuple:
    if not 'Props' in drone:
        return ('Coordinates', 'Missing props in drone')
    if not 'Cameras' in drone['Props']:
        return ('Cameras', 'Missing Cameras in props')
    if drone['Props']['Cameras'] is None:
        return ('Cameras', 'null')
    if len(drone['Props']['Cameras']) < 1:
        return ('Cameras', 'No available Cameras')
    return ('Cameras', 'PASSED')


def test_drone_data(response) -> list:
    drone_tests = []
    for drone in response.json():
        if 'Name' in drone:
            drone_tests.append(('Name', f'{drone["Name"]}'))
        else:
            drone_tests.append(('Name', 'Unknown'))
        drone_tests.append(test_drone_basic(drone))
        drone_tests.append(test_drone_coordinates(drone))
        drone_tests.append(test_drone_camera(drone))
    return drone_tests


def run_tests() -> list:
    '''
    Executes the above tests and wraps it into a single data structure
    '''
    response = requests.get('https://api.ocius.com.au/drones')

    test_groups = {}
    test_groups['API Status'] = [test_API_online(response)]
    test_groups['API Verification'] = test_verify_API_data(response)
    test_groups['Drone Statuses'] = test_drone_data(response)

    return (test_groups, response)

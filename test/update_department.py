#! /usr/bin/env python

from auth0.authentication import GetToken
import auth0.management as amng
import argparse
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'metadata-organizer'))
import src.utils as utils



def get_auth_departments(domain, clientid, secret):
    get_token = GetToken(domain, clientid, client_secret=secret)
    token = get_token.client_credentials('https://{}/api/v2/'.format(domain))
    mgmt_api_token = token['access_token']

    roles = amng.roles.Roles(domain, mgmt_api_token)

    all_departments = []
    i = 0

    all_found = False

    while not all_found:
        new_departments = roles.list(page=i, per_page=100)
        if len(new_departments['roles']) == 0:
            all_found = True
        else:
            all_departments += new_departments['roles']
        i += 1
    sort_departments(all_departments)


def sort_departments(depts):
    department_whitelist = {'intern': ['public']}
    for elem in depts:
        if elem['description'].startswith('LDAP'):
            department_whitelist['intern'].append(elem['name'])
        elif elem['description'].startswith('ext'):
            location = elem['description'].split('_')[1]
            if location not in department_whitelist:
                department_whitelist[location] = []
            department_whitelist[location].append(elem['name'])
    write_to_whitelists(department_whitelist)


def write_to_whitelists(depts):
    yaml_path = os.path.join(os.path.abspath(__file__), '..', 
                             'whitelists', 'department')
    yaml_file = utils.read_in_yaml(yaml_path)
    yaml_file['whitelist'] = depts
    utils.save_as_yaml(yaml_file, yaml_path)



def main():
    parser = argparse.ArgumentParser(prog='update_departments.py')
    parser.add_argument('-d', '--domain', help='auth0 domain')
    parser.add_argument('-id', '--id', help='auth0 client id')
    parser.add_argument('-s', '--secret', help='auth0 secret')

    args = parser.parse_args()
    get_auth_departments(args.domain, args.id, args.secret)


if __name__ == "__main__":
    main()

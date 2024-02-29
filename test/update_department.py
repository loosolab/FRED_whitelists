#! /usr/bin/env python

from auth0.authentication import GetToken
import auth0.management as amng
import argparse
import yaml
import os


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

    sort_departments(all_departments)


def sort_departments(depts):
    department_whitelist = {'intern': ['public']}
    for elem in depts:
        if elem['description'].startswith('LDAP'):
            department_whitelist['intern'].append(elem['name'])
        elif elem['description'].startswith('extern'):
            location = elem['description'].split('_')[1]
            if location not in department_whitelist:
                department_whitelist[location] = []
            department_whitelist[location].append(elem['name'])
    write_to_whitelists(department_whitelist)


def write_to_whitelists(depts):
    yaml_file = os.path.join(os.path.abspath(__file__), '..', 'whitelists',
                             'department')
    with open(yaml_file) as file:
        output = yaml.load(file, Loader=yaml.FullLoader)

    output['whitelist'] = depts

    with open(yaml_file, 'w') as file:
        yaml.dump(output, file, sort_keys=False)


def main():
    parser = argparse.ArgumentParser(prog='update_departments.py')
    parser.add_argument('-d', '--domain', help='auth0 domain')
    parser.add_argument('-id', '--id', help='auth0 client id')
    parser.add_argument('-s', '--secret', help='auth0 secret')

    args = parser.parse_args()
    get_auth_departments(args.domain, args.clientid, args.secret)


if __name__ == "__main__":
    main()

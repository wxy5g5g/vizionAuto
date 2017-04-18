#!/usr/bin/env python
##############################################################################

import json
import requests
import os
import fnmatch
import logging
import time
import argparse
import sys
import uuid


log = logging.getLogger()
log.setLevel('INFO')

class CCCTenant:

    def query_tenant(self, args):
        query_url = 'https://' + args['server_ip'] + ':8443/tenants'
        headers = {'content-type':'application/json'}

        response = requests.get(query_url, verify=False, timeout=60)

        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1

        response_dict = response.json()

        for item in response_dict:
            print item['name']



    def insert_tenant(self, args):
        insert_url = 'https://' + args['server_ip'] + ':8443/tenants?1a6d1bd0-87e8-4231-8f46-4ec8271221c5'
        insert_tenant_json = json.dumps({'name': args['name'], 
                                         'email': args['email'], 
                                         #'group': [args['group']], 
                                         'info': args['info'], 
                                         'password': args['password'], 
                                         'phone': args['phone'], 
                                         'policy': args['policy'], 
                                         'status': args['status'] 
                                         }) 

        headers = {'content-type':'application/json'}

        #response = requests.put(insert_url, data=insert_tenant_json, headers=headers, verify=False, timeout=60)
        response = requests.post(insert_url, data=insert_tenant_json, headers=headers, verify=False, timeout=60)

        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1

        response_dict = response.json()
        print response_dict['status']

    def update_tenant(self, args):
        insert_url = 'https://' + args['server_ip'] + ':8443/tenants'
        insert_tenant_json = json.dumps({'name': args['name'], 
                                         'email': args['email'], 
                                         'group': [args['group']], 
                                         'info': args['info'], 
                                         'password': args['password'], 
                                         'phone': args['phone'], 
                                         'policy': args['policy'], 
                                         'status': args['status'] 
                                         }) 

        headers = {'content-type':'application/json'}

        response = requests.put(insert_url, data=insert_tenant_json, headers=headers, verify=False, timeout=60)
        #response = requests.post(insert_url, data=insert_tenant_json, headers=headers, verify=False, timeout=60)

        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1

        response_dict = response.json()
        print response_dict['status']

    def delete_tenant(self, args):
        delete_url = 'https://' + args['server_ip'] + ':8443/tenants/' + args['name']
        headers = {'content-type':'application/json'}

        response = requests.delete(delete_url, verify=False, timeout=60)

        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1

        response_dict = response.json()
        print response_dict['status']


def main():
    logging.basicConfig()

    client = CCCTenant()

    parser = argparse.ArgumentParser(description='CCC testing.')
    parser.add_argument('-s', '--server_ip', type=str, required=False)

    #args = parser.parse_args()

    subparsers = parser.add_subparsers()


    # query table 
    query_tenant_table = subparsers.add_parser('query_tenant')
    query_tenant_table.set_defaults(func=client.query_tenant)
    query_tenant_table.set_defaults(action='query_tenant')

    # delete tenant 
    delete_tenant_table = subparsers.add_parser('delete_tenant')
    delete_tenant_table.set_defaults(func=client.delete_tenant)
    delete_tenant_table.add_argument('-n', '--name', type=str, required=True)
    delete_tenant_table.set_defaults(action='delete_tenant')

    # insert table 
    insert_tenant_table = subparsers.add_parser('insert_tenant')
    insert_tenant_table.set_defaults(func=client.insert_tenant)
    insert_tenant_table.add_argument('-n', '--name', type=str, required=True)
    insert_tenant_table.add_argument('-e', '--email', type=str, required=True)
    #insert_tenant_table.add_argument('-g', '--group', type=str, required=True)
    insert_tenant_table.add_argument('-i', '--info', type=str, required=True)
    insert_tenant_table.add_argument('-p', '--password', type=str, required=True)
    insert_tenant_table.add_argument('-o', '--phone', type=str, required=True)
    insert_tenant_table.add_argument('-y', '--policy', type=str, required=False)
    insert_tenant_table.add_argument('-u', '--status', type=str, required=True)
    insert_tenant_table.set_defaults(action='insert_tenant')

    # update table 
    update_tenant_table = subparsers.add_parser('update_tenant')
    update_tenant_table.set_defaults(func=client.update_tenant)
    update_tenant_table.add_argument('-n', '--name', type=str, required=True)
    update_tenant_table.add_argument('-e', '--email', type=str, required=True)
    update_tenant_table.add_argument('-g', '--group', type=str, required=True)
    update_tenant_table.add_argument('-i', '--info', type=str, required=True)
    update_tenant_table.add_argument('-p', '--password', type=str, required=True)
    update_tenant_table.add_argument('-o', '--phone', type=str, required=True)
    update_tenant_table.add_argument('-y', '--policy', type=str, required=True)
    update_tenant_table.add_argument('-u', '--status', type=str, required=True)
    update_tenant_table.set_defaults(action='update_tenant')



    #parse the args and call whatever function was selected
    #args = parser.parse_args()
    args = vars(parser.parse_args())    

    try:
       log.info(args['func'])
       rc = args['func'](args)
    except Exception, err:
       log.info('receive error: ' + str(err))
       if 'already exists' in str( err ):
          rc = 0
       elif 'something error in string' in str( err ):
          rc = 2
       else:
          rc = 3

       if rc != 0:
          log.info('rc: %s' % str(rc))
          exit(rc)
       
    #time.sleep(10)

if __name__ == "__main__":
    main()



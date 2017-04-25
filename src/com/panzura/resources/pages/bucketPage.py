#!/usr/bin/env python
import json
import requests
import os
import fnmatch
import logging
import time
import argparse
import sys
import uuid
from resources.pages.page import Page

class CCCBucket(Page):

    def list_snapshot(self, apikey, args):

        query_url = 'https://' + args['server_ip'] + ':8443/buckets/' + args['name'] + '/snapshots' + '?api_key=' + str(apikey)

        headers = {'content-type':'text/plain'}

        response = requests.get(query_url, verify=False, timeout=60)

        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1

        response_dict = response.json()

        for item in response_dict:
            print item['ctime']



    def create_snapshot(self, apikey, args):
        insert_url = 'https://' + args['server_ip'] + ':8443/buckets/' + args['name'] + '/snapshot' + '?api_key=' + str(apikey)

        headers = {'content-type':'text/plain'}

        response = requests.post(insert_url, headers=headers, verify=False, timeout=60)

        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1

        response_dict = response.json()
        print response_dict['status']


    def create_clone(self, apikey, args):
        insert_url = 'https://' + args['server_ip'] + ':8443/buckets/' + args['name'] + '/clone/' + args['clonename'] + '?api_key=' + str(apikey)
        print insert_url 

        headers = {'content-type':'text/plain'}

        response = requests.post(insert_url, headers=headers, verify=False, timeout=60)

        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1

        response_dict = response.json()
        print response_dict['status']


    def delete_snapshot(self, apikey, args):
        delete_url = 'https://' + args['server_ip'] + ':8443/buckets/' + args['name'] + '/snapshot/' + args['ctime'] + '?api_key=' + str(apikey)
        print delete_url
        headers = {'content-type':'application/json'}

        response = requests.delete(delete_url, verify=False, timeout=60)

        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1

        response_dict = response.json()
        print response_dict['status']


    def delete_snapshot_by_ctime(self, apikey, args, ctime):
        delete_url = 'https://' + args['server_ip'] + ':8443/buckets/' + args['name'] + '/snapshot/' + str(ctime) + '?api_key=' + str(apikey)
        print delete_url
        headers = {'content-type':'application/json'}

        response = requests.delete(delete_url, verify=False, timeout=60)

        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1

        response_dict = response.json()
        print response_dict['status']



    def delete_snapshots(self, apikey, args):
        query_url = 'https://' + args['server_ip'] + ':8443/buckets/' + args['name'] + '/snapshots'

        headers = {'content-type':'text/plain'}

        response = requests.get(query_url, verify=False, timeout=60)

        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1

        response_dict = response.json()

        for item in response_dict:
            print item['ctime']
            self.delete_snapshot_by_ctime(args, item['ctime'])
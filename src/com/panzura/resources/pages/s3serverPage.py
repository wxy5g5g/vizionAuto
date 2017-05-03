#!/usr/bin/env python

import os
import time
import argparse
import sys
import uuid
import ast
from resources.pages.page import Page

import boto
import boto.s3.connection
from boto.s3.key import Key



class S3Server(Page):

    conn = None

    def connect(self, args):
        self.conn = boto.connect_s3(
               aws_access_key_id = args['accessKey'],
               aws_secret_access_key = args['secretKey'],
               host = args['server_ip'], 
               port = 443,
               is_secure=True,
               calling_format = boto.s3.connection.OrdinaryCallingFormat(),)
        self.logInfo("have connected with s3 already") 


    def list_bucket(self):
#        bucket = self.conn.create_bucket('my-new-bucket')
        self.logInfo("list all buckets")
        buckets = self.conn.get_all_buckets()
        return buckets   
    
    def create_bucket(self, args):
        bucket = self.conn.create_bucket(args['bucketName'])

    def delete_bucket(self, args):
        bucket = self.conn.delete_bucket(args['name'])


    def upload(self, args):

        callback=None
        md5=None
        reduced_redundancy=False
        content_type=None

        file = open(args['file'], 'r+')

        key = file.name
        bucket = args['bucket'] 

        try:
            size = os.fstat(file.fileno()).st_size
        except:
            # Not all file objects implement fileno(),
            # so we fall back on this
            file.seek(0, os.SEEK_END)
            size = file.tell()

        bucket = self.conn.get_bucket(bucket, validate=True)
        k = Key(bucket)
        k.key = key
        if content_type:
            k.set_metadata('Content-Type', content_type)
        sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy, rewind=True)

        # Rewind for later use
        file.seek(0)

        if sent == size:
            return True
        return False


    def download(self, args):

        bucket_name = args['bucket'] 
        local_path = args['recover'] 

        bucket = self.conn.get_bucket(bucket_name)
        bucket_list = bucket.list()

        for file in bucket_list:
            keyString = str(file.key)
            print "check local and remove file"
            print(keyString);
            #remove_file = "/" + args['bucket'] + "/" + args['file']
            #print remove_file
            if keyString == args['file']:
                # check if file exists locally, if not: download it
                #if not os.path.exists(local_path+keyString):
                print "recover file " + args['file']
                file.get_contents_to_filename(local_path+keyString)
                return True

        return True


    def delete_file(self, args):
        bucket_name = args['bucket'] 
        bucket = self.conn.get_bucket(bucket_name)
        bucket.delete_key(args['file'])

        return True


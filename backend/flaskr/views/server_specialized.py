# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 16:24:16 2021

@author: admin
"""
from eth_keys import keys
import cbor2
from eth_hash.auto import keccak
import dbm
import os

def hex2bytes(hex_string):
    return bytes.fromhex(hex_string[2:])

def bytes2hex(bytes_string):
    return '0x' + bytes_string.hex()

def signature2hex(signature):
    return signature.to_hex()

def hex2signature(hex_value):
    # print(hex_value,1)
    return keys.Signature(hex2bytes(hex_value))

class Database:
    def __init__(self):
        if not os.path.exists(r'../test_data/'):
            os.mkdir(r'../test_data/')
        self.database_dict = dbm.open('./flaskr/test_data/test_data', 'c')
    
    def get(self, key, default):
        return self.database_dict.get(key, default)
    
    def put(self, key, value):
        self.database_dict[key]=value
        
    def synchronize(self):
        pass

class Method_caller:
    def __init__(self, database=Database()):
        if not os.path.exists(r'../picture_files/'):
            os.mkdir(r'../picture_files/')
        self.database = database
    
    def generate_key_pair(self):
        private_key = os.urandom(32)
        public_key = hex2bytes(keys.PrivateKey(private_key).public_key.to_hex())
        return {
            'private_key' : private_key,
            'public_key' : public_key
            }
    
    def initialize_account(self):
        return {
            'nonce': -1, 
            'files' : [],
            }
    

    def save_file(self, public_key, content):
        if not self.database.get(public_key, None):
            account = self.initialize_account()
            self.database.put('public_key', cbor2.dumps(account))
        address = keccak(content)
        name = bytes2hex(address)
        with open(r'./flaskr/picture_files/' + name, 'wb+') as fp:
            fp.write(content)
        if not self.database.get(address, None): 
            self.database.put(address, public_key)
            account['nonce'] += 1
            account['files'].append(address)
            self.database.put('public_key', cbor2.dumps(account))
            self.database.synchronize()
            return address
        else:
            return address
        
    def generate_signature(self, private_key, address):
        pk = keys.PrivateKey(private_key)
        signature = pk.sign_msg(address)
        return hex2bytes(signature2hex(signature))
    
    
    def retrieve_file(self, signature, address):
        public_key = self.database.get(address, None)
        if public_key:
            publicKey = keys.PublicKey(public_key)
            signature = hex2signature(bytes2hex(signature))
            result = publicKey.verify_msg(address, signature)
            name = bytes2hex(address)
            if result:
                with open(r'./flaskr/picture_files/' + name, 'rb+') as fp:
                    file = fp.read()
                    return file
            else:
                return None
                

def NFT_File(NFT_file):
    client = Method_caller()
    # 初始化

    file_content = NFT_file
    # 测试文件内容
    
    key_json = client.generate_key_pair()
    private_key, public_key = key_json['private_key'], key_json['public_key']
    # 生成密钥对
    
    address = client.save_file(public_key, file_content)
    assert address != None
    # 存储文件，获得哈希地址
    
    signature = client.generate_signature(private_key, address)
    # 生成签名，用于取文件
    signature_8=bytes2hex(signature)
    private_key_8=bytes2hex(private_key)
    public_key_8=bytes2hex(public_key)

    file_retrieved = client.retrieve_file(signature, address)
    # 取出文件看看
    #print(file_retrieved+'file')
    print('signature=',signature_8,'private_key=',private_key_8,'public_key=',public_key_8)
    date={}
    date['signature']=signature_8
    date['privatekey']=private_key_8
    date['publickey']=public_key_8
    return date
    
    
    
    
    
    
        

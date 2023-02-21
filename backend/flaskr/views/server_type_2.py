# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 16:24:16 2021

@author: admin
"""
from eth_keys import keys
import cbor2
from eth_hash.auto import keccak
import dbm.dumb as dbm
import os
from datetime import datetime, timezone, timedelta

BEIJING_TIMEZONE = timezone(timedelta(hours=8))


def ctime_str():
    return datetime.strftime(datetime.now(BEIJING_TIMEZONE), '%Y-%m-%d %H:%M:%S')


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

    def clear(self):
        self.database

    def get(self, key, default):
        return self.database_dict.get(key, default)

    def put(self, key, value):
        self.database_dict.update({key: value})
        self.database_dict.sync()


class Method_caller:
    def __init__(self, database=Database()):
        if not os.path.exists(r'../picture_files/'):
            os.mkdir(r'../picture_files/')
        self.database = database

    def generate_key_pair(self):
        private_key = os.urandom(32)
        public_key = hex2bytes(keys.PrivateKey(private_key).public_key.to_hex())
        return {
            'private_key': private_key,
            'public_key': public_key
        }

    def initialize_account(self):
        return {
            'nonce': -1,
            'files': set(),
        }

    def save_file(self, public_key, content):
        if not self.database.get(public_key, None):
            account = self.initialize_account()
            # 账户初始化
            self.database.put('public_key', cbor2.dumps(account))
        address = keccak(content)
        name = bytes2hex(address)
        with open(r'./flaskr/picture_files/' + name, 'wb+') as fp:
            fp.write(content)
        if not self.database.get(address, None):
            ctime = ctime_str()
            NFT_info = {
                "Creator": public_key,
                "Create_time": ctime,
                "Owner": public_key,
                "Transaction_time": ctime,
            }
            # 记录NFT信息
            self.database.put(address, cbor2.dumps(NFT_info))
            account['nonce'] += 1
            account['files'].add(address)
            self.database.put(public_key, cbor2.dumps(account))
            # self.database.synchronize()
            return address
        else:
            return address

    def generate_signature(self, private_key, address):
        # 生成取文件用的签名
        pk = keys.PrivateKey(private_key)
        signature = pk.sign_msg(address)
        return hex2bytes(signature2hex(signature))

    def generate_transfer_signature(self, private_key, NFT_address, to_address):
        # 生成转赠文件的签名
        pk = keys.PrivateKey(private_key)
        signature = pk.sign_msg(NFT_address + to_address)
        return hex2bytes(signature2hex(signature))

    def transfer_file(self, signature, NFT_address, to_address):
        NFT_info = cbor2.loads(self.database.get(NFT_address, b'\xa0'))
        public_key = NFT_info.get('Owner', None)
        if public_key:
            publicKey = keys.PublicKey(public_key)
            signature = hex2signature(bytes2hex(signature))
            result = publicKey.verify_msg(NFT_address + to_address, signature)
            if result:
                NFT_info['Owner'] = to_address
                NFT_info['Transaction_time'] = ctime_str()
                # 修改NFT所有权和交易时间
                from_account = self.database.get(public_key, cbor2.dumps(self.initialize_account()))
                from_account = cbor2.loads(from_account)
                from_account['nonce'] -= 1
                from_account['files'].remove(NFT_address)
                # 修改转赠者账户数据
                to_account = self.database.get(to_address, cbor2.dumps(self.initialize_account()))
                to_account = cbor2.loads(to_account)
                to_account['nonce'] += 1
                to_account['files'].add(NFT_address)
                # 修改受赠者账户数据
                self.database.put(NFT_address, cbor2.dumps(NFT_info))
                self.database.put(public_key, cbor2.dumps(from_account))
                self.database.put(to_address, cbor2.dumps(to_account))
                # 保存所有数据
                return True
            else:
                return False
        else:
            return False

    def retrieve_file(self, signature, address):
        NFT_info = cbor2.loads(self.database.get(address, b'\xa0'))
        public_key = NFT_info.get('Owner', None)
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

    def check_file(self, address):
        NFT_info = cbor2.loads(self.database.get(address, b'\xa0'))
        return NFT_info


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
    signature_8 = bytes2hex(signature)
    private_key_8 = bytes2hex(private_key)
    public_key_8 = bytes2hex(public_key)
    file_retrieved = client.retrieve_file(signature, address)
    # 取出文件看看
    # print(file_retrieved+'file')
    print('signature=', signature_8, 'private_key=', private_key_8, 'public_key=', public_key_8)
    date = {}
    date['signature'] = signature_8
    date['privatekey'] = private_key_8
    date['publickey'] = public_key_8
    return date

def NFT_creator(NFT_file):
    try:
        from pprint import pprint as print
    except:
        pass


    def pretty_info(d):
        for x in d:
            if type(d[x]) == bytes:
                d[x] = bytes2hex(d[x])
        return d

    client = Method_caller()
    # 初始化
    file_content = NFT_file
    # 测试文件内容

    key_json = client.generate_key_pair()
    private_key, public_key = key_json['private_key'], key_json['public_key']
    # 生成第一个账户密钥对

    address = client.save_file(public_key, file_content)
    signature = client.generate_signature(private_key, address)
    # 存储文件，获得哈希地址
    print('pretty_info')
    print(pretty_info(client.check_file(address)))

    data=pretty_info(client.check_file(address))
    data['signature']=bytes2hex(signature)
    data['address']=bytes2hex(address)
    data['private_key']=bytes2hex(private_key)
    file_retrieved = client.retrieve_file(signature, address)
    # 取出文件看看
    print(data)
    print('file_retrieved:')
    print(file_retrieved)
    return data

def NFT_transaction(seller_private_key, file_address, buyer_public_key):
    import time
    time.sleep(5)
    key_json2 = client.generate_key_pair()
    private_key2, public_key2 = key_json2['private_key'], key_json2['public_key']
    # 生成第二个账户密钥对
    transfer_signature = client.generate_transfer_signature(private_key, address, public_key2)
    client.transfer_file(transfer_signature, address, public_key2)
    # 文件转赠

    print('pretty_info:')
    print(pretty_info(client.check_file(address)))

if __name__ == '__main__':
    try:
        from pprint import pprint as print
    except:
        pass


    def pretty_info(d):
        for x in d:
            if type(d[x]) == bytes:
                d[x] = bytes2hex(d[x])
        return d


    client = Method_caller()
    # 初始化

    file_content = b'ssxxx' * 20
    # 测试文件内容

    key_json = client.generate_key_pair()
    private_key, public_key = key_json['private_key'], key_json['public_key']
    # 生成第一个账户密钥对

    address = client.save_file(public_key, file_content)
    # 存储文件，获得哈希地址
    print('pretty_info')
    print(pretty_info(client.check_file(address)))

    import time

    time.sleep(5)
    key_json2 = client.generate_key_pair()
    private_key2, public_key2 = key_json2['private_key'], key_json2['public_key']
    # 生成第二个账户密钥对
    transfer_signature = client.generate_transfer_signature(private_key, address, public_key2)
    client.transfer_file(transfer_signature, address, public_key2)

    # 文件转赠
    print('pretty_info:')
    print(pretty_info(client.check_file(address)))


    signature = client.generate_signature(private_key2, address)
    # 生成签名，用于取文件
    file_retrieved = client.retrieve_file(signature, address)

    # 取出文件看看
    print('file_retrieved:')
    print(file_retrieved)


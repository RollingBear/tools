# -*- coding: utf-8 -*-

#   2019/8/7 0007 上午 11:33     

__author__ = 'RollingBear'

import sys
from functools import partial

import nmap
import telnetlib
import asyncio


def timer(tagName):
    import time

    def wapper(func):
        def aa(self, *args, **kwargs):
            startTime = time.time()
            data = func(self, *args, **kwargs)
            endTime = time.time()
            consume = endTime - startTime
            if consume > 60:
                min, sec = divmod(consume, 60)
                print('{} takes {} minutes {} seconds to execute'.format(tagName, str(min), str(sec)))
            else:
                print('{} takes {} seconds to execute'.format(tagName, str(consume)))

            return data

        return wapper


class HostScanner(object):

    def __init__(self):

        self._hostInfo = []

    @timer(tagName='scan')
    def scan(self, host='127.0.0.1', port=None):

        hostList = self._scanner(host, port)
        loop = asyncio.get_event_loop()

        taskList = []

        for hostDic in hostList:
            taskList.append(loop.create_task(self._isLinux(hostDic['IP'], )))

        for task in taskList:
            task.add_done_callback(partial(self._callback))

        loop.run_until_complete(asyncio.wait(taskList))

        return self._hostInfo

    def _callback(self, future):

        res = future.result()
        self._hostInfo.append(res)

    async def _isLinux(self, host, port='22'):

        try:
            tm = telnetlib.Telnet(host=host, port=port, timeout=5)
            b_content = tm.read_until(b'\n', timeout=5)
            str_content = str(b_content.decode(encoding='utf-8')).strip()

            if 'OPENSSH' in str_content.upper():
                return {'IP': host, 'Status': 'up', 'OSType': 'Linux'}
            else:
                return {'IP': host, 'Status': 'up', 'OSType': 'Unknown'}

        except (ConnectionRefusedError, TimeoutError) as e:
            return {'IP': host, 'Status': 'up', 'OSType': 'Unknown'}

        except Exception as e:
            print('Error occurd in class HostScanner function _isLinux')
            print('Error message:', e)

    def _scanner(self, hosts, ports=None):
        """
        探测某一主机是否存活或者探测给定网段内存活的主机
        :param hosts:  可以是IP也可以是网段，例如 192.168.100.10、192.168.100.0/24
        :param ports:  可以写端口也可以写端口范围，例如22、22-33
        :return:  [{'IP': '127.0.0.1', 'Status': 'up'}, {}, {}]
        """
        data = []
        try:
            nm = nmap.PortScanner()
            """
            -n 不显示主机名，不进行IP到主机名的反向解析
            -sP 使用ICMP协议探测
            -PE 显示哪些端口号开启
            -sP -PE 使用IMCP和TCP来探测，结果不显示端口号
            """
            nm.scan(hosts=hosts, ports=ports, arguments='-sP -PE ')
            # 这里获取的只是返回的有效IP
            hosts_list = nm.all_hosts()

            for host in hosts_list:
                # 通过nmap实例获取主机的信息
                # print(nm[host])
                data.append({"IP": host, "Status": nm[host]["status"]["state"]})
            return data
        except Exception as err:
            print("Error occurd in class ScanHost function _scanner")
            print("Error message: ", err)

def main():
    sh = HostScanner()
    print(sh.scan(hosts="172.16.48.0/24"))
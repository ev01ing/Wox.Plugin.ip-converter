# coding:utf-8
from wox import Wox, WoxAPI
import time
import json
import traceback
import logging
import clipboard
import sys

if sys.version[0] == "2":
    reload(sys)
    sys.setdefaultencoding("utf-8")

LOG_FILE = "./logs/log_ipconverter.log"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILE,
                    filemode='a')


class Main(Wox):

    def query(self, key):
        results = []
        if self.ipv4(key):
            results.append({
                "Title": self.ip2int(key),
                "SubTitle": "转换为int",
                # "IcoPath": "Images/pic.png",
                "JsonRPCAction": {
                    "method": "copy_to_clip",
                    "parameters": [self.ip2int(key)],
                    "dontHideAfterAction": False
                }
            })
            return results
        elif self.is_number(key):
            try:
                ip = self.int2ip(int(key))
                results.append({
                    "Title": ip,
                    "SubTitle": "from int",
                    # "IcoPath": "Images/pic.png",
                    "JsonRPCAction": {
                        "method": "copy_to_clip",
                        "parameters": [ip, ],
                        "dontHideAfterAction": False
                    }
                })
                return results
            except Exception:
                logging.error(traceback.format_exc())

        results.append({
            "Title": u'格式非法 : "%s"' % key,
            "SubTitle": u'tips: "%s"' % key,
            "IcoPath": "Images/pic.png",
            "JsonRPCAction": {
                "method": "copy_to_clip",
                "parameters": [key, ],
                "dontHideAfterAction": True
            }
        })

        return results

    @staticmethod
    def ipv4(value):
        groups = value.split('.')
        if len(groups) != 4 or any(not x.isdigit() for x in groups):
            return False
        return all(0 <= int(part) < 256 for part in groups)

    @staticmethod
    def is_number(key):
        try:
            int(key)
            return True
        except Exception:
            return False

    @staticmethod
    def ip2int(ip):
        ip_items = ip.split(".")
        ip_long = int(ip_items[0])
        ip_long = ip_long << 8 | int(ip_items[1])
        ip_long = ip_long << 8 | int(ip_items[2])
        ip_long = ip_long << 8 | int(ip_items[3])
        return ip_long

    @staticmethod
    def int2ip(ip_int):
        ip = "." + str(ip_int % 256)
        ip_int /= 256
        ip = "." + str(int(ip_int) % 256) + ip
        ip_int /= 256
        ip = "." + str(int(ip_int) % 256) + ip
        ip_int /= 256
        return str(int(ip_int)) + ip

    def copy_to_clip(self, text):
        clipboard.copy(text)


if __name__ == "__main__":
    Main()

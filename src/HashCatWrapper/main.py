import requests
import json
import time

service = "http://127.0.0.1:8080/"

# https://requests.readthedocs.io/en/master/user/quickstart/


def request_work(hashID):
    url = service + "start-work/" + hashID
    approval = requests.put(url)
    return False if approval == "Fail" else True


# TODO Send result to the service
def start_work(hashID, hashType):
    # TODO call hashcat and parse output

    

    res = "From hashcat"
    return res


def ask_for_work():
    url = service + "get-work/"
    work = requests.get(url)
    # print(work.content)
    if work.content == "Fail":
        return
    hashID = json.loads(work.text)['hash']
    hashType = json.loads(work.text)['type']
    if request_work(hashID):
        result = start_work(hashID, hashType)
        url = service + "work-done/" + hashID + "/" + result
        requests.put(url)
        return
    else:
        return


def main():
    while True:
        #time.sleep(1)
        ask_for_work()
        break


if __name__ == '__main__':
    main()

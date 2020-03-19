import requests
import json
import subprocess
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
    dictF = "dict.txt"
    hashesF = "hashes.txt"
    crackedF = "cracked.txt"
    # append the hash to the hashes file
    f = open(hashesF)
    f.write(hashID)
    f.close()
    subprocess.run(["hashcat", "-m", "0", "-o", "cracked.txt", "hashes.txt", dictF])
    solved = subprocess.check_output(['tail', '-1', crackedF])
    if solved.decode().split(":", 1)[0] != hashID:
        return False
    else:
        return solved.decode().split(":", 1)[1]


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
        if result:
            url = service + "work-done/" + hashID + "/" + result
            requests.put(url)
            return
        else:
            # TODO add delete-work api to the private service
            url = service + "delete-work/" + hashID
            requests.put(url)
            return
    else:
        return


def main():
    while True:
        print("Asking for work") 
        ask_for_work()
        time.sleep(10)
        break


if __name__ == '__main__':
    main()

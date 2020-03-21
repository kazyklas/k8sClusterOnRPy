import requests, json, subprocess, time, sys, getopt

service = "http://privateservice:8081/"
attack = "dictionary"

# https://requests.readthedocs.io/en/master/user/quickstart/

dictF = "dict.txt"
hashesF = "hashes.txt"
crackedF = "cracked.txt"


def request_work(hashID):
    url = service + "start-work/" + hashID
    approval = requests.put(url)
    return False if approval == "Fail" else True


def start_work(hashID, hashType):
    # TODO case for hashtype
    f = open(hashesF)
    f.write(hashID)
    f.close()
    if attack == "dictionary":
        subprocess.run(["hashcat", "-m", "0", "-o", crackedF, hashesF, dictF])
   # elif attack == "maskattack":
   #     # TODO
   #     #subprocess.run(["hashcat", ... ])
   # elif attack == "bruteforce":
   #     # TODO
   #     # subprocess.run(["hashcat", ... ])
    solved = subprocess.check_output(['tail', '-1', crackedF])
    if solved.decode().split(":", 1)[0] != hashID:
        return False
    else:
        return solved.decode().split(":", 1)[1]


def ask_for_work():
    url = service + "get-work/"
    try:
        work = requests.get(url)
    except requests.exceptions.ConnectionError:
        return
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


"""
This program takes an argument of the type of the attack it should run.
Than it runs this type of attack on the data that he gets from the private service.
Private service will provide hash and type and based on that it will solve the hash on the node.
"""
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hdm:b", ["mask="])
    except getopt.GetoptError:
        print('main.py [OPTION] [MASK]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("Usage: main.py -attack [MASK]")
            print("For dictionary attack: main.py -d")
            sys.exit()
        elif opt == '-d':
            attack = "dictionary"
        elif opt == "-m":
            attack = "maskattack"
            mask = arg
        elif opt == "-b":
            attack = "bruteforce"
    while True:
        print("Asking for work") 
        ask_for_work()
        time.sleep(10)


if __name__ == '__main__':
    main(sys.argv[1:])

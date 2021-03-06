import json
import concurrent.futures


def TimeCalMT(progDamage, progInstallTime, progHitInterval, progProjectileTime, progAmount, isProgMulti, nodeFirewall, nodeRegeneration, nodeAmount):
    firewall = nodeFirewall
    regen = nodeRegeneration
    time = progInstallTime
    i = 0
    if int(progAmount) <= 0:
        return None
    if isProgMulti == 0:
        for x in range(1,int(nodeAmount)+1):
            while True:
                if firewall <= 0:
                    break
                i += 0.1
                if i == max(progHitInterval - progProjectileTime, 0.1):
                    if (progDamage * int(progAmount)) / 10 > (firewall / 100 * regen) / 10 :
                        firewall -= progDamage * int(progAmount) / 10 
                    else:
                        return None
                    i = 0
                firewall += (firewall / 100 * regen) / 10 
                time += 0.1
                if time > 10000:
                    return time
            firewall = nodeFirewall
    elif isProgMulti == 1:
        while True:
            if firewall <= 0:
                break
            i += 0.1
            if i == max(progHitInterval - progProjectileTime, 0.1):
                if (progDamage * int(progAmount)) / 10 > (firewall / 100 * regen) / 10 :
                    firewall -= progDamage * int(progAmount) / 10
                else:
                    return None
                i = 0
            firewall += (firewall / 100 * regen) 
            time += 0.1
            if time > 10000:
                return time
    return time
      
     
def stealthCalMT(visibilityboost, stealthProgVisibility, stealthProgInstallTime):
    time = 0
    i = 0
    while i < stealthProgInstallTime:
        time += 20
        time += (stealthProgVisibility / 100 * visibilityboost)
        i += 1
    return time    


def calculate(args):
    argsList = args.split()
    progsName = []
    progsLevel = []
    progsAmount = []
    nodesName = []
    nodesLevel = []
    nodesAmount = []
    i = 0
    while i <= len(argsList) - 1:
        progsName.append(argsList[i])
        progsLevel.append(argsList[i+1])
        progsAmount.append(argsList[i+2])
        nodesName.append(argsList[i+3])
        nodesLevel.append(argsList[i+4])
        nodesAmount.append(argsList[i+5])
        i += 6
    i = 0 
    while i < len(nodesAmount):
        with open('{}.json'.format(progsName[i])) as f:
            a = json.load(f)
        with open('{}.json'.format(nodesName[i])) as g:
            b = json.load(g)
            takeOverTime = 0
            
            #Start Calculation here
            with concurrent.futures.ThreadPoolExecutor() as executor:
                if progsName[i] == 'shuriken':
                    calculation = executor.submit(TimeCalMT, a['DPS'][progsLevel[i]], a['installTime'],a['hitInterval'],a['projectileTime'],progsAmount[i],1,b['firewall'][nodesLevel[i]],b['firewallRegeneration'],nodesAmount[i])
                else:
                    calculation = executor.submit(TimeCalMT, a['DPS'][progsLevel[i]], a['installTime'],a['hitInterval'],a['projectileTime'],progsAmount[i],0,b['firewall'][nodesLevel[i]],b['firewallRegeneration'],nodesAmount[i])
                time = calculation.result(timeout=180)
                if time is not None:
                    takeOverTime += time
                    if progsName[i] == 'beamCannon':
                        takeOverTime += 0.5 
            i += 1
    return round(takeOverTime,1)

def stealthCalc(args):
    argsList = args.split()
    nodeLevel = argsList[0]
    progsName = []
    progsLevel = []
    progsAmount = []
    i = 1
    fvisibility = 0
    while i < len(argsList):
        progsName.append(argsList[i])
        progsLevel.append(argsList[i+1])
        progsAmount.append(argsList[i+2])
        i += 3
    with open('scanner.json','r') as b:
        c = json.load(b)
    for i in range(0,len(progsName)):
        with open('{}.json'.format(progsName[i]),'r') as f:
            a = json.load(f)
            e = progsAmount[i]
        for d in range(1,int(e)+1):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                calculation = executor.submit(stealthCalMT, c['visibilityboost'][nodeLevel], a['visibility'][progsLevel[i]], a['installTime'])
                fvisibility += calculation.result()
    return fvisibility


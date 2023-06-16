import requests
import pandas as pd
import numpy as np
import math

# EDIT THIS EXCLUDES LIST WITH ALL POST OFFICE NAMING BILLS AND COMMEMERATIVE COIN BILLS
def check_for_exclusion(bill):
    excludes = [2838, 2808, 1794, 1388, 1096, 987, 807, 3728, 2608, 3575, 3574, 3469, 3354,
                 3177, 2908, 2754, 2473, 2379, 1823, 1687, 1555, 1098, 1060, 996, 599, 412, 
                 328, 292]
    if bill in excludes:
        return False
    else:
        return True
    

def collect_data():
    members = pd.read_csv('members.csv')
    members['sponsor'] = np.NaN
    members['cosponsor'] =  np.NaN
    members['sponsor'] = members['sponsor'].astype(object)
    members['cosponsor'] = members['cosponsor'].astype(object)

    members.set_index('id')

    headers = {"X-API-Key": "9HMffhBj3dNKgNG74L53ycY37VdPFpwOIrsSfVsw"}

    for i in range(len(members['id'])):
        flag118 = True
        startval = 0
        sponsored_list = []
        while flag118:
            id = members['id'][i]
            url = "https://api.congress.gov/v3/member/" + id + "/sponsored-legislation?limit=250&offset=" + str(startval)
            req = requests.get(url, headers=headers)
            norm = pd.json_normalize(req.json())
            sponsored_j = norm['sponsoredLegislation'][0]
            if sponsored_j == []:
                break
            for leg in sponsored_j:
                if leg['congress'] == 118:
                    if leg['type'] == 'HR':
                        sponsored_list.append(leg['number'])
                else:
                    flag118=False
                    break
            startval+=250
        members.at[i, 'sponsor'] = sponsored_list
        print("Found " + len(sponsored_list) + ' bills sponsored by Rep. ' + members['name'][i])


    for i in range(len(members['id'])):
        flag118 = True
        startval = 0
        sponsored_list = []
        while flag118:
            id = members['id'][i]
            url = "https://api.congress.gov/v3/member/" + id + "/cosponsored-legislation?limit=250&offset=" + str(startval)
            req = requests.get(url, headers=headers)
            norm = pd.json_normalize(req.json())
            sponsored_j = norm['cosponsoredLegislation'][0]
            if sponsored_j == []:
                break
            for leg in sponsored_j:
                if leg['congress'] == 118:
                    if leg['type'] == 'HR':
                        sponsored_list.append(leg['number'])
                else:
                    flag118=False
                    break
            startval+=250
        members.at[i, 'cosponsor'] = sponsored_list
        print("Found " + len(sponsored_list) + ' bills cosponsored by Rep. ' + members['name'][i])

    members.to_csv("data.csv", index=False)

def synth_data(members):

    billsbyparty = {}
    cosponsordict = {}
    numbiparcosp = {}

    print("Making bill party table")
    for i in range(len(members['id'])):
        party = members['party'][i]
        sponsorlist = members['sponsor'][i]
        if type(sponsorlist) != float:
            sponsorlist = sponsorlist.strip('][').split(', ')
            if len(sponsorlist) != 0 and sponsorlist != ['']:
                for item in sponsorlist:
                    item = int(item.strip("'"))
                    if check_for_exclusion(item):
                        billsbyparty[item] = party

    print("Counting cosponsors")
    for i in range(len(members['id'])):
        sponsorlist = members['cosponsor'][i]
        biparc = 0
        allc = 0
        party = members['party'][i]
        if type(sponsorlist) != float:
            sponsorlist = sponsorlist.strip('][').split(', ')
            if len(sponsorlist) != 0 and sponsorlist != ['']:
                for item in sponsorlist:
                    item = int(item.strip("'"))
                    if check_for_exclusion(item):
                        try:
                            if billsbyparty[item] == party:
                                allc+=1
                            else:
                                biparc+=1
                                allc+=1
                                if item in numbiparcosp.keys():
                                    numbiparcosp[item] +=1
                                else:
                                    numbiparcosp[item] = 1
                        except KeyError:
                            continue
        cosponsordict[members['id'][i]] = (biparc, allc)

    return billsbyparty, cosponsordict, numbiparcosp

def calculatelugarcomponents(members, cosponsordict, numbiparcosp):
    
    membdata = pd.DataFrame(columns=['name', 'party', 'numc', 'biparc', 'biparsp', 'numsp', 'biparintensity'])

    print("Calculating bipartisan intentisty")
    for i in range(len(members['id'])):
        name = members['name'][i]
        party = members['party'][i]
        numc = cosponsordict[members['id'][i]][1]
        biparc = cosponsordict[members['id'][i]][0]
        biparsp = 0
        totalbiparsp = 0
        # ipartisan Intensity is defined as the base two logarithm 
        # of the average number of Bipartisan Co-sponsors a member 
        # attracted to their bills that received at least one Bipartisan Co-sponsor.

        sponsorlist = members['sponsor'][i]
        if type(sponsorlist) != float:
            sponsorlist = sponsorlist.strip('][').split(', ')
            if sponsorlist == ['']:
                numsp = 0
            else:
                numsp = len(sponsorlist)
                for item in sponsorlist:
                    item = int(item.strip("'"))
                    if check_for_exclusion(item):
                        if item in numbiparcosp.keys():
                            biparsp += 1
                            totalbiparsp += numbiparcosp[item]
            
            if biparsp != 0:
                biparintensity = math.log2(totalbiparsp/biparsp)
            else:
                biparintensity = 0

        else:
            print("WARN: " + name + " sponsorlist type is float")
            numsp = 0
            biparsp = 0
            biparintensity = 0

        membdata.loc[len(membdata.index)] = [name, party, numc, biparc, biparsp, numsp, biparintensity]

    membdata.to_csv("lugar.csv", index=False)

def output_humanreadable(selected, members, billsbyparty, numbiparcosp):
    sponsorships = pd.DataFrame(columns=["member", "bill", "Num R cosp", "intensity"])
    
    for member in selected.keys():
        memb_bills = members['sponsor'][members.index[members['id'] == selected[member]][0]].strip('][').split(', ')
        if len(memb_bills) != 0 and memb_bills != ['']:
            for bill in memb_bills:
                bill = int(bill.strip("'"))
                if not check_for_exclusion(bill):
                    continue
                if bill in numbiparcosp.keys():
                    sponsorships.loc[len(sponsorships.index)] = [member, bill, numbiparcosp[bill], math.log2(numbiparcosp[bill])]
                else:
                    sponsorships.loc[len(sponsorships.index)] = [member, bill, 0, np.nan]
                

    cosponsorships = pd.DataFrame()
    for member in selected.keys():
        bipar = []
        nonbipar = []
        party = members['party'][members.index[members['id'] == selected[member]][0]]
        memb_cosponses = members['cosponsor'][members.index[members['id'] == selected[member]][0]].strip('][').split(', ')
        if len(memb_cosponses) != 0 and memb_cosponses != ['']:
            for bill in memb_cosponses:
                bill = int(bill.strip("'"))
                if not check_for_exclusion(bill):
                    continue
                try:
                    if party == billsbyparty[bill]:
                        nonbipar.append(bill)
                    else:
                        bipar.append(bill)
                except KeyError:
                    continue
        
        bipard = pd.DataFrame({
            str(member + " Bipartisan Bills"): bipar
        })
        nonbipard = pd.DataFrame({
            str(member + " Non-Bipartisan Bills"): nonbipar
        })
        cosponsorships = pd.concat([cosponsorships, bipard], axis=1)
        cosponsorships = pd.concat([cosponsorships, nonbipard], axis=1)
    
    with pd.ExcelWriter("HumanReadableLugar.xlsx") as writer:
        cosponsorships.to_excel(writer, sheet_name="Cosponsorships", index=False)
        sponsorships.to_excel(writer, sheet_name="Sponsorships", index=False)

def main ():
    collect_data()
    members = pd.read_csv('data.csv')
    billsbyparty, cosponsordict, numbiparcosp = synth_data(members)
    calculatelugarcomponents(members, cosponsordict, numbiparcosp)
    selected = {"golden": "G000592",
            "gottheimer": "G000583",
            "spanberger": "S001209",
            "perez": "G000600",}
    output_humanreadable(selected, members, billsbyparty, numbiparcosp)

main()
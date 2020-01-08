############Import Libs############################
import socket
import os
import csv

import os.path
from os import path
import subprocess
import re
import argparse
#import httplib
import httplib2
import requests
############Import Libs END############################


############ Help Section #############################
version = '0.2'
parse = argparse.ArgumentParser(description = 'Chargepoint Alive Checher is an programm to check remotly if an Chargingpoint is reachable and how fast')
parse.add_argument("-m", "--manufactor",required=True , help="\"ALL\" or real names: ABL ABB Efacec Alpitronic Swarco Delta Smight   ")
parse.add_argument("-i", "--inputfile",required=True , help="CSV Station List with IPs")
parse.add_argument("-o", "--outputfile",required=False , help="CSV output with stats of Stations")
parse.add_argument("-v", "--version", help="show program version", action="store_true")
parse.parse_args()
args = parse.parse_args()
############ Help Section END #############################
# define ports below
ports=[["ABL",'80','443'],["ABC",'11','22']]
exceptionhosts = ['ncpocc.pre.cz','10.249.1.230','ocpp.abbext.com','80.149.188.186', '10.249.57.33']
CNT_DOWN = 0
CNT_UP = 0
name = {}
CI = {}
hostname = {}
status = {}

print('')
print('#######################################################')
print('# Selected Manufactor:',args.manufactor)
print('# Input  CSV:',args.inputfile)
print('# Output CSV:',args.outputfile)
print('# Ignored Hosts:',exceptionhosts)
print('#######################################################')
print('')
print('')


######Functions##################################################
def parse_for_losses(s):
    [host, s1]          = s.split(" : ")
    #print ('Inhalt_s1:', s1)
    [Trash_string1, loss_sting, delay_string]       = s1.split("%")

    #print ('Inhalt_AnySring:', Trash_string1)
    #print ('Inhalt_Loss_String:', loss_sting)
    #print ('Inhalt_Delay-String:', delay_string)


    #get packet loss of string
    [_, s2]             = loss_sting.split(" = ")
    [sent, recv, loss]  = s2.split("/")

    #Wenn String nicht leer
    if delay_string != "":
        #print('String nicht leer:', delay_string )
        # get delay time of string
        [Trash_String2, delay_raw_string] = delay_string.split(" = ")
        [min_delay, avg_delay, max_dely] = delay_raw_string.split("/")
        #print ('Delay:', avg_delay)
    else:
        avg_delay = 0
    return {
            "host": host,
            "sent": sent,
            "recv": recv,
            "loss": loss.strip("%"),
            "avg": str(avg_delay).replace(".", ",", 1),
            }



def check_url_ok(url):
    #http = httplib2.Http()
    #resp = http.request(url)[0]
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        return '800'
    urlStatus=r.status_code
    print("status code: ",urlStatus)
    if urlStatus==200:
        elapsedTime= requests.get(url).elapsed.total_seconds()
        return elapsedTime







######Functions END##################################################




# Wenn Ausgabe in Outfile als Parameter gesetzt in File schreiben
if args.outputfile:
    # Irgendwelche -o Parmeter wurden gesetzt

    #Header Line In CSV Datei schreiben
    with open(args.outputfile, mode='w') as employee_file:
        employee_writer = csv.DictWriter(employee_file, delimiter=';', fieldnames = ['id','Hersteller', 'IP', 'Status', 'Paketloss', 'Delay','Urlcheck','Load Test','Comments'])
        employee_writer.writeheader()
        employee_file.close()

#ffunction to loop over ports comparing to its Hersteller
def readPorts(var):
    for arr_i, arr in enumerate(ports):
        for row_i, row in enumerate(arr):
            if row==var and row_i==0:
                return arr

    default_arr=[]
    default_arr.append(var)
    default_arr.append('80')
    return default_arr
#function called when user executes by giving both -m ALL/ selected Hersteller
def runFile(hostname,CNT_UP,CNT_DOWN):
    hostname = hostname
    response = subprocess.run(["fping", '-c', '3', '-q', hostname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = response.stdout.decode("utf-8").strip()
    #print (output)
    parsed = parse_for_losses(output)
    #print('Paket loss in %:', parsed['loss'])
    #print('Delay in ms:', parsed['avg'])
    if response.returncode == 0:
                status = 'UP'
                CNT_UP = CNT_UP + 1
                #result_url_check = check_url_ok('http//'+hostname)
                #print ('URL ChechK:',result_url_check)
    else:
                status = 'Down'
                CNT_DOWN = CNT_DOWN + 1

    arr=readPorts(row['Hersteller'])
    #executes loop fo all the configured ports here
    for arr_i, port in enumerate(arr):
        if arr_i==0:
            continue

        result_url_check = check_url_ok('http//' + hostname + ':'  + port)
        #print('http//' + hostname)
        #print ('URL ChechK:',result_url_check)
        if status == 'Down' :
            remarks ="Unable to reach host"
            urlStatus= port +" DEAD"
        else:
            remarks= "Able to reach host successfullly"

        if result_url_check=='800':
            remarks= remarks + " and " + "Url ping is not successfull"
            if urlStatus== port +" DEAD" :
                 urlStatus= port +" DEAD"
            else:
                urlStatus= port +"-NOT OK"
        else :
            remarks= remarks + ", " + "Url ping is not successfull"
            urlStatus= port +"-OK"
        response = subprocess.run(["fping",'-c','10','-q','-b','40000', hostname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = response.stdout.decode("utf-8").strip()
        loadparsed = parse_for_losses(output)
        if loadparsed['loss'] <'10' and loadparsed['avg'] <'70' :
            loadResult="Passed with and average round trip time" +loadparsed['avg'] + " and with loss of "+loadparsed['loss']
            remarks=remarks+',also load test'+ loadResult
        else:
            loadResult="Failed"
            remarks=remarks+', also load test'+ loadResult
                #print (row['Isoinstanz'], row['Hersteller'] , row['IP'], status, 'Paket loss in %:',parsed['loss'], 'Delay in ms:', parsed['avg'] )
        print (row['Isoinstanz'],'|', row['Hersteller'] ,'|', row['alternatehost'],'|', status, '| Paket loss in %:',parsed['loss'], '|Delay in ms:', parsed['avg'] ,'|URL status:', urlStatus ,'|Loadtest:',loadResult,'|Comments:',remarks)
        #In CSV Datei schreiben
        if args.outputfile:
            # Irgendwelche -o Parmeter wurden gesetzt
            with open(args.outputfile, mode='a') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter=';')
                employee_writer.writerow([row['Isoinstanz'] ,row['Hersteller'] , row['alternatehost'], status, parsed['loss'], parsed['avg'],urlStatus,loadResult,remarks])
            employee_file.close()


with open(args.inputfile, mode='r') as csvinput:
        reader = csv.DictReader(csvinput, delimiter=';' )
        #changed to comma instead of semicolon
        for row in reader:

            #print(row['Hersteller'],args.manufactor)
            # Nur die CSV Datensätze nehmen mit Hersteller matching
            if row['Hersteller'] == args.manufactor:
                hostname = row['alternatehost']
                runFile(hostname,CNT_UP,CNT_DOWN)
            # Alle CSV Datensätze nehmen da alle Hersteller gesucht sind
            elif args.manufactor == 'ALL' and not any([x in row['alternatehost'] for x in exceptionhosts]):
                hostname = row['alternatehost']
                runFile(hostname,CNT_UP,CNT_DOWN)

#csvinput.close()
#employee_writer.close()



print('')
print('')
print('#######################################################')
print('# Summary:')
print('# Stations UP:', CNT_UP)
print('# Stations Down:', CNT_DOWN)
if CNT_DOWN == 0:
    print(  '# Percentage Down: 0% ')
else:
    print('# Percentage Down:', (CNT_UP/CNT_DOWN)*100,'%')
#
print('#######################################################')
print('')

import csv

event_list = list()
tas_event_list = list()
f1input = 'Alarmlogs\CFXVMdata.csv'
f1output = 'solution\outputCFXVM.csv'
f2input = 'Alarmlogs\TASdata.csv'
f2output = 'solution\outputTAS.csv'

class Alarm:
    def __init__(self,alarm):
        self.alarm = alarm

    def __str__(self):
        retstr = ''
        for k, v in self.alarm.items():
            retstr += '%s: %s\n' % (k, v)
        return retstr

    def check(self, key):
        return self.alarm.get(key, 0)

    def add(self, eventid):
        self.alarm['Events'] = eventid

    def compare(self, new_alarm):
        if time_validator(self.alarm['val1'], new_alarm.check('val1')):
            return True
        elif time_validator(self.alarm['val1'], new_alarm.check('val1')) == 120 and pattern_checker(self.alarm['val4'], new_alarm.check('val4')) > 50:
            return True

    def write(self, wo):
        wo.writerow(self.alarm)

class Alarm_TAS:
    def __init__(self,alarm):
        self.alarm = alarm

    def __str__(self):
        retstr = ''
        for k, v in self.alarm.items():
            retstr += '%s: %s\n' % (k, v)
        return retstr

    def check(self, key):
        return self.alarm.get(key, 0)

    def add(self, eventid1):
        self.alarm['Events'] = eventid1

    def compare(self, new_alarm):
        if time_validator(self.alarm['val4'], new_alarm.check('val4')):
            return True
        elif time_validator(self.alarm['val4'], new_alarm.check('val4')) == 120 and pattern_checker(self.alarm['val2'], new_alarm.check('val2')):
            return True

    def write(self, wo):
        wo.writerow(self.alarm)

def date_validator(d):
    d1 = d.split('-')
    if int(d1[1]) == 11:
        return True
    else:
        return False

def time_validator(t1,t2):
    t1_date = t1.split()
    t2_date = t2.split()
    if t1_date[0] == t2_date[0]:
        t1_time = t1_date[1].split(':')
        t2_time = t2_date[1].split(':')
        if int(t1_time[0]) == int(t2_time[0]):
            if int(t1_time[1]) == int(t2_time[1]):
                if (int(t2_time[2]) - int(t1_time[2])) < 40:
                    return True
                else:
                    return 120
            elif (int(t2_time[1]) - int(t1_time[1])) == 1:
                if (int(t2_time[2]) - int(t1_time[2])) <= - 20:
                    return True
                else:
                    return 120
            elif (int(t2_time[1]) - int(t1_time[1])) == 2:
                return 120
        else:
            return False
    else:
        return False

def pattern_checker(pattern1, pattern2):
    if ':' in pattern1:
        p1 = pattern1.split(':')
        p2 = pattern2.split(':')
        pattern_count = 0
        for word in p2:
            if word in p1:
                pattern_count += 1
        return ((pattern_count / len(p1)) * 100)
    else:
        p1 = pattern1.split('-')
        p2 = pattern2.split('-')
        if p1[0] == p2[0]:
            return True


def header(file):
    with open(file) as a1file:
        rcsv_file = csv.reader(a1file)
        for head in rcsv_file:
            break
        head.append('Events')
        return (head)

def sorting(alarm_set):
    eventid = 1
    for elem in alarm_set:
        if elem.check('Events') > 0 :
            continue
        else:
            eventid += 1
            elem.add(eventid)
            for selem in alarm_set:
                if selem.check('Events') > 0 :
                    continue
                elif elem.compare(selem):
                    print(eventid)
                    selem.add(eventid)

# Reading CSVs in to dictionaries. Removing noise data and inserting every row in to Alarm object.


def fopen(finput,list,obj,tag):
    with open(finput) as afile:
        drcsv = csv.DictReader(afile)
        for head in drcsv:
            if head.get('val6') == 'NOTICE':
                continue
            elif tag == "CFXVM":
                if head['val3'] == 'information':
                    continue
                elif date_validator(head.get('val1')):
                    list.append(obj(head))
            else:
                list.append(obj(head))


def fwrite(finput,foutput,list):
    with open(foutput, 'w', newline='') as a1file_o:
        fieldnames = header(finput)
        dwcsv = csv.DictWriter(a1file_o, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                               extrasaction='ignore')
        dwcsv.writeheader()
        for e in list:
            e.write(dwcsv)
fopen(f1input,event_list,Alarm,"CFXVM")
fopen(f2input,tas_event_list,Alarm_TAS,"TAS")

print(len(event_list))
print(len(tas_event_list))

print ("Start sorting event_list")
sorting(event_list)
print ("Start sorting tas_event_list")
sorting(tas_event_list)

print("start writing")

fwrite(f1input,f1output,event_list)
fwrite(f2input,f2output,tas_event_list)

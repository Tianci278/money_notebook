import json
import datetime
import re
import urllib.request, urllib.parse, urllib.error
import os

# get latest forex rate
def latest_forex(base, target):
    try:
        api_base = 'https://api.exchangeratesapi.io/latest?base='+base
        base_rate = urllib.request.urlopen(api_base)
        json_base_rate = json.loads(base_rate.read().decode())
        target_rate = json_base_rate['rates'][target]
        return target_rate
    except:
        print("【Failed to convert forex】")
        return 1
# return available fx list
def get_forex_list():
    forex_list = []
    try:
        forex_api = urllib.request.urlopen('https://api.exchangeratesapi.io/latest')
        json_forex_api = json.loads(forex_api.read().decode())
        for forex in json_forex_api['rates']:
            forex_list.append(forex)
        forex_list.append("EUR")
        return forex_list
    except:
        print("【Please check your internet connection】")
        quit()

# initialize the program: create the json file is not exist
def ini():
    mark = """
Made with spirit of financial independency by Tianci in Sept 2020;
Read readme_en before use
Email: tiancizhangmedia@outlook.com
"""
    if not os.path.exists("memo_v1.4.txt") or os.path.getsize("memo_v1.4.txt") == 0:
        memo_write = open("memo_v1.4.txt","w")
        forex_list = get_forex_list()
        print("【Select your base currency (most frequently used) in the list below】")
        print(forex_list)
        in_list = False
        while True:
            if in_list == True: break
            user_inp3 = input().upper()
            for fx in forex_list:
                if user_inp3 == fx: in_list = True
            if in_list == False: print("【Your selection isn't in the list, please try again】")
        json_dict = {"easp":[], "projects":[], "base_cur":user_inp3}
        memo_write.write(json.dumps(json_dict))
        memo_write.close()
    print(mark)
    memo_read = open("memo_v1.4.txt","r")
    global json_loads
    json_loads = json.loads(memo_read.read())

def read_write_projects(rorw,project):
    if rorw == "read":
        print(json_loads["projects"])
    elif rorw == "write":
        duplicate = False
        for p in json_loads["projects"]:
            if project == p:
                duplicate = True
                break
        if duplicate is False:
            json_loads["projects"].append(project)
            memo_write = open('memo_v1.4.txt','w')
            memo_write.write(json.dumps(json_loads))
            memo_write.close()

# user input start and end date
def input_date():
    while True:
        try:
            print("【Enter start date，yyyy-mm-dd：】")
            user_str = input()
            start_date = datetime.datetime.strptime(user_str, "%Y-%m-%d")
            print("【Enter end date，yyyy-mm-dd：】")
            user_str = input()
            end_date = datetime.datetime.strptime(user_str, "%Y-%m-%d")
            if end_date > start_date:
                break
            print("【Invalid input: end date earlier than start date】")
        except:
            print("【Invalid input（Error code:1）】")
    date_list = []
    date_list.append(start_date.strftime("%Y-%m-%d"))
    date_list.append(end_date.strftime("%Y-%m-%d"))
    return date_list

def balance_easp():
    base_cur = json_loads.get("base_cur")
    print("【Use '+' to connect multiple figures. eg:（100 + 200 + -300 GBP）】")
    for t in range(3):
        while True:
            try:
                if t == 0:
                    correct1 = True
                    print("【Enter your balance at the end date：】")
                elif t == 1:
                    correct1 = True
                    print("【Enter your total spending during the time：】")
                elif t == 2:
                    correct1 = True
                    print("【Enter your total earning during the time：】")
                user_inp6 = input()
                user_inp6_split = re.split(" \+ ", user_inp6)
                the_amount1 = 0
                for fg in user_inp6_split:
                    if re.search("[0-9]$", fg) and not re.search("[A-Z]", fg.upper()):
                        if t == 1 and float(fg) > 0:
                            print("【Please enter negative figures (include 0)】")
                            correct1 = False
                        if t == 2 and float(fg) < 0:
                            print("【Please enter positive figures(include 0)】")
                            correct1 = False
                        the_amount1 = the_amount1 + float(fg)
                    elif re.search("[A-Z]$", fg.upper()) and re.search("^-*[0-9]+", fg) and re.search(" ",fg):
                        fg_split = re.split(" ", fg)
                        forex_list = get_forex_list()
                        if not fg_split[1].upper() in forex_list:
                            print("【Invalid forex code, please re-enter】")
                            correct1 = False
                        if t == 1 and float(fg_split[0]) > 0:
                            print("【Please enter negative figures (include 0)】")
                            correct1 = False
                        if t == 2 and float(fg_split[0]) < 0:
                            print("【Please enter positive figures(include 0)】")
                            correct1 = False
                        rate = latest_forex(fg_split[1].upper(), base_cur)
                        the_amount1 = the_amount1 + float(fg_split[0]) * rate
                        print("Rate：", rate,"Converted：",float(fg_split[0]) * rate)
                    else:
                        print("【Invalid input（Error code:2）】")
                        correct1 = False
            except:
                print("【Invalid input（Error code:2.1）】")
                continue
            if correct1:
                break
        if t == 0:
            json_loads["easp"][-1]["balance"] = the_amount1
            print("Recorded balance:", the_amount1)
        elif t == 1:
            json_loads["easp"][-1]["totsp"] = the_amount1
            print("Recorded spending:", the_amount1)
        elif t == 2:
            json_loads["easp"][-1]["totea"] = the_amount1
            print("Recorded earning:", the_amount1)

def get_rec_book():
    global num_record
    num_record = {}
    num2 = 1
    json_loads["easp"].sort(key = lambda date:date.get("start_date"))
    for dict in json_loads["easp"]:
        dates = dict.get("start_date") + "——" + dict.get("end_date")
        num_record[num2] = dates
        num2 = num2 +1
    for k2, v2 in num_record.items():
        print(k2, v2)

# record pass spending and earning
def record_easp(choice):
    global base_cur
    base_cur = json_loads.get("base_cur")
    # ask for input
    user_inp2 = choice
    user_inp2_split = re.split("\s", user_inp2)
    if re.search("^c", user_inp2):
        start_end_date = input_date()
        date_dict = {}
        date_dict["start_date"] = start_end_date[0]
        date_dict["end_date"] = start_end_date[1]
        json_loads["easp"].append(date_dict)
        balance_easp()
        memo_write = open('memo_v1.4.txt','w')
        memo_write.write(json.dumps(json_loads))
        memo_write.close()
        target_record = -1
    elif re.search("^m", user_inp2):
        try:
            target_record = int(user_inp2_split[1])-1
        except: print("【Invalid input（Error code:3）】")
    elif re.search("^d", user_inp2):
        try:
            target_record = int(user_inp2_split[1])-1
            json_loads["easp"].pop(target_record)
            return
        except:
            print("【Invalid input（Error code:4）】")
            return
    else:
        print("【Invalid input（Error code:5）】")
        return
    # record project
    if re.search("^c", user_inp2):
        current_dates = start_end_date[0] + "——" + start_end_date[1]
    else:
        current_dates = num_record.get(int(user_inp2_split[1]))
    print("""
——————————
Now editing: """, current_dates, """
Create new project = Plus sign + Space + Project name + Space + Figure（+ food -100）
Add figure to a project = Project number + Space + Figure （1 100）
Leave a note for your future self = n + Sapce + Note（n Save more money）
Delete a project = d + Space + Project number （d 2）
Finish editing = f （f）
Note 1: Positive number is income, negative number is spending. All figures based on the main currecnty, adding currency code after the figure (2 200 GBP) can convert currency to base currency.
Note 2: The note will show up next time you open the program.
Note 3: No need for very detailed recording, only record those you want to remember.
——————————""")
    print("【Do you want to add these:】")
    read_write_projects("read","na")
    while True:
        # creating a dict obj counting existing projects
        num_easp = {}
        num = 1
        try:
            for key, value in json_loads["easp"][target_record].items():
                if key != "start_date" and key != "end_date" and key != "balance" and key != "totea" and key != "totsp" and key != "note":
                    # check if value negative or positive
                    if value < 0:
                        eaorsp = "Spending"
                    elif value == 0:
                        eaorsp = ""
                    else: eaorsp = "Earning"
                    # giving the current recording
                    print("【",num," ", key," ", eaorsp," ", value,"】", sep="")
                    num_easp[num] = key
                    num = num + 1
        except: pass
        if json_loads["easp"][target_record].get("note") != None:
            print("【Note:",json_loads["easp"][target_record].get("note"),"】",sep="")
        if num_easp == {}:
            print("【The list is empty, please add a new project first】")
        user_inp = input()
        user_inp_split = re.split("\s", user_inp)
        if re.search("^[0-9]+", user_inp):
            # input checker
            if len(user_inp_split) != 2 and len(user_inp_split) != 3:
                print("【Invalid input（Error code:7）】")
                continue
            rate = 1
            if len(user_inp_split) == 3:
                try:
                    rate = latest_forex(user_inp_split[2].upper(), base_cur)
                except:
                    print("【Invalid forex code, please re-enter】")
                    continue
            try:
                the_project = num_easp.get(int(user_inp_split[0]))
                the_amount = float(user_inp_split[1]) * rate
                base_amount = json_loads["easp"][target_record].get(the_project)
                the_amount = the_amount + base_amount
                json_loads["easp"][target_record][the_project] = the_amount
            except: print("【Invalid input（Error code:8）】")
        elif re.search("^\+", user_inp):
            # input checker
            if len(user_inp_split) != 3 and len(user_inp_split) != 4:
                print("【Invalid input（Error code:9）】")
                continue
            rate = 1
            if len(user_inp_split) == 4:
                try:
                    rate = latest_forex(user_inp_split[3].upper(), base_cur)
                except:
                    print("【Invalid forex code, please re-enter】")
                    continue
            the_project = user_inp_split[1]
            try:
                the_amount = float(user_inp_split[2]) * rate
                json_loads["easp"][target_record][the_project] = the_amount
                read_write_projects("write", user_inp_split[1])
            except:
                print("Invalid input（Error code:9.1）")
        elif re.search("^d", user_inp):
            try:
                if len(user_inp_split) != 2:
                    print("【Invalid input（Error code:10）】")
                    continue
                remove_project = num_easp.get(int(user_inp_split[1]))
                json_loads["easp"][target_record].pop(remove_project)
            except:print("【Invalid input（Error code:11）】")
        elif re.search("^n", user_inp):
            try:
                json_loads["easp"][target_record]["note"] = ' '.join(user_inp_split[1:])
            except: print("【Invalid input（Error code:12）】")
        elif user_inp == "f": break
        else: print("【Invalid input（Error code:13）】")

# give you a total number from s the start date and e the end date
def total_cal(s,e):
    base_cur = json_loads.get("base_cur")
    # calculation
    target_from = int(s) - 1
    target_upto = int(e) - 1
    if s == -3:
        if len(json_loads["easp"]) <= 3:
            target_from = -len(json_loads["easp"])
        else: target_from = -3
        target_upto = - 1
    try:
        sd = json_loads["easp"][target_from].get("start_date")
        ed = json_loads["easp"][target_upto].get("end_date")
    except:
        print("【Range exceeded】")
        return
    num_iter = target_upto - target_from + 1
    if s == -3:
        num_iter = len(json_loads["easp"])
    print("【", sd, "——", ed,"】", sep="")
    if s == e:
        print("Balance：", round(json_loads["easp"][target_from].get("balance"), 2), base_cur)
    else:
        sb = json_loads["easp"][target_from].get("balance")
        eb = json_loads["easp"][target_upto].get("balance")
        if float(sb) > float(eb):
            print("【Balance is declining",round(float(sb), 2),"—>",round(float(eb), 2),"】",sep="")
        elif float(sb) < float(eb):
            print("【Balance is raising",round(float(sb), 2),"—>",round(float(eb), 2),"】",sep="")
    # total spending
    tot_totsp = 0
    for iter in range(num_iter):
        tot_totsp = tot_totsp + json_loads["easp"][target_from].get("totsp")
        target_from = target_from + 1
    target_from = int(s) - 1
    if s == -3:
        target_from = -len(json_loads["easp"])
    print("【Total spending:", round(tot_totsp, 2)," ", base_cur, "】",sep="")
    # total each project spending
    sd = datetime.datetime.strptime(sd, "%Y-%m-%d")
    ed = datetime.datetime.strptime(ed, "%Y-%m-%d")
    timedelta = ed - sd
    duration = re.findall("([0-9]+) days", str(timedelta))
    tot_dict = {}
    for iter in range(num_iter):
        for k3, v3 in json_loads["easp"][target_from].items():
            if k3 != "start_date" and k3 != "end_date" and k3 != "balance" and k3 != "totea" and k3 != "totsp" and k3 != "note":
                amt = tot_dict.get(k3)
                if amt == None: amt = 0
                tot_dict[k3] = v3 + amt
        target_from = target_from + 1
    target_from = int(s) - 1
    if s == -3:
        target_from = -len(json_loads["easp"])
    sorted_dict = sorted(tot_dict.items(), key = lambda v:v[1])
    for kvtot in sorted_dict:
        if float(kvtot[1]) < 0:
            per = str(int(kvtot[1]/tot_totsp*100)) + "%"
            perday = kvtot[1]/int(duration[0])
            if kvtot[0] == "food":
                eg_num = kvtot[1]/tot_totsp
            print("    ","【On"," ",kvtot[0]," ","You totally spent",int(kvtot[1])," ","Monthly average:",int(perday*30)," ","Percentage:",per,"】",sep="")
    try:
        print("    ","Your Engel's law score is:",round(eg_num,3))
    except:pass
    # total earning
    tot_totea = 0
    for iter in range(num_iter):
        tot_totea = tot_totea + json_loads["easp"][target_from].get("totea")
        target_from = target_from + 1
    target_from = int(s) - 1
    if s == -3:
        target_from = -len(json_loads["easp"])
    print("【Total earning:", round(tot_totea, 2)," ", base_cur, "】",sep="")
    # total each project earning
    sorted_dict = sorted(tot_dict.items(), key = lambda v:v[1], reverse=True)
    for kvtot in sorted_dict:
        if float(kvtot[1]) > 0:
            per = str(int(kvtot[1]/tot_totea*100)) + "%"
            perday = kvtot[1]/int(duration[0])
            print("    ","【On"," ",kvtot[0]," ","You totally spent",int(kvtot[1])," ","Monthly average:",int(perday*30)," ","Percentage:",per,"】",sep="")
    # get note
    note = json_loads["easp"][target_upto].get("note")
    if note == None: note = "None (Please add note)"
    print("【Past you sent a message:】")
    print("    ",note)

ini()
if json_loads["easp"] == []:
    print("【Welcome using Money Notebook! Wanna throw your future self a note on money? Add your first record first】")
    record_easp("c")
print("The most recent 3 records:")
total_cal(-3,-3)

show_m = True
while True:
    if show_m:
        print("""
【Records:】""")
        get_rec_book()
        print("""
——————————
See one record = s + Space + Record number （s 1）
See multiple records = s + Space + Record number - Record number （s 1-3）
Modify record = m + Space + Record number（m 1）；
Create new record = c （c）
Delete record = d + Space + Record number（d 2）
Quit the program = f（f）
——————————""")
    uinput = input()
    if re.search("^m", uinput) or re.search("^c", uinput) or re.search("^d", uinput):
        record_easp(uinput)
        memo_write = open('memo_v1.4.txt','w')
        memo_write.write(json.dumps(json_loads))
        memo_write.close()
        show_m = True
    elif re.search("^s", uinput):
        uinput_split = re.split("[\s-]", uinput)
        if re.search("s [0-9]+", uinput) or re.search("s [0-9]+-[0-9]+", uinput):
            if len(uinput_split) == 3:
                total_cal(uinput_split[1],uinput_split[2])
            elif len(uinput_split) == 2:
                total_cal(uinput_split[1],uinput_split[1])
        else:print("【Invalid input（error code: 14）】")
        show_m = False
    elif uinput == "f":break
    else:print("【Invalid input（error code: 15）】")

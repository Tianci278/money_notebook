import json
import datetime
import re
import urllib.request, urllib.parse, urllib.error
import os
import shutil
from language_pack import choose_lan

# get latest forex rate
def latest_forex(base, target):
    try:
        api_base = 'https://api.exchangeratesapi.io/latest?base='+base
        base_rate = urllib.request.urlopen(api_base)
        json_base_rate = json.loads(base_rate.read().decode())
        target_rate = json_base_rate['rates'][target]
        return target_rate
    except:
        print(message["mg1"])
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
        print(message["mg2"])
        quit()

# initialize the program: create the json file is not exist
def ini():
    mark = """
Made with spirit of financial independency by Tianci in Sept 2020;
使用前请阅读readme_cn|Read readme_en before using
联系邮箱|Email: tiancizhangmedia@outlook.com
"""
    if not os.path.exists("memo_v1.4.txt") or os.path.getsize("memo_v1.4.txt") == 0:
        memo_write = open("memo_v1.4.txt","w")
        # decide language of the program
        print("【请选择语言|Please choose a language(CN/EN):】")
        lan = ""
        lan_list = ["CN","EN"]
        while not lan in lan_list:
            lan = input().upper()
            if not lan in lan_list:
                print("【请输入CN或EN|Please enter CN or EN】")
        # decide base currency
        if lan == "CN":
            message = choose_lan("CN")
        elif lan == "EN":
            message = choose_lan("EN")
        forex_list = get_forex_list()
        print(message["mg4"])
        print(forex_list)
        in_list = False
        while True:
            if in_list == True: break
            user_inp3 = input().upper()
            for fx in forex_list:
                if user_inp3 == fx: in_list = True
            if in_list == False: print(message["mg5"])
        json_dict = {"easp":[], "projects":[], "planning":[], "base_cur":user_inp3, "lan":lan} # easp: earning and spending
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
            print(message["mg6"])
            user_str = input()
            start_date = datetime.datetime.strptime(user_str, "%Y-%m-%d")
            print(message["mg7"])
            user_str = input()
            end_date = datetime.datetime.strptime(user_str, "%Y-%m-%d")
            if end_date > start_date:
                break
            print(message["mg8"])
        except:
            print(message["mg9"])
    date_list = []
    date_list.append(start_date.strftime("%Y-%m-%d"))
    date_list.append(end_date.strftime("%Y-%m-%d"))
    return date_list

def balance_easp():
    base_cur = json_loads.get("base_cur")
    print(message["mg10"])
    for t in range(3):
        while True:
            try:
                if t == 0:
                    correct1 = True
                    print(message["mg11"])
                elif t == 1:
                    correct1 = True
                    print(message["mg12"])
                elif t == 2:
                    correct1 = True
                    print(message["mg13"])
                user_inp6 = input()
                user_inp6_split = re.split(" \+ ", user_inp6)
                the_amount1 = 0
                for fg in user_inp6_split:
                    if re.search("[0-9]$", fg) and not re.search("[A-Z]", fg.upper()):
                        if t == 1 and float(fg) > 0:
                            print(message["mg14"])
                            correct1 = False
                        if t == 2 and float(fg) < 0:
                            print(message["mg15"])
                            correct1 = False
                        the_amount1 = the_amount1 + float(fg)
                    elif re.search("[A-Z]$", fg.upper()) and re.search("^-*[0-9]+", fg) and re.search(" ",fg):
                        fg_split = re.split(" ", fg)
                        forex_list = get_forex_list()
                        if not fg_split[1].upper() in forex_list:
                            print(message["mg16"])
                            correct1 = False
                        if t == 1 and float(fg_split[0]) > 0:
                            print(message["mg17"])
                            correct1 = False
                        if t == 2 and float(fg_split[0]) < 0:
                            print(message["mg18"])
                            correct1 = False
                        rate = latest_forex(fg_split[1].upper(), base_cur)
                        the_amount1 = the_amount1 + float(fg_split[0]) * rate
                        print(message["mg85"], rate,message["mg86"],float(fg_split[0]) * rate)
                    else:
                        print(message["mg19"])
                        correct1 = False
            except:
                print(message["mg20"])
                continue
            if correct1:
                break
        if t == 0:
            json_loads["easp"][-1]["balance"] = the_amount1
            print(message["mg21"], the_amount1)
        elif t == 1:
            json_loads["easp"][-1]["totsp"] = the_amount1
            print(message["mg22"], the_amount1)
        elif t == 2:
            json_loads["easp"][-1]["totea"] = the_amount1
            print(message["mg23"], the_amount1)

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
        except: print(message["mg24"])
    elif re.search("^d", user_inp2):
        try:
            target_record = int(user_inp2_split[1])-1
            json_loads["easp"].pop(target_record)
            return
        except:
            print(message["mg25"])
            return
    else:
        print(message["mg26"])
        return
    # record project
    if re.search("^c", user_inp2):
        current_dates = start_end_date[0] + "——" + start_end_date[1]
    else:
        current_dates = num_record.get(int(user_inp2_split[1]))
    print(message["mg27"], current_dates, message["mg28"])
    print(message["mg29"])
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
                        eaorsp = message["mg87"]
                    elif value == 0:
                        eaorsp = ""
                    else: eaorsp = message["mg88"]
                    # giving the current recording
                    print("【",num," ", key," ", eaorsp," ", value,"】", sep="")
                    num_easp[num] = key
                    num = num + 1
        except: pass
        if json_loads["easp"][target_record].get("note") != None:
            print(message["mg30"],json_loads["easp"][target_record].get("note"),message["mg31"],sep="")
        if num_easp == {}:
            print(message["mg32"])
        user_inp = input()
        user_inp_split = re.split("\s", user_inp)
        if re.search("^[0-9]+", user_inp):
            # input checker
            if len(user_inp_split) != 2 and len(user_inp_split) != 3:
                print(message["mg33"])
                continue
            rate = 1
            if len(user_inp_split) == 3:
                try:
                    rate = latest_forex(user_inp_split[2].upper(), base_cur)
                except:
                    print(message["mg34"])
                    continue
            try:
                the_project = num_easp.get(int(user_inp_split[0]))
                the_amount = float(user_inp_split[1]) * rate
                base_amount = json_loads["easp"][target_record].get(the_project)
                the_amount = the_amount + base_amount
                json_loads["easp"][target_record][the_project] = the_amount
            except: print(message["mg35"])
        elif re.search("^\+", user_inp):
            # input checker
            if len(user_inp_split) != 3 and len(user_inp_split) != 4:
                print(message["mg36"])
                continue
            rate = 1
            if len(user_inp_split) == 4:
                try:
                    rate = latest_forex(user_inp_split[3].upper(), base_cur)
                except:
                    print(message["mg37"])
                    continue
            the_project = user_inp_split[1]
            try:
                the_amount = float(user_inp_split[2]) * rate
                json_loads["easp"][target_record][the_project] = the_amount
                read_write_projects("write", user_inp_split[1])
            except:
                print(message["mg38"])
        elif re.search("^d", user_inp):
            try:
                if len(user_inp_split) != 2:
                    print(message["mg39"])
                    continue
                remove_project = num_easp.get(int(user_inp_split[1]))
                json_loads["easp"][target_record].pop(remove_project)
            except:print(message["mg40"])
        elif re.search("^n", user_inp):
            try:
                json_loads["easp"][target_record]["note"] = ' '.join(user_inp_split[1:])
            except: print(message["mg41"])
        elif user_inp == "f": break
        else: print(message["mg42"])

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
        print(message["mg43"])
        return
    num_iter = target_upto - target_from + 1
    if s == -3:
        num_iter = len(json_loads["easp"])
    print(message["mg44"], sd, message["mg45"], ed,message["mg46"], sep="")
    if s == e:
        print(message["mg47"], round(json_loads["easp"][target_from].get("balance"), 2)," ", base_cur,message["mg48"], sep="")
    else:
        sb = json_loads["easp"][target_from].get("balance")
        eb = json_loads["easp"][target_upto].get("balance")
        if float(sb) > float(eb):
            print(message["mg49"],round(float(sb), 2),"—>",round(float(eb), 2),message["mg50"],sep="")
        elif float(sb) < float(eb):
            print(message["mg51"],round(float(sb), 2),"—>",round(float(eb), 2),message["mg52"],sep="")
    # total spending
    tot_totsp = 0
    for iter in range(num_iter):
        tot_totsp = tot_totsp + json_loads["easp"][target_from].get("totsp")
        target_from = target_from + 1
    target_from = int(s) - 1
    if s == -3:
        target_from = -len(json_loads["easp"])
    print(message["mg53"], round(tot_totsp, 2)," ", base_cur, message["mg54"],sep="")
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
            if kvtot[0] == message["mg55"]:
                eg_num = kvtot[1]/tot_totsp
            print("    ",message["mg56"]," ",kvtot[0]," ",message["mg57"],int(kvtot[1])," ",message["mg58"],int(perday*30)," ",message["mg59"],per,sep="")
    try:
        print("    ",message["mg60"],round(eg_num,3))
    except:pass
    # total earning
    tot_totea = 0
    for iter in range(num_iter):
        tot_totea = tot_totea + json_loads["easp"][target_from].get("totea")
        target_from = target_from + 1
    target_from = int(s) - 1
    if s == -3:
        target_from = -len(json_loads["easp"])
    print(message["mg61"], round(tot_totea, 2)," ", base_cur, message["mg62"],sep="")
    # total each project earning
    sorted_dict = sorted(tot_dict.items(), key = lambda v:v[1], reverse=True)
    for kvtot in sorted_dict:
        if float(kvtot[1]) > 0:
            per = str(int(kvtot[1]/tot_totea*100)) + "%"
            perday = kvtot[1]/int(duration[0])
            print("    ",message["mg63"]," ",kvtot[0]," ",message["mg64"],int(kvtot[1])," ",message["mg65"],int(perday*30)," ",message["mg66"],per,sep="")
    # get note
    note = json_loads["easp"][target_upto].get("note")
    if note == None: note = message["mg67"]
    print(message["mg68"])
    print("    ",note)

def if_date(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False

# record or delte plan
def edit_plan(inp):
    # yooooooo new feature
    today = datetime.datetime.today()
    if inp == "+":
        plan_dict = {}
        for t in range(3):
            if t == 0:
                print(message["mg69"])
            if t == 1:
                print(message["mg70"])
            if t == 2:
                print(message["mg71"])
            while True:
                user_input = input()
                if t == 0 and if_date(user_input):
                    the_date = datetime.datetime.strptime(user_input, "%Y-%m-%d")
                    if today <= the_date:
                        the_date = the_date.strftime("%Y-%m-%d")
                        plan_dict["date"] = the_date
                        break
                    else:
                        print(message["mg72"])
                elif t == 0:
                    print(message["mg73"])
                if t == 1:
                    plan_dict["plan"] = user_input
                    break
                if t == 2 and not re.search("\D", user_input[1:]):
                    amt = float(user_input)
                    plan_dict["amount"] = amt
                    break
                elif t == 2:
                    print(message["mg74"])
        json_loads["planning"].append(plan_dict)
    # it deletes the wrong record
    else:
        json_loads["planning"].pop(int(inp)-1)
    memo_write = open('memo_v1.4.txt','w')
    memo_write.write(json.dumps(json_loads))
    memo_write.close()

# bug: the list isnt sorted by date
def show_plan():
    if len(json_loads["easp"]) == 0:
        print(message["mg89"])
        latest_balance = 0
    else:
        latest_balance = json_loads["easp"][-1].get("balance")
    today = datetime.datetime.today()
    json_loads["planning"].sort(key = lambda date:date["date"])
    show = False
    print(message["mg75"])
    for plan in json_loads["planning"]:
        the_date = datetime.datetime.strptime(plan.get("date"), "%Y-%m-%d")
        the_plan = plan.get("plan")
        the_amount = plan.get("amount")
        latest_balance = latest_balance + the_amount
        if the_amount < 0:
            word = message["mg76"]
        else:
            word = message["mg77"]
        if today <= the_date:
            print("    ",json_loads["planning"].index(plan)+1,the_date.date(), the_plan, word, the_amount, "之后余额剩", round(latest_balance, 2))
            show = True
    if not show:
        print(message["mg78"])




ini()
message = choose_lan(json_loads["lan"])
# first open program
if json_loads["easp"] == []:
    print(message["mg79"])
    record_easp("c")
menu = message["mg80"]
# backup file daily everytime the program runs
os.makedirs("memo_backup", exist_ok=True)
today = datetime.date.today().strftime("%Y-%m-%d")
file_name = "memo_v1.4_backup" + today + "Open" + ".txt"
path = "memo_backup/" + file_name
shutil.copy2("memo_v1.4.txt", path)

def show_menu():
    print(message["mg81"])
    total_cal(-3,-3)
    show_plan()
    print(message["mg82"])
    get_rec_book()
    print(menu)
show_menu()
while True:
    uinput = input()
    if re.search("^m", uinput) or re.search("^c", uinput) or re.search("^d", uinput):
        record_easp(uinput)
        memo_write = open('memo_v1.4.txt','w')
        memo_write.write(json.dumps(json_loads))
        memo_write.close()
        show_menu()
    elif re.search("^s", uinput):
        uinput_split = re.split("[\s-]", uinput)
        if re.search("s [0-9]+", uinput) or re.search("s [0-9]+-[0-9]+", uinput):
            if len(uinput_split) == 3:
                total_cal(uinput_split[1],uinput_split[2])
            elif len(uinput_split) == 2:
                total_cal(uinput_split[1],uinput_split[1])
        else:print(message["mg83"])
    elif re.search("\+", uinput) and len(uinput) == 1:
        edit_plan(uinput)
        show_menu()
    elif not re.search("\D", uinput[2:]) and re.search("^- ", uinput):
        edit_plan(uinput[2:])
        show_menu()
    elif uinput == "f":
        # backup file daily everytime the program closes
        os.makedirs("memo_backup", exist_ok=True)
        today = datetime.date.today().strftime("%Y-%m-%d")
        file_name = "memo_v1.4_backup" + today + "Close" + ".txt"
        path = "memo_backup/" + file_name
        shutil.copy2("memo_v1.4.txt", path)
        break
    else:print(message["mg84"])

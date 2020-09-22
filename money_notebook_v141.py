import json
import datetime
import re
import urllib.request, urllib.parse, urllib.error
import os
import shutil

# get latest forex rate
def latest_forex(base, target):
    try:
        api_base = 'https://api.exchangeratesapi.io/latest?base='+base
        base_rate = urllib.request.urlopen(api_base)
        json_base_rate = json.loads(base_rate.read().decode())
        target_rate = json_base_rate['rates'][target]
        return target_rate
    except:
        print("【汇率转换失败】")
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
        print("【请连接网络】")
        quit()

# initialize the program: create the json file is not exist
def ini():
    mark = """
Made with spirit of financial independency by Tianci in Sept 2020;
使用前请阅读readme_cn
联系邮箱: tiancizhangmedia@outlook.com
"""
    if not os.path.exists("memo_v1.4.txt") or os.path.getsize("memo_v1.4.txt") == 0:
        memo_write = open("memo_v1.4.txt","w")
        forex_list = get_forex_list()
        print("【请从以下列表中选择记账基础货币】")
        print(forex_list)
        in_list = False
        while True:
            if in_list == True: break
            user_inp3 = input().upper()
            for fx in forex_list:
                if user_inp3 == fx: in_list = True
            if in_list == False: print("【你的输入不在列表中，请重新输入】")
        json_dict = {"easp":[], "projects":[], "planning":[], "base_cur":user_inp3, "lan":"CN"} # easp: earning and spending
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
            print("【请输入开始日期，yyyy-mm-dd：】")
            user_str = input()
            start_date = datetime.datetime.strptime(user_str, "%Y-%m-%d")
            print("【请输入结束日期，yyyy-mm-dd：】")
            user_str = input()
            end_date = datetime.datetime.strptime(user_str, "%Y-%m-%d")
            if end_date > start_date:
                break
            print("【错误输入：结束日期早于开始日期】")
        except:
            print("【无效输入（错误代码：1）】")
    date_list = []
    date_list.append(start_date.strftime("%Y-%m-%d"))
    date_list.append(end_date.strftime("%Y-%m-%d"))
    return date_list

def balance_easp():
    base_cur = json_loads.get("base_cur")
    print("【可使用“+”来综合计算多笔数额，支持货币转换（100 + 200 + -300 GBP）】")
    for t in range(3):
        while True:
            try:
                if t == 0:
                    correct1 = True
                    print("【请输入结束日期的余额：】")
                elif t == 1:
                    correct1 = True
                    print("【请输入这段时间的总支出：】")
                elif t == 2:
                    correct1 = True
                    print("【请输入这段时间的总收入：】")
                user_inp6 = input()
                user_inp6_split = re.split(" \+ ", user_inp6)
                the_amount1 = 0
                for fg in user_inp6_split:
                    if re.search("[0-9]$", fg) and not re.search("[A-Z]", fg.upper()):
                        if t == 1 and float(fg) > 0:
                            print("【请输入负数（包括0）】")
                            correct1 = False
                        if t == 2 and float(fg) < 0:
                            print("【请输入正数（包括0）】")
                            correct1 = False
                        the_amount1 = the_amount1 + float(fg)
                    elif re.search("[A-Z]$", fg.upper()) and re.search("^-*[0-9]+", fg) and re.search(" ",fg):
                        fg_split = re.split(" ", fg)
                        forex_list = get_forex_list()
                        if not fg_split[1].upper() in forex_list:
                            print("【无效的外汇代码，请重新输入】")
                            correct1 = False
                        if t == 1 and float(fg_split[0]) > 0:
                            print("【请输入负数（包括0）】")
                            correct1 = False
                        if t == 2 and float(fg_split[0]) < 0:
                            print("【请输入正数（包括0）】")
                            correct1 = False
                        rate = latest_forex(fg_split[1].upper(), base_cur)
                        the_amount1 = the_amount1 + float(fg_split[0]) * rate
                        print("汇率：", rate,"换汇后：",float(fg_split[0]) * rate)
                    else:
                        print("【无效输入（错误代码：2）】")
                        correct1 = False
            except:
                print("【无效输入（错误代码：2.1）】")
                continue
            if correct1:
                break
        if t == 0:
            json_loads["easp"][-1]["balance"] = the_amount1
            print("录入余额：", the_amount1)
        elif t == 1:
            json_loads["easp"][-1]["totsp"] = the_amount1
            print("录入支出：", the_amount1)
        elif t == 2:
            json_loads["easp"][-1]["totea"] = the_amount1
            print("录入收入：", the_amount1)

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
        except: print("【无效输入（错误代码：3）】")
    elif re.search("^d", user_inp2):
        try:
            target_record = int(user_inp2_split[1])-1
            json_loads["easp"].pop(target_record)
            return
        except:
            print("【无效输入（错误代码：4）】")
            return
    else:
        print("【无效输入（错误代码：5）】")
        return
    # record project
    if re.search("^c", user_inp2):
        current_dates = start_end_date[0] + "——" + start_end_date[1]
    else:
        current_dates = num_record.get(int(user_inp2_split[1]))
    print("""
——————————
正在编辑：""", current_dates, """
创建新项目 = 加号+空格+项目名称+空格+数额（+ 吃饭 -100）
增加项目数额 = 项目代码+空格+数额 （1 100）
给未来的自己留个备注 = n+空格+备注（n 省着点花）
删除项目 = d+空格+项目代码 （d 2）
返回上级目录 = f （f）
注1：正数为收入，负数为支出；数值默认为基础货币，在数值后+空格+其他货币代码（如2 200 GBP）可将按实时汇率转换为基础货币。
注2：备注会在下次打开程序的时候出现。
注3：不需要事无巨细地记录，只记录你认为重要的项目就可以。
——————————""")
    print("【你是否想要添加这些：】")
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
                        eaorsp = "支出"
                    elif value == 0:
                        eaorsp = ""
                    else: eaorsp = "收入"
                    # giving the current recording
                    print("【",num," ", key," ", eaorsp," ", value,"】", sep="")
                    num_easp[num] = key
                    num = num + 1
        except: pass
        if json_loads["easp"][target_record].get("note") != None:
            print("【备注：",json_loads["easp"][target_record].get("note"),"】",sep="")
        if num_easp == {}:
            print("【当前列表为空，请添加新项目】")
        user_inp = input()
        user_inp_split = re.split("\s", user_inp)
        if re.search("^[0-9]+", user_inp):
            # input checker
            if len(user_inp_split) != 2 and len(user_inp_split) != 3:
                print("【无效输入（错误代码：7）】")
                continue
            rate = 1
            if len(user_inp_split) == 3:
                try:
                    rate = latest_forex(user_inp_split[2].upper(), base_cur)
                except:
                    print("【无效的的外汇代码，请重新输入】")
                    continue
            try:
                the_project = num_easp.get(int(user_inp_split[0]))
                the_amount = float(user_inp_split[1]) * rate
                base_amount = json_loads["easp"][target_record].get(the_project)
                the_amount = the_amount + base_amount
                json_loads["easp"][target_record][the_project] = the_amount
            except: print("【无效输入（错误代码：8）】")
        elif re.search("^\+", user_inp):
            # input checker
            if len(user_inp_split) != 3 and len(user_inp_split) != 4:
                print("【无效输入（错误代码：9）】")
                continue
            rate = 1
            if len(user_inp_split) == 4:
                try:
                    rate = latest_forex(user_inp_split[3].upper(), base_cur)
                except:
                    print("【错误的外汇代码，请重新输入】")
                    continue
            the_project = user_inp_split[1]
            try:
                the_amount = float(user_inp_split[2]) * rate
                json_loads["easp"][target_record][the_project] = the_amount
                read_write_projects("write", user_inp_split[1])
            except:
                print("无效输入（错误代码：9.1）")
        elif re.search("^d", user_inp):
            try:
                if len(user_inp_split) != 2:
                    print("【无效输入（错误代码：10）】")
                    continue
                remove_project = num_easp.get(int(user_inp_split[1]))
                json_loads["easp"][target_record].pop(remove_project)
            except:print("【无效输入（错误代码：11）】")
        elif re.search("^n", user_inp):
            try:
                json_loads["easp"][target_record]["note"] = ' '.join(user_inp_split[1:])
            except: print("【无效输入（错误代码：12）】")
        elif user_inp == "f": break
        else: print("【无效输入（错误代码：13）】")

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
        print("【超出查询范围】")
        return
    num_iter = target_upto - target_from + 1
    if s == -3:
        num_iter = len(json_loads["easp"])
    print("【", sd, "——", ed,"】", sep="")
    if s == e:
        print("【余额：", round(json_loads["easp"][target_from].get("balance"), 2)," ", base_cur,"】", sep="")
    else:
        sb = json_loads["easp"][target_from].get("balance")
        eb = json_loads["easp"][target_upto].get("balance")
        if float(sb) > float(eb):
            print("【余额呈下降趋势：",round(float(sb), 2),"—>",round(float(eb), 2),"】",sep="")
        elif float(sb) < float(eb):
            print("【余额呈上升趋势",round(float(sb), 2),"—>",round(float(eb), 2),"】",sep="")
    # total spending
    tot_totsp = 0
    for iter in range(num_iter):
        tot_totsp = tot_totsp + json_loads["easp"][target_from].get("totsp")
        target_from = target_from + 1
    target_from = int(s) - 1
    if s == -3:
        target_from = -len(json_loads["easp"])
    print("【总支出：", round(tot_totsp, 2)," ", base_cur, "】",sep="")
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
            if kvtot[0] == "食物":
                eg_num = kvtot[1]/tot_totsp
            print("    ","其中"," ",kvtot[0]," ","一共",int(kvtot[1])," ","平均每月",int(perday*30)," ","占总支出的",per,sep="")
    try:
        print("    ","你的恩格尔系数为：",round(eg_num,3))
    except:pass
    # total earning
    tot_totea = 0
    for iter in range(num_iter):
        tot_totea = tot_totea + json_loads["easp"][target_from].get("totea")
        target_from = target_from + 1
    target_from = int(s) - 1
    if s == -3:
        target_from = -len(json_loads["easp"])
    print("【总收入：", round(tot_totea, 2)," ", base_cur, "】",sep="")
    # total each project earning
    sorted_dict = sorted(tot_dict.items(), key = lambda v:v[1], reverse=True)
    for kvtot in sorted_dict:
        if float(kvtot[1]) > 0:
            per = str(int(kvtot[1]/tot_totea*100)) + "%"
            perday = kvtot[1]/int(duration[0])
            print("    ","其中"," ",kvtot[0]," ","一共",int(kvtot[1])," ","平均每月",int(perday*30)," ","占总收入的",per,sep="")
    # get note
    note = json_loads["easp"][target_upto].get("note")
    if note == None: note = "无（请在记录时间块时添加备注）"
    print("【过去的你给你发来信息：】")
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
                print("【请输入一个未来的日期：】")
            if t == 1:
                print("【请输入计划块名称：】")
            if t == 2:
                print("【请输入数额（正数为计划收入，负数为计划支出）】：")
            while True:
                user_input = input()
                if t == 0 and if_date(user_input):
                    the_date = datetime.datetime.strptime(user_input, "%Y-%m-%d")
                    if today <= the_date:
                        the_date = the_date.strftime("%Y-%m-%d")
                        plan_dict["date"] = the_date
                        break
                    else:
                        print("【请输入今天及以后的日期】")
                elif t == 0:
                    print("【无效的日期输入，请重试】")
                if t == 1:
                    plan_dict["plan"] = user_input
                    break
                if t == 2 and not re.search("\D", user_input[1:]):
                    amt = float(user_input)
                    plan_dict["amount"] = amt
                    break
                elif t == 2:
                    print("【请输入数字】")
        json_loads["planning"].append(plan_dict)
    # it deletes the wrong record
    else:
        json_loads["planning"].pop(int(inp)-1)
    memo_write = open('memo_v1.4.txt','w')
    memo_write.write(json.dumps(json_loads))
    memo_write.close()

# bug: the list isnt sorted by date
def show_plan():
    latest_balance = json_loads["easp"][-1].get("balance")
    today = datetime.datetime.today()
    json_loads["planning"].sort(key = lambda date:date["date"])
    show = False
    print("【计划收入/支出：】")
    for plan in json_loads["planning"]:
        the_date = datetime.datetime.strptime(plan.get("date"), "%Y-%m-%d")
        the_plan = plan.get("plan")
        the_amount = plan.get("amount")
        latest_balance = latest_balance + the_amount
        if the_amount < 0:
            word = "需支出"
        else:
            word = "将收入"
        if today <= the_date:
            print("    ",json_loads["planning"].index(plan)+1,the_date.date(), the_plan, word, the_amount, "之后余额剩", round(latest_balance, 2))
            show = True
    if not show:
        print("    暂无任何计划")

ini()
if json_loads["easp"] == []:
    print("【欢迎使用“钱笔记”，请打开你过去的账单，建立你的第一个时间块】")
    record_easp("c")
menu = """——————————
查看一个时间块统计 = s+空格+时间块代码 （s 1）
查看多个时间块统计 = s+空格+时间块代码-时间块代码 （s 1-3）
修改现存的时间块 = m+空格+时间块代码（m 1）；
创建新的时间块 = c （c）
删除时间块 = d+空格+时间块代码（d 2）
添加计划块 = + （+）
删除计划块 = -+空格+计划块代码 （- 3）
结束程序 = f（f）
——————————"""
# backup file daily everytime the program runs
today = datetime.date.today().strftime("%Y-%m-%d")
file_name = "memo_backup" + today + ".txt"
path = "memo_backup/" + file_name
shutil.copy2("memo_v1.4.txt", path)

def show_menu():
    print("最近三条记录的统计信息：")
    total_cal(-3,-3)
    show_plan()
    print("""
【已记录的时间块：】""")
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
        else:print("【无效输入（错误代码14）】")
    elif re.search("\+", uinput) and len(uinput) == 1:
        edit_plan(uinput)
        show_menu()
    elif not re.search("\D", uinput[2:]) and re.search("^- ", uinput):
        edit_plan(uinput[2:])
        show_menu()
    elif uinput == "f":
        # backup file daily everytime the program closes
        today = datetime.date.today().strftime("%Y-%m-%d")
        file_name = "memo_backup" + today + ".txt"
        path = "memo_backup/" + file_name
        shutil.copy2("memo_v1.4.txt", path)
        break
    else:print("【无效输入（错误代码15）】")

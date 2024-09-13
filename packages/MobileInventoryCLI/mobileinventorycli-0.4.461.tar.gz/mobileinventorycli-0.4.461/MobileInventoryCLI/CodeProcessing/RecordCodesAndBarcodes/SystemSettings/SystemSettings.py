from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.RandomStringUtil import *
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Unified.Unified as unified
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FormBuilder import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import prefix_text
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.ReFormula import *

from collections import namedtuple,OrderedDict
import nanoid
from password_generator import PasswordGenerator
import random
from pint import UnitRegistry
import pandas as pd
import numpy as np
from datetime import *
from colored import Style,Fore
import json,sys,math,re,calendar


class systemSettingsMenu:
    def detectGetOrSet(self,name,value,setValue=False):
        value=str(value)
        with Session(ENGINE) as session:
            q=session.query(SystemPreference).filter(SystemPreference.name==name).first()
            ivalue=None
            if q:
                try:
                    if setValue:
                        q.value_4_Json2DictString=json.dumps({name:eval(value)})
                        session.commit()
                        session.refresh(q)
                    ivalue=json.loads(q.value_4_Json2DictString)[name]
                except Exception as e:
                    q.value_4_Json2DictString=json.dumps({name:eval(value)})
                    session.commit()
                    session.refresh(q)
                    ivalue=json.loads(q.value_4_Json2DictString)[name]
            else:
                q=SystemPreference(name=name,value_4_Json2DictString=json.dumps({name:eval(value)}))
                session.add(q)
                session.commit()
                session.refresh(q)
                ivalue=json.loads(q.value_4_Json2DictString)[name]
            return ivalue

    def search(self):
        def mkText(text,data):
            return text
        while True:
            stext=Prompt.__init2__(None,func=mkText,ptext="Search Name or Id",helpText="name or id search",data=None)
            if stext in [None,]:
                break
            pid=None
            try:
                pid=int(stext)
            except Exception as e:
                pid=None

            with Session(ENGINE) as session:
                results=session.query(SystemPreference).filter(or_(SystemPreference.name.icontains(stext),SystemPreference.pid==pid)).all()
                ct=len(results)
                for num,r in enumerate(results):
                    msg=f"{num}/{ct-1} -> {r}"
                    print(msg)
                if ct <= 0:
                    continue
                htext="edit(e)/remove(rm)"
                doWhat=Prompt.__init2__(None,func=mkText,ptext="remove(rm)/<Enter>=Skip to New Search",helpText=htext,data=None)
                if doWhat in [None,]:
                    break
                elif doWhat in ['',]:
                    continue

                def getIds(length):
                    htext="commma separated list of numbers"
                    doWhat=Prompt.__init2__(None,func=mkText,ptext="list index numbers (comma separated)",helpText=htext,data=None)
                    if doWhat in [None,]:
                        return
                    l=doWhat.split(",")
                    tmp=[]
                    for i in l:
                        try:
                            ii=int(i)
                            if 0 <= ii < length:
                                tmp.append(ii)
                        except Exception as e:
                            print(e)
                    return tmp
                
                if doWhat in ['remove','rm','r','remove(r)','del','d','delete','delete(d)']:
                    i=getIds(ct)
                    if i in [[],None]:
                        continue
                    for num,pid in enumerate(i):
                        msg=f'Deleting {num}/{len(i)-1} -> {results[pid]}'
                        print(msg)
                        session.delete(results[pid])
                        if num % 10 == 0:
                            session.commit()
                    session.commit()

    def setWeatherCollect(self):
        def mkBool(text,data):
            try:
                if text in ['','y','yes','t','true','1']:
                    return True
                elif text in ['n','no','f','false','0']:
                    return False
                else:
                    return bool(eval(text))
            except Exception as e:
                print(e)
        state=Prompt.__init2__(None,func=mkBool,ptext="Weather Collection Enabled?",helpText="yes or no",data=None)
        if state in [None,]:
            return
        print(state)
        self.detectGetOrSet(name="CollectWeather",value=state,setValue=True)

    def __init__(self): 
        def mkText(text,data):
            return text
        htext=f"""System Settings Menu Options
{Fore.light_green}show_all|{Fore.light_yellow}sa{Fore.light_steel_blue} - {Fore.light_magenta}list all settings in SystemPreference
{Fore.light_green}search_select,{Fore.light_yellow}ss,{Fore.green_yellow}search{Fore.light_steel_blue} - {Fore.light_magenta}search by name/id, select by number(comma separated list is allowed), prompt for deletion if needed
{Fore.light_green}clear_all,{Fore.light_yellow}clear all,{Fore.green_yellow}ca{Fore.light_steel_blue} - {Fore.light_magenta}clear all system preferences and let system regenerate preferences as necessary
{Fore.light_green}set {Fore.light_blue}upca|{Fore.cyan}ean13|{Fore.spring_green_1}code {Fore.grey_70}detection {Fore.light_red}0{Fore.grey_70}=Disabled|{Fore.light_red}1{Fore.grey_70}=enabled{Fore.light_steel_blue} - {Fore.light_magenta}enable/disable code length based detection in Prompt            
{Fore.light_green}setWeatherCollect{Fore.light_steel_blue} - {Fore.light_magenta}Turn DateMetrics On/Off
{Fore.orange_red_1}{Style.bold}{Style.underline}PollDates For Expiration Menu{Style.reset}
{Fore.light_green}set Expiration_DelPol{Fore.light_steel_blue} - {Fore.light_magenta}Set time in seconds for prompt-delete in Expiry Tracking System{Style.reset}
{Fore.light_green}set Expiration_PastPoll{Fore.light_steel_blue} - {Fore.light_magenta}Set time in seconds to warn that you have past the Expiration Date in Expiry Tracking System{Style.reset}
{Fore.light_green}set Expiration_Poll{Fore.light_steel_blue} - {Fore.light_magenta}Set time in seconds to warn that you are approaching the Best-By/Expiration Date in Expiry Tracking System{Style.reset}
{Style.reset}"""
        while True:
            with Session(ENGINE) as session:
                doWhat=Prompt.__init2__(None,func=mkText,ptext="System Settings: Do What?",helpText=htext,data=None)
                if doWhat in [None,]:
                    break
                elif doWhat.lower() in "show_all,sa".split(","):
                    settings=session.query(SystemPreference).all()
                    ct=len(settings)
                    for num,i in enumerate(settings):
                        msg=f'{num}/{ct-1} -> {i}'
                        print(msg)
                elif doWhat.lower() in ['set Expiration_DelPol'.lower(),]:
                    value=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Seconds (Float): ",helpText="how many seconds past BB_expiry to prompt-delete Expiration Entry",data="float")
                    if value in ['d',]:
                        continue
                    elif value in [None,]:
                        return
                    self.detectGetOrSet("Expiration_DelPol",value,setValue=True)
                elif doWhat.lower() in ['set Expiration_PastPoll'.lower(),]:
                    value=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Seconds (Float): ",helpText="how many seconds past BB_expiry to prompt-delete Expiration Entry",data="float")
                    if value in ['d',]:
                        continue
                    elif value in [None,]:
                        return
                    self.detectGetOrSet("Expiration_PastPoll",value,setValue=True)
                elif doWhat.lower() in ['set Expiration_Poll'.lower(),]:
                    value=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Seconds (Float): ",helpText="how many seconds past BB_expiry to prompt-delete Expiration Entry",data="float")
                    if value in ['d',]:
                        continue
                    elif value in [None,]:
                        return
                    self.detectGetOrSet("Expiration_Poll",value,setValue=True)
                elif doWhat.lower() in "clear_all,clear all,ca".split(","):
                    r=session.query(SystemPreference).delete()
                    session.commit()
                elif doWhat.lower().startswith("set upca detection "):
                    if doWhat.lower().endswith("1"):
                        self.detectGetOrSet("PRESET_UPC_LEN",'12',setValue=True)
                    elif doWhat.lower().endswith("0"):
                        self.detectGetOrSet("PRESET_UPC_LEN",'None',setValue=True)
                elif doWhat.lower().startswith("set ean13 detection "):
                    if doWhat.lower().endswith("1"):
                        self.detectGetOrSet("PRESET_EAN13_LEN",'13',setValue=True)
                    elif doWhat.lower().endswith("0"):
                        self.detectGetOrSet("PRESET_EAN13_LEN",'None',setValue=True)
                elif doWhat.lower().startswith("set code detection "):
                    if doWhat.lower().endswith("1"):
                        self.detectGetOrSet("PRESET_CODE_LEN",'8',setValue=True)
                    elif doWhat.lower().endswith("0"):
                        self.detectGetOrSet("PRESET_CODE_LEN",'None',setValue=True)
                elif doWhat.lower() in "search_select,ss,search".split(","):
                    self.search()
                elif doWhat.lower() == "setWeatherCollect".lower():
                    self.setWeatherCollect()
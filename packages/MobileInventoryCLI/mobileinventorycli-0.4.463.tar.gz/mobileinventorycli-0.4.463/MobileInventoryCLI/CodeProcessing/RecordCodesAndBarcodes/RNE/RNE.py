from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FBMTXT import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FormBuilder import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.DatePicker import *

import pandas as pd
import csv
from datetime import datetime
from pathlib import Path
from colored import Fore,Style,Back
from barcode import Code39,UPCA,EAN8,EAN13
import barcode,qrcode,os,sys,argparse
from datetime import datetime,timedelta
import zipfile,tarfile
import base64,json
from ast import literal_eval
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import upcean

def detectGetOrSet(name,value,setValue=False):
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

class Expiry(BASE,Template):
	__tablename__="Expiry"
	eid=Column(Integer,primary_key=True)
	#if none,see barcode
	EntryId=Column(Integer)
	#in case there is no entry id associated for Barcode entered
	Barcode=Column(String)
	#in case something needs to be noted about it
	Note=Column(String)
	Name=Column(String)
	#datetime of product being worked
	DTOE=Column(DateTime)
	#best by or expiry of product
	BB_Expiry=Column(DateTime)
	#when the product was last rotated by you
	Poll=Column(Float)
	#how many seconds after BB_Expiry to Critical Tell You that there are expireds on the counter before silencing it
	PastPoll=Column(Float)
	#how many seconds after BB_Expiry to Critical Tell You that there are expireds on the counter before auto-removing it
	DelPoll=Column(Float)

	def __init__(self,**kwargs):
		for k in kwargs.keys():
			if k in [s.name for s in self.__table__.columns]:
				setattr(self,k,kwargs.get(k))

class Expiration:
	def scan(self):
		with Session(ENGINE) as session:
			while True:
				try:
					EntryId=None
					#Barcode=barcode

					Note=''
					DTOE=datetime.now()
					'''
					search=session.query(Entry).filter(
							or_(
								Entry.Barcode==barcode,
								Entry.Code==barcode,
								Entry.Barcode.icontains(barcode),
								Entry.Code.icontains(barcode)
								)
							).first()
					if search != None:
						EntryId=search.EntryId
						Barcode=search.Barcode
					'''
					#BB=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Best-By/Expiry:",helpText="write any comments related to this item mm/dd/yy|yyyy",data="datetime")
					#if BB in [None,]:
					#	return
					Poll=detectGetOrSet("Expiration_Poll",value=30*24*60*60)
					PastPoll=detectGetOrSet("Expiration_PastPoll",value=365*24*60*60)
					DelPoll=detectGetOrSet("Expiration_DelPol",value=2*365*24*60*60)
					data={
					'Barcode':{
					'type':'string',
					'default':'',
					},
					'BB_Expiry':{
					'type':'datetime',
					'default':datetime.now()
					},
					'Note':{'type':'string',
					'default':'',
					}
					,
					'Name':{'type':'string',
					'default':'New Item',
					}
					}
					exp=FormBuilder(data=data)
					if exp in [None,]:
						return
					search=session.query(Entry).filter(
							or_(
								Entry.Barcode==exp['Barcode'],
								Entry.Code==exp['Barcode'],
								Entry.Barcode.icontains(exp['Barcode']),
								Entry.Code.icontains(exp['Barcode'])
								)
							).first()
					
					if search != None:
						exp['EntryId']=search.EntryId
						exp['Barcode']=search.Barcode
						exp['Name']=search.Name
					exp['Poll']=Poll
					exp['PastPoll']=PastPoll
					exp['DelPoll']=DelPoll
					exp['DTOE']=datetime.now()					
					nexp=Expiry(**exp)
					session.add(nexp)
					session.commit()
					session.flush()
					session.refresh(nexp)
					print(nexp)
					self.show_warnings(code=exp['Barcode'],regardless=True)
				except Exception as e:
					print(e)

	def show_all(self,returnable=False,export=False):
		with Session(ENGINE) as session:
			query=session.query(Expiry)
			results=query.order_by(Expiry.BB_Expiry.desc()).all()
			ct=len(results)
			if returnable:
				return results
			if ct == 0:
				print(f"{Fore.orange_red_1}There are No Entries in the Expiry Table!")
			else:
				htext=f'''{Fore.light_steel_blue}Of Total Expiry Entries Checked So Far/ [X]
{Fore.light_yellow}Nearing/Past Entries Total/ [Y]
{Fore.light_red}Total Expiry Entries to Check [Z]
{Fore.light_steel_blue}X/{Fore.light_yellow}Y/{Fore.light_red}Z'''
				headers=f'{htext} -> {Fore.light_green}Name|{Fore.cyan}Barcode|{Fore.light_yellow}Note|{Fore.orange_red_1}EntryId|{Fore.light_magenta}eid|{Fore.light_red}BB_Expiry|{Fore.medium_violet_red}DTOE (DateTime of Entry){Style.reset}'
				print(headers)
				bcds=[]
				for num,entry in enumerate(results):
					bcds.append(str(entry.Barcode)[:-1]+f"|len({len(str(entry.Barcode)[:-1])})")
					msg=f'''{Fore.light_yellow}{num}/{Fore.dark_goldenrod}{num+1}/{Fore.light_red}{ct}{Fore.light_magenta} -> {Fore.light_green}{entry.Barcode}|{Fore.green_yellow}{entry.Name}|{Fore.orange_red_1}{Style.bold}{entry.BB_Expiry}|{Fore.medium_violet_red}{entry.DTOE}{Style.reset}'''
					print(msg)
			if export == True:
				if len(results) < 1:
					print("Nothing To Export")
				else:
					df=pd.DataFrame([row.__dict__ for row in results])
					df.insert(len(df.columns),"No Check Digit Barcode",bcds,True)
					toDrop=['DelPoll','Poll','PastPoll','_sa_instance_state','eid','EntryId']
					df.drop(toDrop, axis=1, inplace=True)
					try:
						f=Path("expired.csv")
						df.to_csv(f,index=False)
						print(f"successfuly export to {f}")
					except Exception as e:
						print(e)
					
					try:
						f=Path("expired.xlsx")
						df.to_excel(f,index=False)
						print(f"successfuly export to {f}")
					except Exception as e:
						print(e)

	def search_expo(self,returnable=False,code=None):
		with Session(ENGINE) as session:
			while True:
				if code != None:
					barcode=code
				else:
					barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Barcode|Name|EntryId|Expiry.eid|Date:",helpText="search for to select",data="string")
					if barcode in [None,]:
						return
					elif barcode in ['d','']:
						continue
				eid_=None
				try:
					eid_=int(barcode)
				except Exception as e:
					print(e)
					eid_=None

				entryid=None
				try:
					entryid=int(barcode)
				except Exception as e:
					print(e)
					entryid=None
				dt=FormBuilderMkText(barcode,"datetime-")
				query=session.query(Expiry).filter(
					or_(
						Expiry.Barcode==barcode,
						Expiry.Barcode.icontains(barcode),
						Expiry.Name==barcode,
						Expiry.Name.icontains(barcode),
						Expiry.eid==eid_,
						Expiry.EntryId==entryid,
						Expiry.BB_Expiry==dt,
						)
					)
				results=query.order_by(Expiry.BB_Expiry.desc()).all()
				ct=len(results)
				if returnable:
					return results
				if ct == 0:
					print(f"{Fore.orange_red_1}There are No Entries in the Expiry Table!")
				else:
					for num,entry in enumerate(results):
						msg=f'''{Fore.light_yellow}{num}/{Fore.dark_goldenrod}{num+1}/{Fore.light_red}{ct}{Fore.light_magenta} -> {Fore.light_green}{entry.Barcode}|{Fore.green_yellow}{entry.Name}|{Fore.orange_red_1}{Style.bold}{entry.BB_Expiry}{Style.reset}'''
						print(msg)

	def rm_expo(self):
		toRm=self.search_expo(returnable=True)
		ct=len(toRm)
		if ct == 0:
			print("Nothing to remove")
			return
		for num,entry in enumerate(toRm):
			msg=f'''{Fore.light_yellow}{num}/{Fore.dark_goldenrod}{num+1}/{Fore.light_red}{ct}{Fore.light_magenta} -> {entry}{Style.reset}'''
			print(msg)
		which=Prompt.__init2__(None,func=FormBuilderMkText,ptext="delete what numbers, being the first of the x/x/x? separated by commas if multiples.",helpText="use commas to separate selections",data="list")
		if which in [None,'d']:
			if which == 'd':
				print("A number must be provided here!")
			return
		else:
			select=[]
			for i in which:

				try:
					ii=int(i)
					print(i,toRm[ii],"to remove!")
					select.append(toRm[ii].eid)
				except Exception as e:
					print(e,"processing will continue")
			print(select)
			with Session(ENGINE) as session:
				for s in select:
					r=session.query(Expiry).filter(Expiry.eid==s).first()
					print(r)
					if r:
						session.delete(r)
						session.commit()
						session.flush()

	def rm_expo_bar(self):
		while True:
			try:
				fieldname='Remove Expiry by Barcode'
				mode='REB'
				h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
				barcode=Prompt.__init2__(self,func=FormBuilderMkText,ptext=f"{h} Barcode to Purge:",helpText="barcode to purge from Expiry Completely!",data="string")
				if barcode in [None,]:
					return
				elif barcode.lower() in ['d',]:
					continue
				else:
					with Session(ENGINE) as session:
						done=session.query(Expiry).filter(Expiry.Barcode==barcode).delete()
						session.commit()
						session.flush()
						print(f"{Fore.light_red}Done Deleting {Fore.cyan}{done}{Fore.light_red} Expiration Barcodes!{Style.reset}")


			except Exception as e:
				print(e)
				return



	def show_warnings(self,barcode=None,export=False,regardless=False,code=None):
		with Session(ENGINE) as session:
			if barcode == None:
				results=session.query(Expiry).all()
			else:
				results=self.search_expo(returnable=True,code=code)
			if results in [None,]:
				return
			ct=len(results)
			counter=0
			if ct == 0:
				print(f"{Fore.orange_red_1}No Expiry Results to check...")
				return
			htext=f'''{Fore.light_steel_blue}Of Total Expiry Entries Checked So Far/ [X]
{Fore.light_yellow}Nearing/Past Entries Total/ [Y]
{Fore.light_red}Total Expiry Entries to Check [Z]
{Fore.light_steel_blue}X/{Fore.light_yellow}Y/{Fore.light_red}Z'''
			headers=f'{htext} -> {Fore.light_green}Name|{Fore.cyan}Barcode|{Fore.light_yellow}Note|{Fore.orange_red_1}EntryId|{Fore.light_magenta}eid|{Fore.light_red}BB_Expiry|{Fore.medium_violet_red}DTOE (DateTime of Entry){Style.reset}'
			print(headers)
			exportable=[]
			bcds=[]
			for num,i in enumerate(results):
				warn_date=i.BB_Expiry+timedelta(seconds=i.Poll)
				past_warn_date=i.BB_Expiry+timedelta(seconds=i.PastPoll)
				del_date=i.BB_Expiry+timedelta(seconds=i.DelPoll)
				if ( datetime.now() >= i.BB_Expiry ) or ( regardless == True ):
					exportable.append(i)
					bcds.append(str(i.Barcode)[:-1]+f"|len({len(str(i.Barcode)[:-1])})")
					counter+=1
					iformat=f'{Fore.light_green}{i.Name}|{Fore.cyan}{i.Barcode}|{Fore.light_yellow}{i.Note}|{Fore.orange_red_1}{i.EntryId}|{Fore.light_magenta}{i.eid}|{Fore.light_red}{i.BB_Expiry}|{Fore.medium_violet_red}{i.DTOE}{Style.reset}'
					msg=f'''{Fore.light_steel_blue}{num}/{Fore.light_yellow}{counter}/{Fore.light_red}{ct}-> {iformat}'''
					print(msg)
					if datetime.now() <= warn_date:
						print(f'''{Back.plum_2}{Fore.dark_red_1}{warn_date}: Expiration Warn Date{Style.reset}''')
					elif datetime.now() > warn_date:
						print(f'''{Back.plum_2}{Fore.dark_red_1}{warn_date}: Expiration Warn Date{Fore.dark_green}{Style.bold}*{Style.reset}''')
					if datetime.now() >= warn_date:
						if datetime.now() <= past_warn_date:
							print(f'{Back.chartreuse_2a}{Fore.dark_blue}{Style.bold}{past_warn_date}: Expiration Past Warn Date{Style.reset}')
						elif datetime.now() > past_warn_date:
							print(f'{Back.chartreuse_2a}{Fore.dark_blue}{Style.bold}{past_warn_date}: Expiration Past Warn Date{Fore.dark_red_2}{Style.underline}***{Style.reset}')
					if datetime.now() >= past_warn_date:
						if datetime.now() <= del_date:
							print(f'{Back.dark_red_2}{Fore.orange_1}{del_date}: Expiration Deletion Date{Style.reset}')
						elif datetime.now() > del_date:
							print(f'{Back.dark_red_2}{Fore.orange_1}{del_date}: Expiration Deletion Date{Fore.light_green}{Style.bold}***{Style.reset}')
							delete=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Delete it?",helpText="yes or no",data="boolean")
							if delete in [None,]:
								continue
							elif delete == True:
								session.delete(i)
								session.commit()
								session.flush()
							else:
								pass
				#postMsg=f'''{warn_date}: Warn Date
				#{past_warn_date}: Past Warn Date
				#{del_date}: Deletion Date'''
			if export == True:
				if len(exportable) < 1:
					print("Nothing To Export")
				else:
					df=pd.DataFrame([row.__dict__ for row in exportable])
					df.insert(len(df.columns),"No Check Digit Barcode",bcds,True)
					toDrop=['DelPoll','Poll','PastPoll','_sa_instance_state','eid','EntryId']
					df.drop(toDrop, axis=1, inplace=True)
					try:
						f=Path("expired.csv")
						df.to_csv(f,index=False)
						print(f"successfuly export to {f}")
					except Exception as e:
						print(e)
					
					try:
						f=Path("expired.xlsx")
						df.to_excel(f,index=False)
						print(f"successfuly export to {f}")
					except Exception as e:
						print(e)


	def clear_all(self):
		with Session(ENGINE) as session:
			session.query(Expiry).delete()
			session.commit()
			session.flush()

	def __init__(self,init_only=False):
		#dates are first numeric using 102693 as the string
		#where first 2 digits are month,z-filled if len of month number is less than 2
		#where 3rd-4th digits are day,z-filled if len of day number is less than 2
		#where last 2 digits are year; this is not four digits, as expo is looking ahead only, and i dont
		#expect to be around into the 2100's;z-filled if len of year number is less than 2
		helpText=f'''
{Style.bold}{Fore.orange_red_1}Expiration Menu Options{Style.reset}
	{Fore.light_steel_blue}'scan','expireds','e'{Fore.light_green} -{Fore.cyan} set date for best-by/expiration-date for scanned upc using numeric data provided by label for code/barcode{Style.reset}
	{Fore.light_steel_blue}sw,show-warns,show-warnings,show_warns,show_warnings{Fore.light_green} -{Fore.cyan} prompt for barcode and show warnings; cleans anything past due by prompt{Style.reset}
	{Fore.light_steel_blue}sw*,show-warns*,show-warnings*,show_warns*,show_warnings*{Fore.light_green} -{Fore.cyan} prompt for barcode and show warnings; cleans anything past due by prompt *regardless of BB_Expiry,show entries{Style.reset}
	{Fore.light_steel_blue}swa,show-all-warns,show-all-warnings,show_all_warns,show_all_warnings{Fore.light_green} -show{Fore.cyan} anything within PollDates, where PollDates are [Warn of Upcoming(Poll),Past BB/Expo Date(Past_Warn_Date),cleanup date(De[letion] Date)] cleans anything past due by prompt{Style.reset}
	{Fore.light_steel_blue}'sa','show all','show_all','showall','show-all'{Fore.light_green} -{Fore.cyan} show all expirations and warning{Style.reset}
	{Fore.light_steel_blue}'sea','show export all','show_export_all','showexportall','show-export-all'{Fore.light_green} -{Fore.cyan} show & export all expirations and warning{Style.reset}
	{Fore.light_steel_blue}'re','rm exp','rm_exp','rm-exp','rme'{Fore.light_green} -{Fore.cyan} remove expirations and warnings{Style.reset}
	{Fore.light_steel_blue}reb,re b,rm barcode,rm batch{Fore.light_green} -{Fore.cyan}without confirmation, remove all Expiry with barcode{Style.reset}
	{Fore.light_steel_blue}'search','sch','look','where\'s my key bitch?'{Fore.light_green} -{Fore.cyan} search for a product to see if it was logged by Barcode|Name|EntryId|Expiry.eid|Date{Style.reset}
	{Fore.light_steel_blue}ca,clear all,clear_all{Fore.light_green} -{Fore.cyan} removes all items contained here{Style.reset}
{Style.bold}{Fore.orange_red_1}Notes{Style.reset} {Fore.orange_red_1}Dates{Fore.grey_70}
	Dates can be provided as DD{Fore.light_green}#SEPCHAR#{Fore.grey_70}MM{Fore.light_green}#SEPCHAR#{Fore.grey_70}YY|YYYY
	where {Fore.light_green}#SEPCHAR#{Fore.grey_70} can be any of the punctuation-chars, save for '%'.
	MM - 2-Digit Month
	DD - 2-Digit Day
	YY|YYYY - 2-Digit or 4-Digit Year
	{Fore.light_yellow}10.28/26 {Fore.light_magenta}10.28.26 {Fore.orange_red_1}10/26.93{Fore.cyan} - are valid, and ONLY touch the tip of the glacier{Fore.grey_70}
	if {Fore.light_red}No Day{Fore.grey_70} is provided in {Fore.light_magenta}BB/Exp Date{Fore.grey_70}, then assume day is {Fore.orange_red_1}01
{Style.reset}'''
		while not init_only:
			#for use with header
			fieldname='RotationAndExpiration'
			mode='RNE'
			h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
			doWhat=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Do What?",helpText=helpText,data="String")
			if doWhat in [None,]:
				return
			elif doWhat in ['d',]:
				print(helpText)
				continue
			elif doWhat.lower() in ['scan','expireds','e']:
				self.scan()
			elif doWhat.lower() in ['sa','show all','show_all','showall','show-all']:
				self.show_all()
			elif doWhat.lower() in ['sea','show export all','show_export_all','showexportall','show-export-all']:
				self.show_all(export=True)
			elif doWhat.lower() in ['re','rm exp','rm_exp','rm-exp','rme']:
				self.rm_expo()
			elif doWhat.lower() in ['search','sch','look','where\'s my key bitch?']:
				self.search_expo()
			elif doWhat.lower() in 'swa,show-all-warns,show-all-warnings,show_all_warns,show_all_warnings'.split(','):
				self.show_warnings()
			elif doWhat.lower() in 'sw,show-warns,show-warnings,show_warns,show_warnings'.split(","):
				self.show_warnings(barcode=True)
			elif doWhat.lower() in 'sw*,show-warns*,show-warnings*,show_warns*,show_warnings*'.split(","):
				self.show_warnings(barcode=True,regardless=True)
			elif doWhat.lower() in 'esw,export-show-warns,export-show-warnings,export_show_warns,export_show_warnings'.split(","):
				self.show_warnings(barcode=True,export=True)	
			elif doWhat.lower() in 'ca,clear all,clear_all'.split(','):
				self.clear_all()
			elif doWhat.lower() in 'reb,re b,rm barcode,rm batch'.split(","):
				self.rm_expo_bar()
			else:
				print(helpText)
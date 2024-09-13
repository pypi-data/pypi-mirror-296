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
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExtractPkg.ExtractPkg2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Lookup.Lookup import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DayLog.DayLogger import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ConvertCode.ConvertCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.setCode.setCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Locator.Locator import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ListMode2.ListMode2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.Tasks import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Collector2.Collector2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.LocationSequencer.LocationSequencer import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.PunchCard.PunchCard import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Conversion.Conversion import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.POS.POS import *
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Unified.Unified as unified


class ResetTools:
	def __init__(self,engine,parent):
		self.parent=parent
		self.engine=engine

		def mkT(text,data):
			return text


		self.helpText=f'''
		{Fore.light_red}{Style.bold}factory_reset{Style.reset}{Fore.light_red} - {Fore.light_steel_blue}completely resets everything; best if used before updates{Style.reset}
		{Fore.light_red}iv0|int_val_0 - {Fore.light_steel_blue}sets all entry integer fields to 0{Style.reset}
		{Fore.light_red}rap|reset_all_prices - {Fore.light_steel_blue}sets all entry prices to 0{Style.reset}
		{Fore.light_red}rac|reset_all_codes - {Fore.light_steel_blue}sets all entry codes to ''{Style.reset}
		{Fore.light_red}rats|reset_all_time_stamps - {Fore.light_steel_blue}sets all timestamps to now{Style.reset}
		{Fore.light_red}sai0|reset_all_inlist0 - {Fore.light_salmon_1}set InList/ListQty to False/0 {Style.reset}
		{Fore.light_red}sai1|reset_all_inlist1 - {Fore.light_salmon_1}set InList/ListQty to True/1 {Style.reset}
		{Fore.light_red}sau0|reset_all_useruUpdated - {Fore.light_salmon_1}set userUpdated to False{Style.reset}
		{Fore.light_red}sau1|reset_all_useruUpdated - {Fore.light_salmon_1}set userUpdated to True{Style.reset}
'''



		while True:
			cmd=Prompt.__init2__(None,func=mkT,ptext="Do What?",helpText=self.helpText)
			if cmd in [None,]:
				return
			elif isinstance(cmd,str):
				if cmd.lower() == 'factory_reset':
					reInit()
				elif cmd.lower() in ['iv0','int_val_0']:
					for f in Entry.__table__.columns:
						if f.name not in ['EntryId',] and str(f.type) == 'INTEGER':
							print(f"{Fore.chartreuse_1}Reseting {Fore.spring_green_3a}{f.name}={Fore.light_salmon_1}0{Style.reset}")
							self.setField(f.name,0)
				elif cmd.lower() in ['rap','reset_all_prices']:
					self.setField('Prices',0)
				elif cmd.lower() in ['rac','reset_all_codes']:
					self.setField('Codes','')
				elif cmd.lower() in ['rats','reset_all_time_stamps']:
					self.setField('Timestamp',datetime.now().timestamp())
				elif cmd.lower() in ['sai0','reset_all_inlist0']:
					self.setField('InList',False)
					self.setField('ListQty',0)
				elif cmd.lower() in ['sai1','reset_all_inlist1']:
					self.setField('InList',True)
					self.setField('ListQty',1)
				elif cmd.lower() in ['sau0','reset_all_useruUpdated']:
					self.setField('userUpdated',False)
				elif cmd.lower() in ['sau1','reset_all_useruUpdated']:
					self.setField('userUpdated',True)

	def setField(self,field,value):
			with Session(self.engine) as session:
				results=session.query(Entry).all()
				ct=len(results)
				for num,r in enumerate(results):
					msg=f"{num}/{ct-1} -> {Fore.tan}{r.Name}|{Fore.medium_violet_red}{r.Barcode}|{Fore.light_salmon_1}{r.Code}|{Fore.light_green}{r.EntryId}|{Fore.light_yellow}{field}->{Fore.light_red}{value}{Style.reset}"
					print(msg)
					setattr(r,field,value)
					if num%50==0:
						session.commit()
				session.commit()
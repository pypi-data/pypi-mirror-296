from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FormBuilder import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import prefix_text
from datetime import datetime


class SetCode:
	def setCodeFromBarcode(self):
		print("SetCode")
		if self.engine != None:
			with Session(self.engine) as session:
				self.batchMode=False
				while True:
						#batchMode=input("batch mode[y/n]: ")
						batchMode=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Batch Mode[y/n]?",helpText="Yes or No",data="boolean")
						print(batchMode)
						if batchMode in [None,]:
							return
						if batchMode:
							self.batchMode=True
							break
						else:
							self.batchMode=False
							break
				while True:
					try:
						#barcode=input("barcode: ")
						barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Barcode:",helpText="Product UPC, or #qb to quit batch mode if in batch mode",data="varchar")
						if barcode.lower() == "#qb":
							break
						#checks needed here
						query=session.query(Entry).filter(Entry.Barcode==barcode,Entry.Barcode.icontains(barcode))
						results=query.all()
						if len(results) < 1:
							print("No Results")
						else:
							r=None
							if len(results) == 1:
								r=results[0]
							elif len(results) > 1:
								try:
									while True:
										for num,i in enumerate(results):
											print(f"{num}/{len(results)} -> {i}")
										#select=input("which Entry: ")
										select=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Which Entry?",helpText="please which item number",data="integer")
										if select in [None,]:
											continue
										if select.lower() == 'd':
											select=0
											r=results[select]
											break
										if select == "#qb":
											r=None
											break	
										#select=int(select)
										r=results[select]
										#print(self.batchMode)
										#if not self.batchMode:
										break
								except Exception as e:
									print(e)
							if r != None:
								ncode=Prompt.__init2__(None,func=FormBuilderMkText,ptext="New Code, or #qb = quit batchMode?",helpText="new code to set, or #qb to quit batch mode",data="varchar")
								if ncode in [None,]:
									return
								if ncode.lower() == "#qb":
									break
								if ncode.lower() == 'd':
									ncode=''
								r.Code=ncode
								r.user_updated=True
								session.commit()
								session.flush()
								session.refresh(r)
								print(r,self.batchMode)
						if not self.batchMode:
							break
					except Exception as e:
						print(e)

	def __init__(self,engine=None):
		self.engine=engine
		cmds={
		'setCode from Barcode':{
								'cmds':['cfb','1','code<bc'],
								'exec':self.setCodeFromBarcode,
								'desc':"set Code from Barcode"
			},
		'quit':{
				'cmds':["q","quit","2"],
				'exec':lambda self=self:exit("user quit!"),
				'desc':"quit progam"
				},
		'back':{

				'cmds':['b','back','3'],
				'exec':None,
				'desc':"go back a menu if any"
				}
		}

		while True:
			for cmd in cmds:
				print(f"{cmds[cmd]['cmds']} - {cmds[cmd]['desc']}")
			action=input("Do What? : ")
			for cmd in cmds:
				try:
					if action.lower() in cmds[cmd]['cmds'] and cmds[cmd]['exec']!=None:
						cmds[cmd]['exec']()
						break
					elif action.lower() in cmds[cmd]['cmds'] and cmds[cmd]['exec']==None:
						return
					else:
						raise Exception(f"Invalid Command! {action}")
				except Exception as e:
					print(e)

if __name__ == "__main__":
	SetCode()
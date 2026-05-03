# SevoPediaIndex
#
# Copyright (c) 2008 The BUG Mod.
#
# EF: Converted from Civilopedia version by fitchn.

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import SevoScreenEnums
import BugUtil

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaIndex:

	def __init__(self, main):
		self.top = main
		
		self.LIST_BUTTON_SIZE = 24
		self.SAS_indexSetLayout(False)
		
		self.index = None
		self.letterTextIDs = None
		# <!-- custom: filter reads SevoPediaMain.SAS_szSearchString; the shared top-header search bar
		# is drawn by SevoPediaMain.SAS_syncSearchPanel and refreshed via SAS_refreshActiveListView.
		# This page owns no search state of its own. (Claude code Opus 4.7) -->
		self.SAS_indexWidgetNames = []

	def SAS_indexSetLayout(self, bCategory):
		if bCategory:
			self.X_INDEX = self.top.X_ITEMS
			self.Y_INDEX = self.top.Y_ITEMS
			self.W_INDEX = self.top.W_SCREEN - self.top.X_ITEMS
			self.H_INDEX = self.top.H_ITEMS
		else:
			self.X_INDEX = self.top.X_CATEGORIES
			self.Y_INDEX = self.top.Y_CATEGORIES
			self.W_INDEX = self.top.W_SCREEN - 2 * self.top.X_CATEGORIES
			self.H_INDEX = self.top.H_CATEGORIES
		
		self.X_LETTER = self.X_INDEX + 130  # position of first letter button
		self.Y_LETTER = self.Y_INDEX
		self.W_LETTER = 20

	def SAS_asUnicode(self, value, context):
		if isinstance(value, unicode):
			return value
		if isinstance(value, str):
			try:
				return value.decode("utf-8")
			except:
				try:
					return value.decode("cp1252")
				except:
					raise Exception("SevoPediaIndex: cannot decode '%s': %r" % (context, value))
		return unicode(value)

	def interfaceScreen(self, bCategory=False):
		self.SAS_indexSetLayout(bCategory)
		self.buildIndex()
		self.placeIndex()
	
	def buildIndex(self):
		if self.index:
			return
		
		techList = self.top.getTechList()
		unitList = self.top.getUnitList()
		unitCombatList = self.top.getUnitCategoryList()
		promotionList = self.top.getPromotionList()
		
		buildingList = self.top.getBuildingList()
		nationalWonderList = self.top.getNationalWonderList()
		worldWonderList = self.top.getWorldWonderList()
		projectList = self.top.getProjectList()
		specialistList = self.top.getSpecialistList()
		
		terrainList = self.top.getTerrainList()
		featureList = self.top.getFeatureList()
		bonusList = self.top.getBonusList()
		improvementList = self.top.getImprovementList()
		
		civList = self.top.getCivilizationList()
		leaderList = self.top.getLeaderList()
		traitList = self.top.getTraitList()
		
		civicList = self.top.getCivicList()
		religionList = self.top.getReligionList()
		corporationList = self.top.getCorporationList()
		
		conceptList = self.top.getConceptList()
		newConceptList = self.top.getNewConceptList()
		# <!-- custom: add Builds to index, inspired by Middle-earth mod's PlatyPedia approach (Claude Opus 4.5) -->
		buildList = self.top.getBuildList()
		
		list=[]
		for item in techList:
			if (item[0][0:4]=="The "):
				list.append([item[0][4:]+","+item[0][0:3],"Tech",item])
			else:
				list.append([item[0],"Tech",item])
		for item in unitList:
			if (item[0][:13]=="TXT_KEY_UNIT_"):
				list.append([item[0][13:].capitalize(),"Unit",item])
			else:
				list.append([item[0],"Unit",item])
		for item in unitCombatList:
			list.append([item[0],"UnitCombat",item])
		for item in promotionList:
			if (item[0][:18]=="TXT_KEY_PROMOTION_"):
				list.append([item[0][18:].capitalize(),"Promo",item])
			else:
				list.append([item[0],"Promo",item])
		
		for item in buildingList:
			if (item[0][:17]=="TXT_KEY_BUILDING_"):
				list.append([item[0][17:].capitalize(),"Building",item])
			else:
				list.append([item[0],"Building",item])
		for item in nationalWonderList:
			if (item[0][0:4]=="The "):
				list.append([item[0][4:]+","+item[0][0:3],"Wonder",item])
			elif (item[0][:17]=="TXT_KEY_BUILDING_"):
				list.append([item[0][17:].capitalize(),"Wonder",item])
			else:
				list.append([item[0],"Wonder",item])
		for item in worldWonderList:
			if (item[0][0:4]=="The "):
				list.append([item[0][4:]+","+item[0][0:3],"Wonder",item])
			elif (item[0][:17]=="TXT_KEY_BUILDING_"):
				list.append([item[0][17:].capitalize(),"Wonder",item])
			else:
				list.append([item[0],"Wonder",item])
		for item in projectList:
			if (item[0][0:4]=="The "):
				list.append([item[0][4:]+","+item[0][0:3],"Project",item])
			else:
				list.append([item[0],"Project",item])
		for item in specialistList:
			if (item[0][:19]=="TXT_KEY_SPECIALIST_"):
				list.append([item[0][19:].capitalize(),"Specialist",item])
			else:
				list.append([item[0],"Specialist",item])
		
		for item in terrainList:
			list.append([item[0],"Terrain",item])
		for item in featureList:
			list.append([item[0],"Feature",item])
		for item in bonusList:
			list.append([item[0],"Bonus",item])
		for item in improvementList:
			list.append([item[0],"Improv",item])
		
		for item in civList:
			list.append([item[0],"Civ",item])
		for item in leaderList:
			# <!-- custom: AdvCiv-SAS KI#111 - fail loudly on non-ascii leader names so we can identify the bad entry.
			# We documented this in AdvCiv-SAS (not NIF Gallery) even though the symptom matches; this is where we need the
			# explicit error to trace the root cause since AdvCiv-SAS did not show it yet. (GPT-5.2-Codex) -->
			name = item[0]
			if not isinstance(name, unicode):
				try:
					name.decode('ascii')
				except UnicodeDecodeError:
					raise Exception("SevoPediaIndex: non-ascii leader name in leaderList: %r (item=%r). Fix leader text or path case; see KI#111." % (name, item))
			list.append([item[0],"Leader",item])
		for item in traitList:
			list.append([item[0][2:],"Trait",item])
		
		for item in religionList:
			list.append([item[0],"Religion",item])
		for item in civicList:
			if (item[0][:14]=="TXT_KEY_CIVIC_"):
				list.append([item[0][14:].capitalize(),"Civic",item])
			else:
				list.append([item[0],"Civic",item])
		
		for item in conceptList:
			list.append([item[0],"Concept",item])
		for item in newConceptList:
			list.append([item[0],"NewConcept",item])
		# <!-- custom: add Builds to index (Claude Opus 4.5) -->
		for item in buildList:
			list.append([item[0],"Build",item])

		# <!-- custom: tentative UnicodeDecodeError fix: normalize index labels to unicode before sorting/filtering so Python 2.4 does not implicitly ascii-decode non-ASCII entries; keep strict context in errors if decoding still fails. (GPT-5.3-Codex) -->
		for iEntry in xrange(len(list)):
			list[iEntry][0] = self.SAS_asUnicode(list[iEntry][0], list[iEntry][1])
		
		list.sort()
		self.index = list
		
	def placeIndex(self):
		screen = self.top.getScreen()
		CONCEPT_CHAR = gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar()
		
		if self.SAS_indexWidgetNames:
			for szWidget in self.SAS_indexWidgetNames:
				try:
					screen.deleteWidget(szWidget)
				except:
					pass
			self.SAS_indexWidgetNames = []
		
		# <!-- custom: draw the shared top-header search bar from SevoPediaMain, and register this
		# method as the active refresher so Main's search handlers can invoke it on each keystroke
		# without needing any category-specific branching. (Claude code Opus 4.7) -->
		self.top.SAS_syncSearchPanel()
		self.top.SAS_activeListRefresher = self.placeIndex

		nColumns = 3
		self.tableName = self.top.getNextWidgetName()
		self.SAS_rowToBuild = {}
		self.SAS_rowToTrait = {}  # <!-- custom: row-to-trait mapping for WIDGET_PYTHON trait handling. (Claude Opus 4.5) -->
		self.iTableWidgetId = int(self.tableName.replace(self.top.WIDGET_ID, ""))
		# <!-- custom: search bar lives in the top header, so the Index table uses the full Y_INDEX
		# area below it. (Claude code Opus 4.7) -->
		iTableY = self.Y_INDEX
		iTableH = self.H_INDEX
		# <!-- custom: For Build entries, table selection is the only reliable click signal, so keep the table selectable and capture
		# row->Build mapping in handleInput. We previously tried overlay buttons, but they ignored table scrolling and desynced from rows.
		# Also, if the table doesn't have focus on first open, NOTIFY_CHARACTER goes nowhere and the search bar appears "dead" until
		# you navigate away and back. Setting focus here keeps search responsive and avoids the broken first-load behavior. Credit:
		# Claude Opus 4.5 + GPT-5.2-Codex. (GPT-5.2-Codex (summarized)) -->
		screen.addTableControlGFC(self.tableName, nColumns, self.X_INDEX, iTableY, self.W_INDEX, iTableH, True, True, self.LIST_BUTTON_SIZE, self.LIST_BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.tableName, True)
		screen.setFocus(self.tableName)
		self.SAS_indexWidgetNames.append(self.tableName)
		for i in range(nColumns):
			screen.setTableColumnHeader(self.tableName, i, "", (self.W_INDEX - 10) / nColumns)
		
		iRow = -1
		iColumn = 0
		sLetter = "#"
		iX = self.X_LETTER
		iLetterY = self.Y_INDEX
		self.letterTextIDs = {}
		# <!-- custom: note: while adding leaderhead art_def in AdvCiv-SAS-NIF-Gallery mod we saw the error "UnicodeDecodeError: 'ascii' codec can't decode byte 0xc8 in position 0" and in Sevopedia Leader, fixed by respecting path case sensitivity (e.g. "Art/LeaderHeads"). So reverted a previous patch that would workaround that: prefer to fail loudly instead and fix path or asset cause directly rather. See KI#111. (GPT-5.3-Codex) -->
		szFilter = self.top.SAS_szSearchString.strip().lower()
		bFilter = (len(szFilter) > 0)
		for name, type, item in self.index:
			if item[1] < 0:
				continue
			if bFilter and name.lower().find(szFilter) == -1:
				continue
			if (name[:1] != sLetter):
				sLetter = name[:1]
				screen.appendTableRow(self.tableName)
				iRow += 1
				screen.setTableText(self.tableName, 1, iRow, u"<font=4>- " + sLetter + u" -</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.appendTableRow(self.tableName)
				# create letter button
				textName = self.top.getNextWidgetName()
				letterText = u"<font=4>%s</font>" % sLetter
				screen.setText(textName, "Background", letterText, CvUtil.FONT_CENTER_JUSTIFY, 
						iX, iLetterY, 0, FontTypes.TITLE_FONT, 
						WidgetTypes.WIDGET_GENERAL, iRow, -1)
				self.letterTextIDs[textName] = iRow
				self.SAS_indexWidgetNames.append(textName)
				iX += self.W_LETTER
				iRow += 1
				iColumn = 0
			else:
				iColumn += 1
				if (iColumn >= nColumns):
					screen.appendTableRow(self.tableName)
					iRow += 1
					iColumn = 0
			
			# <!-- custom: refactor, since sText was defined in existing code, reuse it instead of hardcoding it again at each call if i may say and am not mistaken, this also fixes ruff warning and according to chatgpt this is unused as well and safe to remove as well so adding it again; similarly removed unused lines `sButton = ""` and `eWidget = None` and as for lines `iData1 = item[1]` and `iData2 = 1` also using them as variables similarly instead of hardcoding them each time -->
			sText = u"<font=3>" + item[0] + u"</font>"
			iData1 = item[1]
			iData2 = 1
			if (type == "Tech"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getTechInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Unit"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getUnitInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "UnitCombat"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getUnitCombatInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Promo"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getPromotionInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			
			elif (type == "Building"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getBuildingInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Wonder"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getBuildingInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Project"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getProjectInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Specialist"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getSpecialistInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			
			elif (type == "Terrain"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getTerrainInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Feature"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getFeatureInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Bonus"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getBonusInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Improv"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getImprovementInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			# <!-- custom: Build rows use the normal table cell (icon + text) and rely on table selection to trigger pediaJump.
			# This avoids overlay widgets that don't scroll with the table. Credit: Claude Opus 4.5 + GPT-5.2-Codex. (GPT-5.2-Codex (summarized)) -->
			elif (type == "Build"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getBuildInfo(iData1).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				self.SAS_rowToBuild[iRow] = iData1
			
			elif (type == "Civ"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getCivilizationInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Leader"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getLeaderHeadInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			# <!-- custom: Trait rows use WIDGET_GENERAL and row-to-trait mapping like Builds. (Claude Opus 4.5) -->
			elif (type == "Trait"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getTraitInfo(iData1).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				self.SAS_rowToTrait[iRow] = iData1
			
			elif (type == "Civic"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getCivicInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Religion"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getReligionInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			# <!-- custom: base AdvCiv bugfix GPT-5.2-Codex found thanks, was gc.getReligionInfo(iData1).getButton() -->
			elif (type == "Corporation"):
				screen.setTableText(self.tableName, iColumn, iRow, sText, gc.getCorporationInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			
			elif (type == "Concept"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>%c %s</font>" % (CONCEPT_CHAR, item[0]), gc.getConceptInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, iData1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "NewConcept"):
				# <!-- custom: AttributeError root cause note: after removing most Concept/NewConcept infos, this branch must use gc.getNewConceptInfo(iData1); using gc.getConceptInfo(iData1) can return None/wrong entry and then getButton crashes. (GPT-5.3-Codex) -->
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>%c %s</font>" % (CONCEPT_CHAR, item[0]), gc.getNewConceptInfo(iData1).getButton(), WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW, iData1, CvUtil.FONT_LEFT_JUSTIFY)
		
		self.iLastRow = iRow

	def handleInput (self, inputClass):
		BugUtil.debugInput(inputClass)
		# <!-- custom: search typing + CLEAR live in SevoPediaMain.handleInput; this method only
		# handles letter buttons and table-row clicks specific to the Index page. (Claude code Opus 4.7) -->
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED
				and inputClass.getFunctionName() + str(inputClass.getID()) in self.letterTextIDs):
			screen = self.top.getScreen()
			screen.selectRow(self.tableName, self.iLastRow, True)
			screen.selectRow(self.tableName, inputClass.getData1(), True)
			return 1
		
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED
				or inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if inputClass.getFunctionName() == self.top.WIDGET_ID and inputClass.getID() == self.iTableWidgetId:
				iRow = inputClass.getData()
				iBuild = self.SAS_rowToBuild.get(iRow, None)
				if iBuild is not None:
					return self.top.pediaJump(SevoScreenEnums.PEDIA_BUILDS, iBuild, True, False)
				# <!-- custom: Handle trait clicks via row mapping. (Claude Opus 4.5) -->
				iTrait = self.SAS_rowToTrait.get(iRow, None)
				if iTrait is not None:
					return self.top.pediaJump(SevoScreenEnums.PEDIA_TRAITS, iTrait, True, False)
		return 0

# -*- coding: UTF-8 -*-
# Generate new *.inp files from initial *.inp file
#******************************************************
# By Jiashu Yang
# Date: 2018-12-01
#******************************************************
def InpGenerater(IterNum):
	# import numpy as np
	#====================================================================================================
	#-----------------------------------------Basic Information------------------------------------------

	# IterNum = 1
	PartName = 'Part-2DLBeam'
	InstanceName = 'Instance-2DLBeam'
	EleName = 'CPS4R'

	#====================================================================================================
	#-------------------------------------Open and read *.inp file---------------------------------------

	FileName = 'Design.inp'      #Name of the *.inp file including the initial model 
	#Coding format: utf8
	#Changing coding format to avoid "UnicodeDecodeError".
	with open(FileName, mode = 'r', encoding = 'utf8') as InitialInp:       #Open file
	    InitialInpFile = InitialInp.readlines()
	# print(type(InitialInpFile))
	# print(len(InitialInpFile))
	#+++++++++++No Need+++++++++++
	# InitialInpFile = []
	# for line in InitialInpLine:  #Reading the file to a list
	#     InitialInpFile.append(line)
	# print(InitialInpFile == InitialInpLine)
	#+++++++++++No Need+++++++++++
	#====================================================================================================
	#---------------------------------Get IDs and coordinates of nodes-----------------------------------

	NodeStart = 0	                #Index of the line for the start of nodes information
	TargetStr1 = '*Node'
	for lines in InitialInpFile:
	    NodeStart += 1
	    NodeFlag = lines.find(TargetStr1)
	    if NodeFlag >= 0:
	        break	                #Exit loop if '*Node' found

	NodeID = []                     #A list for nodes IDs
	NodeCoord = [[]]
	for index in range((len(InitialInpFile[NodeStart].split())-2)):#Void list according to dimension of the model
	    NodeCoord.append([])

	for lines in InitialInpFile[NodeStart:]:
	    IDCoord = lines.split()
	    if IDCoord[0].strip(',').isdigit():                     #Node coordients started with an int in type 'str'
	        NodeID.append(int(IDCoord[0].strip(',')))           #Node ID
	        for coord in IDCoord[1:]:
	            NodeCoord[IDCoord.index(coord,1)-1].append(float(coord.strip(',')))   #Coordinates
	    else:
	        break

	#Only need to do for loop 0
	if IterNum == 0:
		# Save all node coordinates to file
		with open('NodesFull.dat', mode = 'w', encoding = 'utf-8') as NodeFull:
			for nd in NodeID:
				ndc = str(nd) + '\t'

				for nci in range(len(NodeCoord)):
					ndc = ndc + str(NodeCoord[nci][NodeID.index(nd)]) + '\t'

				NodeFull.write(ndc + '\n')

	# print(NodeCoord)

	#====================================================================================================
	#------------------------------Get IDs and connectivities of elements--------------------------------

	EleStart = 0	#Index of the line for the start of elements information
	TargetStr2 = '*Element'
	for lines in InitialInpFile:
	    EleStart += 1
	    EleFlag = lines.find(TargetStr2)
	    if EleFlag >= 0:
	        break

	EleID = []
	EleNodes = [[]]
	for index in range((len(InitialInpFile[EleStart].split())-2)):#Void list according to the number of nodes per element
	    EleNodes.append([])
	# print(EleNodes)

	for lines in InitialInpFile[EleStart:]:
	    IDConnec = lines.split()
	    if IDConnec[0].strip(',').isdigit():                    #Element connectivities started with an int in type 'str'
	        EleID.append(int(IDConnec[0].strip(',')))           #Element ID
	        for node in IDConnec[1:]:
	            #A trap for nodes may have the same ID with element.
	            #IDConnec.index(node) may lead to wrong result
	            #Replace IDConnec.index(node) with IDConnec.index(node,1) to escape the element ID
	            #By Jiashu Yang, 2018-11-30
	            EleNodes[IDConnec.index(node,1)-1].append(int(node.strip(',')))   #Node ID
	    else:
	        break

	# for ii in range(len(EleNodes)):
	#     print(EleNodes[ii])

	#Only need to do for loop 0
	if IterNum == 0:
		#Save all elements connectivity to file 
		with open('ElementsFull.dat', mode = 'w', encoding = 'utf-8') as ElementsFull:
			for ele in EleID:
				elec = str(ele) + '\t'

				for eleci in range(len(EleNodes)):
					elec = elec + str(EleNodes[eleci][EleID.index(ele)]) + '\t'

				ElementsFull.write(elec + '\n')

	#====================================================================================================
	#-------------------------------------Solid and void elements----------------------------------------

	if IterNum == 0:
		DV = [1.0] * len(EleNodes[0])        #Elastic modulus for each solid element
	else:
		#Read file generated from Matlab
		DVFileName = './DesignVariables/DV_Iter' + str(IterNum) + '.dat'
		with open(DVFileName, mode = 'r', encoding = 'utf8') as DesignVars:       #Open file
		    DVStr = DesignVars.readlines()

		DV = []
		for dv in DVStr:
			DV.append(float(dv.strip()))

	# SolidElement and Existed Nodes
	SolidElements = []
	NodeExisted = []

	kk = 0
	for ei in DV:
		if ei == 1:		#if element ei exist
			SolidElements.append(EleID[kk])
		kk += 1

	# print(len(EleNodes))
	for ni in NodeID:
		for nilist in EleNodes:
			# print(nilist)
			if ni in nilist:	#if node ni exist
				# print(ni)
				NodeExisted.append(ni)
				break
	# NodeExisted = NodeID.copy()
	# SolidElements = EleID.copy()

	##****************************No Need for SOFT KILL BESO******************************
	# #Save existed elements connectivity to file 
	# with open('ElementsSolid.dat', mode = 'w', encoding = 'utf-8') as ElementsS:
	# 	for ele in SolidElements:
	# 		elec = str(ele) + '\t'

	# 		for eleci in range(len(EleNodes)):
	# 			elec = elec + str(EleNodes[eleci][EleID.index(ele)]) + '\t'

	# 		ElementsS.write(elec + '\n')

	# # Save existed node coordinates to file
	# with open('NodesExisted.dat', mode = 'w', encoding = 'utf-8') as NodeE:
	# 	for nd in NodeExisted:
	# 		ndc = str(nd) + '\t'

	# 		for nci in range(len(NodeCoord)):
	# 			ndc = ndc + str(NodeCoord[nci][NodeID.index(nd)]) + '\t'

	# 		NodeE.write(ndc + '\n')
	##****************************No Need for SOFT KILL BESO******************************

	#====================================================================================================
	#--------------------------------Creat sets for each existed element---------------------------------

	# VoidElements = list(set(EleID).difference(SolidElements))       #Complement of the set of solid elements is the set of void elements

	EleSetName = []
	EleSetsCommands = []        #A list for sets creation commands
	for ele in SolidElements:
	    EleSetsCommandsTmp = []
	    EleSetNameTmp = 'Set-Ele_' + str(ele)
	    EleSetName.append(EleSetNameTmp)
	    EleSetsCommandsTmp.append('*Elset, elset = ' + EleSetNameTmp + ', generate\n')
	    EleSetsCommandsTmp.append(str(ele) + ', ' + str(ele) + ', ' + '1\n')
	    EleSetsCommands.extend(EleSetsCommandsTmp)
	# print(len(EleSetsCommands))
	# print(EleSetsCommands[0:2])

	#====================================================================================================
	#------------------------------Creat material for each existed element-------------------------------

	ElModuEle = [1.0] * len(SolidElements)
	PossRatioEle = [0.3] * len(SolidElements)      #Possion ratio for each solid element
	EleMatCommands = [
	'**\n', 
	'** MATERIALS\n',
	'**\n'
	]                                               #A list for material creation commands
	EleMatName = []
	for ele in SolidElements:
	    EleMatCommandsTmp = []
	    EleMatNameTmp = 'Material_Ele_' + str(ele)
	    EleMatName.append(EleMatNameTmp)
	    EleMatCommandsTmp.append('*Material, name = ' + EleMatNameTmp + '\n')
	    EleMatCommandsTmp.append('*Elastic\n')
	    EleMatCommandsTmp.append(str(ElModuEle[SolidElements.index(ele)]) + ', ' + str(PossRatioEle[SolidElements.index(ele)]) + '\n')
	    EleMatCommands.extend(EleMatCommandsTmp)

	# print(len(EleMatCommands))
	# print(EleMatCommands[0:3])


	#====================================================================================================
	#------------------------------Creat Sections for each existed element-------------------------------

	EleSecCommands = []        #A list for section creation commands
	for ele in SolidElements:
	    EleSecCommandsTmp = []
	    EleSecCommandsTmp.append('*Solid Section, elset = ' + EleSetName[SolidElements.index(ele)] + ', material = ' + EleMatName[SolidElements.index(ele)] + '\n')
	    EleSecCommandsTmp.append(',\n')
	    EleSecCommands.extend(EleSecCommandsTmp)
	# print(len(EleSecCommands))
	# print(EleSecCommands[0:2])

	#====================================================================================================
	#------------------------------------------Model information-----------------------------------------

	import time

	CurrTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

	HeadingInfoCommand = [
	'**\n',
	'*Heading\n',
	'** Job name: Job-Iter' + str(IterNum) + '\n',
	'** Model name: Model-Iter' + str(IterNum) + '\n',
	'** Generated by: Jiashu Yang',
	'** Time: ' + CurrTime + '\n',
	'** Analyzed by Abaqus 2017\n',
	'**\n'
	]

	#====================================================================================================
	#-------------------------------------------Abaqus Settings------------------------------------------

	AbaSettingCommand = [
	'**\n',
	'*Preprint, echo=NO, model=NO, history=NO, contact=NO\n',
	'**\n'
	]

	#====================================================================================================
	#-------------------------------------------Nodes information----------------------------------------

	NCommand = []
	for n in NodeExisted:
		NCommandTmp = str(n) + ', '
		for ii in range(len(NodeCoord)):
			NCommandTmp = NCommandTmp + str(NodeCoord[ii][NodeID.index(n)]) + ', '
			# print(NodeCoord[ii][NodeID.index(n)])
		#++++++++++++++Error Code+++++++++++++++++
	        # for co in NodeCoord[NodeID.index(n)]:
	        #     # print(NodeCoord[NodeID.index(n)])
	        #     NCommandTmp = NCommandTmp + str(co) + ', '
		#++++++++++++++Error Code+++++++++++++++++
		# NCommandTmp.rstrip(', ')
		NCommandTmp = NCommandTmp[:-2] + '\n'
		NCommand.append(NCommandTmp)
	# print(NCommand[0])

	#====================================================================================================
	#-----------------------------------------Elements information---------------------------------------

	ECommand = []
	for e in SolidElements:
		ECommandTmp = str(e) + ', '
		for ii in range(len(EleNodes)):
			ECommandTmp = ECommandTmp + str(EleNodes[ii][EleID.index(e)]) + ', '
		#++++++++++++++Error Code+++++++++++++++++
		# for n in EleNodes[EleID.index(e)]:
		#     ECommandTmp = ECommandTmp + str(n) + ', '
		#++++++++++++++Error Code+++++++++++++++++
		#ECommandTmp.rstrip(',')
	    #ECommandTmp = ECommandTmp.rstrip(', ')         #Why dosen't work here?
		ECommandTmp = ECommandTmp[:-2] + '\n'           #List slides don't include the last index and -1 refers to the last one
		ECommand.append(ECommandTmp)
	# print(ECommand[0])
	# print(len(ECommand))
	#====================================================================================================
	#-------------------------------------------Parts information----------------------------------------

	AbaPartCommand = [
	'**\n',
	'*Part, name = ' + PartName + '\n'
	]
	AbaNodeCommand = ['*Node\n']
	AbaEleCommand = ['*Element, type = ' + EleName + '\n']
	AbaPartCommand.extend(AbaNodeCommand)
	AbaPartCommand.extend(NCommand)
	AbaPartCommand.extend(AbaEleCommand)
	AbaPartCommand.extend(ECommand)
	AbaPartCommand.extend(EleSetsCommands)
	AbaPartCommand.extend(EleSecCommands)
	AbaPartCommand.extend(['*End Part\n'])

	#====================================================================================================
	#-----------------------------------------Assembly information---------------------------------------

	AbaAssemblyCommand = [
	'**\n',
	'** ASSEMBLY\n',
	'**\n',
	'*Assembly, name=Assembly\n',
	'**\n',
	'*Instance, name= ' + InstanceName +', part=' + PartName + '\n',
	'*End Instance\n',
	'**\n',
	'*Nset, nset=Nset-BoundaryCond, instance=' + InstanceName + '\n'
	]

	#Consider the situation that some of the node may be deleted from the model
	BCN1 = [7, 8, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276]
	BCN2 = [277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292]
	BCN3 = [ 293, 294, 295, 296, 297, 298, 299, 300, 301]

	AbaAssemblyCommand1 = []

	for ni in BCN1:
		if ni not in NodeExisted:	#if node ni do not exist
			BCN1.remove(ni)
			break
	BCN1C = ''
	for ni in BCN1:
		BCN1C = BCN1C + str(ni) + ', '
	BCN1C = BCN1C[:-2] + '\n'
	if len(BCN1) != 0:
		AbaAssemblyCommand1.extend(BCN1C)

	for ni in BCN2:
		if ni not in NodeExisted:	#if node ni do not exist
			BCN2.remove(ni)
			break
	BCN2C = ''
	for ni in BCN2:
		BCN2C = BCN2C + str(ni) + ', '
	BCN2C = BCN2C[:-2] + '\n'
	if len(BCN2) != 0:
		AbaAssemblyCommand1.extend(BCN2C)

	for ni in BCN3:
		if ni not in NodeExisted:	#if node ni exist
			BCN3.remove(ni)
			break
	BCN3C = ''
	for ni in BCN3:
		BCN3C = BCN3C + str(ni) + ', '
	BCN3C = BCN3C[:-2] + '\n'
	if len(BCN3) != 0:
		AbaAssemblyCommand1.extend(BCN3C)

	# '   7,   8, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276\n',
	# ' 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292\n',
	# ' 293, 294, 295, 296, 297, 298, 299, 300, 301\n',

	AbaAssemblyCommand2 = [
	'*Nset, nset=NSet-ConcentrateForce,instance=' + InstanceName + '\n',
	' 4,\n',
	'*End Assembly\n',
	'**\n'
	]
	AbaAssemblyCommand.extend(AbaAssemblyCommand1)
	AbaAssemblyCommand.extend(AbaAssemblyCommand2)
	#====================================================================================================
	#-------------------------------------------Boundary Condition----------------------------------------

	AbaBCCommand = [
	'**\n',
	'** BOUNDARY CONDITIONS\n',
	'**\n',
	'** Name: BC-1 Type: Displacement/Rotation\n',
	'*Boundary\n',
	'Nset-BoundaryCond, 1, 1\n',
	'Nset-BoundaryCond, 2, 2\n',
	]

	#====================================================================================================
	#-------------------------------------------Load information-----------------------------------------

	AbaLoadCommand = [
	'**\n',
	'** LOADS\n',
	'**\n',
	'** Name: Load-1   Type: Concentrated force\n',
	'*Cload\n',
	'NSet-ConcentrateForce, 2, -1.\n',
	'**\n'
	]

	#====================================================================================================
	#--------------------------------------------Outputs request-----------------------------------------

	#Output including default sets and user defined sets
	AbaOutputCommand = [
	'**\n',
	'** OUTPUT REQUESTS\n',
	'**\n',
	'*Restart, write, frequency=0\n',
	'**\n',
	'** FIELD OUTPUT: SEDensity\n',
	'**\n',
	'*Output, field\n',
	'*Element Output, directions=YES\n',
	'ELEDEN,\n',
	'**\n',
	'** DEFAULT FIELD OUTPUT\n',
	'** FIELD OUTPUT: F-Output-1\n',
	'**\n',
	'*Output, field, variable=PRESELECT\n',
	'**\n',
	'** HISTORY OUTPUT: ExtWork\n',
	'**\n',
	'*Output, history\n',
	'*Energy Output\n',
	'ALLWK,\n',
	'**\n',
	'** DEFAULT HISTORY OUTPUT\n',
	'** HISTORY OUTPUT: H-Output-1\n',
	'**\n',
	'*Output, history, variable=PRESELECT\n',
	]

	#====================================================================================================
	#-------------------------------------------Step information-----------------------------------------

	#Step information including Step, Load and Output
	AbaStepCommand = [
	'**\n',
	'** STEP: Step-1\n',
	'**\n',
	'*Step, name=Step-1, nlgeom=NO\n',
	'*Static\n',
	'1., 1., 1e-05, 1.\n'
	]
	AbaStepCommand.extend(AbaLoadCommand)
	AbaStepCommand.extend(AbaOutputCommand)
	AbaStepCommand.append('*End Step\n')

	#====================================================================================================
	#----------------------------------------------Input Files-------------------------------------------

	#Assemble all the commands togather
	AbaInpFile = []
	AbaInpFile.extend(HeadingInfoCommand)
	AbaInpFile.extend(AbaSettingCommand)
	AbaInpFile.extend(AbaPartCommand)
	AbaInpFile.extend(AbaAssemblyCommand)
	AbaInpFile.extend(EleMatCommands)
	AbaInpFile.extend(AbaBCCommand)
	AbaInpFile.extend(AbaStepCommand)

	InpName = 'Job-Iter' + str(IterNum) + '.inp'            #Name of new *.inp file
	with open(InpName, mode = 'w', encoding = 'utf8') as NewInp:    #Write commands to new inp file
	    NewInp.writelines(AbaInpFile)

if __name__ == '__main__':
	with open('IterNum.dat', mode = 'rb+') as IN:    #Get iteration numbers from file
		IterNumLisStr = IN.readlines()

	IterNumStr = IterNumLisStr[0]
	IterNum = int(float(IterNumStr))
	InpGenerater(IterNum)
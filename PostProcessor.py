# -*- coding: UTF-8 -*-
# To creat set in *.odb files for reslut display
#************************************************************
# By J S Yang
# Date: 2018-12-04
#************************************************************

#Labrary import
from abaqus import *
from abaqusConstants import *
from odbAccess import *
import io
import os
from caeModules import *
from driverUtils import executeOnCaeStartup

# Function PostProc
def PostProc(IterNum):
	#Output data base
	OdbName = 'Job-Iter' + str(IterNum) + '.odb'
	Odb = openOdb(OdbName)
	Assembly = Odb.rootAssembly
	Instance = Assembly.instances['INSTANCE-2DLBEAM']
	Elem = Instance.elements
	
	# #Read design variables
	# DVFileName = './DesignVariables/DV_Iter' + str(IterNum) + '.dat'
	# # DVFileName = 'DV_Iter' + str(IterNum) + '.dat'
	# with io.open(DVFileName, mode = 'r', encoding = 'utf8') as DesignVars:       #Open file
	# 	DVStr = DesignVars.readlines()
	# #Convert from 'str' to 'float'
	# DV = []
	# for dv in DVStr:
	# 	DV.append(float(dv.strip()))

	# #Creat list for solid and void elements
	# VEID = []
	# SEID = []
	# for ii in range(len(DV)):
	# 	# if DV[ii] == 1.0:
	# 	SEID.append(ii + 1)
		# else:
		# 	VEID.append(ii + 1)

	#Convert from list to tuple
	# TSEID = tuple(SEID)
	# TVEID = tuple(VEID)
	
	#Creat element sets for display
	# Instance.ElementSetFromElementLabels(name = 'SES', elementLabels = TSEID)
	# Instance.ElementSetFromElementLabels(name = 'VES', elementLabels = TVEID)
	
	#Display window
	session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=200, height=150)
	session.viewports['Viewport: 1'].makeCurrent()
	session.viewports['Viewport: 1'].maximize()
	
	#Set backgroud color to white
	session.graphicsOptions.setValues(backgroundColor = '#FFFFFF', backgroundStyle = SOLID)
	
	executeOnCaeStartup()
	
	#Display optimized structure
	session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=ON)
	# o1 = session.openOdb(name = OdbName)
	session.viewports['Viewport: 1'].setValues(displayedObject=Odb)
	#Remove void elements in viewpoint
	# leaf = dgo.LeafFromElementSets(elementSets=('INSTANCE-2DLBEAM.VES', ))
	# session.viewports['Viewport: 1'].odbDisplay.displayGroup.remove(leaf=leaf)
	session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triad=OFF, legend=OFF, title=OFF, state=OFF, annotations=OFF, compass=OFF)
	#Save graph to *.png file
	session.printOptions.setValues(reduceColors=False, vpDecorations=False)		#vpDecorations -> title or not
	FileName1 = 'TopOptRes' + str(IterNum)
	session.printToFile(fileName=FileName1, format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
	
	#Display von Mises stress field
	session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
	session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(contourStyle=CONTINUOUS)
	session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triad=OFF, title=OFF, state=OFF, annotations=OFF, compass=OFF)
	session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(legend=ON)
	session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(legendFont='-*-calibri-medium-r-normal-*-*-120-*-*-p-*-*-*')
	#session.viewports['Viewport: 1'].AnnotationOptions.setValues(state=False)
	#leaf = dgo.LeafFromElementSets(elementSets=('INSTANCE-2DLBEAM.VES', ))
	#session.viewports['Viewport: 1'].odbDisplay.displayGroup.add(leaf=leaf)
	#Save graph to *.png file
	session.printOptions.setValues(reduceColors=False, vpDecorations=False)
	FileName2 = 'TopOptStr' + str(IterNum)
	session.printToFile(fileName=FileName2, format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
	Odb.close()

# Main function
if __name__ == '__main__':
	TotalIterNum = len(os.listdir('./DesignVariables'))			#Total number of iterations
	for ii in range(TotalIterNum):
		PostProc(ii)
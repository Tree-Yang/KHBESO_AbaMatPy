#Define a function to get result from *.odb files
#******************************************************
# By J S Yang
# Date: 2018-12-02
#******************************************************

from odbAccess import *
from abaqusConstants import *
import io

def OdbReading(IterNum):
    #====================================================================================================
    #-----------------------------------------Basic Information------------------------------------------

    # IterNum = 1
    #File Names
    OdbFile = 'Job-Iter' + str(IterNum) + '.odb'
    EleElasEnerDenFile = 'EleElasEnerDen.dat'
    EleElasEnerDenFileO = 'EleElasEnerDenO.dat'
    ModelTotExtWorkFile = 'ModelTotExtWork.dat'

    #====================================================================================================
    #----------------------------------Element elastic energy density------------------------------------

    OutputDB = openOdb(OdbFile)
    OutputStep = OutputDB.steps['Step-1']
    OutputFrame = OutputStep.frames[-1]
    EleElasEnerDen = OutputFrame.fieldOutputs['ESEDEN'].values # Get elastic element energy desity
    if os.path.isfile(EleElasEnerDenFileO):
        os.remove(EleElasEnerDenFileO)
    if os.path.isfile(EleElasEnerDenFile):
        os.rename(EleElasEnerDenFile,EleElasEnerDenFileO)
    ##ATTENTION: Python 2.x is different from Python 3.x on files reading and writing
    with io.open(EleElasEnerDenFile, mode = 'wb+') as EsedenFile:    #Write element elsatic energy density into files
        for ee in EleElasEnerDen:
            EsedenFile.write(str(ee.elementLabel) + '\t' +str(ee.data) + '\n')

    #====================================================================================================
    #----------------------------------Total model external force work-----------------------------------

    OutputHistReg = OutputStep.historyRegions['Assembly ASSEMBLY']
    ModelTotExtWork = OutputHistReg.historyOutputs['ALLWK'].data[-1][1]    #Total external work
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #Change to append mode
    # with io.open(ModelTotExtWorkFile, mode = 'wb+') as AllwkFile:    #Write element elsatic energy density into files
    #     AllwkFile.write(str(ModelTotExtWork) + '\n')
    with io.open(ModelTotExtWorkFile, mode = 'ab+') as AllwkFile:    #Write element elsatic energy density into files
        AllwkFile.write(str(ModelTotExtWork) + '\n')
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Main function
if __name__ == '__main__':
    with io.open('IterNum.dat', mode = 'rb+') as IN:    #Get iteration numbers from file
        IterNumLisStr = IN.readlines()
    IterNumStr = IterNumLisStr[0]
    IterNum = int(float(IterNumStr))
    OdbReading(IterNum)
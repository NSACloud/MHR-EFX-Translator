#Author: NSA Cloud
from os import fstat

from .gen_functions import textColors,raiseWarning,raiseError,getPaddingAmount,read_short,read_uint,read_int,read_uint64,read_float,read_ubyte,read_string,read_unicode_string,read_byte,write_uint,write_int,write_uint64,write_float,write_short,write_ubyte,write_string,write_unicode_string,write_byte

class SIZEDATA():
    def __init__(self):
        self.HEADER_SIZE = 48
        self.UNKN_PARAMETER_VALUE_SIZE = 24
        self.BONE_MURMUR_HASH_SIZE = 16
        self.FIELD_PARAMETER_VALUE_SIZE = 44
        self.PARENT_OPTION_RELATION_SIZE = 2
class EFXRHeader():
    def __init__(self):
        self.magic = 1920493157
        self.unkn0 = 0
        self.entryCount = 0
        self.entryLength = 0
        self.actionCount = 0
        self.fieldParameterCount = 0
        self.unknParameterCount = 0
        self.collisionEffectCount = 0
        self.collisionEffectLength = 0
        self.boneCount = 0
        self.parentOptionsEntryCount = 0
        self.unkn8 = 0
        
    def read(self,file):
        #print("Reading Header...")
        self.magic = read_uint(file)
        if self.magic != 1920493157:
            raiseError("File is not a supported efx file.")
        self.unkn0 = read_uint(file)
        self.entryCount = read_uint(file)
        self.entryLength = read_uint(file)
        self.actionCount = read_uint(file)
        self.fieldParameterCount = read_uint(file)
        self.unknParameterCount = read_uint(file)
        self.collisionEffectCount = read_uint(file)
        self.collisionEffectLength = read_uint(file)
        self.boneCount = read_uint(file)
        self.parentOptionsEntryCount = read_uint(file)
        self.unkn8 = read_uint(file)
        
    def write(self,file):
        write_uint(file, self.magic)
        write_uint(file, self.unkn0)
        write_uint(file, self.entryCount)
        write_uint(file, self.entryLength)
        write_uint(file, self.actionCount)
        write_uint(file, self.fieldParameterCount)
        write_uint(file, self.unknParameterCount)
        write_uint(file, self.collisionEffectCount)
        write_uint(file, self.collisionEffectLength)
        write_uint(file, self.boneCount)
        write_uint(file, self.parentOptionsEntryCount)
        write_uint(file, self.unkn8)

class EntryNames():
    def __init__(self):
        self.unknParameterNameList = []
        self.boneNameList = []
        self.actionNameList = []
        self.fieldParameterNameList = []
        self.efxNameList = []
        self.collisionEffectNameList = []
        
    def read(self,file,header):
        #print("Reading Entry Names...")
        self.unknParameterNameList = []
        for i in range(0,header.unknParameterCount):
            self.unknParameterNameList.append((read_string(file),read_unicode_string(file,readBufferSize=256)))

        self.boneNameList = []
        for i in range(0,header.boneCount):
            self.boneNameList.append((read_string(file),read_unicode_string(file,readBufferSize=256)))
        
        self.actionNameList = []
        for i in range(0,header.actionCount):
            self.actionNameList.append(read_string(file))
        
        self.fieldParameterNameList = []
        for i in range(0,header.fieldParameterCount):    
            self.fieldParameterNameList.append(read_string(file))
        
        self.efxNameList = []
        for i in range(0,header.entryCount):    
            self.efxNameList.append(read_string(file))
            
        self.collisionEffectNameList = []
        for i in range(0,header.collisionEffectCount):    
            self.collisionEffectNameList.append(read_string(file))
        
    def write(self,file):
        #print("Writing Entry Names...")
        for name in self.unknParameterNameList:     
            write_string(file,name[0])
            write_unicode_string(file,name[1])

        for name in self.boneNameList:     
            write_string(file,name[0])
            write_unicode_string(file,name[1])
        
        for name in self.actionNameList:     
            write_string(file,name)
        
        for name in self.fieldParameterNameList:     
            write_string(file,name)
            
        for name in self.efxNameList:     
            write_string(file,name)
        
        for name in self.collisionEffectNameList:     
            write_string(file,name)
    def calculateSize(self):
        entryLength = 0
        #Japanese characters can be several bytes,so strings are encoded to get length
        for name in self.unknParameterNameList:
            entryLength += len(name[0].encode("utf-8"))+1
            entryLength += len(name[1].encode("utf-16le"))+2
        for name in self.boneNameList:
            entryLength += len(name[0].encode("utf-8"))+1
            entryLength += len(name[1].encode("utf-16le"))+2
        for name in self.actionNameList:
            entryLength += len(name.encode("utf-8")) + 1
        for name in self.fieldParameterNameList:
            entryLength += len(name.encode("utf-8")) + 1
        for name in self.efxNameList:
            entryLength += len(name.encode("utf-8")) + 1
        for name in self.collisionEffectNameList:
            entryLength += len(name.encode("utf-8")) + 1
        return entryLength
class UnknParameterValue():
    def __init__(self):
        self.unkn0 = 0
        self.unkn1 = 0
        self.unkn2 = 0
        self.unkn3 = 0
        self.unkn4 = 0
        self.unkn5 = 0
        
    def read(self,file):
        self.unkn0 = read_uint(file)
        self.unkn1 = read_uint(file)
        self.unkn2 = read_uint(file)
        self.unkn3 = read_uint(file)
        self.unkn4 = read_uint(file)
        self.unkn5 = read_uint(file)
    
    def write(self,file):
        write_uint(file,self.unkn0)
        write_uint(file,self.unkn1)
        write_uint(file,self.unkn2)
        write_uint(file,self.unkn3)
        write_uint(file,self.unkn4)
        write_uint(file,self.unkn5)
        
class SubHeader():
    def __init__(self):
        self.unknParameterValueList = []
        self.boneMurmurHashList = []
        self.boneUsageIndexList = []
    def read(self,file,header):
        #print(file.tell())
        self.unknParameterValueList = []   
        for i in range(0,header.unknParameterCount):
            unknParameter = UnknParameterValue()
            unknParameter.read(file)
            self.unknParameterValueList.append(unknParameter)
        
        self.boneMurmurHashList = []
        for i in range(0,header.boneCount):
            self.boneMurmurHashList.append(read_uint64(file))
        
        self.boneUsageIndexList = []
        for i in range(0,header.parentOptionsEntryCount):
            self.boneUsageIndexList.append(read_short(file))
    def write(self,file):
        for parameter in self.unknParameterValueList:
            parameter.write(file)
        for boneHash in self.boneMurmurHashList:
            write_uint64(file,boneHash)
        for boneUsageIndex in self.boneUsageIndexList:
            write_short(file,boneUsageIndex)

class EFXAttribute():
    def __init__(self):
        self.itemType = 0
        self.unknSeqNum = 0
        self.itemStruct = None

    def read(self,file):
        #print(file.tell())
        self.itemType = read_uint(file)
        self.unknSeqNum = read_uint(file)
        self.itemStruct = getEFXItemStruct(self.itemType,"MHRiseSB")()
        self.itemStruct.read(file)

    def write(self,file):
        write_uint(file,self.itemType)
        write_uint(file,self.unknSeqNum)
        self.itemStruct.write(file)
        
class Action():
    def __init__(self):
        self.actionUnkn0 = 0
        self.actionUnkn1 = 0
        self.actionAttributeCount = 0
        self.actionAttributeList = []
        
    def read(self,file):
        #print(file.tell())
        self.actionUnkn0 = read_uint(file)
        self.actionUnkn1 = read_uint(file)
        self.actionAttributeCount = read_uint(file)
        self.actionAttributeList = []
        for i in range(0,self.actionAttributeCount):
            actionAttribute = EFXAttribute()
            actionAttribute.read(file)
            self.actionAttributeList.append(actionAttribute)
    def write(self,file):
        write_uint(file,self.actionUnkn0)
        write_uint(file,self.actionUnkn1)
        write_uint(file,self.actionAttributeCount)
        for actionAttribute in self.actionAttributeList:
            actionAttribute.write(file)

#class FieldParameterValue():#TODO

#class MainBody():#TODO

#class CollisionEffects():#TODO

#class EOF():#TODO

class EFXR():
    def __init__(self):
        self.header = EFXRHeader()
        self.entryNames = EntryNames()
        self.subheader = SubHeader()
        self.actionList = []
        self.fieldParameterValueList = []
        #self.mainBody = MainBody()#TODO
        self.collisionEffectList = []
        #self.eof = EOF()#TODO
        
        self.fileSize = 0#For reading only, set when initialized
    def read(self,file):
        startPos = file.tell()
        
        self.header.read(file)
        self.entryNames.read(file,self.header)
        self.subheader.read(file,self.header)
        for i in range(0,self.header.actionCount):
            action = Action()
            action.read(file)
            self.actionList.append(action)#TODO
        self.efxData = file.read(self.fileSize-(file.tell()-startPos))#TEMPORARY, skips parsing efx attributes. Read to end of file as bytes
        
        #print("end pos " + str(file.tell()))
        self.fieldParameterValueList = []
        for i in range(0,self.header.fieldParameterCount):
            #fieldParameterValue = FieldParameterValue()#TODO
            #self.fieldParameterValueList.append(fieldParameterValue.read(file))#TODO
            pass
        #self.mainBody = MainBody()#TODO
        #self.mainBody.read(file)
        self.collisionEffectList = []
        for i in range(0,self.header.collisionEffectCount):
            #collisionEffect = CollisionEffect()#TODO
            #self.collisionEffectsList.append(collisionEffect.read(file))#TODO
            pass
        #self.eof = EOF()#TODO
        #self.eof.read(file)#TODO
        
    def write(self,file):
        self.header.write(file)
        self.entryNames.write(file)
        self.subheader.write(file)
        for action in self.actionList:
            action.write(file)          
        
        for fieldParameterValue in self.fieldParameterValueList:
            #fieldParameterValue.write(file)#TODO
            pass
        #self.mainBody.write(file)
        for collisionEffect in self.collisionEffectList:
            #collisionEffect.write(file)#TODO
            pass
        #self.eof.write(file)#TODO
        file.write(self.efxData)#TEMPORARY
    def updateSizes(self):
        sizeData = SIZEDATA()
        #self.header.entryCount = len(self.mainBody.EFXEntryList)#TODO
        self.header.entryLength = self.entryNames.calculateSize()
        self.header.actionCount = len(self.actionList)
        #self.header.fieldParameterCount = len(self.fieldParameterValueList)#TODO
        self.header.unknParameterCount = len(self.subheader.unknParameterValueList)
        #self.header.collisionEffectCount = len(self.collisionEffectList)#TODO
        self.header.boneCount = len(self.subheader.boneMurmurHashList)
        #self.header.parentOptionsEntryCount = self.mainBody.getEFXBoneUsage()#TODO
        #self.unkn8 = 0#TODO
        
        #Making the assumption that actions wont be nested inside actions
        if self.header.actionCount == 0:
            self.fileSize = (sizeData.HEADER_SIZE +
                self.header.entryLength +
                self.header.unknParameterCount * sizeData.UNKN_PARAMETER_VALUE_SIZE +               
                self.header.boneCount * sizeData.BONE_MURMUR_HASH_SIZE +
                self.header.parentOptionsEntryCount*sizeData.PARENT_OPTION_RELATION_SIZE +
                len(self.efxData)#TEMPORARY
                #self.header.fieldParameterCount * sizeData.FIELD_PARAMETER_VALUE_SIZE +# Included in efxData
                #self.header.collisionEffectLength
                )
        for action in self.actionList:
            for actionAttribute in action.actionAttributeList:
                if type(actionAttribute.itemStruct) == "PlayEmitter":
                    actionAttribute.itemStruct.actionEFXR.updateSizes()
                    actionAttribute.itemStruct.fileSize = actionAttribute.itemStruct.actionEFXR.fileSize
def readEFXFile(filepath):
    file = open(filepath,"rb")
    mainEFXR = EFXR()
    mainEFXR.fileSize = fstat(file.fileno()).st_size
    mainEFXR.read(file)
    file.close()
    return mainEFXR

def writeEFXFile(filepath,mainEFXR):
    mainEFXR.updateSizes()
    file = open(filepath,"wb")
    mainEFXR.write(file)
    file.close()
    #print("Wrote " + filepath)
    
from .re_efx_item import getEFXItemStruct
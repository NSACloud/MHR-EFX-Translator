#Author: NSA Cloud

#VERSION: V1

#REQUIRES translators package
#pip install translators

CACHEPATH = "translationCache.tsv"
FROM_LANGUAGE = "ja"#pick ja or auto
TO_LANGUAGE = "en"
#NOTE:New translation speed can likely be sped up exponentially by translating all new strings in a file at once in a single string and separating them with a delimiter symbol. Rather than the one string at a time system that the tool does now.
#However, all the translation is already done and cached, so I didn't see much need to implement it.


import time
start_time = time.time()

import os
import csv
import sys

from modules.gen_functions import textColors,raiseWarning,raiseError
from modules.file_re_efx import readEFXFile,writeEFXFile

#DEBUGPATH = "test"
def readTranslationCache(filepath):
    translationDict = {}
    if os.path.isfile(filepath):
        tsv_file = open(filepath,newline='',encoding='utf-8-sig')
        read_tsv = csv.reader(tsv_file, delimiter="\t")      
        next(read_tsv)#Skip header row
        for row in read_tsv:
            translationDict[row[0]] = row[1]
        tsv_file.close()
    return translationDict

"""#Writes translation cache as it runs,since it wouldn't save if it got stuck somewhere
def saveTranslationCache(filepath,translationDict):
    file = open(filepath,"w")
    file.write("JapaneseName\tEnglishName\n")
    for entry in translationDict.items():
        file.write(entry[0]+"\t"+entry[1]+"\n")
    file.close()
"""

def translateEFXDirectory(DIRPATH):
    import translators as ts
    successCount = 0
    translationDict = readTranslationCache(CACHEPATH);
    #print(translationDict)
    print("Read "+str(len(translationDict.items()))+" translations from cache.")
    
    print("Translating EFX files, this will take a while if new translations are being done.\nPress CTRL + C to cancel.\n")
    with open(CACHEPATH,"w",newline='',encoding='utf-8-sig') as cache:
        translationCache = csv.writer(cache,delimiter="\t")
        translationCache.writerow(["JapaneseName","EnglishName"])
        for entry in translationDict.items():
            #print(entry)
            translationCache.writerow([entry[0],entry[1]])
        for root, dirs, files in os.walk(DIRPATH):
            for file in files:
                if ".efx" in file:
                    try:
                        print("Translating "+file)
                        EFX = readEFXFile(os.path.join(root, file))
                        
                    except Exception as e:
                        print("Failed to read " + os.path.join(root, file)+" - " + str(e)+"\n")
                    
                    listSize = len(EFX.entryNames.efxNameList)
                    for index,efxName in enumerate(EFX.entryNames.efxNameList):
                        if translationDict.get(efxName,None) == None:
                            try:
                                print("\tTranslating EFX name "+str(index+1) +" of "+str(listSize))
                                translationDict[efxName] = ts.google(efxName,from_language=FROM_LANGUAGE,to_language=TO_LANGUAGE).replace(" ","_").replace("__","_").replace("__","_")
                                EFX.entryNames.efxNameList[index] = translationDict[efxName]
                                translationCache.writerow([str(efxName),str(translationDict[efxName])])
                                
                            except:
                                raiseWarning("Failed to translate efx name - " + str(index))
                            
                        else:
                            EFX.entryNames.efxNameList[index] = translationDict[efxName]
                        #print(efxName)
                        pass
                    listSize = len(EFX.entryNames.collisionEffectNameList)
                    for index,collisionEffectName in enumerate(EFX.entryNames.collisionEffectNameList):
                        if translationDict.get(collisionEffectName,None) == None:
                            try:
                                print("\tTranslating Collision Effect name "+str(index+1) +" of "+str(listSize))
                                translationDict[collisionEffectName] = ts.google(collisionEffectName,from_language=FROM_LANGUAGE,to_language=TO_LANGUAGE).replace(" ","_").replace("__","_").replace("__","_")
                                EFX.entryNames.collisionEffectNameList[index] = translationDict[collisionEffectName]
                                translationCache.writerow([str(collisionEffectName),str(translationDict[collisionEffectName])])
                            except:
                                raiseWarning("Failed to translate collision effect name - " + str(index))
                            
                        else:
                            EFX.entryNames.collisionEffectNameList[index] = translationDict[collisionEffectName]
                    #Translate internal actions
                    for actionIndex,action in enumerate(EFX.actionList):
                        print("\tTranslating Action "+str(actionIndex))
                        for actionAttribute in action.actionAttributeList:
                            if type(actionAttribute.itemStruct) == "PlayEmitter":
                                actionEFXR = actionAttribute.itemStruct.actionEFXR
                                listSize = len(actionEFXR.entryNames.efxNameList)
                                for index,efxName in enumerate(actionEFXR.entryNames.efxNameList):
                                    if translationDict.get(efxName,None) == None:
                                        try:
                                            print("\t\tTranslating EFX name "+str(index+1) +" of "+str(listSize))
                                            translationDict[efxName] = ts.google(efxName,from_language=FROM_LANGUAGE,to_language=TO_LANGUAGE).replace(" ","_").replace("__","_").replace("__","_")
                                            actionEFXR.entryNames.efxNameList[index] = translationDict[efxName]
                                            translationCache.writerow([str(efxName),str(translationDict[efxName])])
                                        except:
                                            raiseWarning("Failed to translate efx name - " + str(index))
                                        
                                    else:
                                        actionEFXR.entryNames.efxNameList[index] = translationDict[efxName]
                                    #print(efxName)
                                    pass
                                listSize = len(actionEFXR.entryNames.collisionEffectNameList)
                                for index,collisionEffectName in enumerate(actionEFXR.entryNames.collisionEffectNameList):
                                    if translationDict.get(collisionEffectName,None) == None:
                                        try:
                                            print("\t\tTranslating Collision Effect name "+str(index+1) +" of "+str(listSize))
                                            translationDict[collisionEffectName] = ts.google(collisionEffectName,from_language=FROM_LANGUAGE,to_language=TO_LANGUAGE).replace(" ","_").replace("__","_").replace("__","_")
                                            actionEFXR.entryNames.collisionEffectNameList[index] = translationDict[collisionEffectName]
                                            translationCache.writerow([str(collisionEffectName),str(translationDict[collisionEffectName])])
                                        except:
                                            raiseWarning("Failed to translate collision effect name - " + str(index))
                                        
                                    else:
                                        actionEFXR.entryNames.collisionEffectNameList[index] = translationDict[collisionEffectName]
                    
                    try:
                        os.makedirs(os.path.join("translatedEFX",os.path.relpath(root,start=os.path.dirname(DIRPATH))))
                    except:
                        pass
                    try:
                        writeEFXFile(os.path.join("translatedEFX",os.path.relpath(os.path.join(root,file),start=os.path.dirname(DIRPATH))), EFX)#Copy path as a relative path to the translatedEFX directory
                        successCount += 1
                    except Exception as e:
                        print("Failed to write " + os.path.join(root, file)+" - " + str(e)+"\n")
    """            
    try:
        saveTranslationCache(CACHEPATH, translationDict)
        print("Saved " +str(len(translationDict.items()))+" translations to cache.")
    except Exception as e:
        print("Failed to save translation cache " + CACHEPATH +" - " + str(e)+"\n")
    """
    print("\nTranslated " + str(successCount) + " files in %.2f seconds" % (time.time() - start_time))
    print("Saved translated EFX files to "+os.path.abspath("translatedEFX"))
#MAIN
if len(sys.argv) > 1:
    if os.path.isdir(sys.argv[1]):
        translateEFXDirectory(sys.argv[1])
        print("\nPress Enter to exit.")
        input()
    else:
        print("Drag a directory containing efx files to be translated onto the tool. All subdirectories will be searched.\nPress enter to exit.")
        input()
else:
    print("Drag a directory containing efx files to be translated onto the tool. All subdirectories will be searched.\nPress enter to exit.")
    input()
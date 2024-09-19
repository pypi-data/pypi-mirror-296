import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
import math
import sys
import numpy as np
import pdb
from perforatedai import globalsFile as gf
import os
import time
import warnings
from perforatedai import pb_layer as PB
from perforatedai import pb_models as PBM
from perforatedai import check_license
from perforatedai import cleanLoad as CL
from perforatedai import blockwisePB as BPB

def getPBModules(net, depth):
    #print('calling get params on %s, depth %d' % (type(net).__name__, depth))
    allMembers = net.__dir__()
    thisList = []
    if issubclass(type(net),nn.Sequential) or issubclass(type(net),nn.ModuleList):
        for submoduleID in range(len(net)):
            #if there is a self pointer ignore it
            if net[submoduleID] is net:
                continue
            if type(net[submoduleID]) is PB.pb_neuron_layer:
                thisList = thisList + [net[submoduleID]]

            else:
                #print('sub list not one so continuing')
                thisList = thisList + getPBModules(net[submoduleID], depth + 1)            
    else:
        for member in allMembers:        
            #if(type(net).__name__ == 'ConvModule'):
                #pdb.set_trace()
            if getattr(net,member,None) is net:
                continue
            if type(getattr(net,member,None)) is PB.pb_neuron_layer:
                #print('sub is one so converting')
                thisList = thisList + [getattr(net,member)]
                #print(thisList)            
            elif issubclass(type(getattr(net,member,None)),nn.Module):
                thisList = thisList + getPBModules(getattr(net,member), depth+1)
            #else:
                #print('not calling convert on %s depth %d' % (member, depth))            
            
    #print('finish depth %d' % depth)
    #print(thisList)
    return thisList 

def getPBModuleParams(net, depth):
    #print('calling get params on %s, depth %d' % (type(net).__name__, depth))
    allMembers = net.__dir__()
    thisList = []
    if issubclass(type(net),nn.Sequential) or issubclass(type(net),nn.ModuleList):
        for submoduleID in range(len(net)):
            if type(net[submoduleID]) is PB.pb_neuron_layer:
                #print('sub list is one so converting')
                for param in net[submoduleID].parameters():
                    if(param.requires_grad):
                        thisList = thisList + [param]
                #print(thisList)

            else:
                #print('sub list not one so continuing')
                thisList = thisList + getPBModuleParams(net[submoduleID], depth + 1)            
    else:
        for member in allMembers:        
            #if(type(net).__name__ == 'ConvModule'):
                #pdb.set_trace()
            if type(getattr(net,member,None)) is PB.pb_neuron_layer:
                #print('sub is one so converting')
                for param in getattr(net,member).parameters():
                    if(param.requires_grad):
                        thisList = thisList + [param]
                #print(thisList)            
            elif issubclass(type(getattr(net,member,None)),nn.Module):
                thisList = thisList + getPBModuleParams(getattr(net,member), depth+1)
            #else:
                #print('not calling convert on %s depth %d' % (member, depth))            
            
    #print('finish depth %d' % depth)
    #print(thisList)
    return thisList



def getPBNetworkParams(net):
    paramList = getPBModuleParams(net, 0)
    #pdb.set_trace()
    return paramList


def replacePredefinedModules(startModule,  pretrainedPB):
    index = gf.modulesToReplace.index(type(startModule))
    return gf.replacementModules[index](startModule)

def getPretrainedPBAttr(pretrainedPB, member):
    if(pretrainedPB is None):
        return None
    else:
        return getattr(pretrainedPB,member)

def getPretrainedPBVar(pretrainedPB, submoduleID):
    if(pretrainedPB is None):
        return None
    else:
        return pretrainedPB[submoduleID]


def convertModule(net,  pretrainedPB, depth, nameSoFar):
    if(gf.verbose):
        print('calling convert on %s depth %d' % (net, depth))
        print('calling convert on %s: %s, depth %d' % (nameSoFar, type(net).__name__, depth))
    if(type(net) is PB.pb_neuron_layer):
        if(gf.verbose):
            print('this is only being called because something in your model is pointed to twice by two different variables.  Highest thing on the list is one of the duplicates')
        return net
    allMembers = net.__dir__()
    if issubclass(type(net),nn.Sequential) or issubclass(type(net),nn.ModuleList):
        skipNextForBatch = False
        submoduleID = 0
        seqLen = len(net)
        while submoduleID < seqLen:
#            pdb.set_trace()
            if(skipNextForBatch):
                if(issubclass(type(net),PBM.SequentialWithExtra)):
                    #print('eliminating sequential %d' % submoduleID)
                    net = PBM.SequentialWithExtra(*[net[i] for i in range(len(net)) if i!=submoduleID])
                    seqLen -= 1
                    submoduleID += 1
                    skipNextForBatch = False
                    #pdb.set_trace()
                    continue
                elif(issubclass(type(net),nn.Sequential)):
                    #print('eliminating sequential %d' % submoduleID)
                    net = nn.Sequential(*[net[i] for i in range(len(net)) if i!=submoduleID])
                    seqLen -= 1
                    submoduleID += 1
                    skipNextForBatch = False
                    #pdb.set_trace()
                    continue
                else:
                    print('not setup for this')
#                    pdb.set_trace()
            skipNextForBatch = False
            if type(net[submoduleID]) in gf.modulesToReplace:
                if(gf.verbose):
                    print('Seq sub is in replacement module so replaceing: %s' % nameSoFar + '[' + str(submoduleID) + ']')
                net[submoduleID] = replacePredefinedModules(net[submoduleID],  getPretrainedPBVar(pretrainedPB, submoduleID))
            if (type(net[submoduleID]) in gf.modulesToConvert
                or
                type(net[submoduleID]).__name__ in gf.moduleNamesToConvert):
                if(gf.verbose):
                    print('Seq sub is in conversion list so initing PB for: %s' % nameSoFar + '[' + str(submoduleID) + ']')
                batchNorm = None
                if(submoduleID + 1 < len(net)) and (issubclass(type(net[submoduleID+1]), torch.nn.modules.batchnorm._BatchNorm) or issubclass(type(net[submoduleID+1]), torch.nn.modules.instancenorm._InstanceNorm) or
                issubclass(type(net[submoduleID+1]), torch.nn.modules.normalization.LayerNorm)):
                #and gf.internalBatchNorm:
                    print('Normilization warning for: ' + nameSoFar)
                    pdb.set_trace()
    
                net[submoduleID] = PB.pb_neuron_layer(net[submoduleID], nameSoFar + '[' + str(submoduleID) + ']', pretrainedPB=getPretrainedPBVar(pretrainedPB, submoduleID))
                if (issubclass(type(net[submoduleID]), torch.nn.modules.batchnorm._BatchNorm) or  
                    issubclass(type(net[submoduleID]), torch.nn.modules.instancenorm._InstanceNorm) or
                    issubclass(type(net[submoduleID]), torch.nn.modules.normalization.LayerNorm)):
                    #print('potentially found a batchNorm Layer that wont be convereted: %s' % (nameSoFar + '[' + str(submoduleID) + ']'))
                    pdb.set_trace()
            else:
                if(net != net[submoduleID]):
                    net[submoduleID] = convertModule(net[submoduleID],  getPretrainedPBVar(pretrainedPB, submoduleID), depth + 1, nameSoFar + '[' + str(submoduleID) + ']')            
                #else:
                    #print('%s is a self pointer so skipping' % (nameSoFar + '[' + str(submoduleID) + ']'))
            submoduleID += 1
    elif(type(net) in gf.modulestoSkip):
        #print('skipping type for returning from call to: %s' % (nameSoFar)) 
        return net
    else:
        for member in allMembers:        
            #if(type(net).__name__ == 'ConvModule'):
            if type(getattr(net,member,None)) in gf.modulesToReplace:
                if(gf.verbose):
                    print('sub is in replacement module so replaceing: %s' % nameSoFar + '.' + member)
                setattr(net,member,replacePredefinedModules(getattr(net,member,None),  getPretrainedPBAttr(pretrainedPB, member)))
            if (type(getattr(net,member,None)) in gf.modulesToConvert
                or
                type(getattr(net,member,None)).__name__ in gf.moduleNamesToConvert):
                if(gf.verbose):
                    print('sub is in conversion list so initing PB for: %s' % nameSoFar + '.' + member)
                setattr(net,member,PB.pb_neuron_layer(getattr(net,member),nameSoFar + '.' + member, pretrainedPB=getPretrainedPBAttr(pretrainedPB,member)))
            elif issubclass(type(getattr(net,member,None)),nn.Module):
                #pdb.set_trace()
                if(net != getattr(net,member)):
                    setattr(net,member,convertModule(getattr(net,member),  getPretrainedPBAttr(pretrainedPB,member), depth+1, nameSoFar + '.' + member))
                #else:
                    #print('%s is a self pointer so skipping' % (nameSoFar + '.' + member))

            if (issubclass(type(getattr(net,member,None)), torch.nn.modules.batchnorm._BatchNorm) or issubclass(type(getattr(net,member,None)), torch.nn.modules.instancenorm._InstanceNorm) or
                 issubclass(type(getattr(net,member,None)), torch.nn.modules.normalization.LayerNorm)):
                print('potentially found a batchNorm Layer that wont be convereted2: %s' % (nameSoFar + '.' + member))
                pdb.set_trace()
            else:
                if(gf.verbose):
                    print('not calling convert on %s depth %d' % (member, depth))            
    if(gf.verbose):
        print('returning from call to: %s' % (nameSoFar)) 
    #pdb.set_trace()
    return net


#putting pretrainedNormal, pretrainedPB as a flag here becqause might want to replace modules 
#pretraiend PB is required isntead of just loading in case a system needs to do any specific instantiation stuff
#that PB conflicts with and then convert network needs to be called after that is setup
#update later - i dont understand the above comment.  I think these were added when duplicating the main module rather than just adding it by reference. why would you ever want to load a pretrained PB but then convert something else?
def convertNetwork(net, pretrainedPB = None, layerName=''):

    license_file = './license.yaml'
    status = check_license.valid_license(license_file)

    if not status:
        print("License Invalid. Quiting...")
        exit(1)

    #if youre loading from a pretrained PB make sure to reset the tracker to be this ones, otherwise it will load the other ones 
    if(not pretrainedPB is None):
        gf.reInitPB = True
    if type(net) in gf.modulesToReplace:
        net = replacePredefinedModules(net,  pretrainedPB)
    if(type(net) in gf.modulesToConvert):
        if(layerName == ''):
            print('converting a single layer without a name, add a layerName param to the call')
            exit(-1)
        net = PB.pb_neuron_layer(net, layerName, pretrainedPB=pretrainedPB)
    else:
        net = convertModule(net,  pretrainedPB, 0, 'model')
    #pdb.set_trace()
    missedOnes = []
    for name, param in net.named_parameters():
        wrapped = 'wrapped' in param.__dir__()
        if(wrapped):
            if(gf.verbose):
                print('param %s is now wrapped' % (name))
        else:
            missedOnes.append(name)
    if(len(missedOnes) != 0):
        print('The following params are not wrapped or are wrapped as part of a larger module.\n------------------------------------------------------------------')
        for name in missedOnes:
            print(name)
        print('------------------------------------------------------------------\nPress enter to confirm you do not want them to be refined')
        input()
        print('confirmed')
    if(not pretrainedPB is None):
        for memberVar in pretrainedPB.memberVars:
            gf.pbTracker.memberVars[memberVar] = pretrainedPB.memberVars[memberVar]
    return net


def saveSystem(net, folder, name, dontSaveLocally = False):
    if(dontSaveLocally):
        folder = '/tmp/' + folder
    #else:
        #print('saving extra things function is for internal use only')
        #exit()
    if(gf.verbose):
        print('saving system %s' % name)
    net.memberVars = {}
    for memberVar in gf.pbTracker.memberVars:
        if memberVar == 'schedulerInstance' or memberVar == 'optimizerInstance':
            continue
        net.memberVars[memberVar] = gf.pbTracker.memberVars[memberVar]
    saveNet(net, folder, name, dontSaveLocally)

def loadSystem(folder, name, loadFromRestart = False, switchLoad = False):
    if(switchLoad):
        folder = '/tmp/' + folder
    if(gf.verbose):
        print('loading system %s' % name)
    net = loadNet(folder,name,loadFromRestart)
    for memberVar in net.memberVars:
        if memberVar == 'schedulerInstance' or memberVar == 'optimizerInstance':
            continue
        gf.pbTracker.memberVars[memberVar] = net.memberVars[memberVar]

    #always reset the timer, this should get rid of those epochs that take crazy long becuse they are using an old time
    gf.pbTracker.savedTime = time.time()
    
    gf.pbTracker.loaded=True
    #always reset this to 0 so networks will know if they are continuing to improve. dont need to reset running accuracy for this and dont 
    gf.pbTracker.memberVars['currentBestValidationScore'] = 0
    gf.pbTracker.memberVars['epochLastImproved'] = gf.pbTracker.memberVars['numEpochsRun']
    if(gf.verbose):
        print('after loading epoch last improved is %d mode is %c' % (gf.pbTracker.memberVars['epochLastImproved'], gf.pbTracker.memberVars['mode']))
    return net

    
def saveNet(net, folder, name, dontSaveLocally):
    #if(not dontSaveLocally or (not (folder[:5] == '/tmp/'))):
        #print('saving extra things function is for internal use only')
        #exit()
    #print('calling save: %s' % name)
    gf.pbTracker.archiveLayer()
    net.memberVars['numPBNeuronLayers'] = gf.pbTracker.memberVars['numPBNeuronLayers']
    if not os.path.isdir(folder):
        os.makedirs(folder)
    save_point = folder + '/'
    if not os.path.isdir(save_point):
        os.mkdir(save_point)
    oldList = gf.pbTracker.PBNeuronLayerVector
    gf.pbTracker.PBNeuronLayerVector = []
    net.pbTracker = gf.pbTracker
    torch.save(net, save_point + name + '.pt')
    #this is needed because archive taggers deletes everything because tagger objects cant be pickled
    gf.pbTracker.PBNeuronLayerVector = oldList
    gf.pbTracker.restoreTaggers()



#add a flag to ignore all warnings
def addFutureWarning():
    warnings.filters.insert(0,('ignore', None, Warning, None, 0))

#delete the warning we just set
def removeFutureWarning():
    del warnings.filters[0]
    
def loadNet(folder, name,loadFromRestart):
    #print('calling load % s' % name)
    save_point = folder + '/' 
    addFutureWarning()
    net = torch.load(save_point + name + '.pt', map_location=torch.device('cpu')) 
    removeFutureWarning()
    net.to(gf.device)
    gf.pbTracker = net.pbTracker
    gf.pbTracker.resetLayerVector(net,loadFromRestart)
    gf.pbTracker.memberVars['numPBNeuronLayers'] = net.memberVars['numPBNeuronLayers']
    #gf.pbTracker.doTempReinitializeThing()
    gf.pbTracker.restoreTaggers()
    
    return net


def paiSaveSystem(net, folder, name):
    folder = '/pai/'+folder
    #print('saving system %s' % name)
    net.memberVars = {}
    for memberVar in gf.pbTracker.memberVars:
        if memberVar == 'schedulerInstance' or memberVar == 'optimizerInstance':
            continue
        net.memberVars[memberVar] = gf.pbTracker.memberVars[memberVar]
    paiSaveNet(net, folder, name)

def deepCopyPAI(net):
    torch.save(net, './' + str(gf.pbTracker.startTime) + '_temp.pt')
    addFutureWarning()
    net = torch.load('./' + str(gf.pbTracker.startTime) + '_temp.pt', map_location='cpu')
    removeFutureWarning()
    os.remove('./' + str(gf.pbTracker.startTime) + '_temp.pt')
    return net

def paiSaveNet(net, folder, name):
    #print('calling save: %s' % name)
    #gf.pbTracker.archiveLayer()
    net = deepCopyPAI(net)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    save_point = folder + '/'
    if not os.path.isdir(save_point):
        os.mkdir(save_point)
    net = BPB.blockwiseNetwork(net)
    net = deepCopyPAI(net)
    net = CL.refreshNet(net)
    torch.save(net, save_point + name + '_pai.pt')

def changeLearningModes(net, folder, name, doingPB, switchLoad = False):
    
    if(doingPB == False):
        #do keep track of times it switched here so other things work out
        #this is so that if you set doingPB to be false it still does learning rate restart
        gf.pbTracker.memberVars['switchEpochs'].append(gf.pbTracker.memberVars['numEpochsRun'])
        gf.pbTracker.memberVars['lastSwitch'] = gf.pbTracker.memberVars['switchEpochs'][-1]
        gf.pbTracker.resetValsForScoreReset()
        return net
    if(gf.pbTracker.memberVars['mode'] == 'n'):
        print('Importing best Model for switch to PB...')
        currentEpoch = gf.pbTracker.memberVars['numEpochsRun']
        overWrittenEpochs = gf.pbTracker.memberVars['overWrittenEpochs']
        overWrittenExtra = gf.pbTracker.memberVars['extraScores']
        if(gf.drawingPB):
            overWrittenVal = gf.pbTracker.memberVars['accuracies']
        else:
            overWrittenVal = gf.pbTracker.memberVars['nAccuracies']
        preloadPBs = gf.pbTracker.memberVars['numPBNeuronLayers']
        net = loadSystem(folder, name, switchLoad=switchLoad)
        gf.pbTracker.setPBTraining()        
        gf.pbTracker.memberVars['overWrittenEpochs'] = overWrittenEpochs
        gf.pbTracker.memberVars['overWrittenEpochs'] += currentEpoch - gf.pbTracker.memberVars['numEpochsRun']
        gf.pbTracker.memberVars['totalEpochsRun'] = gf.pbTracker.memberVars['numEpochsRun'] + gf.pbTracker.memberVars['overWrittenEpochs']
        gf.pbTracker.memberVars['overWrittenExtras'].append(overWrittenExtra)
        gf.pbTracker.memberVars['overWrittenVals'].append(overWrittenVal)
        if(gf.drawingPB):
            gf.pbTracker.memberVars['nswitchEpochs'].append(gf.pbTracker.memberVars['numEpochsRun'])
        else:
            #append the last switch minus the length of this epoch set
            if(len(gf.pbTracker.memberVars['switchEpochs']) == 0):
                #add the first switch
                gf.pbTracker.memberVars['nswitchEpochs'].append(gf.pbTracker.memberVars['numEpochsRun'])
            else:
                #lastImprovedPoint = (len(self.memberVars['nAccuracies'])-1) - (self.memberVars['numEpochsRun']-self.memberVars['numEpochsRun'])
                gf.pbTracker.memberVars['nswitchEpochs'].append(gf.pbTracker.memberVars['nswitchEpochs'][-1] + ((gf.pbTracker.memberVars['numEpochsRun'])-(gf.pbTracker.memberVars['switchEpochs'][-1])))
            
        gf.pbTracker.memberVars['switchEpochs'].append(gf.pbTracker.memberVars['numEpochsRun'])
        gf.pbTracker.memberVars['lastSwitch'] = gf.pbTracker.memberVars['switchEpochs'][-1]
    else:
        print('Switching back to N...')
        setBest = gf.pbTracker.memberVars['currentNSetGlobalBest']
        gf.pbTracker.setNormalTraining()
        #append the last switch minus the length of this epoch set
        if(len(gf.pbTracker.memberVars['pswitchEpochs']) == 0):
            #need to account for the first one starting at 0
            gf.pbTracker.memberVars['pswitchEpochs'].append(((gf.pbTracker.memberVars['numEpochsRun']-1)-(gf.pbTracker.memberVars['switchEpochs'][-1])))
        else:
            gf.pbTracker.memberVars['pswitchEpochs'].append(gf.pbTracker.memberVars['pswitchEpochs'][-1] + ((gf.pbTracker.memberVars['numEpochsRun'])-(gf.pbTracker.memberVars['switchEpochs'][-1])))
        gf.pbTracker.memberVars['switchEpochs'].append(gf.pbTracker.memberVars['numEpochsRun'])
        gf.pbTracker.memberVars['lastSwitch'] = gf.pbTracker.memberVars['switchEpochs'][-1]
        #if want to retain all PB or learning PBLive and this last one did in fact improve global score
        if(gf.retainAllPB or (gf.learnPBLive and setBest)):
            print('Saving model before starting normal training to retain PBNodes regardless of next N Phase results')
            saveSystem(net, folder, name, switchLoad)
        #if its just doing P for learn PB live then switch back immdetealy
        if(gf.noExtraNModes):
            net = changeLearningModes(net, folder, name, doingPB)
            
    pytorch_total_params = sum(p.numel() for p in net.parameters())
    gf.pbTracker.memberVars['paramCounts'].append(pytorch_total_params)
    
    return net




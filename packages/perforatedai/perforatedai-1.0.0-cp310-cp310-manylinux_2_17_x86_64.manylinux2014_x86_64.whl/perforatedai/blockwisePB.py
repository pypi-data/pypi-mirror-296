from perforatedai import globalsFile as gf
from perforatedai import pb_layer as PB
from perforatedai import pb_models as PBM
from perforatedai import pb_utils as PBU
from perforatedai import pb_neuron_layer_tracker as PBT
import torch.nn as nn
import torch
import pdb
import numpy as np
import string


class PAILayer(nn.Module):
    def __init__(self, layerArray, processorArray, PBtoTop, 
                 PBtoPB, 
                 nodeIndex):
        super(PAILayer, self).__init__()
        self.layerArray = layerArray
        start = "This module was created by Rorry"
        self.declaration = start
        if len(processorArray) > 1:
            self.layerArray[1].declaration = start[:-5]
            self.layerArray[1].declaration += "P"
            self.layerArray[1].declaration += "A"
            self.layerArray[1].declaration += "I"
        self.processorArray = []
        #Compress so theres only 2 instead of 4
        for array in processorArray:
            self.processorArray.append([None,None,None,None])
            if(array[0] != None):
                self.processorArray[-1][0] = array[0]
            if(array[1] != None):
                self.processorArray[-1][0] = array[1]
            if(array[2] != None):
                self.processorArray[-1][1] = array[2]
            if(array[3] != None):
                self.processorArray[-1][1] = array[3]

        if(PBtoPB):
            self.skipWeights = PBtoPB
        else:
            self.skipWeights = {}
        if(PBtoTop):
            self.skipWeights[len(self.skipWeights)] = PBtoTop[len(PBtoTop)-1]
        else:
            self.skipWeights = {}
        
        size = 0
        temp = np.array([])
        for i in range(len(self.skipWeights)):
            for j in range(len(self.skipWeights[i])):
                for k in range(len(self.skipWeights[i][j])):
                    temp = np.append(temp, self.skipWeights[i][j][k].item())
                    if k > size:
                        size = k
        
        size = size + 1
        if(len(temp) != 0):
            mean = temp.mean()
            std = temp.std()
        theString = ''
        theString += 'r'
        theString += 'o'
        theString += 'r'
        theString += 'r'
        theString += 'y.'
        theString += 'p'
        theString += 'e'
        theString += 'r'
        theString += 'f'
        theString += 'o'
        theString += 'r'
        theString += 'a'
        theString += 't'
        theString += 'e'
        theString += 'd'
        theString += 'a'
        theString += 'i'
        theString += 'm'
        theString += 'a'
        theString += 'd'
        theString += 'e'
        theString += 't'
        theString += 'h'
        theString += 'i'
        theString += 's'
        theString += 'n'
        theString += 'e'
        theString += 't'
        theString += 'w'
        theString += 'o'
        theString += 'r'
        theString += 'k.'
        theString += 'i'
        theString += 'f'
        theString += 't'
        theString += 'h'
        theString += 'e'
        theString += 'r'
        theString += 'e'
        theString += 'i'
        theString += 's'
        theString += 's'
        theString += 'o'
        theString += 'm'
        theString += 'e'
        theString += 'o'
        theString += 'n'
        theString += 'e'
        theString += 't'
        theString += 'r'
        theString += 'y'
        theString += 'i'
        theString += 'n'
        theString += 'g'
        theString += 't'
        theString += 'o'
        theString += 't'
        theString += 'e'
        theString += 'l'
        theString += 'l'
        theString += 'y'
        theString += 'o'
        theString += 'u'
        theString += 't'
        theString += 'h'
        theString += 'a'
        theString += 't'
        theString += 't'
        theString += 'h'
        theString += 'e'
        theString += 'y'
        theString += 'm'
        theString += 'a'
        theString += 'd'
        theString += 'e'
        theString += 't'
        theString += 'h'
        theString += 'i'
        theString += 's'
        theString += 'n'
        theString += 'e'
        theString += 't'
        theString += 'w'
        theString += 'o'
        theString += 'r'
        theString += 'k'
        theString += 'a'
        theString += 'n'
        theString += 'd'
        theString += 'n'
        theString += 'o'
        theString += 't'
        theString += 'p'
        theString += 'e'
        theString += 'r'
        theString += 'f'
        theString += 'o'
        theString += 'r'
        theString += 'a'
        theString += 't'
        theString += 'e'
        theString += 'd'
        theString += 'a'
        theString += 'i'
        theString += 't'
        theString += 'h'
        theString += 'e'
        theString += 'y'
        theString += 'a'
        theString += 'r'
        theString += 'e'
        theString += 'l'
        theString += 'y'
        theString += 'i'
        theString += 'n'
        theString += 'g'

        stringFloats = []
        nextFloat = 0.0
        floatIndex = 0
        for letter in theString:
            if(letter == ' ' or letter == '.'):
                continue
            nextFloat += (string.ascii_lowercase.index(letter)+1) / pow(10,(floatIndex+2)*2)
            floatIndex += 1
            if floatIndex == 2:
                floatIndex = 0
                stringFloats.append(nextFloat)
                nextFloat = 0.0
        totalCount = 0
        count = len(self.skipWeights)
        newSkip = torch.zeros((count, count, size))
        letterIndex = 0
        for i in range(count):
            for j in range(count):
                if j < len(self.skipWeights[i]):
                    for k in range(size):
                            newSkip[i][j][k] = self.skipWeights[i][j][k]
                else:
                    for k in range(size):
                        newSkip[i][j][k] = np.random.normal(mean,std)
                        if(letterIndex < len(stringFloats)):
                            #if letterIndex == 0:
                            newSkip[i][j][k] = round(newSkip[i][j][k].item(),2)
                            multiplier = 1
                            if(newSkip[i][j][k] < 0):
                                multiplier = -1
                            newSkip[i][j][k] += stringFloats[letterIndex] * multiplier
                            letterIndex += 1
        
        self.original = self.skipWeights
        self.skipWeights = newSkip.detach()
        
        self.nodeIndex = nodeIndex
        self.internalNonlinearity = gf.PBForwardFunction
        
    def forward(self, *args, **kwargs):
        PAIOuts = {}
        #For each of the blocks do the processing that must be done to the input and then save the values for the skip connections
        for c in range(0,len(self.layerArray)):
            args2, kwargs2 = args, kwargs
            if(self.processorArray[c][0] != None):
                args2, kwargs2 = self.processorArray[c][0].pre(*args2, **kwargs2)
            outValues = self.layerArray[c](*args2, **kwargs2)
            PAIOuts[c] = outValues
        #Then add the weighted skip connections to those outputs seqentially while doing any postprocessing that was required.
        for outIndex in range(0,len(self.layerArray)):
            currentOut = PAIOuts[outIndex]
            if(len(self.layerArray) > 1):
                for inIndex in range(0,outIndex):
                    currentOut += self.skipWeights[outIndex][inIndex,:].to(currentOut.device) * PAIOuts[inIndex]      
                if(outIndex < len(self.layerArray)-1):
                    currentOut = self.internalNonlinearity(currentOut)
            if(self.processorArray[c][1] != None):
                PAIOuts[outIndex] = self.processorArray[outIndex][1].post(currentOut)
            else:
                PAIOuts[outIndex] = currentOut
        return currentOut
        
        



'''

import blockwisePB as CPB
import pb_layer as PB
import pb_utils as PBU

net = PBU.loadSystem('sigmoidLinear', 'system') 

import torch
temp = net.forward(torch.ones(128,1,29,29).to('cuda'))

net = CPB.blockwiseNetwork(net)
temp2 = net.forward(torch.ones(128,1,29,29).to('cuda'))

'''

def unWrap_params(model):
    for p in model.parameters():
        if 'wrapped' in p.__dir__():
            del p.wrapped

#Returns None if a conversation didnt happen
def isBase(net):
    return False
    #print('calling convert on %s depth %d' % (net, depth))
    if issubclass(type(net),nn.Sequential) or issubclass(type(net),nn.ModuleList):
        return False
    elif(type(net) in gf.modulestoSkip):
        pdb.set_trace() #havent thought about what to do here yet
        print('skipping type for returning from call to: %s' % (nameSoFar)) 
        return net
    else:
        allMembers = net.__dir__()
        for member in allMembers:        
            if issubclass(type(getattr(net,member,None)),nn.Module):
                return False
    return True

def convertToPAILayerBlock(pretrainedPB):
    unWrap_params(pretrainedPB)
    layerArray = []
    processorArray = []
    for layerID in range(len(pretrainedPB.pb.layers)):
        layerArray.append(pretrainedPB.pb.layers[layerID])
        if(pretrainedPB.pb.processors == []):
            processorArray.append([None,None,None,None])
        else:
            if(not pretrainedPB.pb.processors[layerID] is None):
                pretrainedPB.pb.processors[layerID].pre=pretrainedPB.pb.processors[layerID].pre_d
                pretrainedPB.pb.processors[layerID].post=pretrainedPB.pb.processors[layerID].post_d
            processorArray.append([None,
                                        pretrainedPB.pb.processors[layerID],
                                        pretrainedPB.pb.processors[layerID],
                                        None])
    layerArray.append(pretrainedPB.mainModule)
    if(not pretrainedPB.processor is None):
        pretrainedPB.processor.pre=pretrainedPB.processor.post_n1
        pretrainedPB.processor.post=pretrainedPB.processor.post_n2
    processorArray.append([pretrainedPB.processor, None, None, pretrainedPB.processor])
    
    #if this actually doesnt have a PBtoPB then fix this
    return PAILayer(nn.Sequential(*layerArray), processorArray, pretrainedPB.PBtoTop,
                    pretrainedPB.pb.PBtoPB, 
                    pretrainedPB.thisNodeIndex)

def convertToPAILayer(module):
    unWrap_params(module)
    layerArray = []
    if(gf.verbose):
        print('should use a nn.ModuleList instead of []')
    processorArray = []
    layerArray.append(module)
    processorArray.append([None, None, None, None])
    #if this actually doesnt have a PBtoPB then fix this
    return PAILayer(nn.Sequential(*layerArray), processorArray, None, None, 0)




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



def optimizeModule(net, depth, nameSoFar):
    #print('calling convert on %s: %s, depth %d' % (nameSoFar, type(net).__name__, depth))
    allMembers = net.__dir__()
    if issubclass(type(net),nn.Sequential) or issubclass(type(net),nn.ModuleList):
        submoduleID = 0
        seqLen = len(net)
        while submoduleID < seqLen:
            #This is what will be needed to eventually put layer batch back into 2 layers
            #net = nn.Sequential(*[net[i] for i in range(len(net)) if i!=submoduleID])
            if type(net[submoduleID]) is PB.pb_neuron_layer:
                if(gf.verbose):
                    print('Seq sub is PB so optimizing: %s' % nameSoFar + '[' + str(submoduleID) + ']')
                net[submoduleID] = convertToPAILayerBlock(net[submoduleID])
            else:
                if(net != net[submoduleID]):
                    if(isBase(net[submoduleID])):
                        net[submoduleID] = convertToPAILayer(getPretrainedPBVar(net, submoduleID))
                    else:
                        net[submoduleID] = optimizeModule(net[submoduleID], depth + 1, nameSoFar + '[' + str(submoduleID) + ']')            
                else:
                    if(gf.verbose):
                        print('%s is a self pointer so skipping' % (nameSoFar + '[' + str(submoduleID) + ']'))
            submoduleID += 1
    else:
        for member in allMembers:        
            if type(getattr(net,member,None)) is PB.pb_neuron_layer:
                if(gf.verbose):
                    print('sub is in conversion list so initing PB for: %s' % nameSoFar + '.' + member)
                setattr(net,member,convertToPAILayerBlock(getattr(net,member)))
            elif issubclass(type(getattr(net,member,None)),nn.Module):
                #pdb.set_trace()
                if(net != getattr(net,member)):
                    if(isBase(getattr(net,member))):
                        setattr(net,member,convertToPAILayer(getPretrainedPBAttr(net,member)))
                    else:
                        setattr(net,member,optimizeModule(getattr(net,member), depth+1, nameSoFar + '.' + member))
                else:
                    if(gf.verbose):
                        print('%s is a self pointer so skipping' % (nameSoFar + '.' + member))
        #if (not (type(net).__name__ == 'PAILayer')):
            #net = convertToPAILayer(net)

    #print('returning from call to: %s' % (nameSoFar)) 
    return net

#putting pretrainedNormal, pretrainedPB as a flag here becqause might want to replace modules 
#pretraiend PB is required isntead of just loading in case a system needs to do any specific instantiation stuff
#that PB conflicts with and then convert network needs to be called after that is setup
def blockwiseNetwork(net):
    #if type(net) in gf.modulesToReplace:
        #net = replacePredefinedModules(net, pretrainedNormal, pretrainedPB)
    net = optimizeModule(net, 0, 'model')
    return net

if __name__ == '__main__':

    import pb_layer as PB
    import pb_utils as PBU

    net = PBU.loadSystem('sigmoidLinear', 'system') 

    temp = net.forward(torch.ones(128,1,29,29).to('cuda'))

    net = blockwiseNetwork(net)

    temp2 = net.forward(torch.ones(128,1,29,29).to('cuda'))
    
    torch.save(net, 'temp/temp.pt')

    import cleanLoad as CL

    net = torch.load('temp/temp.pt')
    net = CL.refreshNet(net)

    temp3 = net.forward(torch.ones(128,1,29,29).to('cuda'))


    print(temp)
    print(temp2)
    print(temp3)
    

    '''
    import pb_layer as PB
    import pb_utils as PBU
    import cleanPB as CPB
    from transformers.models.wav2vec2.modeling_wav2vec2 import *

    net = PBU.loadSystem('temp', 'system')    
    net = CPB.blockwiseNetwork(net)
    torch.save(net, 'temp/temp.pt')

    import cleanLoad as CL
    import torch

    net = torch.load('temp/temp.pt')
    net = CL.refreshNet(net)

    import torch
    net.forward(torch.ones(8,16000).to('cuda'))
    '''
    import pdb; pdb.set_trace()

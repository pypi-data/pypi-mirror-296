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
from itertools import chain

from datetime import datetime
from perforatedai import pb_models as PBM
from perforatedai import pb_neuron_layer_tracker as PBT
from perforatedai import pb_utils as PBU
import copy


pretrainedPBLoadValues = ['out_channels', 'pbLayersAdded', 'PBtoTop', 'newestPBtoTop', 'mainModule', 'name']
pretrainedPBDendriteLoadValues = ['out_channels']

dendriteTensorValues = ['topPBCandidateAverage', 
                        'PrevPBCandidateCorrelation', 
                        'currentCorrelationsForParallel', 
                        'bestScore',
                        'previousBestScore',
                        'PrevPBCandidateAverage',
                        'mainGradAverageForScaling',
                        'candidateGradAverageForScaling',
                        'indexesOfbest',
                        'nodesBestImprovedThisEpoch',
                        'parentsAverageDvector',
                        #'parentsAverageDMags',
                        'normalPassAverageD',
                        #'normalPassAverageDMags',
                        #'normalPassAverageDSq'
                        ]
dendriteSingleValues = ['breaking',
                        'locked',
                        'bestScoreImprovedThisTimeStep',
                        'bestScoreImprovedThisEpoch',
                        #'parentsAverageDSq'
                        ]

#These are included above, they just get skipped for reinit if not live
nonLiveSkipValues = [   'normalPassAverageD',
                        #'normalPassAverageDMags',
                        #'normalPassAverageDSq'
                        ]    



if(gf.doingThing):
    dendriteSingleValues = dendriteSingleValues + ['normalPassMaxMeanAct', 'parentMaxMeanAct']
    nonLiveSkipValues = nonLiveSkipValues + ['normalPassMaxMeanAct']

dendriteInitValues = ['initialized',
                       'parallelBuffersInitialized',
                      'currentDInit']
#This is intentionally before adding the data parallel values which dont get zeroed at rinit
dendriteReinitValues = dendriteTensorValues + dendriteSingleValues
if(gf.usingPAIDataParallel):
    dendriteTensorValues.append('currentDSum')
    dendriteTensorValues.append('currentDMagsSum')
    #dendriteSingleValues.append('currentDSqSum')

dendriteSaveValues = dendriteTensorValues + dendriteSingleValues + dendriteInitValues

valueTrackerArrays = ['currentParentD', 'pbOuts']

    
def fakeCopy(net):
    
    torch.save(net, str(gf.pbTracker.startTime) + '_temp.pt')
    PBU.addFutureWarning()
    net = torch.load(str(gf.pbTracker.startTime) + '_temp.pt')
    PBU.removeFutureWarning()
    os.remove(str(gf.pbTracker.startTime) + '_temp.pt')
    return net


def filterForward(grad_out, Values, candidateNonlinearOuts):
    
    #This assumes that no matter what is happening you will always get batch_size, neurons, otherdims... as setup
    
    with torch.no_grad():
        val = grad_out.detach()
        if(not Values[0].currentDInit.item()):
            #make sure all dimensions are accounted for
            
            if(len(Values[0].thisInputDimensions) != len(grad_out.shape)):
                print('The following layer has not properly set thisInputDimensions')
                print(Values[0].layerName)
                print('it is expecting:')
                print(Values[0].thisInputDimensions)
                print('but recieved')
                print(grad_out.shape)
                if(not gf.debuggingInputDimensions):
                    exit(0)
                else:
                    gf.debuggingInputDimensions = 2
                    return


                #return
            #make sure the ones that should be fixed are correct
            for i in range(len(Values[0].thisInputDimensions)):
                if(Values[0].thisInputDimensions[i] == 0):
                    break
                if(not (grad_out.shape[i] == Values[0].thisInputDimensions[i])
                    and not Values[0].thisInputDimensions[i] == -1):
                    print('The following layer has not properly set thisInputDimensions with this incorrect shape')
                    print(Values[0].layerName)
                    print('it is expecting:')
                    print(Values[0].thisInputDimensions)
                    print('but recieved')
                    print(grad_out.shape)
                    if(not gf.debuggingInputDimensions):
                        exit(0)
                    else:
                        gf.debuggingInputDimensions = 2
                        return
                    #return
            
            with(torch.no_grad)():
                if(gf.verbose):
                    print('setting d shape for')
                    print(Values[0].layerName)
                
                Values[0].setOutChannels(val.size())
                Values[0].setupArrays(Values[0].out_channels)
            #why would we not want to set this for data parallel?
            #if(gf.usingPAIDataParallel == False):
            Values[0].currentDInit[0] = 1
        #self.currentD = val
        
        mathTuple = []
        viewTuple = []
        fullMult = 1
        for i in range(len(val.size())):
            if i == Values[0].thisNodeIndex:
                viewTuple.append(-1)
                continue
            fullMult *= val.shape[i]
            mathTuple.append(i)
            viewTuple.append(1)
        if(gf.pbTracker.memberVars['mode'] =='p'):
            for i in range(0,gf.globalCandidates):
                #this is where the grad_in is actually set for the tagger
                averageDMatrix = Values[i].parentsAverageDvector.view(viewTuple)
                if(gf.debuggingMemoryLeak and len(Values[i].currentParentD) != 0):
                    print('%s called backward but then didnt get PAIified.  This can cause a memory leak. Check processors.' % Values[i].layerName)
                if(len(candidateNonlinearOuts) == 0):
                    print('Trying to call backwards but module %s wasn\'t PAIified' % Values[i].layerName)
                    exit(0)
                Values[i].currentParentD.append((val - (averageDMatrix)).detach())
                candidateNonlinearOuts[i].register_hook(lambda grad: Values[i].currentParentD[-1])
                #pretty sure this next line is the right way to do this, not above.  doesnts eem to really have any significant impact though.  should run normal unit tests and xor_main with it to be sure.
                #Values[i].currentParentD = (val).detach()
                #candidateNonlinearOuts[i].register_hook(lambda grad: (Values[i].currentParentD  - (Values[i].parentsAverageDmatrix)))
        
        if(gf.usingPAIDataParallel):
            Values[0].currentDSum = val.sum(mathTuple) / fullMult
            Values[0].currentDMagsSum = val.abs().sum(mathTuple) / fullMult
            '''
            if(gf.gradSumFirst):
                Values[0].currentDSqSum = ((val)**2).sum(mathTuple) #if changing here change next
            else:
                Values[0].currentDSqSum = ((val)).sum(mathTuple)**2
            '''
        else:            
            Values[0].normalPassAverageD *= 0.99
            Values[0].normalPassAverageD += (val.sum(mathTuple) * 0.01) / fullMult
            #Values[0].normalPassAverageDMags *= 0.99
            #Values[0].normalPassAverageDMags += (val.abs().sum(mathTuple) * 0.01) / fullMult
            #Values[0].normalPassAverageDStd = Values[0].normalPassAverageDStd * 0.99 + val.std((mathTuple))*0.01

            #this is **2 after everything because it is a scalar to scale the final grad_in.  The final gradient that actually gets applied is gradient.sum(mathTuple)
            #final weight adjustment/actual grad value is net.module.mainModule[0].pbNeuronLayer.currentD.sum(mathTuple)
            #You can tell this by looking at the bias values in grad.  It will be similar for the convolution kernel weight values in grad
            '''
            Values[0].normalPassAverageDSq *= 0.99
            if(gf.gradSumFirst):
                Values[0].normalPassAverageDSq += ((val)**2).sum(mathTuple) * 0.01# / fullMult #if changing here change previous in dataparallel
            else:
                Values[0].normalPassAverageDSq += ((val)).sum(mathTuple)**2 * 0.01# / fullMult
            '''
                    
                #Values[0].currentDout = grad_output
            if(gf.learnPBLive):
                fullMult = 1
                viewTuple = []
                for dim in range(len(val.shape)):
                    if dim == Values[0].thisNodeIndex:
                        viewTuple.append(-1)
                        continue
                    fullMult *= val.shape[dim]
                    viewTuple.append(1)
                    
                #Keep these values updated on the fly  if this works, might only need to do mean, above and will stay the same and be faster.
                #Values[0].parentsAverageDMags.copy_(Values[0].normalPassAverageDMags.double().detach().clone()/(fullMult))
                Values[0].parentsAverageDvector.copy_(Values[0].normalPassAverageD.detach().clone()/(fullMult))
                #Values[0].parentsAverageDSq.copy_(Values[0].normalPassAverageDSq.double().mean().detach().clone())#/fullMult)

                Values[0].parentsAverageDvector.requires_grad = False
                #Values[0].parentsAverageDSq.requires_grad = False
                #Values[0].parentsAverageDMags.requires_grad = False


def setGrad_params(model, toSet):
    for p in model.parameters():
        p.requires_grad = toSet

def setWrapped_params(model):
    for p in model.parameters():
        p.wrapped = True


class pb_neuron_layer(nn.Module):
    
    def __init__(self, startModule, name, pretrainedPB=None):
        super(pb_neuron_layer, self).__init__()

        
        if(pretrainedPB is None):
            self.mainModule = startModule
            self.name = name
        else:
            self.mainModule = pretrainedPB.mainModule
            self.name = pretrainedPB.name
            
        setWrapped_params(self.mainModule)
        if(gf.verbose):
            print('initing a layer %s with main type %s' % (self.name, type(self.mainModule)))
            print(startModule)
        if(type(self.mainModule) in gf.modluesWithProcessing):
            moduleIndex = gf.modluesWithProcessing.index(type(self.mainModule))
            self.processor = gf.moduleProcessingClasses[moduleIndex]()
            if(gf.verbose):
                print('with processor')
                print(self.processor)
        elif(type(self.mainModule).__name__ in gf.moduleNamesWithProcessing):
            moduleIndex = gf.moduleNamesWithProcessing.index(type(self.mainModule).__name__)
            self.processor = gf.moduleByNameProcessingClasses[moduleIndex]()
            if(gf.verbose):
                print('with processor')
                print(self.processor)
        else:
            self.processor = None
            
        #TODO: used?
        self.handle = None
        if(gf.pbTracker == [] or gf.reInitPB):
            PBT.defaultInitPBTracker(True)
            gf.reInitPB = False
                
        self.randomPBtoCandidates = gf.defaultRandomPBtoCandidates
        self.activationFunctionValue = -1
        
        
        self.thisInputDimensions = gf.inputDimensions
        if(self.thisInputDimensions.count(0) != 1):
            print('5 Need exactly one 0 in the input dimensions: %s' % self.name)
            print(self.thisInputDimensions)
            exit(-1)
        self.thisNodeIndex = gf.inputDimensions.index(0)
        self.pbLayersAdded = 0
        #have to do it like this because .cat to make it bigger returns a variable instead of a parameter so it cant just keep being made bigger
        self.PBtoTop = {}
        self.register_parameter('newestPBtoTop', None)
        self.CandidatetoTop = {}
        self.register_parameter('currentCandidatetoTop', None)
        if(pretrainedPB is None):
            self.pb = pb_dendrite_layer(self.mainModule,
                                        pb_dropout_rate = gf.defaultPbDropout, 
                                        randomPBtoCandidates = self.randomPBtoCandidates,
                                        activationFunctionValue = self.activationFunctionValue,
                                        name = self.name)
        else:
            self.pb = pretrainedPB.pb
        if ((issubclass(type(startModule),nn.Linear) or #if this is a linear
            (issubclass(type(startModule),gf.PBSequential) and issubclass(type(startModule.model[0]),nn.Linear))) #or its layer batch with a linear
            and (np.array(self.thisInputDimensions)[2:] == -1).all()): #and everything past 2 is a negative 1
            self.setThisInputDimensions(self.thisInputDimensions[0:2])

        
        if(not pretrainedPB is None):
            self.loadFromPretrainedPB(pretrainedPB)
        gf.pbTracker.addPBNeuronLayer(self)        

    def __str__(self):
        self.printed = True
        real = False
        full = False
        if(gf.variableP == 1919):
            totalString = 'PAILayer(\n\t'
            totalString += self.mainModule.__str__().replace('\n','\n\t')
            totalString += '\n)'
        elif(real):
            totalString = 'PAILayer('
            totalString += self.mainModule.__class__.__name__
            totalString += ')'
        elif(full):
            return self.pb.__str__()
        else:
            totalString = self.mainModule.__str__()
            #if its using sub modules that can be replace just replace them
            if('Linear' in totalString or 
               'Conv1d' in totalString or 
               'Conv2d' in totalString or 
               'Conv3d' in totalString):
                totalString = totalString.replace('Linear','PAILayer(Linear')
                totalString = totalString.replace('Conv1d','PAILayer(Conv1d')
                totalString = totalString.replace('Conv2d','PAILayer(Conv2d')
                totalString = totalString.replace('Conv3d','PAILayer(Conv3d')
            #else its a more complicated thing so just acknowledge its been wrapped
            else:
                totalString = 'PAILayer(' + totalString + ')'
        return totalString
    def __repr__(self):
        return self.__str__()

    def loadFromPretrainedPB(self, pretrainedPB):
        for valueName in pretrainedPBLoadValues:
            setattr(self,valueName, getattr(pretrainedPB,valueName))
        self.pb.dendriteLoadFromPretrainedPB(pretrainedPB.pb)


    def setThisInputDimensions(self, newInputDimensions):
        self.thisInputDimensions = newInputDimensions
        if(newInputDimensions.count(0) != 1):
            print('6 need exactly one 0 in the input dimensions: %s' % self.name)
            print(newInputDimensions)
        self.thisNodeIndex = newInputDimensions.index(0)
        self.pb.setThisInputDimensions(newInputDimensions)

        

    def setMode(self, mode):
        if(gf.verbose):
            print('%s calling set mode %c' % (self.name, mode))
        if(mode == 'n'):
            self.pb.setMode(mode)
            if(self.pbLayersAdded > 0):
                if(gf.learnPBLive):
                    values = torch.cat((self.PBtoTop[self.pbLayersAdded-1],nn.Parameter(self.CandidatetoTop.detach().clone())),0)
                else:
                    values = torch.cat((self.PBtoTop[self.pbLayersAdded-1],nn.Parameter(torch.zeros((1,self.out_channels), device=self.PBtoTop[self.pbLayersAdded-1].device, dtype=gf.dType))),0)
                self.PBtoTop[self.pbLayersAdded] = nn.Parameter(values.detach().clone().to(gf.device), requires_grad=True)
                self.register_parameter('newestPBtoTop', self.PBtoTop[self.pbLayersAdded])
            else:
                if(gf.learnPBLive):
                    self.PBtoTop[0] = nn.Parameter(self.CandidatetoTop.detach().clone(), requires_grad=True)
                else:
                    self.PBtoTop[0] = nn.Parameter(torch.zeros((1,self.out_channels), device=gf.device, dtype=gf.dType).detach().clone(), requires_grad=True)
                self.register_parameter('newestPBtoTop', self.PBtoTop[self.pbLayersAdded])
            self.pbLayersAdded += 1
            setGrad_params(self.mainModule, True)
            #pbto top [x] is a nodesXPBlayers array, old one of one smaller is deleted and never used again
            if(self.pbLayersAdded > 0):
                self.PBtoTop[self.pbLayersAdded-1].requires_grad = True            
        else:
            #this gets set in n mode and isnt needed till first p mode so set here
            '''
            DEBUG: If you are getting here but out_channels has not been set
            A common reason is that this layer never had gradients flow through it.
            I have seen this happen because:
                The weights were frozen (requires_grad = False)
                something was added but not used. e.g. self.layer was then added to self.layerPB 
                    but forward is only called on layerPB.  in these cases remove self from the original
                
            '''
            try:
                self.out_channels = self.pb.pbValues[0].out_channels
                self.pb.out_channels = self.pb.pbValues[0].out_channels
            except Exception as e:
                #if this is happening just stop this layer from being converted and remove it from places that it should be
                print(e)
                print('this occured in layer: %s' % self.pb.pbValues[0].layerName)
                print('If you are getting here but out_channels has not been set')
                print('A common reason is that this layer never had gradients flow through it.')
                print('I have seen this happen because:')
                print('-The weights were frozen (requires_grad = False)')
                print('-A model is added but not used so it was convereted but never PB initialized')
                print('-A module was converted that doesn\'t have weights that get modified so backward doesnt flow through it')
                print('If this is normal behavior set gf.checkedSkippedLayers = True in the main to ignore')
                print('You can also set right now in this pdb terminal to have this not happen more after checking all layers this cycle.')
                if(not gf.checkedSkippedLayers):
                    import pdb; pdb.set_trace()
                return False
            #only change mode if it actually is learning and calculating grads
            self.pb.setMode(mode)
            if(gf.learnPBLive):
                self.CandidatetoTop = nn.Parameter(torch.zeros((1,self.out_channels), device=gf.device, dtype=gf.dType).detach().clone(), requires_grad=True)
                self.register_parameter('currentCandidatetoTop', self.CandidatetoTop)    
                
                #THIS SHOULDNT BE NEEDED BUT MESSED IT UP IN THIS RUN
                setGrad_params(self.mainModule, True)
                #pbto top [x] is a nodesXPBlayers array, old one of one smaller is deleted and never used again
                if(self.pbLayersAdded > 0):
                    self.PBtoTop[self.pbLayersAdded-1].requires_grad = True



            #set normal layers to no longer learn
            else:
                setGrad_params(self.mainModule, False)
                if(self.pbLayersAdded > 0):
                    self.PBtoTop[self.pbLayersAdded-1].requires_grad = False
        return True

        
    def addPBLayer(self):
        self.pb.addPBLayer()
    def addLoadedPBLayer(self):
        self.pb.addLoadedPBLayer()
    
    def loadTaggerValues(self):
        self.pb.loadTaggerValues()
    def addPBNodes(self, numberNodes):
        self.pb.in_channels = self.in_channels
        self.pb.out_channels = self.out_channels
        self.pb.stride = self.stride
        self.pb.padding = self.padding
        self.pb.kernel_size = self.kernel_size
        self.pb.addPBNodes(numberNodes)
            
    def forward(self, *args, **kwargs):
        if(gf.debuggingInputDimensions == 2):
            print('all input dim problems now printed')
            exit(0)
        out = self.mainModule(*args, **kwargs)
        if not self.processor is None:
            out = self.processor.post_n1(out)

        
        pbOuts, candidateOuts, candidateNonlinearOuts, candidateOutsNonZeroed = self.pb(*args, **kwargs)


        if(self.pbLayersAdded > 0):
            for i in range(0,self.pbLayersAdded):
                #Freemium thresholds at 1.0
                #self.PBtoTop[self.pbLayersAdded-1][i,:][self.PBtoTop[self.pbLayersAdded-1][i,:] > 1] = 1
                #self.PBtoTop[self.pbLayersAdded-1][i,:][self.PBtoTop[self.pbLayersAdded-1][i,:] < -1] = -1
                toTop = self.PBtoTop[self.pbLayersAdded-1][i,:]
                for dim in range(len(pbOuts[i].shape)):
                    if(dim == self.thisNodeIndex):
                        continue
                    toTop = toTop.unsqueeze(dim)
                if(gf.confirmCorrectSizes):
                    toTop = toTop.expand(list(pbOuts[i].size())[0:self.thisNodeIndex] + [self.out_channels] + list(pbOuts[i].size())[self.thisNodeIndex+1:])
                #PARALELL HACK TODO what does this mean?
                out = ( out + (pbOuts[i].to(out.device) * toTop.to(out.device)))
        
        #if pb is not in p mode it means this one isnt doing a grad
        if(gf.pbTracker.memberVars['mode'] == 'p' and self.pb.mode == 'p'):
            ## NEED LOOP HERE
            for i in range(0,gf.globalCandidates):
                if(gf.learnPBLive):
                    toTop = self.CandidatetoTop[i,:]
                    for dim in range(len(candidateOutsNonZeroed[i].shape)):
                        if(dim == self.thisNodeIndex):
                            continue
                        toTop = toTop.unsqueeze(dim)
                    if(gf.confirmCorrectSizes):
                        toTop = toTop.expand(list(candidateOutsNonZeroed[i].size())[0:self.thisNodeIndex] + [self.out_channels] + list(candidateOutsNonZeroed[i].size())[self.thisNodeIndex:])                    
                    out = ( out + (candidateOutsNonZeroed[i].to(out.device) * toTop.to(out.device)))
                        
                #also try this before the next out thing
                out = (out + candidateOuts[i].to(out.device))                 
        #POINT1    
        if(gf.pbTracker.memberVars['mode'] == 'n' and gf.doingThing):
            if(out.abs().max() > self.pb.pbValues[0].normalPassMaxMeanAct):
                self.pb.pbValues[0].normalPassMaxMeanAct[0] = out.abs().max().item()
                if(gf.learnPBLive):
                    self.pb.pbValues[0].parentMaxMeanAct.copy_(self.pb.pbValues[0].normalPassMaxMeanAct[0].detach().clone())
                    self.pb.pbValues[0].parentMaxMeanAct.requires_grad = False
            if(self.pb.pbValues[0].normalPassMaxMeanAct[0] == 0):
                print('An entire layer got exactly 0 Correlation')
                pdb.set_trace()

        #POINT2
        if(out.requires_grad):
            if candidateNonlinearOuts == {}:
                out.register_hook(lambda grad: filterForward(grad, self.pb.pbValues, {}))
            else:
                candidateNonlinearOuts[0] = candidateNonlinearOuts[0].to(out.device)
                out.register_hook(lambda grad: filterForward(grad, self.pb.pbValues, candidateNonlinearOuts))
        if not self.processor is None:
            out = self.processor.post_n2(out)
        return out
    
    def archiveLayer(self):
        self.pb.archiveLayer()


    

def init_params(model):
    for p in model.parameters():
        p.data=torch.randn(p.size())*.01#Random weight initialisation

class pb_dendrite_layer(nn.Module):
    def __init__(self, initialModule, pb_dropout_rate=0.0,  
                 #resNetLayer=False,
                 randomPBtoCandidates=False, activationFunctionValue=0.3, name='noNameGiven'):
        super(pb_dendrite_layer, self).__init__()
        
        if(pb_dropout_rate > 0.0000001):
            print('initing with dropout')
            self.doingDropout = True
            self.pb_dropout_rate = pb_dropout_rate
            self.pbDropoutLayers = nn.ModuleList([])
        else:
            self.doingDropout = False
        self.layers = nn.ModuleList([])
        self.processors = []
        self.numPBLayers = 0
        
        #default to n mode
        self.mode = 'n'
        
        #this is a flag for if the layer is already archived.  this will only happen if a network
        #has two pointers to the same layer but it sometimes does.
        self.archived = False
        
        self.name=name
        self.parentModule = initialModule
                            
        #base layer options
        self.currentRecurrentPassTensors = []
        self.currentRecurrentPassCandidateTensors = []
        
        self.thisInputDimensions = gf.inputDimensions
        if(self.thisInputDimensions.count(0) != 1):
            print('1 need exactly one 0 in the input dimensions: %s' % self.name)
            print(self.thisInputDimensions)
            exit(-1)
        self.thisNodeIndex = gf.inputDimensions.index(0)


        #self.resNetLayer = resNetLayer
        #PB VALUES
        #self.pbValues = nn.ModuleList([])
        self.normalLearningTaggers = {}
        #self.pbOuts = {}
        self.internalRecurrent = False

        self.bestWeights = {}
        self.bestBiases = {}
        self.bestBNWeights = {}
        self.bestBNBiases = {}
        self.PBtoCandidates = {}
        self.PBtoPB = {}
        self.addedTaggers = False
        self.randomPBtoCandidates = randomPBtoCandidates
        self.activationFunctionValue = activationFunctionValue
        self.pbValues = nn.ModuleList([])
        for j in range(0, gf.globalCandidates):
            if(gf.verbose):
                print('creating pb Values for %s' % (self.name))
            self.pbValues.append(pbValueTracker(False, self.activationFunctionValue, self.name, self.thisInputDimensions))

    def setThisInputDimensions(self, newInputDimensions):
        self.thisInputDimensions = newInputDimensions
        if(newInputDimensions.count(0) != 1):
            print('2 Need exactly one 0 in the input dimensions: %s' % self.name)
            print(newInputDimensions)
            exit(-1)
        self.thisNodeIndex = newInputDimensions.index(0)
        for j in range(0, gf.globalCandidates):
            self.pbValues[j].setThisInputDimensions(newInputDimensions)


    def setupSave(self):
        
        for valueName in dendriteSaveValues:
            setattr(self,valueName,{})
        for j in range(0, gf.globalCandidates):
            for valueName in dendriteSaveValues:
                getattr(self,valueName)[j] = getattr(self.pbValues[j],valueName)
                delattr(self.pbValues[j],valueName)
        
    def archiveLayer(self):
        if self.archived:
            #print('skipping archive %s' % self.name)
            return
        #print('calling archive %s' % self.name)
        if(self.addedTaggers):
            self.setupSave()
            del self.pbValues
        self.archived = True                



    def restoreTaggers(self):
        if not self.archived:
            #print('skipping restore %s' % self.name)
            return

        #print('calling restore Taggers %s' % self.name)
        if(self.addedTaggers == False):
            self.archived = False                
            return
        self.pbValues = nn.ModuleList([])
        for j in range(0, gf.globalCandidates):
            self.pbValues.append(pbValueTracker(self.initialized[j], self.activationFunctionValue, self.name, self.thisInputDimensions, self.out_channels))

            
            for valueName in dendriteSaveValues:
                setattr(self.pbValues[j],valueName, getattr(self,valueName)[j])
            self.pbValues[j].activationFunctionValue = self.activationFunctionValue
            
            
        #clear the temporary saved tensors
        for valueName in dendriteSaveValues:
            setattr(self,valueName,{})
        self.archived = False

    def dendriteLoadFromPretrainedPB(self, pretrainedPB):
        for j in range(0, gf.globalCandidates):
            for valueName in (dendriteSaveValues + pretrainedPBDendriteLoadValues):
                setattr(self.pbValues[j],valueName, getattr(pretrainedPB.pbValues[j],valueName))
            self.pbValues[j].activationFunctionValue = pretrainedPB.activationFunctionValue            

    def addPBLayer(self):
                
        self.candidateLayer = nn.ModuleList([])
        self.candidateBestLayer = nn.ModuleList([])
        if(gf.verbose):
            print(self.name)
            print('setting candidate processors')
        self.candidateProcessors = []
        with torch.no_grad():
            for i in range(0, gf.globalCandidates):
                
                newModule = fakeCopy(self.parentModule)
                init_params(newModule)
                setGrad_params(newModule, True)
                self.candidateLayer.append(newModule)
                self.candidateBestLayer.append(newModule)
                if(type(self.parentModule) in gf.modluesWithProcessing):
                    moduleIndex = gf.modluesWithProcessing.index(type(self.parentModule))
                    self.candidateProcessors.append(gf.moduleProcessingClasses[moduleIndex]())
                elif(type(self.parentModule).__name__ in gf.moduleNamesWithProcessing):
                    moduleIndex = gf.moduleNamesWithProcessing.index(type(self.parentModule).__name__)
                    self.candidateProcessors.append(gf.moduleByNameProcessingClasses[moduleIndex]())

                

        for i in range(0, gf.globalCandidates):
            self.candidateLayer[i].to(gf.device)
            self.candidateBestLayer[i].to(gf.device)
            

        #normalize AverageDSq?
        #normalPassAverageDSq = normalPassAverageDSq/((normalPassAverageDSq*normalPassAverageDSq).sum()).sqrt()
        # for i in range(0, self.out_channels):
        for j in range(0, gf.globalCandidates):
            self.pbValues[j].reinitializeForPB(0)
        
        self.addedTaggers = True
            
            

        if(self.numPBLayers > 0):
            for j in range(0,gf.globalCandidates): #Loopy Loops
                self.PBtoCandidates[j] = nn.Parameter(torch.zeros((self.numPBLayers, self.out_channels), device=gf.device, dtype=gf.dType), requires_grad=True)
                self.PBtoCandidates[j].data.pbWrapped = True
                if(self.randomPBtoCandidates):
                    with torch.no_grad():
                        self.PBtoCandidates[j].normal_(0, math.sqrt(2. / self.out_channels))
                self.register_parameter(('PBtoCandidates'+str(j)), self.PBtoCandidates[j])


 
    
        
    def setMode(self, mode):
        self.mode = mode
        if(gf.verbose):
            print('pb calling set mode %c' % mode)
        if(mode == 'n'):
            if(gf.verbose):
                print('so calling all the things to add to layers')
            for i in range(0,gf.globalCandidates):
                self.pbValues[i].locked[0] = 1
                
                
            if(self.doingDropout):
                self.pbDropoutLayers.append(nn.Dropout(p=self.pb_dropout_rate).to(gf.device))

            #copy weights/bias from correct candidates
            if(self.numPBLayers == 1):
                self.PBtoPB = {}
                self.PBtoPB[0] = []
            if(self.numPBLayers >= 1):
                self.PBtoPB[self.numPBLayers] = torch.zeros([self.numPBLayers,self.out_channels], requires_grad=False, device=gf.device, dtype=gf.dType)#NEW
            with torch.no_grad():
                if(gf.globalCandidates > 1):
                    print('This was a flag that will be needed if using multiple candidates.  It\s not set up yet but nice work finding it.')
                    pdb.set_trace()
                planeMaxIndex = 0
                self.layers.append(fakeCopy(self.candidateBestLayer[planeMaxIndex]))
                self.layers[self.numPBLayers].to(gf.device)
                if(self.numPBLayers > 0):
                    if(gf.verbose):
                        print('this maybe shuould have a clone and data')
                    self.PBtoPB[self.numPBLayers].copy_(self.PBtoCandidates[planeMaxIndex])
                if(type(self.parentModule) in gf.modluesWithProcessing):
                    self.processors.append(self.candidateProcessors[planeMaxIndex])
                if(type(self.parentModule).__name__ in gf.moduleNamesWithProcessing):
                    self.processors.append(self.candidateProcessors[planeMaxIndex])

            #set PB nodes to no longer learn
            
            setGrad_params(self.layers[self.numPBLayers], False)

            if(self.numPBLayers > 0):
                for j in range(0,gf.globalCandidates): #Loopy Loops
                    self.PBtoCandidates[j].requires_grad = False


            del self.candidateLayer, self.candidateBestLayer

            self.numPBLayers += 1
        
    def killerRecursive(self, inVals):
        if type(inVals) is list:
            if(len(inVals) == 0):
                return inVals, None
            for index in range(len(inVals)):
                inVals[index], device = self.killerRecursive(inVals[index])
        elif type(inVals) is tuple:
            if(len(inVals) == 0):
                return inVals, None
            for index in range(len(inVals)):
                inVals = list(inVals)
                inVals[index], device = self.killerRecursive(inVals[index])
                inVals = tuple(inVals)
        elif type(inVals) is dict:
            if(len(inVals.keys()) == 0):
                return inVals, None
            for index in inVals.keys():
                inVals[index], device = self.killerRecursive(inVals[index])
        elif issubclass(torch.Tensor, type(inVals)):
            with torch.cuda.device_of(inVals):
                toReturn = gradKiller(inVals).detach().clone()
                return toReturn, inVals.device
        else:
            return inVals, None
        return inVals, device

    def killerRecursiveOld(self, inVals):
        if type(inVals) is list:
            for index in range(len(inVals)):
                inVals[index] = self.killerRecursive(inVals[index])
        elif type(inVals) is tuple:
            for index in range(len(inVals)):
                inVals = list(inVals)
                inVals[index] = self.killerRecursive(inVals[index])
                inVals = tuple(inVals)
        elif type(inVals) is dict:
            for index in inVals.keys():
                inVals[index] = self.killerRecursive(inVals[index])
        elif issubclass(torch.Tensor, type(inVals)):
            return gradKiller(inVals).detach().clone()
        return inVals
        
    def forward(self, *args, **kwargs):
        outs = {}
            
        for c in range(0,self.numPBLayers):
            args2, device = self.killerRecursive(args)
            kwargs2, device2 = self.killerRecursive(kwargs)
            #args2, = self.killerRecursive(args)
            #kwargs2 = self.killerRecursive(kwargs)
            if(self.processors != []):
                args2, kwargs2 = self.processors[c].pre_d(*args2, **kwargs2)
            outValues = self.layers[c](*args2, **kwargs2)
            if(self.processors != []):
                outs[c] = self.processors[c].post_d(outValues)
            else:
                outs[c] = outValues




        for outIndex in range(0,self.numPBLayers):
            currentOut = outs[outIndex]
            viewTuple = []
            for dim in range(len(currentOut.shape)):
                if dim == self.thisNodeIndex:
                    viewTuple.append(-1)
                    continue
                viewTuple.append(1)

            for inIndex in range(0,outIndex):
                #PARALLEL HACK
                currentOut += self.PBtoPB[outIndex][inIndex,:].view(viewTuple).to(currentOut.device) * outs[inIndex]            
            currentOut.copy_( gf.PBForwardFunction(currentOut))
            if(self.doingDropout):
                for outIndex in range(0,self.numPBLayers):
                    currentOut.copy_( self.pbDropoutLayers[outIndex](currentOut))
        candidateOuts = {}
        candidateNonlinearOuts = {}
        candidateNonZeroed = {}
        for i in range(0,gf.globalCandidates):
            #self.mode will only not also be p if this is not learning
            if(gf.pbTracker.memberVars['mode'] == 'p' and self.mode == 'p'):
                args2, device = self.killerRecursive(args)
                kwargs2, device2  = self.killerRecursive(kwargs)
                if device is None:
                    device = device2

                '''
                DEBUG: if youre here this layer should have PB nodes which means
                candidate processors should have been initialized.  If its not you are likely
                still pointing to the old model that doesnt have PB nodes added.  make sure
                when you call add validation score you are properly setting the model
                '''
                if(self.candidateProcessors != []):
                    args2, kwargs2 = self.candidateProcessors[i].pre_d(*args2, **kwargs2)
                
                '''
                DEBUG:
                If you are getting a cpu vs gpu issue on this line its because the model is receiving args that are on the wrong thing, but within the forward function it gets passed to the correct spot.  don't ever call to() in the forward function, call it before it gets passed in
                '''
                candidateOutValues = self.candidateLayer[i].to(device)(*args2, **kwargs2)
                if(self.candidateProcessors != []):
                    candidateOuts[i] = self.candidateProcessors[i].post_d(candidateOutValues)
                else:
                    candidateOuts[i] = candidateOutValues

                for inIndex in range(self.numPBLayers):
                    #PARALLEL HACK
                    candidateOuts[i] = candidateOuts[i].to(device) + self.PBtoCandidates[i][inIndex,:].view(viewTuple).to(device) * outs[inIndex]


                candidateOuts[i] = pbTagger(candidateOuts[i], self.pbValues[i])

                #import pdb; pdb.set_trace()
                candidateNonlinearOuts[i] = gf.PBForwardFunction(candidateOuts[i]).to(device)
                    
                #candidateNonlinearOuts chosen randomly, just generally saying dont do this during inference, only training.
                if(self.training):
                    if(gf.debuggingMemoryLeak and len(self.pbValues[i].pbOuts) != 0):
                            print("%s is going forward but not backward.  This will cause a memory leak unless it is a recurrent layer.  currenlty stacked %d times" % (self.name, len(self.pbValues)))
                            print('Make sure your forward pass isnt forwarding something that doesnt get used in the final loss calculation and make sure that your eval and test functions have the model in eval() mode')
                            print('if this is supposed to be the case set gf.debuggingMemoryLeak = False')
                            #import pdb; pdb.set_trace()
                    self.pbValues[i].pbOuts.append(candidateNonlinearOuts[i].detach().clone().to(device))
                candidateNonZeroed[i] = candidateNonlinearOuts[i].detach().clone().to(device)
                candidateOuts[i] = noForward(candidateNonlinearOuts[i])
        
        return outs, candidateOuts, candidateNonlinearOuts, candidateNonZeroed
    


def pbTagger(inp, Values):
    class Tagger(torch.autograd.Function):
        @staticmethod
        def forward(ctx, inp):
            return inp
        @staticmethod
        def backward(ctx, grad_out):
            with torch.no_grad():
                savedValues = Values

                if(savedValues.locked):
                    return grad_out*0, None

                mathTuple = []
                viewTuple = []
                for i in range(len(grad_out.size())):
                    if i == Values.thisNodeIndex:
                        viewTuple.append(-1)
                        continue
                    mathTuple.append(i)
                    viewTuple.append(1)


                eps = 0.00000001
                direction = savedValues.PrevPBCandidateCorrelation.sign()
                tempReshapeDirection = direction.view(viewTuple)
                #PARALLEL HACK
                currentCorrelations = savedValues.pbOuts[-1].to(savedValues.currentParentD[-1].device) * (savedValues.currentParentD[-1])
                


                currentCorrelations = currentCorrelations.sum((mathTuple))
                    
                #got rid of averagedsq because doing a proportional scaling later so this scaling doesnt matter.
                grad_in = -(grad_out.detach() * (tempReshapeDirection))# / ((savedValues.parentsAverageDSq + eps))

                #print('top')
                #print(savedValues.topPBCandidateAverage)
                #print('ave')
                #print(savedValues.PrevPBCandidateAverage)

                #adjust correlations
                
                
                
                
                savedValues.topPBCandidateAverage = savedValues.pbOuts[-1].mean((mathTuple)).to(savedValues.currentParentD[-1].device)

                        
                savedValues.PrevPBCandidateAverage = savedValues.PrevPBCandidateAverage * 0.99 + savedValues.topPBCandidateAverage * 0.01


                #print('new top')
                #print(savedValues.topPBCandidateAverage)
                #print('new ave')
                #print(savedValues.PrevPBCandidateAverage)
                if(not gf.usingPAIDataParallel):
                    cor = currentCorrelations - (savedValues.PrevPBCandidateAverage * savedValues.parentsAverageDvector) # / net['layers'][l]['sumSqError'][j]
                    #print('prev')
                    #print(savedValues.PrevPBCandidateCorrelation)
                    #print('cor')
                    #print(cor)
                    #print('currentCorrelations')
                    #print(currentCorrelations)
                    savedValues.PrevPBCandidateCorrelation = savedValues.PrevPBCandidateCorrelation * 0.99
                    savedValues.PrevPBCandidateCorrelation = savedValues.PrevPBCandidateCorrelation + cor * 0.01
                    #print('next prev')
                    #print(savedValues.PrevPBCandidateCorrelation)


                    
                    tempAbs = savedValues.PrevPBCandidateCorrelation.detach().abs()
                    
                    #best score is the max score of the previous best score and the current recently averaged correlation
                    
                    [savedValues.bestScore, tempBestIndices] =  torch.max(torch.cat((savedValues.bestScore.unsqueeze(0),tempAbs.unsqueeze(0)), 0),0)
                                    
                    
                    #if that best score has improved enough or this is the very first iteration
                    if((
                        (
                        (savedValues.bestScore*(1.0-gf.pbImprovementThreshold))-savedValues.previousBestScore).max()>0.00000001 and (savedValues.bestScore - savedValues.previousBestScore).max() > gf.pbImprovementThresholdRaw)  or savedValues.initialized.item() == 0):

                        # say that best score did improve this epoch and time step
                        savedValues.bestScoreImprovedThisEpoch[0] = 1
                        #print('setting best score improved this timestep with')
                        #print(savedValues.bestScore)
                        #print(savedValues.previousBestScore)
                        #print(savedValues.initialized.item())
                        savedValues.bestScoreImprovedThisTimeStep[0] = 1
                        #set the indexes of the best candidate
                        savedValues.indexesOfbest = tempBestIndices
                        
                        ##check where tempabs = bestscore and save the weights for those candidates in forward for the layer next itearation
                            #this is where that saveBest function was maybe called?
                        [values,indexes] = torch.max(savedValues.indexesOfbest,0)
                        savedValues.nodesBestImprovedThisEpoch = (savedValues.nodesBestImprovedThisEpoch + savedValues.indexesOfbest)
                        #only replace the ones that are bigger                            
                        savedValues.previousBestScore = torch.max(savedValues.bestScore, savedValues.previousBestScore).detach()
                        
                        
                        
                            
                        
                    else:
                        #print('setting best score improved this timestep with')
                        #print(savedValues.bestScore)
                        #print(savedValues.previousBestScore)
                        #print(savedValues.initialized.item())
                        savedValues.bestScoreImprovedThisTimeStep[0] = 0
                        savedValues.indexesOfbest *= 0
                    if(savedValues.breaking.item()):
                        pdb.set_trace()
                else: # if not new dataparallel all of this is being done in gather
                    savedValues.currentCorrelationsForParallel = currentCorrelations
                    
                if(savedValues.initialized.item() < gf.initialCorrelationBatches):#*2?
                    #for the first 10 iterations average out the initial conditions a little bit
                    #at the beggining have it equal the actual average, not the abs average
                    #this is because the best is the abs of running best, but running best is average of a bunch of positives and negatives, so to just initialize as a single value it it a high positive or negative
                
                    savedValues.candidateGradAverageForScaling = savedValues.candidateGradAverageForScaling * savedValues.initialized
                    savedValues.candidateGradAverageForScaling = savedValues.candidateGradAverageForScaling +  grad_in.abs().mean(mathTuple)
                    savedValues.candidateGradAverageForScaling = savedValues.candidateGradAverageForScaling / (savedValues.initialized + 1.0)
                    savedValues.mainGradAverageForScaling = savedValues.mainGradAverageForScaling * savedValues.initialized
                    savedValues.mainGradAverageForScaling = savedValues.mainGradAverageForScaling + savedValues.currentParentD[-1].abs().mean(mathTuple)
                    savedValues.mainGradAverageForScaling = savedValues.mainGradAverageForScaling / (savedValues.initialized + 1.0)

                    if(not gf.usingPAIDataParallel):
                        savedValues.PrevPBCandidateAverage *= savedValues.initialized
                        savedValues.PrevPBCandidateAverage += savedValues.topPBCandidateAverage
                        savedValues.PrevPBCandidateAverage /= savedValues.initialized + 1.0
                        #print('init update PrevPBCandidateAverage')
                        #print(savedValues.PrevPBCandidateAverage)

                        cor = currentCorrelations - (savedValues.PrevPBCandidateAverage * savedValues.parentsAverageDvector) # / net['layers'][l]['sumSqError'][j]
                        #print('init update cor')
                        #print(cor)

                        savedValues.PrevPBCandidateCorrelation *= savedValues.initialized
                        savedValues.PrevPBCandidateCorrelation += cor
                        savedValues.PrevPBCandidateCorrelation /= savedValues.initialized + 1.0
                        #print('init update prev')
                        #print(savedValues.PrevPBCandidateCorrelation)
                    else:
                        savedValues.currentCorrelationsForParallel = currentCorrelations
                    #and other values should be zeroed so they dont effect things during this initialization step
                    savedValues.bestScore = savedValues.bestScore.detach() * 0
                    savedValues.previousBestScore = savedValues.previousBestScore.detach() * 0
                    savedValues.initialized = savedValues.initialized + 1.0
                    #print('initialized')
                    #print(savedValues.initialized.item())
                    scalar = 0.0000000
                else:
                    '''
                    if this candidate is getting errors so low that the average at this point is 0 it is likely because vanishing gradient has died so theres not much to do here anyway
                    just set scalar to 0 and move on.  TODO: see if there is a better way to to this?  When it was caught with with autograd.detect_anomaly(): around forward->backward .normalPassAverageD was actually
                    just a super small number but not exactly 0.  this means there is some amount of error it just is getting deleted after averaging because of float resolution.
                    '''
                    if(savedValues.candidateGradAverageForScaling.mean().item() == 0):
                        #pdb.set_trace()
                        scalar = 0.0
                    else:
                        #savedValues.candidateGradAverageForScaling = grad_in.abs().mean(mathTuple) * 0.001 + savedValues.candidateGradAverageForScaling * 0.999
                        #grad_in = (grad_in * (savedValues.parentsAverageDvector.abs().mean()/savedValues.candidateGradAverageForScaling.abs().mean())) / savedValues.currentParentD.abs().std()#.view(1,-1,1,1))
                        #scalar = savedValues.parentsAverageDvector.abs().mean()/savedValues.candidateGradAverageForScaling.abs().mean()
                        scalar = savedValues.mainGradAverageForScaling.mean()/savedValues.candidateGradAverageForScaling.mean()
                        #print('\n\n%s scaler ended up as ' % savedValues.layerName)
                        #print(scalar)
                        #print('with')
                        #print(savedValues.parentsAverageDMags.mean())
                        #print('from')
                        #print(savedValues.mainGradAverageForScaling.mean())
                        #print('and')
                        #print(savedValues.candidateGradAverageForScaling.mean())
                        
                        #scalar = (1/savedValues.parentsAverageDSq)
                        #scalar = 1 seems to not make things die.  gotta figure out a way to do this scalar reasonably.  Why would this not work if its scaling it to the same magnitude as the main gradient is learning?
                        #scalar = 1
                        
                if(gf.doingThing):
                    scalar /= savedValues.parentMaxMeanAct.item()

                grad_in = grad_in * scalar#.view(1,-1,1,1))
                del savedValues.currentParentD[-1]
                del savedValues.pbOuts[-1]                
                return grad_in, None
    return Tagger.apply(inp)


def gradKiller(inp):
    class Killer(torch.autograd.Function):
        @staticmethod
        def forward(ctx, inp):
            #print('forward called')
            return inp
        @staticmethod
        def backward(ctx, grad_out):
            #print('backward called')
            return grad_out * 0, None
    return Killer.apply(inp)


def noForward(inp):
    class noForwardd(torch.autograd.Function):
        @staticmethod
        def forward(ctx, inp):
            return inp * 0
        @staticmethod
        def backward(ctx, grad_out):
            return grad_out     
    return noForwardd.apply(inp)

    
 


        
class pbValueTracker(nn.Module):
    def __init__(self, initialized, activationFunctionValue, name, inputDimensions, out_channels=-1):
        super(pbValueTracker, self).__init__()
        
        self.layerName = name
        
        for valName in dendriteInitValues:
            self.register_buffer(valName, torch.zeros(1, device=gf.device, dtype=gf.dType))
        self.initialized[0] = initialized
        self.activationFunctionValue = activationFunctionValue
        self.thisInputDimensions = inputDimensions        
        if(self.thisInputDimensions.count(0) != 1):
            print('3 need exactly one 0 in the input dimensions: %s' % self.layerName)
            print(self.thisInputDimensions)
            exit(-1)
        self.thisNodeIndex = inputDimensions.index(0) 
        if(out_channels != -1):
            self.setupArrays(out_channels)   

    def setThisInputDimensions(self, newInputDimensions):
        self.thisInputDimensions = newInputDimensions
        if(newInputDimensions.count(0) != 1):
            print('4 need exactly one 0 in the input dimensions: %s' % self.layerName)
            print(newInputDimensions)
            exit(-1)
        self.thisNodeIndex = newInputDimensions.index(0)

    def setOutChannels(self, shapeValues):
        if(type(shapeValues) == torch.Size):
            self.out_channels = int(shapeValues[self.thisNodeIndex])
        else:
            self.out_channels = int(shapeValues[self.thisNodeIndex].item())
    def setupArrays(self, out_channels):
        self.out_channels = out_channels
        for valName in dendriteTensorValues:
            self.register_buffer(valName, torch.zeros(out_channels, device=gf.device, dtype=gf.dType))
 
        for name in valueTrackerArrays:
            # if its not copying then just make arrays so they can get deleted every time
            #if(not gf.usingPAIDataParallel):
            setattr(self,name,[])
            #else: # if it is copying make parameter lists so they are separtae and deleiton is not required
                #setattr(self,name,torch.nn.ParameterList())

        #parent values
        for valName in dendriteSingleValues:
            self.register_buffer(valName, torch.zeros(1, device=gf.device, dtype=gf.dType))            
        
    def reinitializeForPB(self, initialized):
        self.initialized[0] = initialized
        for valName in dendriteReinitValues:
            if((not valName in nonLiveSkipValues) or gf.learnPBLive):
                setattr(self,valName,getattr(self,valName) * 0)

        if(gf.doingThing):
            self.parentMaxMeanAct.copy_(self.normalPassMaxMeanAct.detach().clone())
            self.parentMaxMeanAct.requires_grad = False
        #self.parentsAverageDMags.copy_(self.normalPassAverageDMags.double().detach().clone())
        self.parentsAverageDvector.copy_(self.normalPassAverageD.detach().clone())
        #self.parentsAverageDSq.copy_(self.normalPassAverageDSq.double().mean().detach().clone())
        self.parentsAverageDvector.requires_grad = False
        #self.parentsAverageDSq.requires_grad = False
        #self.parentsAverageDMags.requires_grad = False
        
        
        
        

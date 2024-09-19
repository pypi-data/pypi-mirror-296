import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
import math
import sys
import numpy as np
import pdb
from perforatedai import globalsFile as gf

import time
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')
import pandas as pd
import copy

from perforatedai import pb_layer as PB
from perforatedai import pb_utils as PBU
from perforatedai import check_license



def defaultInitPBTracker(doingPB=True, saveName='DefaultName'):
    if(doingPB==False):
        gf.pbTracker = pb_neuron_layer_tracker(doingPB=False, saveName=saveName)
        gf.pbTracker.savedTime = time.time()
        return
    if(gf.switchMode == -1):
        print('you need to set swich mode')
        pdb.set_trace()
    if(gf.paramValsSetting == -1):
        print('you need to set paramValsSetting mode')
        pdb.set_trace()
    if(gf.inputDimensions == []):
        print('you need to set inputDimensions')
        pdb.set_trace()
        
    gf.pbTracker = pb_neuron_layer_tracker(doingPB=True,saveName=saveName) 


class pb_neuron_layer_tracker():
    
    def __init__(self, doingPB, saveName, makingGraphs=True, paramValsSetting=-1, values_per_train_epoch=-1, values_per_val_epoch=-1):
        #this allows the tracker to be initialized to just track values so if you want to test and make comparable graphs without pb layers you can use the same tracker
        self.memberVars = {}
        #Whether or not PB will be running
        self.memberVars['doingPB'] = doingPB
        #How many Dendrite Nodes have been added
        self.memberVars['numPBNeuronLayers'] = 0
        self.PBNeuronLayerVector = []
        self.memberVars['mode'] = 'n'
        self.memberVars['numEpochsRun'] = -1
        self.memberVars['totalEpochsRun'] = -1
        # Last epoch that the validation score or correlation score was improved
        self.memberVars['epochLastImproved'] = 0
        # Running validation accuracy
        self.memberVars['runningAccuracy'] = 0
        # True if maxing validation, False if minimizing Loss
        self.memberVars['maximizingScore'] = True
        # Mode for switching back and forth between learning modes
        self.memberVars['switchMode'] = gf.switchMode
        # Epoch of the last switch
        self.memberVars['lastSwitch'] = 0
        self.memberVars['currentBestValidationScore'] = 0
        # Last epoch where the learning rate was updated
        self.memberVars['lastLREpochCount'] = -1
        self.memberVars['globalBestValidationScore'] = 0
        #list of switch epochs
        #last validation score of a switch is this.  so if there are 10 epochs, this will be 9
        self.memberVars['switchEpochs'] = []
        #paramter counts at each network structure
        self.memberVars['paramCounts'] = []
        self.memberVars['nswitchEpochs'] = []
        self.memberVars['pswitchEpochs'] = []
        self.memberVars['accuracies'] = []
        self.memberVars['lastImprovedAccuracies'] = []
        self.memberVars['testAccuracies'] = []
        self.memberVars['nAccuracies'] = []
        self.memberVars['runningAccuracies'] = []
        self.memberVars['extraScores'] = {}
        self.memberVars['testScores'] = []
        self.memberVars['nExtraScores'] = {}
        self.memberVars['trainingLoss'] = []
        self.memberVars['trainingLearningRates'] = []
        self.memberVars['bestScores'] = []
        self.memberVars['currentScores'] = []
        self.memberVars['watchWeights'] = []
        self.memberVars['nEpochTimes'] = []
        self.memberVars['pEpochTimes'] = []
        self.memberVars['nTrainTimes'] = []
        self.memberVars['pTrainTimes'] = []
        self.memberVars['nValTimes'] = []
        self.memberVars['pValTimes'] = []
        self.memberVars['overWrittenExtras'] = []
        self.memberVars['overWrittenVals'] = []
        self.memberVars['overWrittenEpochs'] = 0
        self.memberVars['paramValsSetting'] = gf.paramValsSetting
        self.memberVars['optimizer'] = []
        self.memberVars['scheduler'] = []
        self.memberVars['optimizerInstance'] = []
        self.memberVars['schedulerInstance'] = []

        self.loaded = False

        self.memberVars['manualTrainSwitch'] = False
    
        if(gf.doingMeanBest):
            self.memberVars['bestMeanScores'] = []
        self.memberVars['currentNLearningRateInitialSkipSteps'] = 0
        self.memberVars['lastMaxLearningRateSteps'] = 0
        self.memberVars['lastMaxLearningRateValue'] = -1
        #this is to be filled in with [learning rate 1->2, and learning rate 2 start] to be compared
        self.memberVars['currentStepScores'] = []
        self.memberVars['currentStepCount'] = 0
        
        #set these to be True for the first initialization N
        self.memberVars['committedToInitialRate'] = True
        self.memberVars['currentNSetGlobalBest'] = True
        self.memberVars['bestMeanScoreImprovedThisEpoch'] = 0

        self.values_per_train_epoch=values_per_train_epoch
        self.values_per_val_epoch=values_per_val_epoch
        self.saveName = saveName
        self.makingGraphs = makingGraphs

        self.startTime = time.time()
        self.savedTime = 0
        self.startEpoch(internalCall=True)

        if(gf.verbose):
            print('initing with switchMode%s' % (self.memberVars['switchMode']))
        
        if(gf.usingPAIDataParallel == False and torch.cuda.device_count() > 1):
            input('Seeing multiple GPUs but not using PAIDataParallel.  Please either perform the PAIDataParallel steps from the README or include CUDA_VISIBLE_DEVICES=0 in your call')
        if(gf.usingPAIDataParallel == True and torch.cuda.device_count() == 1):
            input('Seeing one GPUs but using custom data parallel.')
            
    
    #this function is for when loading but then also need to change anything
    def doTempReinitializeThing(self):
        print('doing a temp doTempReinitializeThing make sure you want this')
        pdb.set_trace()
        for layer in self.PBNeuronLayerVector:
            layer.pb.candidateGradAverageForScaling = layer.pb.candidateGradAverage
            layer.pb.mainGradAverageForScaling = layer.pb.candidateGradAverage
    #this is the case for if you just want to use their optimizer and follow along rather than handle it here
    def setOptimizerInstance(self, optimizerInstance):
        self.memberVars['optimizerInstance'] = optimizerInstance
    def setOptimizer(self, optimizer):
        self.memberVars['optimizer'] = optimizer
    def setScheduler(self, scheduler):
        if(not scheduler is torch.optim.lr_scheduler.ReduceLROnPlateau):
            if(gf.verbose):
                print('Not using reduce on plateou, this is not reccomended')        
        self.memberVars['scheduler'] = scheduler
        
        
        
    def incrementScheduler(self, numTicks, mode):
        currentSteps = 0
        currentTicker = 0
        for param_group in gf.pbTracker.memberVars['optimizerInstance'].param_groups:
            learningRate1 = param_group['lr']
        crashTest = 0
        if(gf.verbose):
            print('using scheduler:')
            print(type(self.memberVars['schedulerInstance']))
        while currentTicker < numTicks:
            if(gf.verbose):
                print('lower start rate initial %f stepping %d times' % (learningRate1, gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']))
            if type(self.memberVars['schedulerInstance']) is torch.optim.lr_scheduler.ReduceLROnPlateau:
                if(mode == 'stepLearningRate'):
                    #step with the counter as last improved accuracy from the initial value before this switch.  This is used to initially start with a lower rate
                    self.memberVars['schedulerInstance'].step(metrics=self.memberVars['lastImprovedAccuracies'][gf.pbTracker.stepsAfterSwitch()-1])
                elif(mode == 'incrementEpochCount'):
                    #step with the the improved epoch counts up to current location, this is used when loading.
                    self.memberVars['schedulerInstance'].step(metrics=self.memberVars['lastImprovedAccuracies'][-((numTicks-1)-currentTicker)-1])
            else:
                    self.memberVars['schedulerInstance'].step()
            for param_group in gf.pbTracker.memberVars['optimizerInstance'].param_groups:
                learningRate2 = param_group['lr']
            if(learningRate2 != learningRate1):
                currentSteps += 1
                learningRate1 = learningRate2
                if(mode == 'stepLearningRate'):
                    currentTicker += 1
                if(gf.verbose):
                    print('1 step %d to %f' % (currentSteps, learningRate2))
            if(mode == 'incrementEpochCount'):
                currentTicker += 1
            crashTest += 1
            if(crashTest > 2000):
                pdb.set_trace()
        return currentSteps, learningRate1
    
    
    def setupOptimizer(self, net, optArgs, schedArgs = None):
        #if this optimizer is just passing in the model then skip it
        if(not 'model' in optArgs.keys()):
            if(self.memberVars['mode'] == 'n'):
                optArgs['params'] = filter(lambda p: p.requires_grad, net.parameters())
            else:
                #schedArgs['patience'] = gf.pPatience
                #count = 0
                #for param in optArgs['params']:
                    #print(param)
                    #count = count + 1
                #print(count)
                optArgs['params'] = PBU.getPBNetworkParams(net)
                #pdb.set_trace()
        optimizer = self.memberVars['optimizer'](**optArgs)
        self.memberVars['optimizerInstance'] = optimizer
        if(self.memberVars['scheduler'] != []):
            self.memberVars['schedulerInstance'] = self.memberVars['scheduler'](optimizer, **schedArgs)
            currentSteps = 0
            for param_group in gf.pbTracker.memberVars['optimizerInstance'].param_groups:
                learningRate1 = param_group['lr']
            if(gf.verbose):
                print('resetting scheduler with %d steps and %d initial ticks to skip' % (gf.pbTracker.stepsAfterSwitch(), gf.initialHistoryAfterSwitches))
            #reversed is fine because it is required for the first if and not used in the second if
            #if we just triggered a reset where we want to start with a lower learning rate then keep adding the last epoch improved until we get there
            if(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps'] != 0):
                additionalSteps, learningRate1 = self.incrementScheduler(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps'], 'stepLearningRate')
                currentSteps += additionalSteps
            if(self.memberVars['mode'] == 'n' or gf.learnPBLive):
                initial = gf.initialHistoryAfterSwitches
            else:
                initial = 0
            if(gf.pbTracker.stepsAfterSwitch() > initial):
                #minus an extra 1 becuase this will be getting called after start epoch has been called at the end of add validation score, which means steps after switch will actually be off by 1
                additionalSteps, learningRate1 = self.incrementScheduler((gf.pbTracker.stepsAfterSwitch() - initial)-1, 'incrementEpochCount')
                currentSteps += additionalSteps
                #then after getting to the initial point if it loaded and has completed some steps after switch then apply those
            if(gf.verbose):
                print('scheduler update loop with %d ended with %f' % (currentSteps, learningRate1))
                print('scheduler ended with %d steps and lr of %f' % (currentSteps, learningRate1))
            self.memberVars['currentStepCount'] = currentSteps
            return optimizer, self.memberVars['schedulerInstance']
        else:
            return optimizer

    def clearOptimizerAndScheduler(self):
        #self.memberVars['optimizer'] = []
        #self.memberVars['scheduler'] = []
        self.memberVars['optimizerInstance'] = []
        self.memberVars['schedulerInstance'] = []


    def switchTime(self):
        switchPhrase = 'No mode, this should never be the case.'
        if(self.memberVars['switchMode'] == gf.doingSwitchEveryTime):
           switchPhrase = 'doingSwitchEveryTime'
        elif(self.memberVars['switchMode'] == gf.doingHistory):
           switchPhrase = 'doingHistory'
        elif(self.memberVars['switchMode'] == gf.doingFixedSwitch):
           switchPhrase = 'doingFixedSwitch'
        elif(self.memberVars['switchMode'] == gf.doingNoSwitch):
           switchPhrase = 'doingNoSwitch'
        print('Checking PB switch with mode %c, switch mode %s, epoch %d, last improved epoch %d, total Epochs %d, capAtN setting: %d, n: %d, p:%d' % (self.memberVars['mode'], switchPhrase, self.memberVars['numEpochsRun'], self.memberVars['epochLastImproved'], self.memberVars['totalEpochsRun'], gf.capAtN, gf.nEpochsToSwitch, gf.pEpochsToSwitch))
        #this will fill in epoch last improved
        self.bestPBScoreImprovedThisEpoch()
        if(self.memberVars['switchMode'] == gf.doingNoSwitch):
            print('Returning False - doing no switch mode')
            return False
        if(self.memberVars['switchMode'] == gf.doingSwitchEveryTime):
            print('Returning True - switching every time')
            return True
        if(((self.memberVars['mode'] == 'n') or gf.learnPBLive) and (self.memberVars['switchMode'] == gf.doingHistory) and (gf.pbTracker.memberVars['committedToInitialRate'] == False) and (gf.dontGiveUpUnlessLearningRateLowered)
           and (self.memberVars['currentNLearningRateInitialSkipSteps'] < self.memberVars['lastMaxLearningRateSteps']) and self.memberVars['scheduler'] != []):
            print('Returning False since no first step yet and comparing initial %d to last max %d' %(self.memberVars['currentNLearningRateInitialSkipSteps'], self.memberVars['lastMaxLearningRateSteps']))
            return False
        capSwitch = False
        if(len(self.memberVars['switchEpochs']) == 0):
            thisCount = (self.memberVars['numEpochsRun'])
        else:
            thisCount = (self.memberVars['numEpochsRun'] - self.memberVars['switchEpochs'][-1])
        if(self.memberVars['switchMode'] == gf.doingHistory and self.memberVars['mode'] == 'p' and gf.capAtN):
            #if(len(self.memberVars['switchEpochs']) == 1):
            #trying method with always capping at the first N
            prevCount = self.memberVars['switchEpochs'][0]
            #else:
                #prevCount = self.memberVars['switchEpochs'][-1] - self.memberVars['switchEpochs'][-2]
            #print('Checking capAtN switch with this count  %d, prev %d' % (thisCount, prevCount))
            if(thisCount >= prevCount):
                capSwitch = True
                print('catAtN is True')
        if(self.memberVars['switchMode'] == gf.doingHistory and 
            (
                ((self.memberVars['mode'] == 'n') and (self.memberVars['numEpochsRun'] - self.memberVars['epochLastImproved'] >= gf.nEpochsToSwitch) and thisCount >= gf.initialHistoryAfterSwitches + gf.nEpochsToSwitch)
                or
                (((self.memberVars['mode'] == 'p') and (self.memberVars['numEpochsRun'] - self.memberVars['epochLastImproved'] >= gf.pEpochsToSwitch)))
             or capSwitch)):
            print('Returning True - History and last improved is hit or capAtN is hit')
            return True
        if(self.memberVars['switchMode'] == gf.doingFixedSwitch and ((self.memberVars['totalEpochsRun']%gf.fixedSwitchNum == 0) and self.memberVars['numEpochsRun'] >= gf.firstFixedSwitchNum)):
            print('Returning True - Fixed switch number is hit')
            return True
        print('Returning False - no triggers to switch have been hit')
        return False
    
    def stepsAfterSwitch(self):
        if(self.memberVars['paramValsSetting'] == gf.paramValsByTotalEpoch):
            return self.memberVars['numEpochsRun']
        elif(self.memberVars['paramValsSetting'] == gf.paramValsByUpdateEpoch):
            return self.memberVars['numEpochsRun'] - self.memberVars['lastSwitch']
        elif(self.memberVars['paramValsSetting'] == gf.paramValsByNormalEpochStart):
            if(self.memberVars['mode'] == 'p'):
                return self.memberVars['numEpochsRun'] - self.memberVars['lastSwitch']
            else:
                return self.memberVars['numEpochsRun']
        else:
            print('%d is not a valid param vals option' % self.memberVars['paramValsSetting'])
            pdb.set_trace()
    
    
    
    
    
    def addPBNeuronLayer(self, newLayer, initialAdd=True):
        #if its a duplicate just ignore the second addition
        if(newLayer in self.PBNeuronLayerVector):
            return
        self.PBNeuronLayerVector.append(newLayer)
        if(self.memberVars['doingPB']):
            PB.setWrapped_params(newLayer)
            '''
            if(self.memberVars['mode'] == 'p'):
                for i in range(0, gf.globalCandidates):
                    self.candidateLayer[i].weight.pbWrapped = True
                    self.candidateLayer[i].bias.pbWrapped = True
                    self.candidateBatchNorm[i].weight.pbWrapped = True
                    self.candidateBatchNorm[i].bias.pbWrapped = True
                    self.candidateBatchNorm[i].running_mean.pbWrapped = True
                    self.candidateBatchNorm[i].running_var.pbWrapped = True
                    if(self.numPBLayers > 0):
                        self.PBtoCandidates[i].data.pbWrapped = True
            '''
        if(initialAdd):
            self.memberVars['bestScores'].append([])
            self.memberVars['currentScores'].append([])

        
        
 
    
    def resetLayerVector(self, net,loadFromRestart):
       thisList = PBU.getPBModules(net, 0)
       for module in thisList:
            self.addPBNeuronLayer(module, initialAdd=loadFromRestart)
            
    def justSetMode(self, mode):
        for layer in self.PBNeuronLayerVector:
            layer.justSetMode(mode)

    def getTimingInfo(self):
        Times = [[],[],[],[],[],[],[],[],[],[]]
        for layer in self.PBNeuronLayerVector:
            Times[0].append(layer.timingPhase1)
            Times[1].append(layer.timingPhase2)
            Times[2].append(layer.timingPhase3)
            Times[3].append(layer.timingPhase4)
            Times[4].append(layer.timingPhase5)
            Times[5].append(layer.pb.timingPhase1)
            Times[6].append(layer.pb.timingPhase2)
            Times[7].append(layer.pb.timingPhase3)
            Times[8].append(layer.pb.timingPhase4)
            Times[9].append(layer.pb.timingPhase5)
        return Times
    
    
    def TEMPFUNCTION(self):
        for layer in self.PBNeuronLayerVector:
            layer.timingPhase1 = 0
            layer.timingPhase2 = 0
            layer.timingPhase3 = 0
            layer.timingPhase4 = 0
            layer.timingPhase5 = 0
            layer.pb.timingPhase1 = 0
            layer.pb.timingPhase2 = 0
            layer.pb.timingPhase3 = 0
            layer.pb.timingPhase4 = 0
            layer.pb.timingPhase5 = 0
        
    def resetValsForScoreReset(self):
        if(gf.findBestLR):
            self.memberVars['committedToInitialRate'] = False        
        self.memberVars['currentNSetGlobalBest'] = False
        #dont rest the global best, but do reset the current best, this is needed when doing learning rate picking to not retain old best
        self.memberVars['currentBestValidationScore'] = 0
        self.memberVars['lastLREpochCount'] = -1
                
    def setPBTraining(self):
        #self.restoreTaggers()
        if(gf.verbose):
            print('calling set PBTraining')

        for layer in self.PBNeuronLayerVector[:]:
                worked = layer.setMode('p')
                '''
                This should only happen if you have a layer that was added to the PB vector
                but then its never actually be used.  This can happen when you have set a layers
                to have requires_grad = False or when you have a modlue as a member variable but
                its not actually part of the network.  in that case remove it from future things
                '''
                if not worked:
                    self.PBNeuronLayerVector.remove(layer)
                
        self.addPBLayer()
        #reset last improved counter when switching modes
        self.memberVars['mode'] = 'p'
        self.memberVars['currentNLearningRateInitialSkipSteps'] = 0
        if(gf.learnPBLive):
            self.resetValsForScoreReset()

        self.memberVars['lastMaxLearningRateSteps'] = self.memberVars['currentStepCount']

        gf.pbTracker.memberVars['currentStepScores'] = []

    def setNormalTraining(self):
        for layer in self.PBNeuronLayerVector:
            layer.setMode('n')
        #reset last improved counter when switching modes
        #self.reinitializeForPB(0)
        self.memberVars['mode'] = 'n'
        self.memberVars['numPBNeuronLayers'] += 1
        self.memberVars['currentNLearningRateInitialSkipSteps'] = 0
        self.resetValsForScoreReset()

        self.memberVars['currentStepScores'] = []        
        if(gf.learnPBLive):
            self.memberVars['lastMaxLearningRateSteps'] = self.memberVars['currentStepCount']

    def startEpoch(self, internalCall=False):
        if(self.memberVars['manualTrainSwitch'] and internalCall==True):
            return
        #if its not a self call but it hasnt been initialized yet initialize
        if(internalCall==False and self.memberVars['manualTrainSwitch'] == False):
            self.memberVars['manualTrainSwitch'] = True
            #if calling this from a main loop reset the saved time so it knows this is the first call again
            self.savedTime = 0
            self.memberVars['numEpochsRun'] = -1
            self.memberVars['totalEpochsRun'] = -1
        #init value so first epoch
        end = time.time()
        if(self.memberVars['manualTrainSwitch']):
            if(self.savedTime != 0):
                if(self.memberVars['mode'] == 'p'):
                    self.memberVars['pValTimes'].append(end - self.savedTime)
                else:
                    self.memberVars['nValTimes'].append(end - self.savedTime)
        if(self.memberVars['mode'] == 'p'):
            for layer in self.PBNeuronLayerVector:
                for m in range(0, gf.globalCandidates):
                    with torch.no_grad():
                        layer.pb.pbValues[m].bestScoreImprovedThisEpoch *= 0
                        layer.pb.pbValues[m].nodesBestImprovedThisEpoch *= 0
            self.memberVars['bestMeanScoreImprovedThisEpoch'] = 0

        #if this was not a normal increment then reset epochLast improved.  This should only be the case right after loads?
        self.memberVars['numEpochsRun'] += 1
        self.memberVars['totalEpochsRun'] = self.memberVars['numEpochsRun'] + self.memberVars['overWrittenEpochs']
        self.savedTime = end


    def stopEpoch(self, internalCall=False):
        end = time.time()
        if(self.memberVars['manualTrainSwitch'] and internalCall==True):
            return
        if(self.memberVars['manualTrainSwitch']):
            if(self.memberVars['mode'] == 'p'):
                self.memberVars['pTrainTimes'].append(end - self.savedTime)
            else:
                self.memberVars['nTrainTimes'].append(end - self.savedTime)
        else:
            if(self.memberVars['mode'] == 'p'):
                self.memberVars['pEpochTimes'].append(end - self.savedTime)
            else:
                self.memberVars['nEpochTimes'].append(end - self.savedTime)            
        self.savedTime = end




    #this is for if the pb score improved
    def bestPBScoreImprovedThisEpoch(self, firstCall=True):

        #This function must also set epoch last improved and fill in candidate weights
        
        
        #this is just scoring candidates. validation score below is for n mode
        if(self.memberVars['mode'] == 'n'):
            return False
        gotABest = False
        ignore = False
        for layer in self.PBNeuronLayerVector:
            if(layer.pb.pbValues[0].initialized < gf.initialCorrelationBatches and not ignore):
                print('You set gf.initialCorrelationBatches to be greater than an entire epoch %d < %d.  This can result in weights not being updated.  You should set that gf.initialCorrelationBatches to be lower than the batches in one epoch. Start over or Load from \'latest\' for %s. It was caught on layer%s' % (layer.pb.pbValues[0].initialized, gf.initialCorrelationBatches,self.saveName,layer.name))
                print('If you are here for debugging with a tiny dataset or breaks feel free to ignore(this may happen more than once)')
                pdb.set_trace()
                ignore = True
            for m in range(0, gf.globalCandidates):
                #if(firstCall):
                    #print('got the following improved with the next following sores')
                    #print(layer.pb.pbValues[m].nodesBestImprovedThisEpoch)
                    #print(layer.pb.pbValues[m].bestScore)
                if(layer.pb.pbValues[m].bestScoreImprovedThisEpoch[0]):#if its anything other than 0, gets set to 1 but can be greater than that in gather
                    if(not gf.doingMeanBest):
                        if(not gf.learnPBLive):
                            self.memberVars['epochLastImproved'] = self.memberVars['numEpochsRun']
                            if(gf.verbose):
                                print('4 epoch improved is %d' % gf.pbTracker.memberVars['epochLastImproved'])
                    #update the best weights
                    #pdb.set_trace()
                    if(firstCall):
                        for node in range(len(layer.pb.pbValues[m].nodesBestImprovedThisEpoch)):
                            if(layer.pb.pbValues[m].nodesBestImprovedThisEpoch[node] > 0):
                                #print('node %d improved so saving its weights' % node)
                                with torch.no_grad():
                                    layer.pb.candidateBestLayer[m] = copy.deepcopy(layer.pb.candidateLayer[m])
                            #else:
                            #print('node %d did not improve' % node)
                    gotABest = True
        if(gf.doingMeanBest):
            if(self.memberVars['bestMeanScoreImprovedThisEpoch']):
                if(not gf.learnPBLive):
                    self.memberVars['epochLastImproved'] = self.memberVars['numEpochsRun']
                    if(gf.verbose):
                        print('5 epoch improved is %d' % gf.pbTracker.memberVars['epochLastImproved'])
                return True
            else:
                return False
        return gotABest
    
    def initialize(self, doingPB, saveName, makingGraphs, maximizingScore=True, num_classes=10000000000, values_per_train_epoch=-1, values_per_val_epoch=-1, zoomingGraph=True, pretrained=False):
        self.memberVars['doingPB'] = doingPB
        self.memberVars['maximizingScore'] = maximizingScore
        self.saveName = saveName
        self.zoomingGraph = zoomingGraph
        self.makingGraphs = makingGraphs
        #if(pretrained):
            #self.memberVars['committedToInitialRate'] = True
        if(self.loaded == False):
            self.memberVars['runningAccuracy'] = (1.0/num_classes) * 100
        self.values_per_train_epoch=values_per_train_epoch
        self.values_per_val_epoch=values_per_val_epoch
        
    def saveGraphs(self, extraString=''):
        if(self.makingGraphs == False):
            return
        
        saveFolder = '.'
        #if(gf.paiSaves):
            #saveolder = '/pai'
        
        plt.ioff()
        fig = plt.figure(figsize=(28,14))
        ax = plt.subplot(221)
        
        
        df1 = None
        
        for listID in range(len(self.memberVars['overWrittenExtras'])):
            for extraID in self.memberVars['overWrittenExtras'][listID]:
                ax.plot(np.arange(len(self.memberVars['overWrittenExtras'][listID][extraID])), self.memberVars['overWrittenExtras'][listID][extraID], 'r')
            ax.plot(np.arange(len(self.memberVars['overWrittenVals'][listID])), self.memberVars['overWrittenVals'][listID], 'b')
        
        if(gf.drawingPB):
            accuracies = self.memberVars['accuracies']
            extraScores = self.memberVars['extraScores']
        else:
            accuracies = self.memberVars['nAccuracies']
            extraScores = self.memberVars['extraScores']
        
        ax.plot(np.arange(len(accuracies)), accuracies, label='Validation Scores')
        ax.plot(np.arange(len(self.memberVars['runningAccuracies'])), self.memberVars['runningAccuracies'], label='Validation Running Scores')
        for extraScore in extraScores:
            ax.plot(np.arange(len(extraScores[extraScore])), extraScores[extraScore], label=extraScore)
        plt.title(saveFolder + '/' + self.saveName + "Scores")
        plt.xlabel('Epochs')
        plt.ylabel('Score')
        
        #this will add a point at emoch last improved so while watching can tell when a switch is coming
        lastImproved = self.memberVars['epochLastImproved']
        #if(self.memberVars['epochLastImproved'] == self.memberVars['numEpochsRun'] + 1):#if it is current epochs run that means it just improved within add validation score so epoch last improved is setup for next epoch
            #lastImproved -= 1
        if(gf.drawingPB):
            ax.plot(lastImproved, self.memberVars['globalBestValidationScore'], 'bo', label='Global best (y)')
            ax.plot(lastImproved, accuracies[lastImproved], 'go', label='Epoch Last Improved \nmight be wrong in\nfirst after switch')
        else:
            if(self.memberVars['mode'] == 'n'):
                missedTime = self.memberVars['numEpochsRun'] - lastImproved
                ax.plot((len(self.memberVars['nAccuracies'])-1) - missedTime, self.memberVars['nAccuracies'][-(missedTime+1)], 'go', label='Epoch Last Improved')
            
        
        pd1 = pd.DataFrame({'Epochs': np.arange(len(accuracies)), 'Validation Scores': accuracies})
        pd2 = pd.DataFrame({'Epochs': np.arange(len(self.memberVars['runningAccuracies'])), 'Validation Running Scores': self.memberVars['runningAccuracies']})
        pd1 = pd.concat([pd1, pd.DataFrame(pd2)], ignore_index=True)        
        for extraScore in extraScores:
            pd2 = pd.DataFrame({'Epochs': np.arange(len(extraScores[extraScore])), extraScore: extraScores[extraScore]})
            pd1 = pd.concat([pd1, pd.DataFrame(pd2)], ignore_index=True)        

        pd1.to_csv(saveFolder + '/' + self.saveName + extraString + 'Scores.csv', index=False)
        pd1.to_csv('pd.csv', float_format='%.2f', na_rep="NAN!")
        del pd1, pd2
        
        #if it has done as switch set the y min to be the average from before the switch, which will ideally be backloaded with the flatline but also slightly below that from the initial lower epochs
        if(len(self.memberVars['switchEpochs']) > 0 and self.memberVars['switchEpochs'][0] > 0 and self.zoomingGraph):
            #if this one is saving the training accuracies
            #if len(trainingAccuracies) > 0:
                #minVal = np.min((np.array(accuracies[0:self.memberVars['switchEpochs'][0]]).mean(),np.array(trainingAccuracies[0:self.memberVars['switchEpochs'][0]]).mean()))
            #else:
            if(gf.pbTracker.memberVars['maximizingScore']):
                minVal = np.array(accuracies[0:self.memberVars['switchEpochs'][0]]).mean()
                for extraScore in extraScores:
                    minPot = np.array(extraScores[extraScore][0:self.memberVars['switchEpochs'][0]]).mean()
                    if minPot < minVal:
                        minVal = minPot
                ax.set_ylim(ymin=minVal)
            else:
                maxVal = np.array(accuracies[0:self.memberVars['switchEpochs'][0]]).mean()
                for extraScore in extraScores:
                    maxPot = np.array(extraScores[extraScore][0:self.memberVars['switchEpochs'][0]]).mean()
                    if maxPot > maxVal:
                        maxVal = maxPot
                ax.set_ylim(ymax=maxVal)
                
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        if(gf.drawingPB and self.memberVars['doingPB']):
            color = 'r'
            for switcher in self.memberVars['switchEpochs']:
                plt.axvline(x=switcher, ymin=0, ymax=1,color=color)
                if(color == 'r'):
                    color = 'b'
                else:
                    color ='r'
        else:
            for switcher in self.memberVars['nswitchEpochs']:
                plt.axvline(x=switcher, ymin=0, ymax=1,color='b')
        ax = plt.subplot(222)        
        if(self.memberVars['manualTrainSwitch']):
            ax.plot(np.arange(len(self.memberVars['nTrainTimes'])), self.memberVars['nTrainTimes'], label='Normal Epoch Train Times')
            ax.plot(np.arange(len(self.memberVars['pTrainTimes'])), self.memberVars['pTrainTimes'], label='PB Epoch Train Times')
            ax.plot(np.arange(len(self.memberVars['nValTimes'])), self.memberVars['nValTimes'], label='Normal Epoch Val Times')
            ax.plot(np.arange(len(self.memberVars['pValTimes'])), self.memberVars['pValTimes'], label='PB Epoch Val Times')
            plt.title(saveFolder + '/' + self.saveName + "times (by train() and eval())")
            plt.xlabel('Iteration')
            plt.ylabel('Epoch Time in Seconds ')
            ax.set_ylim(ymin=0)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            
            
            pd1 = pd.DataFrame({'Epochs': np.arange(len(self.memberVars['nTrainTimes'])), 'Normal Epoch Train Times': self.memberVars['nTrainTimes']})
            pd2 = pd.DataFrame({'Epochs': np.arange(len(self.memberVars['pTrainTimes'])), 'PB Epoch Train Times': self.memberVars['pTrainTimes']})
            pd1 = pd.concat([pd1, pd.DataFrame(pd2)], ignore_index=True)        
            pd2 = pd.DataFrame({'Epochs': np.arange(len(self.memberVars['nValTimes'])), 'Normal Epoch Val Times': self.memberVars['nValTimes']})
            pd1 = pd.concat([pd1, pd.DataFrame(pd2)], ignore_index=True)        
            pd2 = pd.DataFrame({'Epochs': np.arange(len(self.memberVars['pValTimes'])), 'PB Epoch Val Times': self.memberVars['pValTimes']})
            pd1 = pd.concat([pd1, pd.DataFrame(pd2)], ignore_index=True)        
            pd1.to_csv(saveFolder + '/' + self.saveName + extraString + 'Times.csv', index=False)
            pd1.to_csv('pd.csv', float_format='%.2f', na_rep="NAN!")
            del pd1, pd2
        else:
            ax.plot(np.arange(len(self.memberVars['nEpochTimes'])), self.memberVars['nEpochTimes'], label='Normal Epoch Times')
            ax.plot(np.arange(len(self.memberVars['pEpochTimes'])), self.memberVars['pEpochTimes'], label='PB Epoch Times')
            plt.title(saveFolder + '/' + self.saveName + "times (by train() and eval())")
            plt.xlabel('Iteration')
            plt.ylabel('Epoch Time in Seconds ')
            ax.set_ylim(ymin=0)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            pd1 = pd.DataFrame({'Epochs': np.arange(len(self.memberVars['nEpochTimes'])), 'Normal Epoch Times': self.memberVars['nEpochTimes']})
            pd2 = pd.DataFrame({'Epochs': np.arange(len(self.memberVars['pEpochTimes'])), 'PB Epoch Times': self.memberVars['pEpochTimes']})
            pd1 = pd.concat([pd1, pd.DataFrame(pd2)], ignore_index=True)
            pd1.to_csv(saveFolder + '/' + self.saveName + extraString + 'Times.csv', index=False)
            pd1.to_csv('pd.csv', float_format='%.2f', na_rep="NAN!")
            del pd1, pd2
        
        
        
        if(self.values_per_train_epoch != -1 and self.values_per_val_epoch != -1):
            ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
            ax2.set_ylabel('Single Datapoint Time in Seconds')  # we already handled the x-label with ax1
            ax2.plot(np.arange(len(self.memberVars['nTrainTimes'])), np.array(self.memberVars['nTrainTimes'])/self.values_per_train_epoch, linestyle='dashed', label='Normal Train Item Times')
            ax2.plot(np.arange(len(self.memberVars['pTrainTimes'])), np.array(self.memberVars['pTrainTimes'])/self.values_per_train_epoch, linestyle='dashed', label='PB Train Item Times')
            ax2.plot(np.arange(len(self.memberVars['nValTimes'])), np.array(self.memberVars['nValTimes'])/self.values_per_val_epoch, linestyle='dashed', label='Normal Val Item Times')
            ax2.plot(np.arange(len(self.memberVars['pValTimes'])), np.array(self.memberVars['pValTimes'])/self.values_per_val_epoch, linestyle='dashed', label='PB Val Item Times')
            ax2.tick_params(axis='y')
            ax2.set_ylim(ymin=0)
            ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        
        
        
        
        ax = plt.subplot(223)        
        
        #ax.plot(np.arange(len(self.memberVars['trainingLoss'])), self.memberVars['trainingLoss'], label='Loss')
        #plt.title(saveFolder + '/' + self.saveName + "Loss")
        #plt.xlabel('Epochs')
        #plt.ylabel('Loss')
        #ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        #pd1 = pd.DataFrame({'Epochs': np.arange(len(self.memberVars['trainingLoss'])), 'Loss': self.memberVars['trainingLoss']})
        #pd1.to_csv(saveFolder + '/' + self.saveName + 'Loss.csv', index=False)
        #pd1.to_csv('pd.csv', float_format='%.2f', na_rep="NAN!")
        #del pd1
        
        ax.plot(np.arange(len(self.memberVars['trainingLearningRates'])), self.memberVars['trainingLearningRates'], label='learningRate')
        plt.title(saveFolder + '/' + self.saveName + "learningRate")
        plt.xlabel('Epochs')
        plt.ylabel('learningRate')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        pd1 = pd.DataFrame({'Epochs': np.arange(len(self.memberVars['trainingLearningRates'])), 'learningRate': self.memberVars['trainingLearningRates']})
        pd1.to_csv(saveFolder + '/' + self.saveName + extraString + 'learningRate.csv', index=False)
        pd1.to_csv('pd.csv', float_format='%.2f', na_rep="NAN!")
        del pd1


        pd1 = pd.DataFrame({'Switch Number': np.arange(len(self.memberVars['switchEpochs'])), 'Switch Epoch': self.memberVars['switchEpochs']})
        pd1.to_csv(saveFolder + '/' + self.saveName + extraString + 'switchEpochs.csv', index=False)
        pd1.to_csv('pd.csv', float_format='%.2f', na_rep="NAN!")
        del pd1


        pd1 = pd.DataFrame({'Switch Number': np.arange(len(self.memberVars['paramCounts'])), 'Param Count': self.memberVars['paramCounts']})
        pd1.to_csv(saveFolder + '/' + self.saveName + extraString + 'paramCounts.csv', index=False)
        pd1.to_csv('pd.csv', float_format='%.2f', na_rep="NAN!")
        del pd1
        
        testScores = self.memberVars['testScores']
        
        #if not tracking test scores just do validation scores again.
        if(len(self.memberVars['testScores']) == 0):
            testScores = self.memberVars['accuracies']
        switchCounts = len(self.memberVars['switchEpochs']) 
        bestTest = []
        bestValid = []
        assosciatedParams = []
        for switch in range(0,switchCounts,2):
            startIndex = 0
            if(switch != 0):
                startIndex = self.memberVars['switchEpochs'][switch-1] + 1
            endIndex = self.memberVars['switchEpochs'][switch]+1
            bestValidIndex = startIndex + np.argmax(self.memberVars['accuracies'][startIndex:endIndex])
            
            bestValidScore = self.memberVars['accuracies'][bestValidIndex]
            bestTestScore = testScores[bestValidIndex]
            bestValid.append(bestValidScore)
            bestTest.append(bestTestScore)
            assosciatedParams.append(self.memberVars['paramCounts'][switch])
        #if its in n mode
        if(self.memberVars['mode'] == 'n' and 
            #its not the very first epoch of n mode, which means the last accuracy was the last one of p mode
            (
            ((len(self.memberVars['switchEpochs']) == 0) or
                (self.memberVars['switchEpochs'][-1] + 1 != len(self.memberVars['accuracies']))
                ))):
            startIndex = 0
            if(len(self.memberVars['switchEpochs']) != 0):
                startIndex = self.memberVars['switchEpochs'][-1] + 1
            bestValidIndex = startIndex + np.argmax(self.memberVars['accuracies'][startIndex:])
            bestValidScore = self.memberVars['accuracies'][bestValidIndex]
            bestTestScore = testScores[bestValidIndex]
            bestValid.append(bestValidScore)
            bestTest.append(bestTestScore)
            assosciatedParams.append(self.memberVars['paramCounts'][-1])
        

        pd1 = pd.DataFrame({'Param Counts': assosciatedParams, 'Max Valid Scores':bestValid, 'Max Test Scores':bestTest})
        pd1.to_csv(saveFolder + '/' + self.saveName + extraString + 'bestTestScores.csv', index=False)
        pd1.to_csv('pd.csv', float_format='%.2f', na_rep="NAN!")
        del pd1

            
        
        
        ax = plt.subplot(224)
        if(self.memberVars['doingPB']):
            pd1 = None
            pd2 = None
            NUM_COLORS = len(self.PBNeuronLayerVector)
            if( len(self.PBNeuronLayerVector) > 0 and len(self.memberVars['currentScores'][0]) != 0):
                NUM_COLORS *= 2
            cm = plt.get_cmap('gist_rainbow')
            ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
            for layerID in range(len(self.PBNeuronLayerVector)):
                ax.plot(np.arange(len(self.memberVars['bestScores'][layerID])), self.memberVars['bestScores'][layerID], label=self.PBNeuronLayerVector[layerID].name)
                pd2 = pd.DataFrame({'Epochs': np.arange(len(self.memberVars['bestScores'][layerID])), 'Best ever for all nodes Layer ' + self.PBNeuronLayerVector[layerID].name: self.memberVars['bestScores'][layerID]})
                if(pd1 is None):
                    pd1 = pd2
                else:
                    pd1 = pd.concat([pd1, pd.DataFrame(pd2)], ignore_index=True)
                if(len(self.memberVars['currentScores'][layerID]) != 0):
                    ax.plot(np.arange(len(self.memberVars['currentScores'][layerID])), self.memberVars['currentScores'][layerID], label='Best current for all Nodes Layer ' +  self.PBNeuronLayerVector[layerID].name)
                pd2 = pd.DataFrame({'Epochs': np.arange(len(self.memberVars['currentScores'][layerID])), 'Best current for all nodes Layer ' + self.PBNeuronLayerVector[layerID].name: self.memberVars['currentScores'][layerID]})
                pd1 = pd.concat([pd1, pd.DataFrame(pd2)], ignore_index=True)
            if(gf.doingMeanBest and len(self.memberVars['bestMeanScores']) != 0):
                ax.plot(np.arange(len(self.memberVars['bestMeanScores'])), self.memberVars['bestMeanScores'], label='Best Means', color='k', marker='o')
                pd2 = pd.DataFrame({'Epochs': np.arange(len(self.memberVars['bestMeanScores'])), 'Best Means': self.memberVars['bestMeanScores']})
                pd1 = pd.concat([pd1, pd.DataFrame(pd2)], ignore_index=True)
            plt.title(saveFolder + '/' + self.saveName + " Best PBScores")
            plt.xlabel('Epochs')
            plt.ylabel('Best PBScore')
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=math.ceil(len(self.PBNeuronLayerVector)/30))
            for switcher in self.memberVars['pswitchEpochs']:
                plt.axvline(x=switcher, ymin=0, ymax=1,color='r')
            
            if(self.memberVars['mode'] == 'p'):
                missedTime = self.memberVars['numEpochsRun'] - lastImproved
                #T
                plt.axvline(x=(len(self.memberVars['bestScores'][0])-(missedTime+1)), ymin=0, ymax=1,color='g')
                

            
            pd1.to_csv(saveFolder + '/' + self.saveName + extraString + 'Best PBScores.csv', index=False)
            pd1.to_csv('pd.csv', float_format='%.2f', na_rep="NAN!")
            del pd1, pd2

        
        
        fig.tight_layout()
        plt.savefig(saveFolder + '/' + self.saveName+extraString+'.png')
        
        plt.close('all')
        
        
            
        if(self.memberVars['watchWeights'] != []):
            plt.close('all')

            
            loopOneRange = range(self.memberVars['watchWeights'].shape[0])
            loopTwoRange = range(self.memberVars['watchWeights'].shape[1])
            for NodeID in loopOneRange:
                maxNum = math.ceil(self.memberVars['watchWeights'].shape[1]/2.0)
                fig = plt.figure(figsize=(14*maxNum/2,14))
                for ID1 in loopTwoRange:
                    ax = plt.subplot(2,maxNum,ID1 + 1)
                    ax.plot(np.arange(len(self.memberVars['watchWeights'][NodeID][ID1])), self.memberVars['watchWeights'][NodeID][ID1], label='weight %d' % ((ID1)))
                    plt.title("weight change " + str(ID1))
                    plt.xlabel('batch')
                    plt.ylabel('weight value')
                    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                    plt.ylim((-np.absolute(self.memberVars['watchWeights']).max(),np.absolute(self.memberVars['watchWeights']).max()))
                fig.tight_layout()
                plt.savefig(saveFolder + '/' + self.saveName + '_watchedPBWeights_Node' + str(NodeID) + extraString + '.png')
                plt.close('all')

            
            plt.close('all')

            #why is over written trains not being graphed.  check what batch times actuall are, are validations being added to training during pb?
        


    def addLoss(self, loss):
        if (type(loss) is float) == False and (type(loss) is int) == False:
            loss = loss.item()
        self.memberVars['trainingLoss'].append(loss)
    def addLearningRate(self, learningRate):
        if (type(learningRate) is float) == False and (type(learningRate) is int) == False:
               learningRate = learningRate.item()
        self.memberVars['trainingLearningRates'].append(learningRate)
    

    def addBestScores(self):
        
        totalMeanBest = 0
        layerID = 0
        for layer in self.PBNeuronLayerVector:
            layerMeanBest = 0
            #this is really already abs
            layerMeanBest += layer.pb.pbValues[0].bestScore.abs().mean().item()
            layerMax = 0
            for plane in range(0,layer.out_channels):
                planeMax = 0
                for candidate in range(0,gf.globalCandidates):
                    if(abs(layer.pb.pbValues[candidate].bestScore[plane]) >= abs(planeMax)):
                        planeMax = layer.pb.pbValues[candidate].bestScore[plane]
                if(abs(planeMax) >= abs(layerMax)):
                    layerMax = planeMax
            if (type(layerMax) is int):
                print('Didn\'t get any non zero scores or a score is nan or inf.')
                pdb.set_trace()
            self.memberVars['bestScores'][layerID].append(abs(layerMax.item()))
            layerMeanBest /= layer.out_channels
            totalMeanBest += layerMeanBest
            layerID += 1
        if(gf.doingMeanBest):
            totalMeanBest / len(self.PBNeuronLayerVector)
            if(len(self.memberVars['switchEpochs']) == 0):
                countSinceSwitch = gf.pbTracker.memberVars['numEpochsRun']
            else:
                countSinceSwitch = (gf.pbTracker.memberVars['numEpochsRun'] - self.memberVars['switchEpochs'][-1])-1
            if(countSinceSwitch == 0):
                if(gf.verbose):
                    print('got current best mean PB %f compared to old 0.0' % (totalMeanBest))
                self.memberVars['bestMeanScores'].append(totalMeanBest)
                self.memberVars['bestMeanScoreImprovedThisEpoch'] = 1
            elif(((totalMeanBest*(1.0-gf.pbImprovementThreshold))-self.memberVars['bestMeanScores'][-1])>0.0000001 and (totalMeanBest - self.memberVars['bestMeanScores'][-1]) > gf.improvementThresholdRaw):
                if(gf.verbose):
                    print('Better current best mean PB %f compared to old %f' % (totalMeanBest, self.memberVars['bestMeanScores'][-1]))
                self.memberVars['bestMeanScores'].append(totalMeanBest)
                self.memberVars['bestMeanScoreImprovedThisEpoch'] = 1
            else:
                if(gf.verbose):
                    print('Not Better current best mean PB %f compared to old %f' % (totalMeanBest, self.memberVars['bestMeanScores'][-1]))
                self.memberVars['bestMeanScores'].append(self.memberVars['bestMeanScores'][-1])
                self.memberVars['bestMeanScoreImprovedThisEpoch'] = 0
                
                
        #print('list is:')
        #print(self.memberVars['bestScores'])

    def addCurrentScores(self):
        layerID = 0
        #currentMean = 0
        for layer in self.PBNeuronLayerVector:
            #currentMean += layer.pb.pbValues[0].PrevPBCandidateCorrelation.abs().mean().item()

            layerMax = 0
            for plane in range(0,layer.out_channels):
                planeMax = 0
                for candidate in range(0,gf.globalCandidates):
                    tempAbs = layer.pb.pbValues[candidate].PrevPBCandidateCorrelation.detach().clone().abs()
                    if(abs(tempAbs[plane]) >= abs(planeMax)):
                        planeMax = tempAbs[plane]
                if(abs(planeMax) >= abs(layerMax)):
                    layerMax = planeMax
            if (type(layerMax) is int):
                print('didnt get any non zero scores?')
                pdb.set_trace()
            if(not gf.doingMeanBest):
                self.memberVars['currentScores'][layerID].append(abs(layerMax.item()))
            layerID += 1
        #currentMean /= len(self.PBNeuronLayerVector)
        #if(gf.doingMeanBest):
            #self.memberVars['currentScores'][layerID].append(currentMean)
            
    def addCurrentWeights(self):            
        for layer in self.PBNeuronLayerVector:            
            if(layer.debugPBWeights and self.memberVars['mode'] == 'p'):
                weights = np.concatenate((layer.pb.candidateLayer[0].weight.detach().cpu().numpy(),np.expand_dims(layer.pb.candidateLayer[0].bias.detach().cpu().numpy(),1)), axis=1)
                weights = np.expand_dims(weights,2)
                if(self.memberVars['watchWeights'] == []):
                    self.memberVars['watchWeights'] = weights
                else:
                    self.memberVars['watchWeights'] = np.concatenate((self.memberVars['watchWeights'],weights),axis=2)


    def addExtraScore(self, score, extraScoreName):
        if (type(score) is float) == False and (type(score) is int) == False:
               score = score.item()
        if(gf.verbose):
            print('adding extra score %s of %f' % (extraScoreName, float(score)))
        if((extraScoreName in self.memberVars['extraScores']) == False):
                self.memberVars['extraScores'][extraScoreName] = []
        self.memberVars['extraScores'][extraScoreName].append(score)
        if(self.memberVars['mode'] == 'n'):
            if((extraScoreName in self.memberVars['nExtraScores']) == False):
                    self.memberVars['nExtraScores'][extraScoreName] = []
            self.memberVars['nExtraScores'][extraScoreName].append(score)

    def addTestScore(self, score, extraScoreName):
        self.addExtraScore(score, extraScoreName)
        if (type(score) is float) == False and (type(score) is int) == False:
               score = score.item()
        if(gf.verbose):
            print('adding test score %s of %f' % (extraScoreName, float(score)))
        self.memberVars['testScores'].append(score)

    #This is for if the validation score improved
    def addValidationScore(self, accuracy, net, saveName, forceSwitch=False):
        if(self.memberVars['doingPB']):
            for param_group in self.memberVars['optimizerInstance'].param_groups:
                learningRate = param_group['lr']
            self.addLearningRate(learningRate)
        
        
        if(len(self.memberVars['paramCounts']) == 0):
            pytorch_total_params = sum(p.numel() for p in net.parameters())
            self.memberVars['paramCounts'].append(pytorch_total_params)

        
        
        print('Adding validation score %f' % accuracy)
        #make sure you are passing in the model and not the dataparallel wrapper
        if issubclass(type(net), nn.DataParallel):
            print('Need to call .module when using add validation score')
            pdb.set_trace()
            exit(-1)
        if 'module' in net.__dir__():
            print('Need to call .module when using add validation score')
            pdb.set_trace()
            exit(-1)

        if (type(accuracy) is float) == False:
            accuracy = accuracy.item()
        file_name = 'best_model'
        if(len(self.memberVars['switchEpochs']) == 0):
            countSinceSwitch = gf.pbTracker.memberVars['numEpochsRun']
        else:
            countSinceSwitch = (gf.pbTracker.memberVars['numEpochsRun'] - self.memberVars['switchEpochs'][-1])-1
        #dont update running accuracy during c training
        if(self.memberVars['mode'] == 'n' or gf.learnPBLive):
            #print('adding validation score with %d since switch' % countSinceSwitch)
            if(countSinceSwitch < gf.initialHistoryAfterSwitches):
                if countSinceSwitch == 0:
                    self.memberVars['runningAccuracy'] = accuracy
                else:
                    self.memberVars['runningAccuracy'] = self.memberVars['runningAccuracy'] * (1-(1.0/(countSinceSwitch+1))) + accuracy * (1.0/(countSinceSwitch+1))
            else:
                self.memberVars['runningAccuracy'] = self.memberVars['runningAccuracy'] * (1.0 - 1.0 / gf.historyLookback) + accuracy * (1.0 / gf.historyLookback)
        if(self.memberVars['mode'] == 'p'):
            #print('adding best scores score with %d since switch' % countSinceSwitch)
            #add best scores here because this happens all the way at the end of a training validation loop which means they will just be filled in
            self.addBestScores()
            #current score was just adding the insantaneou correlation at the current batch, so good if debugging batch by batch, not needed for now just adding at epoch
            #self.addCurrentScores()

        
        self.memberVars['accuracies'].append(accuracy)
        if(self.memberVars['mode'] == 'n'):
            self.memberVars['nAccuracies'].append(accuracy)
        if gf.drawingPB or self.memberVars['mode'] == 'n' or gf.learnPBLive:
            self.memberVars['runningAccuracies'].append(self.memberVars['runningAccuracy'])
        
        self.stopEpoch(internalCall=True)
        
        improved = False
        
        
        
        if(self.memberVars['mode'] == 'n') or gf.learnPBLive:
            
            
            if( #score improved, or no score yet, and (always switching or enough time to do a switch)
                ((gf.pbTracker.memberVars['maximizingScore'] and (self.memberVars['runningAccuracy']*(1.0 - gf.improvementThreshold) > self.memberVars['currentBestValidationScore']))
                 or
                 ((not gf.pbTracker.memberVars['maximizingScore']) and (self.memberVars['runningAccuracy']*(1.0 + gf.improvementThreshold) < self.memberVars['currentBestValidationScore'])) or (self.memberVars['currentBestValidationScore'] == 0))#if current best is 0 that means it just reset, so want this score to count like it always would for the above case. 
                 and 
                ((countSinceSwitch > gf.initialHistoryAfterSwitches) or (self.memberVars['switchMode'] == gf.doingSwitchEveryTime))):
                if(gf.pbTracker.memberVars['maximizingScore']):
                    if(gf.verbose):
                        print('\n\ngot score of %f (average %f, *%f=%f) which is higher than %f so setting epoch to %d\n\n' %(accuracy, self.memberVars['runningAccuracy'], 1-gf.improvementThreshold,self.memberVars['runningAccuracy']*(1.0 - gf.improvementThreshold), self.memberVars['currentBestValidationScore'], self.memberVars['numEpochsRun']))
                else:
                    if(gf.verbose):
                        print('\n\ngot score of %f (average %f, *%f=%f) which is lower than %f so setting epoch to %d\n\n' %(accuracy, self.memberVars['runningAccuracy'], 1+gf.improvementThreshold,self.memberVars['runningAccuracy']*(1.0 + gf.improvementThreshold), self.memberVars['currentBestValidationScore'], self.memberVars['numEpochsRun']))
                    
                self.memberVars['currentBestValidationScore'] = self.memberVars['runningAccuracy']
                if((gf.pbTracker.memberVars['maximizingScore'] and self.memberVars['currentBestValidationScore'] > self.memberVars['globalBestValidationScore'])
                   or (not gf.pbTracker.memberVars['maximizingScore'] and self.memberVars['currentBestValidationScore'] < self.memberVars['globalBestValidationScore']) or (self.memberVars['globalBestValidationScore'] == 0)):
                    if(gf.verbose):
                        print('this also beats global best of %f so saving' % self.memberVars['globalBestValidationScore'])
                    self.memberVars['globalBestValidationScore'] = self.memberVars['currentBestValidationScore']
                    self.memberVars['currentNSetGlobalBest'] = True
                    #save system
                    PBU.saveSystem(net, saveName, file_name, dontSaveLocally = not gf.testSaves)
                    if(gf.paiSaves):
                        PBU.paiSaveSystem(net, saveName, file_name)
                self.memberVars['epochLastImproved'] = self.memberVars['numEpochsRun']
                if(gf.verbose):
                    print('2 epoch improved is %d' % gf.pbTracker.memberVars['epochLastImproved'])
                improved = True
            else:
                
                if(gf.verbose):
                    print('Not saving new best because:')
                    if(countSinceSwitch <= gf.initialHistoryAfterSwitches):
                        print('not enough history since switch%d <= %d' % (countSinceSwitch, gf.initialHistoryAfterSwitches))
                    elif(gf.pbTracker.memberVars['maximizingScore']):
                        print('got score of %f (average %f, *%f=%f) which is not higher than %f' %(accuracy, self.memberVars['runningAccuracy'], 1-gf.improvementThreshold,self.memberVars['runningAccuracy']*(1.0 - gf.improvementThreshold), self.memberVars['currentBestValidationScore']))
                    else:
                        print('got score of %f (average %f, *%f=%f) which is not lower than %f' %(accuracy, self.memberVars['runningAccuracy'], 1+gf.improvementThreshold,self.memberVars['runningAccuracy']*(1.0 + gf.improvementThreshold), self.memberVars['currentBestValidationScore']))
                    
                #if its the first epoch save a model so there is never a problem with not finidng a model
                if(len(self.memberVars['accuracies']) == 1 or gf.saveAllEpochs):
                    if(gf.verbose):
                        print('Saving first model or all models')
                    #save system
                    PBU.saveSystem(net, saveName, file_name, dontSaveLocally = not gf.testSaves)
                    if(gf.paiSaves):
                        PBU.paiSaveSystem(net, saveName, file_name)
                    
        else:
            if(self.bestPBScoreImprovedThisEpoch(firstCall = False)):
                if(gf.verbose):
                    print('best PB score improved')
                self.memberVars['epochLastImproved'] = self.memberVars['numEpochsRun']
                if(gf.verbose):
                    print('3 epoch improved is %d' % gf.pbTracker.memberVars['epochLastImproved'])
                improved = True
            else:
                if(gf.verbose):
                    print('best PB score not improved')
        if(gf.testSaves):
            #save system
            PBU.saveSystem(net, saveName, 'latest')
        if(gf.paiSaves):
            PBU.paiSaveSystem(net, saveName, 'latest')

        self.memberVars['lastImprovedAccuracies'].append(self.memberVars['epochLastImproved'])



        restructured = False
        #if it is time to switch based on scores and counter
        if((self.switchTime() == True) or forceSwitch):
            '''
            if((gf.pbTracker.memberVars['mode'] == 'n') and (gf.pbTracker.memberVars['numPBNeuronLayers'] > 0)):
                # net, did not improve, did not restructure, training is over
                gf.pbTracker.saveGraphs()
                print('Freemium only allows one dendrite so quiting rather than adding a second')
                return net, False, False, True
            '''
            
            if(((gf.pbTracker.memberVars['mode'] == 'n') or gf.learnPBLive) #if its currently in n mode, or its learning live, i.e. if it potentially might have higher accuracy
               and (gf.pbTracker.memberVars['currentNSetGlobalBest'] == False) # and it did not beat the current best
               ): #then restart with a new set of PB nodes
                if(gf.verbose):
                    print('Planning to switch to p mode but best last %d current start %f and last maximum %d or rate %.8f' % (gf.pbTracker.memberVars['currentNSetGlobalBest'],
                                                                        self.memberVars['currentNLearningRateInitialSkipSteps'], self.memberVars['lastMaxLearningRateSteps'], self.memberVars['lastMaxLearningRateValue'])) 
                #pdb.set_trace()
                now = datetime.now()
                dt_string = now.strftime("_%d.%m.%Y.%H.%M.%S")
                if(gf.verbose):
                    print('1 saving break %s' % (dt_string+'_noImprove_lr_'+str(self.memberVars['currentNLearningRateInitialSkipSteps'])))
                gf.pbTracker.saveGraphs(dt_string+'_noImprove_lr_'+str(self.memberVars['currentNLearningRateInitialSkipSteps']))
                net = PBU.loadSystem(saveName, 'switch_' + str(len(gf.pbTracker.memberVars['switchEpochs'])),switchLoad = not gf.testSaves)
                #if just didnt learn try the other learning mode again, i.e. if it didnt learn with N add another set of P's
                net = PBU.changeLearningModes(net, saveName, file_name, self.memberVars['doingPB'], switchLoad = not gf.testSaves)
                #but if learning during P's. then save after changing modes so that if you reload again you'll try it the other way.                      
            else: #if did improve keep the nodes and switch back to a new P mode
                if(gf.verbose):
                    print('calling switchMode with %d, %d, %d, %f' % (gf.pbTracker.memberVars['currentNSetGlobalBest'],
                                                                        self.memberVars['currentNLearningRateInitialSkipSteps'], self.memberVars['lastMaxLearningRateSteps'], self.memberVars['lastMaxLearningRateValue']))
                #pdb.set_trace()#want to draw the fullAverageParentD to see if there is any pattern that should have been able to be learned for all the planes in the layer that isnt learning
                gf.pbTracker.saveGraphs('_beforeSwitch_'+str(len(gf.pbTracker.memberVars['switchEpochs'])))
                #just for testing save what it was like before switching
                if(gf.testSaves):
                    PBU.saveSystem(net, saveName, 'beforeSwitch_' + str(len(gf.pbTracker.memberVars['switchEpochs'])))
                net = PBU.changeLearningModes(net, saveName, file_name, self.memberVars['doingPB'], switchLoad = not gf.testSaves)
                
            #AT THIS POINT gf.pbTracker might no longer be self.  Don't do any more calls to self after this point.  gf.pbTracker will refer to self still if there was not a switch

            #if restructured is true then you're just about to reset the scheduler and optimizer to clear them before saving
            restructured = True
            gf.pbTracker.clearOptimizerAndScheduler() 
            
            #if gf.testSaves just save as usual, if not saving everything then save to /tmp
            PBU.saveSystem(net, saveName, 'switch_' + str(len(gf.pbTracker.memberVars['switchEpochs'])), dontSaveLocally = not gf.testSaves)

        elif(gf.pbTracker.memberVars['scheduler'] != []):
            for param_group in gf.pbTracker.memberVars['optimizerInstance'].param_groups:
                learningRate1 = param_group['lr']
            if(type(self.memberVars['schedulerInstance']) is torch.optim.lr_scheduler.ReduceLROnPlateau):
                if(countSinceSwitch > gf.initialHistoryAfterSwitches or self.memberVars['mode'] == 'p'):
                    if(gf.verbose):
                        print('updating scheduler with last improved %d from current %d' % (self.memberVars['epochLastImproved'],self.memberVars['numEpochsRun']))
                    if(self.memberVars['scheduler'] != []):
                        self.memberVars['schedulerInstance'].step(metrics=self.memberVars['epochLastImproved'])
                        if(gf.pbTracker.memberVars['scheduler'] is torch.optim.lr_scheduler.ReduceLROnPlateau):
                            if(gf.verbose):
                                print('scheduler is now at %d bad epochs' % self.memberVars['schedulerInstance'].num_bad_epochs)
                else:
                    if(gf.verbose):
                        print('not stepping optimizer since hasnt initialized')
            elif(self.memberVars['scheduler'] != []):
                if(countSinceSwitch > gf.initialHistoryAfterSwitches or self.memberVars['mode'] == 'p'):
                    if(gf.verbose):
                        print('incrementing scheduler to count %d' % self.memberVars['schedulerInstance']._step_count)
                    self.memberVars['schedulerInstance'].step()
                    if(gf.pbTracker.memberVars['scheduler'] is torch.optim.lr_scheduler.ReduceLROnPlateau):
                        if(gf.verbose):
                            print('scheduler is now at %d bad epochs' % self.memberVars['schedulerInstance'].num_bad_epochs)
            if(countSinceSwitch <= gf.initialHistoryAfterSwitches and self.memberVars['mode'] == 'n'):
                if(gf.verbose):
                    print('not stepping with history %d and current %d' % (gf.initialHistoryAfterSwitches, countSinceSwitch))
            for param_group in gf.pbTracker.memberVars['optimizerInstance'].param_groups:
                learningRate2 = param_group['lr']
            stepped = False
            atLastCount = False
            if(gf.verbose):
                print('checking if at last with scores %d, count since switch %d and last count %d' % (len(gf.pbTracker.memberVars['currentStepScores']), countSinceSwitch, gf.pbTracker.memberVars['lastLREpochCount']))
            #Then if either it is double that (first value 1->2) or exactly that, (start at 2) then go into this check even though the learning rate didnt just step because it might never again 
            if(((len(gf.pbTracker.memberVars['currentStepScores']) == 0) and countSinceSwitch == gf.pbTracker.memberVars['lastLREpochCount']*2)
               or ((len(gf.pbTracker.memberVars['currentStepScores']) == 1) and countSinceSwitch == gf.pbTracker.memberVars['lastLREpochCount'])):
                atLastCount = True
            if(gf.verbose):
                print('at last count %d with count %d and last LR count %d' % (atLastCount, countSinceSwitch,  gf.pbTracker.memberVars['lastLREpochCount']))
            
            if(learningRate1 != learningRate2):
                stepped = True
                self.memberVars['currentStepCount'] += 1
                if(gf.verbose):
                    print('learning learning rate just stepped to %.10e with %d total steps' % (learningRate2, gf.pbTracker.memberVars['currentStepCount']))
                if(gf.pbTracker.memberVars['currentStepCount'] == gf.pbTracker.memberVars['lastMaxLearningRateSteps']):
                    if(gf.verbose):
                        print('%d steps is the max of the last switch mode' % gf.pbTracker.memberVars['currentStepCount'])
                    #If this was the first step and it is the max then set it.  Want to set when 1->2 gets to 2, not when 0->1 hits 2 as its stopping point
                    if(gf.pbTracker.memberVars['currentStepCount'] - gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps'] == 1):
                        gf.pbTracker.memberVars['lastLREpochCount'] = countSinceSwitch

            if(gf.verbose):
                print('learning rates were %.8e and %.8e started with %f, and is now at %d commited %d then either this (non zero) or eventually comparing to %d steps or rate %.8f' %
                                                        (learningRate1, learningRate2, 
                                                         gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps'],
                                                         self.memberVars['currentStepCount'],
                                                         gf.pbTracker.memberVars['committedToInitialRate'],
                                                         gf.pbTracker.memberVars['lastMaxLearningRateSteps'],
                                                         gf.pbTracker.memberVars['lastMaxLearningRateValue']))
            

            #if the learning rate just stepped check in on the restart at lower rate
            if((gf.pbTracker.memberVars['scheduler'] != []) 
               and ((gf.pbTracker.memberVars['mode'] == 'n') or gf.learnPBLive) #if its currently in n mode, or its learning live, i.e. if it potentially might have higher accuracy
               and (stepped or atLastCount)): #and the learning rate just stepped
                if(gf.pbTracker.memberVars['committedToInitialRate'] == False): #and it hasnt commited yet
                    bestScoreSoFar = gf.pbTracker.memberVars['globalBestValidationScore']
                    #want to make sure it does this this time do a find for 'max count 1'.
                    if(gf.verbose):
                        print('in statements to check next learning rate with stepped %d and max count %d' % (stepped, atLastCount))
                    if(len(gf.pbTracker.memberVars['currentStepScores']) == 0 #if there are currently no scores
                        and (gf.pbTracker.memberVars['currentStepCount'] - gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps'] == 2# and either it just did its second step
                            or atLastCount)): #of it didnt, but this is the max count
                        #if restructured is true then you're just about to reset the scheduler and optimizer to clear them before saving
                        restructured = True
                        gf.pbTracker.clearOptimizerAndScheduler() 
                        #save the system for this initial condition
                        #save old global so if it doesnt beat it it wont overwrite during loading
                        oldGlobal = gf.pbTracker.memberVars['globalBestValidationScore']
                        #save old accuracy to track it
                        oldAccuracy = gf.pbTracker.memberVars['currentBestValidationScore']
                        #if old counts is not -1 that means its on the last max learning rate so want to retain it and use the same one for the next time
                        oldCounts = gf.pbTracker.memberVars['lastLREpochCount']
                        skip1 = gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']
                        now = datetime.now()
                        dt_string = now.strftime("_%d.%m.%Y.%H.%M.%S")
                        gf.pbTracker.saveGraphs(dt_string+'_PBCount_' + str(gf.pbTracker.memberVars['numPBNeuronLayers']) + '_startSteps_' +str(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']))
                        if(gf.testSaves):
                            PBU.saveSystem(net, saveName, 'PBCount_' + str(gf.pbTracker.memberVars['numPBNeuronLayers']) + '_startSteps_'  + str(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']))
                        if(gf.verbose):
                            print('saving with initial steps: %s with current best %f' % (dt_string+'_PBCount_' + str(gf.pbTracker.memberVars['numPBNeuronLayers']) + '_startSteps_' +str(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']), oldAccuracy))
                        #then load back at the start and try with the lower initial learning rate
                        net = PBU.loadSystem(saveName, 'switch_' + str(len(gf.pbTracker.memberVars['switchEpochs'])), switchLoad = not gf.testSaves)
                        gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps'] = skip1 + 1
                        #if this next one is going to be at the min learning rate of last switch mode
                        gf.pbTracker.memberVars['currentStepScores'].append(oldAccuracy)
                        gf.pbTracker.memberVars['globalBestValidationScore'] = oldGlobal
                        gf.pbTracker.memberVars['lastLREpochCount'] = oldCounts
                    elif(len(gf.pbTracker.memberVars['currentStepScores']) == 1):#if there is one score already, and this in theory is the first step at the second score
                        gf.pbTracker.memberVars['currentStepScores'].append(gf.pbTracker.memberVars['currentBestValidationScore'])                        
                        if((gf.pbTracker.memberVars['maximizingScore'] and gf.pbTracker.memberVars['currentStepScores'][0] > gf.pbTracker.memberVars['currentStepScores'][1])
                           or ((not gf.pbTracker.memberVars['maximizingScore']) and gf.pbTracker.memberVars['currentStepScores'][0] < gf.pbTracker.memberVars['currentStepScores'][1])): #and the first one is higher than the current one
                           
                            #if restructured is true then you're just about to reset the scheduler and optimizer to clear them before saving
                            restructured = True
                            gf.pbTracker.clearOptimizerAndScheduler() 
                           #then reload the current one, and then say we're good to go
                            if(gf.verbose):
                                print('Got initial %d step score %f and %d score at step %f so loading old score' % (gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']-1,gf.pbTracker.memberVars['currentStepScores'][0], gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps'],gf.pbTracker.memberVars['currentStepScores'][1])) 
                            
                            priorBest = gf.pbTracker.memberVars['currentStepScores'][0]
                            #save this one that gets tossed
                            now = datetime.now()
                            dt_string = now.strftime("_%d.%m.%Y.%H.%M.%S")
                            gf.pbTracker.saveGraphs(dt_string+'_PBCount_' + str(gf.pbTracker.memberVars['numPBNeuronLayers']) + '_startSteps_' +str(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']))
                            if(gf.testSaves):
                                PBU.saveSystem(net, saveName, 'PBCount_' + str(gf.pbTracker.memberVars['numPBNeuronLayers']) + '_startSteps_'  + str(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']))
                            if(gf.verbose):
                                print('saving with initial steps: %s' % (dt_string+'_PBCount_' + str(gf.pbTracker.memberVars['numPBNeuronLayers']) + '_startSteps_' +str(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps'])))
                            if(gf.testSaves):
                                net = PBU.loadSystem(saveName, 'PBCount_' + str(gf.pbTracker.memberVars['numPBNeuronLayers']) + '_startSteps_'  + str(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']-1))
                            #also save graphs for this one that gets chosen
                            now = datetime.now()
                            dt_string = now.strftime("_%d.%m.%Y.%H.%M.%S")
                            gf.pbTracker.saveGraphs(dt_string+'_PBCount_' + str(gf.pbTracker.memberVars['numPBNeuronLayers']) + '_startSteps_' +str(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']) + 'PICKED')
                            if(gf.testSaves):
                                PBU.saveSystem(net, saveName, 'PBCount_' + str(gf.pbTracker.memberVars['numPBNeuronLayers']) + '_startSteps_'  + str(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']))
                            if(gf.verbose):
                                print('saving with initial steps: %s' % (dt_string+'_PBCount_' + str(gf.pbTracker.memberVars['numPBNeuronLayers']) + '_startSteps_' +str(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps'])))
                            gf.pbTracker.memberVars['committedToInitialRate'] = True
                            gf.pbTracker.memberVars['lastMaxLearningRateSteps'] = gf.pbTracker.memberVars['currentStepCount']
                            gf.pbTracker.memberVars['lastMaxLearningRateValue'] = learningRate2
                            #set the best score to be the higher schore to not overwrite it
                            gf.pbTracker.memberVars['currentBestValidationScore'] = priorBest
                            if(gf.verbose):
                                print('Setting laxt max steps to %d and lr %f' % (gf.pbTracker.memberVars['lastMaxLearningRateSteps'], gf.pbTracker.memberVars['lastMaxLearningRateValue']))
                        else: #if the current one is higher so want to check the next lower one without reloading
                            if(gf.verbose):
                                print('Got initial %d step score %f and %d score at step %f so NOT loading old score and continuing with this score' % (gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']-1,gf.pbTracker.memberVars['currentStepScores'][0], gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps'],gf.pbTracker.memberVars['currentStepScores'][1])) 
                            if(atLastCount):#if this is the last one though, then also set it to be the one that is picked

                                #if restructured is true then you're just about to reset the scheduler and optimizer to clear them before saving
                                restructured = True
                                gf.pbTracker.clearOptimizerAndScheduler() 
                                now = datetime.now()
                                dt_string = now.strftime("_%d.%m.%Y.%H.%M.%S")
                                gf.pbTracker.saveGraphs(dt_string+'_PBCount_' + str(gf.pbTracker.memberVars['numPBNeuronLayers']) + '_startSteps_' +str(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']) + 'PICKED')
                                if(gf.testSaves):
                                    PBU.saveSystem(net, saveName, 'PBCount_' + str(gf.pbTracker.memberVars['numPBNeuronLayers']) + '_startSteps_'  + str(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps']))
                                if(gf.verbose):
                                    print('saving with initial steps: %s' % (dt_string+'_PBCount_' + str(gf.pbTracker.memberVars['numPBNeuronLayers']) + '_startSteps_' +str(gf.pbTracker.memberVars['currentNLearningRateInitialSkipSteps'])))
                                gf.pbTracker.memberVars['committedToInitialRate'] = True
                                gf.pbTracker.memberVars['lastMaxLearningRateSteps'] = gf.pbTracker.memberVars['currentStepCount']
                                gf.pbTracker.memberVars['lastMaxLearningRateValue'] = learningRate2
                                if(gf.verbose):
                                    print('Setting laxt max steps to %d and lr %f' % (gf.pbTracker.memberVars['lastMaxLearningRateSteps'], gf.pbTracker.memberVars['lastMaxLearningRateValue']))
#to test that this is working make sure that 4 shows 4 picked.
                                
                        #reset scores here so it will be ready for the next switch.  need this for if it likes it, or if it wants to keep going and then check next pair
                        gf.pbTracker.memberVars['currentStepScores'] = []
                    #dont let the new ones overwrite the old ones
                    
                    
                    elif(len(gf.pbTracker.memberVars['currentStepScores']) == 2):
                        print('Shouldnt ever be 2 here.  Please let Perforated AI know if this happened.')
                        pdb.set_trace()
                    gf.pbTracker.memberVars['globalBestValidationScore'] = bestScoreSoFar
                    
                else:
                    if(gf.verbose):
                        print('Setting last max steps to %d and lr %f' % (gf.pbTracker.memberVars['lastMaxLearningRateSteps'], gf.pbTracker.memberVars['lastMaxLearningRateValue']))
                    gf.pbTracker.memberVars['lastMaxLearningRateSteps'] += 1
                    gf.pbTracker.memberVars['lastMaxLearningRateValue'] = learningRate2
                
#AT THIS POINT gf.pbTracker might no longer be self.  Don't do any more calls to self after this point.  gf.pbTracker will refer to self still if there was not a switch
        gf.pbTracker.startEpoch(internalCall=True)
        gf.pbTracker.saveGraphs()
        if(restructured):
            gf.pbTracker.memberVars['epochLastImproved'] = gf.pbTracker.memberVars['numEpochsRun']
            if(gf.verbose):
                print('Setting epoch last improved to %d' % gf.pbTracker.memberVars['epochLastImproved'])
            now = datetime.now()
            dt_string = now.strftime("_%d.%m.%Y.%H.%M.%S")
            if(gf.verbose):
                print('not saving restructure right now')
            #PBU.saveSystem(net, saveName, 'restructureAt' + dt_string)

        if(gf.verbose):
            print('completed adding score.  restructured is %d\ncurrent switch list is:' % restructured)
            print(gf.pbTracker.memberVars['switchEpochs'])
        
        
        
        return net, improved, restructured, False #Always false because if its getting here its in infinite training mode
            
            
    def addPBNodes(self, numberNodes):
        if(numberNodes == 0):
            return
        for layer in self.PBNeuronLayerVector:
            layer.addPBNodes(numberNodes)

    def addLoadedPBLayer(self):
        for layer in self.PBNeuronLayerVector:
            layer.addLoadedPBLayer()

    def archiveLayer(self):
        #print('calling main archive')
        #if(self.memberVars['mode'] == 'p'):
        for layer in self.PBNeuronLayerVector:
            layer.archiveLayer()

    def restoreTaggers(self):
        #print('calling main restore')
        #if(self.memberVars['mode'] == 'p'):
        for layer in self.PBNeuronLayerVector:
            layer.pb.restoreTaggers()
    def addPBLayer(self):
        for layer in self.PBNeuronLayerVector:
            layer.addPBLayer()


        

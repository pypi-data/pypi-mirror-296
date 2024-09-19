import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
import torchvision.models.resnet as resnetPT
import math
import pdb
from itertools import chain
from perforatedai import globalsFile as gf

#if you are using a custom file include like this
import sys
#sys.path.append('/home/rbrenner/PerferatedBackpropagation/examples/FixRes')
#import Res as resnetPT


'''
to use this for sequentials just wrap it.  EG:

nn.Linear(2 * hidden_dim, 512),
nn.LayerNorm(512),
>>
PBM.layer(Batch(nn.Linear(2 * hidden_dim, 512),
nn.LayerNorm(512)),
'''


'''
class Squeezer(torch.nn.Module):
    def __init__(self):
        super(Squeezer, self).__init__()
    def forward(self, x):
        return x.squeeze(0)
'''
'''
class gruBatch(nn.Sequential):
        def __init__(self, gru, bnLayer):
            super(gruBatch, self).__init__()
            self.gru = gru
            self.bnLayer = bnLayer
        def forward(self, x, h):
            x, h = self.gru(x, h)
            x = self.bnLayer(x)
            return x, h
'''
'''
class layerBatchIdentity(nn.Sequential):
        def __init__(self, linLayer, bnLayer, otherLayer = None):
            super(layerBatchIdentity, self).__init__()
            if(otherLayer is None):
                self.model = nn.Sequential(
                    linLayer,bnLayer)
            else:
                self.model = nn.Sequential(
                    linLayer,bnLayer,otherLayer)
        def forward(self, x, identity):
            return self.model(x) + identity['identity']
'''
# Processing for something that outputs 2 tensors with the first one being what we want to correlate with
# This ignores the extra output from the Dendrite blocks
class multiOutputProcesser2():
    def post_n1(self, *args, **kawrgs):
        out = args[0][0]
        extraOut = args[0][1]
        self.extraOut = extraOut
        return out
    def post_n2(self, *args, **kawrgs):
        out = args[0]
        return out, self.extraOut
    def pre_d(self, *args, **kwargs):
        return args, kwargs
    def post_d(self, *args, **kawrgs):
        out = args[0][0]
        return out

# Processing for something that outputs 3 tensors with the first one being what we want to correlate with
# This ignores the extra output from the Dendrite blocks
class multiOutputProcesser3():
    def post_n1(self, *args, **kawrgs):
        out = args[0][0]
        extraOut = args[0][1]
        extraOut2 = args[0][1]
        self.extraOut = extraOut
        self.extraOut2 = extraOut2
        return out
    def post_n2(self, *args, **kawrgs):
        out = args[0]
        return out, self.extraOut, self.extraOut2
    def pre_d(self, *args, **kwargs):
        return args, kwargs
    def post_d(self, *args, **kawrgs):
        out = args[0][0]
        return out



#two transfromer functions
class Wav2Vec2FeatureProjectionProcessor():
    # main forward returns hidden and norm hidden.  we want PB to just work with hidden
    def post_n1(self, *args, **kawrgs):
        hidden_states = args[0][0]
        norm_hidden_states= args[0][1]
        self.norm_hidden_states = norm_hidden_states
        return hidden_states
    #This function is called right before passing final value forward, should return everything that gets returned from main module
    def post_n2(self, *args, **kawrgs):
        hidden_states = args[0]
        return hidden_states, self.norm_hidden_states
    #nothing is done for pre_d just pass it the same values
    def pre_d(self, *args, **kwargs):
        return args, kwargs
        
    #for post processsing just ignore the norm hidden states part
    def post_d(self, *args, **kawrgs):
        hidden_states = args[0][0]
        return hidden_states
#this just wraps the tensor as part 1 of a tuple for some reason??
class Wav2Vec2EncoderLayerProcessor():
    #remove the tuple
    def post_n1(self, *args, **kawrgs):
        out = args[0][0]
        return out
    #add the tuple back
    def post_n2(self, *args, **kawrgs):
        out = args[0]
        return (out,)
    #nothing is done for pre_d just pass it the same values
    def pre_d(self, *args, **kwargs):
        return args, kwargs
    #remove the tuble
    def post_d(self, *args, **kawrgs):
        out = args[0][0]
        return out






#LSTMCellProcessor defined here to use as example of how to setup processing functions.
#Even though this is one class, what really happens is that the main module has one instance, which will use post_n1 and post_n2 and then each new Dendrite node gets a unique sepearte individual isntance to use pre_d and post_d
class LSTMCellProcessor():
    #The neuron does eventually need to return h_t and c__t, but h_t gets modified py the Dendrite
    #nodes first so it needs to be extracted in post_n1, and then gets added back in post_n2
    #post_n1 is called right after the main module is called before any Dendrite processing.  It should return only the part of the output that you want to do Dendrite learning for.  
    def post_n1(self, *args, **kawrgs):
        h_t = args[0][0]
        c_t = args[0][1]
        #store the cell state temporarily and just use the hidden state to do Dendrite functions
        self.c_t_n = c_t
        return h_t
    #post_n2 is called right before passing final value forward, should return everything that gets returned from main module
    #h_t at this point has been modified with Dendrite processing
    def post_n2(self, *args, **kawrgs):
        h_t = args[0]
        return h_t, self.c_t_n
    #input to pre_d will be (input, (h_t, c_t))
    #pre_d does filtering to make sure Dendrite is getting the right input.  This typically would be done in the training loop.  For example, with an LSTM this is where you check if its the first itration or not and either pass the Dendrite the regular args to the neuron or pass the Dendrite its own internal state.
    def pre_d(self, *args, **kwargs):
        h_t = args[1][0]
        #if its the initial step then just use the normal input and zeros
        if(h_t.sum() == 0):
            return args, kwargs
        #if its not the first one then return the input it got with its own h_t and c_t to replace parents
        else:
            return (args[0], (self.h_t_d, self.c_t_d)), kwargs
        
    #For post processsing post_d just getting passed the output, which is (h_t,c_t). Then it wants to only pass along h_t as the output for the function to be passed to the parent while retaining both h_t and c_t.  post_d saves what needs to be saved for next time and passes forward only the Dendrite part that will be added to the parent
    def post_d(self, *args, **kawrgs):
        h_t = args[0][0]
        c_t = args[0][1]
        self.h_t_d = h_t
        self.c_t_d = c_t
        return h_t

# Similar to the above but for GRU
class GRUProcessor():
    def post_n1(self, *args, **kawrgs):
        output = args[0][0]
        h_t = args[0][1]
        self.h_t = h_t
        return output
    def post_n2(self, *args, **kawrgs):
        output = args[0]
        return output, self.h_t
    def pre_d(self, *args, **kwargs):
        if(len(args) == 1 or args[1].sum() == 0):
            return args, kwargs
        else:
            return (args[0], self.h_t_d), kwargs
    def post_d(self, *args, **kawrgs):
        output = args[0][0]
        h_t_d = args[0][1]
        self.h_t_d = h_t_d
        return output
 
#This LSTM processor works as above but operates with the final hidden state being passed rather than output
class LSTMProcessorReturnHidden():
    def post_n1(self, *args, **kawrgs):
        self.output = args[0][0]
        hidden = args[0][1][0]
        self.cell = args[0][1][1]
        return hidden
    def post_n2(self, *args, **kawrgs):
        hidden = args[0]
        return self.output, (hidden, self.cell)
    def pre_d(self, *args, **kwargs):
        hidden = args[1][0]
        if(hidden.sum() == 0):
            return args, kwargs
        else:
            return (args[0], (self.dendrite_hidden, self.dendrite_cell)), {}
        
    def post_d(self, *args, **kawrgs):
        output = args[0][0]
        hidden = args[0][1][0]
        cell = args[0][1][1]
        self.dendrite_hidden = hidden
        self.dendrite_cell = cell
        return hidden


'''
class GRUProcessor():
    #Post processing does eventually need to return h_t and c__t, but h_t gets modified py the PB nodes first so it needs to be extracted in post 1, and then gets added back in post 2
    def post_n1(self, *args, **kawrgs):
        h_t = args[0][0]
        c_t = args[0][1]
        #store the cell state temporarily and just use the hidden state to do PB functions
        self.c_t_n = c_t
        return h_t
    def post_n2(self, *args, **kawrgs):
        h_t = args[0]
        return h_t, self.c_t_n
    #Pass in an extra argument for if its the first input to use the original val and not the internal val
    def pre_d(self, *args, **kwargs):
        c_t = args[0][0]
        h_t = args[1][0]
        first = args[2]
        if first:
            return args, kwargs
        #if its not the first one then return the input it got with its own c_t to replace parents
        else:
            return (args[0], self.c_t_d,first),{}
    #for post processsing its just getting passed the output, which is (h_t,c_t). Then it wants to just pass along h_t as the output for the function to be passed to the parent while retaining both
    def post_d(self, *args, **kawrgs):
        h_t = args[0][0]
        c_t = args[0][1]
        self.c_t_d = c_t
        return h_t

'''


class MyBatchNorm1d(nn.BatchNorm1d):
    def __init__(self, num_features, eps=1e-5, momentum=0.1,
                 affine=True, track_running_stats=True):
        super(MyBatchNorm1d, self).__init__(
            num_features, eps, momentum, affine, track_running_stats)

    def forward(self, input):
        self._check_input_dim(input)

        exponential_average_factor = 0.0

        if self.training and self.track_running_stats:
            if self.num_batches_tracked is not None:
                self.num_batches_tracked += 1
                if self.momentum is None:  # use cumulative moving average
                    exponential_average_factor = 1.0 / float(self.num_batches_tracked)
                else:  # use exponential moving average
                    exponential_average_factor = self.momentum

        # calculate running estimates
        if self.training:
            self.mean = input.mean([0])
            # use biased var in train
            self.var = input.var([0], unbiased=False)
            self.n = input.numel() / input.size(1)
            with torch.no_grad():
                self.running_mean = exponential_average_factor * self.mean\
                    + (1 - exponential_average_factor) * self.running_mean
                # update running_var with unbiased var
                self.running_var = exponential_average_factor * self.var * self.n / (self.n - 1)\
                    + (1 - exponential_average_factor) * self.running_var
        else:
            self.mean = self.running_mean
            self.var = self.running_var

        input = (input - self.mean[None, :]) / (torch.sqrt(self.var[None, :] + self.eps))
        if self.affine:
            input = input * self.weight[None, :] + self.bias[None, :]

        return input



    def forwardPB(self, input):
        self._check_input_dim(input)
        tempmean = self.mean.detach().clone()
        tempvar = self.var.detach().clone()
        tempweight = self.weight.detach().clone()
        tempbias = self.bias.detach().clone()
        input = (input - tempmean[None, :]) / (torch.sqrt(tempvar[None, :] + self.eps))
        if self.affine:
            input = input * tempweight[None, :] + tempbias[None, :]

        return input


class SequentialWithExtra(nn.Sequential):
    def forward(self, input, extra):
        for module in self:
            input = module(input, extra)
        return input

'''
class BasicBlockPB(nn.Module):
    expansion = 1

    ' ' '
    this inits from scratch, but really can just call with a nn one so do that every time
    def __init__(self, inplanes, planes, stride=1, downsample=None, groups=1,
                 base_width=64, dilation=1, norm_layer=None):
        super(BasicBlockPB, self).__init__()
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        if groups != 1 or base_width != 64:
            raise ValueError('BasicBlockPB only supports groups=1 and base_width=64')
        if dilation > 1:
            raise NotImplementedError("Dilation > 1 not supported in BasicBlockPB")
        # Both self.conv1 and self.downsample layers downsample the input when stride != 1
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

        self.b1 = nn.Sequential(
                resnetPT.conv3x3(inplanes, planes, stride),
                norm_layer(planes)
            )
        self.b2 = SequentialWithExtra(
                resnetPT.conv3x3(planes, planes),
                norm_layer(planes)
            )
    ' ' '
    def __init__(self, otherBlock):
        super(BasicBlockPB, self).__init__()
        # Both self.conv1 and self.downsample layers downsample the input when stride != 1
        self.relu = otherBlock.relu
        self.downsample = otherBlock.downsample
        self.stride = otherBlock.stride

        self.b1 = layerBatch(
                otherBlock.conv1,
                otherBlock.bn1
            )
        self.b2 = layerBatchIdentity(
                otherBlock.conv2,
                otherBlock.bn2
            )


    def forward(self, x):
        identity = x
        if self.downsample is not None:
            identity = self.downsample(x)

        out = self.b1(x)
        out = F.relu(out)

        out = self.b2.forward(out, {'identity':identity})

        out = F.relu(out)

        return out


class BottleneckPB(nn.Module):
    expansion = 4
    ' ' '
    this inits from scratch, but really can just call with a nn one so do that every time

    def __init__(self, inplanes, planes, stride=1, downsample=None, groups=1,
                 base_width=64, dilation=1, norm_layer=None):
        super(BottleneckPB, self).__init__()
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        width = int(planes * (base_width / 64.)) * groups
        # Both self.conv2 and self.downsample layers downsample the input when stride != 1
        
        self.b1 = nn.Sequential(
            resnetPT.conv3x3(inplanes, width),
            norm_layer(width)
        )
        self.b2 = nn.Sequential(
            resnetPT.conv3x3(width, width, stride, groups, dilation),
            norm_layer(width)
        )
        self.b3 = SequentialWithExtra(
            resnetPT.conv3x3(width, planes * self.expansion),
            norm_layer(planes * self.expansion)
        )

        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride
    ' ' '
    def __init__(self, otherBottleneck):
        super(BottleneckPB, self).__init__()
        self.b1 = layerBatch(
            otherBottleneck.conv1,
            otherBottleneck.bn1
        )
        self.b2 = layerBatch(
            otherBottleneck.conv2,
            otherBottleneck.bn2
        )
        self.b3 = layerBatchIdentity(
            otherBottleneck.conv3,
            otherBottleneck.bn3
        )

        self.relu = otherBottleneck.relu
        self.downsample = otherBottleneck.downsample
        self.stride = otherBottleneck.stride

    def forward(self, x):
        identity = x
        out = self.b1(x)
        out = F.relu(out)

        out = self.b2(out)
        out = F.relu(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out = self.b3.forward(out, {'identity':identity})

        #out += identity
        out = F.relu(out)

        return out
'''

#this just turns layer batch into a sequential thing, hasnt been tested with the basic block and bottle neck thing like this, but with them just being coverted directly now it shouldnt matter
class ResNetPB(nn.Module):
    def __init__(self, otherResNet):
        super(ResNetPB, self).__init__()
        
        self._norm_layer = otherResNet._norm_layer

        self.inplanes = otherResNet.inplanes
        self.dilation = otherResNet.dilation
        self.groups = otherResNet.groups
        self.base_width = otherResNet.base_width
        self.b1 = gf.pbSequential([
             otherResNet.conv1,
             otherResNet.bn1]
        )

        self.relu = otherResNet.relu
        self.maxpool = otherResNet.maxpool
        for i in range(1,5):
            setattr(self, 'layer' + str(i), self._make_layerPB(getattr(otherResNet,'layer' + str(i)),otherResNet, i))
        self.avgpool = otherResNet.avgpool
        self.fc = otherResNet.fc

    #this might not be needed now that the blocks are just being converted
    def _make_layerPB(self, otherBlockSet,otherResNet, blockID):

        layers = []
        for i in range(len(otherBlockSet)):
            if(type(otherBlockSet[i]) == resnetPT.BasicBlock):
                layers.append((otherBlockSet[i]))
            elif(type(otherBlockSet[i]) == resnetPT.Bottleneck):
                layers.append((otherBlockSet[i]))
            else:
                print('your resnet uses a block type that has not been accounted for.  customizaiton might be required')
                print(type(getattr(otherResNet,'layer' + str(blockID))))
                pdb.set_trace()

        return nn.Sequential(*layers)

    def _forward_impl(self, x):
        # See note [TorchScript super()]
        x = self.b1(x)
        x = F.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)

        return x

    def forward(self, x):
        return self._forward_impl(x)


class PBLSTMCell(nn.Module):



    #debugging init
    def __init__(self, input_size, hidden_size, bias = True,
              init_mode = 0,
              weight_ih=[], weight_hh=[], bias_ih=[], bias_hh=[]):
        super(PBLSTMCell, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.bias = bias
        self.x2h = nn.Linear(self.input_size, 4 * self.hidden_size, bias=self.bias)
        self.h2h = nn.Linear(self.hidden_size, 4 * self.hidden_size, bias=self.bias)
        with torch.no_grad():
            fromCell = False
            if(fromCell):
                self.x2h.weight.data.copy_(LSTMCell.x2h.weight.detach().clone())
                self.x2h.bias.data.copy_(LSTMCell.x2h.bias.detach().clone())
                self.h2h.weight.data.copy_(LSTMCell.h2h.weight.detach().clone())
                self.h2h.bias.data.copy_(LSTMCell.h2h.bias.detach().clone())
            elif(init_mode != 0):
                self.x2h.weight.data.copy_(weight_ih.detach().clone())
                self.x2h.bias.data.copy_(bias_ih.detach().clone())
                self.h2h.weight.data.copy_(weight_hh.detach().clone())
                self.h2h.bias.data.copy_(bias_hh.detach().clone())

        

        self.ingate = nn.Linear(self.input_size+self.hidden_size, self.hidden_size, bias=self.bias)
        self.forgetgate = nn.Linear(self.input_size+self.hidden_size, self.hidden_size, bias=self.bias)
        self.cellgate = nn.Linear(self.input_size+self.hidden_size, self.hidden_size, bias=self.bias)
        self.outgate = nn.Linear(self.input_size+self.hidden_size, self.hidden_size, bias=self.bias)            
        
        ingate_weights_in, forgetgate_weights_in, cellgate_weights_in, outgate_weights_in = self.x2h.weight.chunk(4, 0)
        ingate_bias_in, forgetgate_bias_in, cellgate_bias_in, outgate_bias_in = self.x2h.bias.chunk(4, 0)
        ingate_weights_h, forgetgate_weights_h, cellgate_weights_h, outgate_weights_h = self.h2h.weight.chunk(4, 0)
        ingate_bias_h, forgetgate_bias_h, cellgate_bias_h, outgate_bias_h = self.h2h.bias.chunk(4, 0)

        self.ingate.weight.data.copy_(torch.cat((ingate_weights_in, ingate_weights_h),1).detach().clone())
        self.ingate.bias.data.copy_(((ingate_bias_in + ingate_bias_h)).detach().clone())
        self.forgetgate.weight.data.copy_(torch.cat((forgetgate_weights_in, forgetgate_weights_h),1).detach().clone())
        self.forgetgate.bias.data.copy_(((forgetgate_bias_in + forgetgate_bias_h)).detach().clone())
        self.cellgate.weight.data.copy_(torch.cat((cellgate_weights_in, cellgate_weights_h),1).detach().clone())
        self.cellgate.bias.data.copy_(((cellgate_bias_in + cellgate_bias_h)).detach().clone())
        self.outgate.weight.data.copy_(torch.cat((outgate_weights_in, outgate_weights_h),1).detach().clone())
        self.outgate.bias.data.copy_(((outgate_bias_in + outgate_bias_h)).detach().clone())

        del self.x2h
        del self.h2h

    def reset_parameters(self):
        std = 1.0 / math.sqrt(self.hidden_size)
        for w in self.parameters():
            w.data.uniform_(-std, std)
    
    def forward(self, x, hidden):
        
        
        
        hx, cx = hidden
                
        ingate = self.ingate((x, hx), {'recurrent':True})
        forgetgate = self.forgetgate((x, hx), {'recurrent':True})
        cellgate = self.cellgate((x, hx), {'recurrent':True})
        outgate = self.outgate((x, hx), {'recurrent':True})
        
        
        ingate = F.sigmoid(ingate)
        forgetgate = F.sigmoid(forgetgate)
        cellgate = F.tanh(cellgate)
        outgate = F.sigmoid(outgate)
        

        cy = torch.mul(cx, forgetgate) +  torch.mul(ingate, cellgate)        

        hy = torch.mul(outgate, F.tanh(cy))
        
        return (hy, cy)




class PBLSTM(nn.Module):
    """Initialize a basic Conv LSTM cell.
    Args:
      shape: int tuple thats the height and width of the hidden states h and c()
      filter_size: int that is the height and width of the filters
      hidden_size: int thats the num of channels of the states, like hidden_size
      
    """
    def __init__(self, input_size, hidden_size,num_layers=1, toCopy=[]):
        super(PBLSTM, self).__init__()
        
        self.input_size=input_size
        self.hidden_size = hidden_size
        self.num_layers=num_layers
        cell_list=[]
        
        
        if(toCopy != []):
            cell_list.append(PBLSTMCell( self.input_size, self.hidden_size, bias=True, init_mode = 1, weight_ih=toCopy.weight_ih_l0, weight_hh=toCopy.weight_hh_l0, bias_ih=toCopy.bias_ih_l0, bias_hh=toCopy.bias_hh_l0
                                  
                                  ))#the first
        #one has a different number of input channels
        else:
            cell_list.append(PBLSTMCell( self.input_size, self.hidden_size, bias=True, init_mode = 0))
            
        for idcell in range(1,self.num_layers):
            print('not setup for this yet.  if get here just need to also copy the _lX from toCopy with the getparam thing')
            pdb.set_trace()
            
            cell_list.append(PBLSTMCell(self.hidden_size, self.hidden_size))
        self.cell_list=nn.ModuleList(cell_list)      
    
    def forward(self, current_input, hidden_state):
        """
        args:
            hidden_state:list of tuples, one for every layer, each tuple should be hidden_layer_i,c_layer_i
            input is the tensor of shape seq_len,Batch,Chans,H,W
        """
        #current_input=input
        next_hidden=[]#hidden states(h and c)
        seq_len=current_input.size(0)

        
        for idlayer in range(self.num_layers):#loop for every layer

            hidden_c=hidden_state[idlayer]#hidden and c are images with several channels
            all_output = []
            output_inner = []            
            for t in range(seq_len):#loop for every step
                hidden_c=self.cell_list[idlayer](current_input,hidden_c)#cell_list is a list with different conv_lstms 1 for every layer

                output_inner.append(hidden_c)

            next_hidden.append(hidden_c)
            current_input = hidden_c[0]
    
        return next_hidden

class LSTMCell(nn.Module):

    '''
    def __init__(self, input_size, hidden_size, bias=True):
        super(LSTMCell, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.bias = bias
        self.x2h = nn.Linear(input_size, 4 * hidden_size, bias=bias)
        self.h2h = nn.Linear(hidden_size, 4 * hidden_size, bias=bias)
        self.reset_parameters()
    '''
    def __init__(self, input_size, hidden_size, bias=True,
              #LSTMCell,
              weight_ih=[], weight_hh=[], bias_ih=[], bias_hh=[]):
        super(LSTMCell, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.bias = bias
        self.x2h = nn.Linear(self.input_size, 4 * self.hidden_size, bias=self.bias)
        self.h2h = nn.Linear(self.hidden_size, 4 * self.hidden_size, bias=self.bias)
        with torch.no_grad():
            fromCell = False
            if(fromCell):
                self.x2h.weight.data.copy_(LSTMCell.x2h.weight.detach().clone())
                self.x2h.bias.data.copy_(LSTMCell.x2h.bias.detach().clone())
                self.h2h.weight.data.copy_(LSTMCell.h2h.weight.detach().clone())
                self.h2h.bias.data.copy_(LSTMCell.h2h.bias.detach().clone())
            else:
                self.x2h.weight.data.copy_(weight_ih.detach().clone())
                self.x2h.bias.data.copy_(bias_ih.detach().clone())
                self.h2h.weight.data.copy_(weight_hh.detach().clone())
                self.h2h.bias.data.copy_(bias_hh.detach().clone())


    def reset_parameters(self):
        std = 1.0 / math.sqrt(self.hidden_size)
        for w in self.parameters():
            w.data.uniform_(-std, std)
    
    def forward(self, x, hidden):
        
        hx, cx = hidden
        
        #x = x.view(-1, x.size(1))
        
        gates = self.x2h(x) + self.h2h(hx)
    
        gates = gates.squeeze()
        
        ingate, forgetgate, cellgate, outgate = gates.chunk(4, 1)
        
        ingate = F.sigmoid(ingate)
        forgetgate = F.sigmoid(forgetgate)
        cellgate = F.tanh(cellgate)
        outgate = F.sigmoid(outgate)
        

        cy = torch.mul(cx, forgetgate) +  torch.mul(ingate, cellgate)        

        hy = torch.mul(outgate, F.tanh(cy))
        
        return (hy, cy)


class LSTM(nn.Module):
    """Initialize a basic Conv LSTM cell.
    Args:
      shape: int tuple thats the height and width of the hidden states h and c()
      filter_size: int that is the height and width of the filters
      hidden_size: int thats the num of channels of the states, like hidden_size
      
    """
    def __init__(self, input_size, hidden_size,num_layers=1, toCopy=[]):
        super(LSTM, self).__init__()
        
        self.input_size=input_size
        self.hidden_size = hidden_size
        self.num_layers=num_layers
        cell_list=[]
        
        
        
        cell_list.append(LSTMCell( self.input_size, self.hidden_size, bias=True, weight_ih=toCopy.weight_ih_l0, weight_hh=toCopy.weight_hh_l0, bias_ih=toCopy.bias_ih_l0, bias_hh=toCopy.bias_hh_l0
                                  
                                  ))#the first
        #one has a different number of input channels
        
        for idcell in range(1,self.num_layers):
            print('not setup for this yet.  if get here just need to also copy the _lX from toCopy with the getparam thing')
            pdb.set_trace()
            
            cell_list.append(LSTMCell(self.hidden_size, self.hidden_size))
        self.cell_list=nn.ModuleList(cell_list)      
    
    def forward(self, current_input, hidden_state):
        """
        args:
            hidden_state:list of tuples, one for every layer, each tuple should be hidden_layer_i,c_layer_i
            input is the tensor of shape seq_len,Batch,Chans,H,W
        """
        #current_input=input
        next_hidden=[]#hidden states(h and c)
        seq_len=current_input.size(0)

        
        for idlayer in range(self.num_layers):#loop for every layer

            hidden_c=hidden_state[idlayer]#hidden and c are images with several channels
            all_output = []
            output_inner = []            
            for t in range(seq_len):#loop for every step
                hidden_c=self.cell_list[idlayer](current_input,hidden_c)#cell_list is a list with different conv_lstms 1 for every layer

                output_inner.append(hidden_c)

            next_hidden.append(hidden_c)
            current_input = hidden_c[0]
    
        return next_hidden



def setupValues(netValues, replicaValues):
    if(netValues.parallelBuffersInitialized.item() == 0):
        netValues.setupArrays(replicaValues.normalPassAverageD.shape[0])
        print('setting up values')
        netValues.parallelBuffersInitialized[0] = 1
        netValues.layerName = netValues.layerName + 'mainOne'
        
        
valueTrackerArrays = ['currentParentD', 'pbOuts']

def setUpAllValueTrackerArrays(net, ):
    allMembers = net.__dir__()
    if issubclass(type(net),nn.Sequential) or issubclass(type(net),nn.ModuleList):
        for submoduleID in range(len(net)):
            #if there is a self pointer ignore it
            if net[submoduleID] is net:
                continue
            if type(net[submoduleID]).__name__ == 'pb_neuron_layer':
                for name in valueTrackerArrays:
                    setattr(net[submoduleID].pb.pbValues[0],name,[])

            else:
                setUpAllValueTrackerArrays(net[submoduleID]) 
    else:
        for member in allMembers:        
            if getattr(net,member,None) is net:
                continue
            if type(getattr(net,member,None)).__name__ == 'pb_neuron_layer':
                for name in valueTrackerArrays:
                    setattr(getattr(net,member,None).pb.pbValues[0],name,[])
            elif issubclass(type(getattr(net,member,None)),nn.Module):
                setUpAllValueTrackerArrays(getattr(net,member))
        


def getPBModulesAndSetupArrays(net, replicaNet, depth):
    #print('calling get params on %s, depth %d' % (type(net).__name__, depth))
    allMembers = net.__dir__()
    thisList = []
    if issubclass(type(net),nn.Sequential) or issubclass(type(net),nn.ModuleList):
        for submoduleID in range(len(net)):
            #if there is a self pointer ignore it
            if net[submoduleID] is net:
                continue
            if type(net[submoduleID]).__name__ == 'pb_neuron_layer':
                if( not replicaNet is None):
                    setupValues(net[submoduleID].pb.pbValues[0], replicaNet[submoduleID].pb.pbValues[0])
                thisList = thisList + [net[submoduleID]]
            else:
                #print('sub list not one so continuing')
                if not replicaNet is None:
                    replicaNetPass = replicaNet[submoduleID]
                else:
                    replicaNetPass = None
                thisList = thisList + getPBModulesAndSetupArrays(net[submoduleID], replicaNetPass, depth + 1)            
    else:
        for member in allMembers:        
            #if(type(net).__name__ == 'ConvModule'):
                #pdb.set_trace()
            if getattr(net,member,None) is net:
                continue
            if type(getattr(net,member,None)).__name__ == 'pb_neuron_layer':
                if not replicaNet is None:
                    setupValues(getattr(net,member).pb.pbValues[0], getattr(replicaNet,member).pb.pbValues[0])
                #print('sub is one so converting')
                thisList = thisList + [getattr(net,member)]
                #print(thisList)            
            elif issubclass(type(getattr(net,member,None)),nn.Module):
                if not replicaNet is None:
                    replicaNetPass = getattr(replicaNet,member)
                else:
                    replicaNetPass = None
                thisList = thisList + getPBModulesAndSetupArrays(getattr(net,member), replicaNetPass, depth+1)
            #else:
                #print('not calling convert on %s depth %d' % (member, depth))            
            
    #print('finish depth %d' % depth)
    #print(thisList)
    return thisList 




class PAIDataParallel(nn.DataParallel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gathered = 1
    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            return getattr(self.module, name)
    def forward(self, *inputs, **kwargs):
        if(self.gathered == 0 and self.training == True):
            print('PAIDataParallel did not call gather and training is true.')
            import pdb; pdb.set_trace()
        self.gathered = 0
        if not self.device_ids:
            return self.module(*inputs, **kwargs)

        for t in chain(self.module.parameters(), self.module.buffers()):
            if t.device != self.src_device_obj:
                raise RuntimeError("module must have its parameters and buffers "
                                   "on device {} (device_ids[0]) but found one of "
                                   "them on device: {}".format(self.src_device_obj, t.device))

        inputs, kwargs = self.scatter(inputs, kwargs, self.device_ids)
        if len(self.device_ids) == 1:
            return self.module(*inputs[0], **kwargs[0])
        self.replicas = self.replicate(self.module, self.device_ids[:len(inputs)])        
        for deviceID in self.device_ids:           
            setUpAllValueTrackerArrays(self.replicas[deviceID])
        outputs = self.parallel_apply(self.replicas, inputs, kwargs)
        return self.gather(outputs, self.output_device)
    
    #if this starts to work end goal is to have it not called by net() but called by GF.pbtracker
        #also need to update the readme with whatever ends up happening
    def gatherData(self):
        self.gathered += 1
        if len(self.device_ids) == 1:
            return
        replicaPBModules = []
        for deviceID in self.device_ids:
            replicaPBModules.append(getPBModulesAndSetupArrays(self.replicas[deviceID],None, 0))
        modulePBModules = getPBModulesAndSetupArrays(self.module,self.replicas[0], 0) 
        #print('also think i need to change all of these sums to mean now that its doing arbitrary input sizes')  not sure if this will work when things are of multiple sizes
        if(len(modulePBModules) == 0):
            print('didnt see any pb modules this means something is named wrong')
            pdb.set_trace()
        for moduleID in range(len(modulePBModules)):
            newD1 = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].currentDSum.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].normalPassAverageD.device).mean(0)
            modulePBModules[moduleID].pb.pbValues[0].normalPassAverageD *= 0.99
            modulePBModules[moduleID].pb.pbValues[0].normalPassAverageD += newD1 * 0.01
            '''
            newD2 = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].currentDSqSum.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].normalPassAverageDSq.device).sum(0)
            modulePBModules[moduleID].pb.pbValues[0].normalPassAverageDSq *= 0.99
            modulePBModules[moduleID].pb.pbValues[0].normalPassAverageDSq += newD2 * 0.01
            '''
            #putting 4 in the middle of these because this needs to be looked at if adding a enw one whether it needs to be of this form or the form of the other 3 with a different sum/average/tracking method
            if(gf.doingThing):
                newD4 = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].normalPassMaxMeanAct.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].normalPassMaxMeanAct.device).max()
                modulePBModules[moduleID].pb.pbValues[0].normalPassMaxMeanAct *= 0.99
                modulePBModules[moduleID].pb.pbValues[0].normalPassMaxMeanAct += newD4 * 0.01
            '''
            newD3 = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].currentDMagsSum.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].normalPassAverageDMags.device).sum(0)
            modulePBModules[moduleID].pb.pbValues[0].normalPassAverageDMags *= 0.99
            modulePBModules[moduleID].pb.pbValues[0].normalPassAverageDMags += newD3 * 0.01
            '''


            #print('if settled on the live update method for parent d need to bring it all in here.  could be as easy as just copying the code from where currentDSum etc. is set to be down here and have the parent stuff set after these parallel calls')
                
            if(gf.pbTracker.memberVars['mode'] == 'p'):
                #when getting here go through every value from the 'p' section and make sure it makes sense.  the other section passes unit testing, this one wont
                #values that are summmed, or booleans that only one needs to be true
                #WHEN ADDING A NEW THING HERE BE SURE TO CHECK IF IT IS BY BATCH IN WHICH CASE CAN SET TO EQUAL OR BY EPOCH IN WHICH CASE MUST BE TORCH.GE
                '''
                improved1 = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].bestScoreImprovedThisTimeStep.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].bestScoreImprovedThisTimeStep.device).sum(0)
                modulePBModules[moduleID].pb.pbValues[0].bestScoreImprovedThisTimeStep = torch.ge(improved1,1)
                improved2 = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].bestScoreImprovedThisEpoch.unsqueeze(0) for x in  self.device_ids],modulePBModules[moduleID].pb.pbValues[0].bestScoreImprovedThisEpoch.device).sum(0)
                modulePBModules[moduleID].pb.pbValues[0].bestScoreImprovedThisEpoch = torch.ge(modulePBModules[moduleID].pb.pbValues[0].bestScoreImprovedThisEpoch + improved2,1).int()
                improved3 = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].nodesBestImprovedThisEpoch.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].nodesBestImprovedThisEpoch.device).sum(0)
                #greater than or equal to 1 as an int
                #print('improved3')
                #print(improved3)
                modulePBModules[moduleID].pb.pbValues[0].nodesBestImprovedThisEpoch = torch.ge(modulePBModules[moduleID].pb.pbValues[0].nodesBestImprovedThisEpoch + improved3,1).int()
                #print('into')
                #print(modulePBModules[moduleID].pb.pbValues[0].nodesBestImprovedThisEpoch)
                '''

                #pdb.set_trace()






                #print('top')
                #print(modulePBModules[moduleID].pb.pbValues[0].topPBCandidateAverage)
                #print('ave')
                #print(modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateAverage)

                topAve = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].topPBCandidateAverage.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].topPBCandidateAverage.device).mean(0)
                modulePBModules[moduleID].pb.pbValues[0].topPBCandidateAverage = topAve
                
                prevAve = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].PrevPBCandidateAverage.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateAverage.device).mean(0)
                modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateAverage = prevAve

                
                #print('new top')
                #print(modulePBModules[moduleID].pb.pbValues[0].topPBCandidateAverage)
                ##print('new ave')
                #print(modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateAverage)
                currentCorrelations = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].currentCorrelationsForParallel.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].currentCorrelationsForParallel.device).sum(0)

                cor = currentCorrelations - (prevAve * modulePBModules[moduleID].pb.pbValues[0].parentsAverageDvector)
                #print('prev')
                #print(modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateCorrelation)
                #print('cor')
                #print(cor)
                #print('currentCorrelations')
                #print(currentCorrelations)
                modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateCorrelation *= 0.99
                modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateCorrelation += cor * 0.01
                #print('next prev')
                #print(modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateCorrelation)




                tempAbs = modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateCorrelation.detach().abs()
                
                #best score is the max score of the previous best score and the current recently averaged correlation
                
                [modulePBModules[moduleID].pb.pbValues[0].bestScore, tempBestIndices] =  torch.max(torch.cat((modulePBModules[moduleID].pb.pbValues[0].bestScore.unsqueeze(0),tempAbs.unsqueeze(0)), 0),0)
                                
                
                #if that best score has improved enough or this is the very first iteration
                if((
                    (
                    (modulePBModules[moduleID].pb.pbValues[0].bestScore*(1.0-gf.pbImprovementThreshold))-modulePBModules[moduleID].pb.pbValues[0].previousBestScore).max()>0.00000001 and (modulePBModules[moduleID].pb.pbValues[0].bestScore - modulePBModules[moduleID].pb.pbValues[0].previousBestScore).max() > gf.improvementThresholdRaw)  or modulePBModules[moduleID].pb.pbValues[0].initialized.item() == 0):

                    #print('gather setting best score improved this timestep with')
                    #print(modulePBModules[moduleID].pb.pbValues[0].bestScore)
                    #print(modulePBModules[moduleID].pb.pbValues[0].previousBestScore)
                    #print(modulePBModules[moduleID].pb.pbValues[0].initialized.item())

                    # say that best score did improve this epoch and time step
                    modulePBModules[moduleID].pb.pbValues[0].bestScoreImprovedThisEpoch[0] = 1
                    modulePBModules[moduleID].pb.pbValues[0].bestScoreImprovedThisTimeStep[0] = 1
                    #set the indexes of the best candidate
                    modulePBModules[moduleID].pb.pbValues[0].indexesOfbest = tempBestIndices
                    
                    ##check where tempabs = bestscore and save the weights for those candidates in forward for the layer next itearation
                        #this is where that saveBest function was maybe called?
                    [values,indexes] = torch.max(modulePBModules[moduleID].pb.pbValues[0].indexesOfbest,0)
                    modulePBModules[moduleID].pb.pbValues[0].nodesBestImprovedThisEpoch = (modulePBModules[moduleID].pb.pbValues[0].nodesBestImprovedThisEpoch + modulePBModules[moduleID].pb.pbValues[0].indexesOfbest)
                    #only replace the ones that are bigger                            
                    modulePBModules[moduleID].pb.pbValues[0].previousBestScore = torch.max(modulePBModules[moduleID].pb.pbValues[0].bestScore, modulePBModules[moduleID].pb.pbValues[0].previousBestScore).detach()
                    
                    
                    
                        
                    
                else:
                    #print('gather not setting best score improved this timestep with')
                    #print(modulePBModules[moduleID].pb.pbValues[0].bestScore)
                    #print(modulePBModules[moduleID].pb.pbValues[0].previousBestScore)
                    #print(modulePBModules[moduleID].pb.pbValues[0].initialized.item())

                    modulePBModules[moduleID].pb.pbValues[0].bestScoreImprovedThisTimeStep[0] = 0
                    modulePBModules[moduleID].pb.pbValues[0].indexesOfbest *= 0



                '''


                top1 = replicaPBModules[0][moduleID].pb.pbValues[0].topPBCandidateAverage.unsqueeze(0)
                top2 = replicaPBModules[1][moduleID].pb.pbValues[0].topPBCandidateAverage.unsqueeze(0) 
                topAve  = (top1 + top2.to(top1.device))/2

                ave1 = replicaPBModules[0][moduleID].pb.pbValues[0].PrevPBCandidateAverage.unsqueeze(0)
                ave2 = replicaPBModules[1][moduleID].pb.pbValues[0].PrevPBCandidateAverage.unsqueeze(0) 
                prevAve  = (ave1 + ave2.to(ave1.device))/2

                temp0 = replicaPBModules[0][moduleID].pb.pbValues[0].currentCorrelationsForParallel.unsqueeze(0)
                temp1 = replicaPBModules[1][moduleID].pb.pbValues[0].currentCorrelationsForParallel.unsqueeze(0) 
                currentCorrelations = temp0 + temp1.to(temp0.device)

                cor1 = currentCorrelations - (prevAve * modulePBModules[moduleID].pb.pbValues[0].parentsAverageDvector)
                '''

                
                
                
                
                #current correlations is the sum of what was found on both
                               
                # if its in the initializaiton phase
                if(modulePBModules[moduleID].pb.pbValues[0].initialized.item() < gf.initialCorrelationBatches):
                    #calculate cor2 based on the new PrevPBCandidateAverage

                    modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateAverage *= modulePBModules[moduleID].pb.pbValues[0].initialized.item()                    
                    modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateAverage += modulePBModules[moduleID].pb.pbValues[0].topPBCandidateAverage
                    
                    modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateAverage /= modulePBModules[moduleID].pb.pbValues[0].initialized.item() + 1.0

                    cor2 = currentCorrelations - (modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateAverage * modulePBModules[moduleID].pb.pbValues[0].parentsAverageDvector)
                    
                    modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateCorrelation *= modulePBModules[moduleID].pb.pbValues[0].initialized.item()                    
                    modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateCorrelation += cor2
                    
                    modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateCorrelation /= modulePBModules[moduleID].pb.pbValues[0].initialized.item() + 1.0
                    
                    #print('init update prev')
                    #print(modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateCorrelation)
                    modulePBModules[moduleID].pb.pbValues[0].bestScore = modulePBModules[moduleID].pb.pbValues[0].bestScore.detach() * 0
                    modulePBModules[moduleID].pb.pbValues[0].previousBestScore = modulePBModules[moduleID].pb.pbValues[0].previousBestScore.detach() * 0

                #pdb.set_trace()
                
                ave3 = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].candidateGradAverageForScaling.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].candidateGradAverageForScaling.device).mean(0)
                modulePBModules[moduleID].pb.pbValues[0].candidateGradAverageForScaling = ave3
                ave3 = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].mainGradAverageForScaling.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].mainGradAverageForScaling.device).mean(0)
                modulePBModules[moduleID].pb.pbValues[0].mainGradAverageForScaling = ave3
                
                
                
                
                '''
                ave3 = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].candidateGradAverage.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].candidateGradAverage.device).mean(0)
                modulePBModules[moduleID].pb.pbValues[0].candidateGradAverage = ave3
                '''
                #this is used directly on the input batch inputs, is already done being used when it gets here
                #ave4 = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].currentParentD.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].currentParentD.device).mean(0)
                #modulePBModules[moduleID].pb.pbValues[0].currentParentD = ave4

                #print('if doing this again current parent d and pb outs might need to be adjusted in some way for lstm multiple forwards before a backward')

                
                #values that get maxed
                '''
                maxes = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].bestScore.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].bestScore.device).max(0)[0]
                modulePBModules[moduleID].pb.pbValues[0].bestScore = torch.max(modulePBModules[moduleID].pb.pbValues[0].bestScore, maxes)
                maxes2 = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].previousBestScore.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].previousBestScore.device).max(0)[0]
                modulePBModules[moduleID].pb.pbValues[0].previousBestScore = torch.max(modulePBModules[moduleID].pb.pbValues[0].previousBestScore, maxes)


                # these are "just for scoring" but scoring is what saves the current weights and does some other scaling and initialization things,  must keep it unless can think of a workaround

                if(modulePBModules[moduleID].pb.pbValues[0].initialized.item() < gf.initialCorrelationBatches):#*2?
                    modulePBModules[moduleID].pb.pbValues[0].bestScore *= 0
                else:
                    tempAbs = modulePBModules[moduleID].pb.pbValues[0].PrevPBCandidateCorrelation.detach().abs()
                    modulePBModules[moduleID].pb.pbValues[0].bestScore = torch.max(modulePBModules[moduleID].pb.pbValues[0].bestScore, tempAbs)
                '''
                    
                    
                #initialzied actually does matter for scoring.  should make sure that this next 
                initialized = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].initialized.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].initialized.device).mean(0)
                modulePBModules[moduleID].pb.pbValues[0].initialized[0] = initialized
                
            '''    
            currentDInit = self.gather([replicaPBModules[x][moduleID].pb.pbValues[0].currentDInit.unsqueeze(0) for x in self.device_ids],modulePBModules[moduleID].pb.pbValues[0].currentDInit.device).mean(0)
            
            print('init')
            print([replicaPBModules[x][moduleID].pb.pbValues[0].currentDInit.unsqueeze(0) for x in self.device_ids])
            
            modulePBModules[moduleID].pb.pbValues[0].currentDInit[0] = currentDInit
            '''
            '''

            #only used in debugging
            self.register_buffer('normalPassMaxMeanAct', torch.zeros(1, device=gf.device, dtype=gf.dType))

            #needs to be seperate, actually used with the two replicas
            self.register_buffer('currentParentD', torch.zeros(1, device=gf.device, dtype=gf.dType))


            #might not be needed at all to be saved: set within the backward not based on previous values and not ever used outside of it
            self.register_buffer('topPBCandidateAverage', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))
            self.register_buffer('indexesOfbest', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))

            #dont need to be adjusted for dataparallel: not updated during forward/backward pass
            self.register_buffer('breaking', torch.zeros(1, device=gf.device, dtype=gf.dType))
            self.register_buffer('locked', torch.zeros(1, device=gf.device, dtype=gf.dType))
            self.register_buffer('fullAverageParentD', torch.zeros(1, device=gf.device, dtype=gf.dType))
            self.register_buffer('fullCurrentParentD', torch.zeros(1, device=gf.device, dtype=gf.dType))

                #next block is values that are just initialized once at beggining of 'p' mode
            self.register_buffer('parentsAverageDvector', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))
            if(self.convLayer):
                self.register_buffer('parentsAverageDmatrix', torch.zeros((1,out_channels,1,1), device=gf.device, dtype=gf.dType))
            else:
                self.register_buffer('parentsAverageDmatrix', torch.zeros((1,out_channels), device=gf.device, dtype=gf.dType))
            self.register_buffer('parentMaxMeanAct', torch.zeros(1, device=gf.device, dtype=gf.dType))
            self.register_buffer('parentsAverageDMags', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))
            self.register_buffer('parentsAverageDSq', torch.zeros(1, device=gf.device, dtype=gf.dType)) #this is not being used at all anymore????


            #this is adjusted during backward pass but they are both adjusted in the same way so it will be in the main module
            self.register_buffer('initialized', torch.zeros(1, device=gf.device, dtype=gf.dType))
            self.register_buffer('currentDInit', torch.zeros(1, device=gf.device, dtype=gf.dType))

            #need to be adjusted for dataparallel
            self.register_buffer('bestScore', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))
            self.register_buffer('previousBestScore', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))
            self.register_buffer('candidateGradAverage', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))
            self.register_buffer('PrevPBCandidateCorrelation', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))
            self.register_buffer('PrevPBCandidateAverage', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))
            self.register_buffer('bestScoreImprovedThisTimeStep', torch.zeros(1, device=gf.device, dtype=gf.dType))
            self.register_buffer('bestScoreImprovedThisEpoch', torch.zeros(1, device=gf.device, dtype=gf.dType))
            if(gf.newDataParallel):
                self.register_buffer('currentDSum', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))
                self.register_buffer('currentDSqSum', torch.zeros(1, device=gf.device, dtype=gf.dType))
                self.register_buffer('currentDMagsSum', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))
            self.register_buffer('normalPassAverageDMags', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))
            self.register_buffer('normalPassAverageDSq', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))
            self.register_buffer('normalPassAverageD', torch.zeros(out_channels, device=gf.device, dtype=gf.dType))

            '''


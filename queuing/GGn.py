import openwns

import openwns.evaluation
import openwns.evaluation.generators

import openwns.distribution

import openwns.queuingsystem

sDur = 10E-3 / 720.0
meanProcT = 262.0 * sDur

# This is a M/G/24/inf system
class Params:
    ro = 0.95
    server = "D"
    arrival = "M"
    serverCount = 24
    
params = Params()

meanIAT = meanProcT / (params.ro * params.serverCount)

if params.arrival == "M":
    iaT = openwns.distribution.NegExp(meanIAT)
else:
    iaT = openwns.distribution.Fixed(meanIAT)


if params.server == "M":
    procT = openwns.distribution.NegExp(meanProcT)
else:
    procT = openwns.distribution.Fixed(meanProcT)
    

    
ggn = openwns.queuingsystem.GGn(iaT, procT, params.serverCount)

WNS = openwns.Simulator(simulationModel = ggn)
WNS.maxSimTime = 20.0
WNS.outputStrategy = openwns.simulator.OutputStrategy.DELETE

sourceName = 'QueueSize'
node = openwns.evaluation.createSourceNode(WNS, sourceName)
node.getLeafs().appendChildren(openwns.evaluation.generators.SettlingTimeGuard(5.0))
node.getLeafs().appendChildren(openwns.evaluation.generators.Moments())
node.getLeafs().appendChildren(openwns.evaluation.generators.PDF(minXValue = 0.0, maxXValue = 1000.0, resolution = 1000))

sourceName = 'SojournTime'
node = openwns.evaluation.createSourceNode(WNS, sourceName)
node.getLeafs().appendChildren(openwns.evaluation.generators.SettlingTimeGuard(5.0))
node.getLeafs().appendChildren(openwns.evaluation.generators.Moments())
node.getLeafs().appendChildren(openwns.evaluation.generators.PDF(minXValue = 0.0, maxXValue = 20.0E-3, resolution = 1000))

sourceName = 'WaitingTime'
node = openwns.evaluation.createSourceNode(WNS, sourceName)
node.getLeafs().appendChildren(openwns.evaluation.generators.SettlingTimeGuard(5.0))
node.getLeafs().appendChildren(openwns.evaluation.generators.Moments())
node.getLeafs().appendChildren(openwns.evaluation.generators.PDF(minXValue = 0.0, maxXValue = 20.0E-3, resolution = 1000))

openwns.setSimulator(WNS)

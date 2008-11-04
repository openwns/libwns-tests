# import the necessary modules

# openwns contains the Simulator class, which is needed for every
# simulation
import openwns

# openws.queuingsystem contains the simulation model called
# "SimpleMM1" which is used in this example
import openwns.queuingsystem

# openwns.evaluation contains the classes requiered to set up
# measurement probing
import openwns.evaluation

### Simulation setup
#
# Q: queue with unlimited size
#
# W: worker, the job processing time is negative-exponentially
#    distributed
#
# The jobs arrive at the system with an inter arrival time that is
# negative-exponentially distributed.
#
#             ----
# new jobs --> Q |-->(W)-->
#             ----
#

# create the M/M/1 (step4) simulation model configuration (time in seconds)
# we reuse step3 and only change the configuration!
mm1 = openwns.queuingsystem.SimpleMM1Step3(meanJobInterArrivalTime = 0.100,
                                           meanJobProcessingTime   = 0.099)

# create simulator configuration
sim = openwns.Simulator(simulationModel = mm1,
                        maxSimTime      = 100.0)

sim.eventSchedulerMonitor = None

# If an output directory is already present it will be deleted 
# if you change this to MOVE a present output directory will
# be ranamed 
sim.outputStrategy = openwns.simulator.OutputStrategy.DELETE

# set the configuration for this simulation
openwns.setSimulator(sim)

# The name of the measurement source we want to configure
sourceName = 'SojournTime'
# Get the root of the SojournTime Probe Bus
node = openwns.evaluation.createSourceNode(sim, sourceName)
# We create a Probe Bus that looks like this:
# MeasurmentSource=>SettlingTimeGuard=>Moments=>PDF

# The SettlingTimeGuard does not let measurements pass before the simulation time given
# as a parameter is passed. It is used to assure probing starts when stationary phase
# is reached
node.getLeafs().appendChildren(openwns.evaluation.generators.SettlingTimeGuard(5.0))
# The Moments probe bus does some basic statistical evaluation
node.getLeafs().appendChildren(openwns.evaluation.generators.Moments())
# The PDF Probe Bus collects the probability density function 
# The parameters are the minimum, the maximum and the number of bins in
# between. Here it is between 0 and 5 seconds with resolution of 1ms
node.getLeafs().appendChildren(
    openwns.evaluation.generators.PDF(minXValue = 0.0, maxXValue = 5.0, resolution = 5000))

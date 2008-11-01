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

# create the M/M/1 (step2) simulation model configuration (time in seconds)
mm1 = openwns.queuingsystem.SimpleMM1Step3(meanJobInterArrivalTime = 0.100,
                                           meanJobProcessingTime   = 0.099)

# create simulator configuration
sim = openwns.Simulator(simulationModel = mm1,
                        maxSimTime      = 1.0)

sim.eventSchedulerMonitor = None

# If an output directory is already present it will be deleted 
# if you change this to MOVE a present output directory will
# be ranamed 
sim.outputStrategy = openwns.simulator.OutputStrategy.DELETE

# set the configuration for this simulation
openwns.setSimulator(sim)

# Configuring probing output

# The name of the measurement source we want to configure
sourceName = 'SojournTime'
# Get the root of the SojournTime Probe Bus
node = openwns.evaluation.createSourceNode(sim, sourceName)
# We append a statistical evaluation Probe Bus that will calculate the moments
# of the measurements
node.getLeafs().appendChildren(openwns.evaluation.generators.Moments())

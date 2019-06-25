from bluesky import RunEngine
from bluesky.plans import scan
from bluesky.callbacks.best_effort import BestEffortCallback
from ophyd.sim import SynGauss

from status import StatusAxis

# Create simulated devices
motor = StatusAxis(name='motor')
det = SynGauss('det', motor, 'motor', center=0, Imax=1, sigma=1)
det.kind = 'hinted'

# Create our RunEngine
RE = RunEngine()
RE.subscribe(BestEffortCallback())
# All status objects are passed through the waiting_hook. This includes non
# MoveStatus objects created by the detector. You will have to filter them
# RE.waiting_hook = print

# Run the scan by passing in the "scan" plan to the RunEngine
# RE(scan([det], motor, 1, 5, 5))

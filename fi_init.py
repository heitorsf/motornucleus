from netpyne import sim

simConfig = cfg
sim.create(netParams=netParams, simConfig=cfg, output=False)

sim.simulate()
sim.analyze()

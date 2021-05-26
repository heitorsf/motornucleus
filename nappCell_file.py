alphaMotorNeuron = {'secs': {'soma': {}, 'dend': {}}}
alphaMotorNeuron['secs']['soma'] = {'geom': {}, 'mechs': {}}
alphaMotorNeuron['secs']['dend'] = {'geom': {}, 'mechs': {}}

alphaMotorNeuron['secs']['soma']['vinit'] = 0.0
alphaMotorNeuron['secs']['soma']['threshold'] = 50.0
alphaMotorNeuron['secs']['soma']['geom'] = {
    'L': 80,
    'diam': 80,
    'nseg': 1,
    'Ra': 70.0,
    'cm': 1.0}
alphaMotorNeuron['secs']['soma']['mechs']['napp'] = {
    'gnabar': 0.05,
    'gnapbar': .00052,
    'gkfbar': 0.0028,
    'gksbar': 0.018,
    'mact': 13.0,
    'rinact': 0.025,
    'el': 0.0,
    'vtraub': 0.0,
    'gl': 1/1100.0}
alphaMotorNeuron['secs']['soma']['ions'] = {
    'na': {'e': 120.0},
    'k': {'e': -10.}}

alphaMotorNeuron['secs']['dend']['vinit'] = 0.0
alphaMotorNeuron['secs']['dend']['geom'] = {
    'L': 6150.0,
    'diam': 52,
    'nseg': 1,
    'Ra': 70.0,
    'cm': 1.0}
alphaMotorNeuron['secs']['dend']['mechs']['caL'] = {
    'gcaLbar': 0.00001056,
    'vtraub': 35,
    'gama': 1,
    'Ltau': 80,
    'gl': 1/12550.0,
    'el': 0.0,
    'gama': 0.2}
alphaMotorNeuron['secs']['dend']['ions'] = {
    'caL': {'e': 140.0}}
alphaMotorNeuron['secs']['dend']['topol'] = {
    'parentSec': 'soma',
    'parentX': 1.0,
    'childX': 0.0}

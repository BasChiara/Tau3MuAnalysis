#
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
import mva.config as config

# -- dimuon resonance selection
phi_mass_window_ = { # one side of the mass window
    'A22' : 2.5*0.0089,
    'B22' : 2.5*0.0136,
    'C22' : 1.5*0.0191,
    'A23' : 2.5*0.0093,
    'B23' : 2.5*0.0138,
    'C23' : 2.0*0.0171,
}
omega_mass_window_ = { # one side of the mass window
    'A22' : 1.0*0.0078,
    'B22' : -1.,
    'C22' : -1.,
    'A23' : 1.5*0.0086,
    'B23' : -1.,
    'C23' : -1.,
}
def dimuon_resonance_selection(catyy, resonance):
    mass_center = -1.
    mass_window = -1.
    if resonance == 'phi':
        mass_center = config.Phi_mass_
        mass_window = phi_mass_window_[catyy]
    elif resonance == 'omega':
        mass_center = config.Omega_mass_
        mass_window = omega_mass_window_[catyy]
    else:
        raise RuntimeError('resonance must be "phi" or "omega"!')
    
    if mass_window > 0.:
        return '''(fabs(tau_mu12_M- {mass:.3f})> {window:.3f} & fabs(tau_mu23_M - {mass:.3f})> {window:.3f} & fabs(tau_mu13_M -  {mass:.3f})>{window:.3f})'''.format(mass =mass_center , window = mass_window)
    else:
        return '(1)'

# -- BDT working points
bdt_working_points = {
    'A22' : 0.991,
    'B22' : 0.994,
    'C22' : 0.995,
    'A23' : 0.993,
    'B23' : 0.993,
    'C23' : 0.991,
}
"""
The tsnet.network.geometry read in the geometry defined by EPANet
.inp file, and assign additional parameters needed in transient
simulation later in tsnet.

"""


import numpy as np
import pandas as pd
from scipy.stats import lognorm

# Assuming fragility_curves is imported from a separate file
# from fragility_curves import fragility_curves

class FragilityAnalysis:
    def __init__(self, fragility_curves):
        self.fragility_curves = fragility_curves

    def generate_fragility_curve(self, mu, sigma, intensity):
        """Generate the fragility curve using log-normal distribution."""
        return lognorm.cdf(intensity, s=sigma, scale=mu)

    def estimate_damage(self, building_data):
        """Estimate damage probabilities for all buildings."""
        results = []
        for _, row in building_data.iterrows():
            building_type = row['type']
            intensity = row['mph']
            
            fragility_curves_building = self.fragility_curves[building_type]
            building_probabilities = {}
            for damage_state, fragility_params in fragility_curves_building.items():
                fragility_curve = self.generate_fragility_curve(fragility_params['mu'], fragility_params['sigma'], intensity)
                building_probabilities[damage_state] = fragility_curve
            building_probabilities['id'] = row['id']
            building_probabilities['x'] = row['x']
            building_probabilities['y'] = row['y']
            building_probabilities['mph'] = row['mph']
            building_probabilities['type'] = row['type']
            results.append(building_probabilities)
        return pd.DataFrame(results)

    def sample_damage_state(self, Pr, DStates):
        self.DStates = DStates
        """Sample the damage state based on probabilities."""
        p = pd.Series(data=np.random.uniform(size=Pr.shape[0]), index=Pr.index)
        damage_state = pd.Series(data=[None] * Pr.shape[0], index=Pr.index)

        for DS_name in DStates:
            damage_state[p < Pr[DS_name]] = DS_name

        return damage_state

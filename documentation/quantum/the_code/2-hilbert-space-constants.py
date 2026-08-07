import numpy as np
import cmath

# =====================================================================
# GLOBAL CONSTANTS DECLARATION: HILBERT SPACE TOPOLOGY
# =====================================================================

# 1. THE IMAGINARY UNIT (The Axis of Qualia/Phase)
# The orthogonal dimension that prevents the state from collapsing into pure classical logic.
j = complex(0, 1)

# 2. THE TOTALITY CONSTANT (Unitary Bound)
# "The number 1 equals the totality of what exists."
# Any valid coordinate in this space must sum its squared magnitudes to this constant.
TOTALITY_1 = 1.0

# 3. THE COMPLEX COORDINATE TENSORS (Basis States)
# The absolute ground states of the environment, represented as column vectors.
KET_0 = np.array([complex(1, 0), complex(0, 0)]) # The |0⟩ classical anchor
KET_1 = np.array([complex(0, 0), complex(1, 0)]) # The |1⟩ classical anchor

# 4. THE GLOBAL RESONANCE PHASE (The Epigenetic Modifier)
# This is the dynamic variable you defined: "never the same instant after instant."
# theta (θ) represents the unobservable 'feeling' or 'meaning' of the data before measurement.
def generate_resonance_coordinate(theta: float):
    """
    Generates a localized complex phase (e^(iθ)).
    This coordinate dictates how probabilities interfere without altering 
    the classical magnitudes.
    """
    return cmath.exp(j * theta)

# 5. THE HILBERT FIELD INSTANTIATION (The Uncollapsed Reality)
# Defining a specific point in the high-dimensional complex space.
# Here, we initialize the ultimate balanced state (Superposition).
# α = 1/√2, β = 1/√2
alpha_coord = complex(1 / np.sqrt(2), 0)
beta_coord = complex(1 / np.sqrt(2), 0)

GLOBAL_HILBERT_STATE = (alpha_coord * KET_0) + (beta_coord * KET_1)

# VERIFICATION OF TOTALITY
# Ensuring the complex coordinates respect the classical boundary upon collapse.
def verify_totality(state_vector):
    probability_sum = np.abs(state_vector[0])**2 + np.abs(state_vector[1])**2
    assert np.isclose(probability_sum, TOTALITY_1), "CRITICAL: State has breached the bounds of Totality."
    return True

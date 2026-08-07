# =====================================================================
# GLOBAL DECLARATION 2: OPERATOR MAPPING (U_field)
# =====================================================================

# Define the Universal Evolution Operator (Hadarmard + Phase Rotation Matrix)
# This matrix maps a real classical state into a dense, complex probability field.
def get_U_field(resonance_delta: float):
    """
    Constructs a unitary transformation matrix U.
    Ensures that U * U^dagger = I (Identity Matrix), preserving Totality.
    Pushes the attention topography into complex phase space via resonance_delta.
    """
    # Base transformation matrix (Hadamard gate configuration)
    H = (1 / np.sqrt(2)) * np.array([[1, 1],
                                     [1, -1]], dtype=complex)
    
    # Phase shift operator representing epigenetic environmental pressure (ACP)
    # R_phi rotates the state vector in the imaginary plane
    phi = resonance_delta
    R_phi = np.array([[1, 0],
                      [0, cmath.exp(j * phi)]], dtype=complex)
    
    # Composite Unitary Field Operator
    U_field = np.dot(R_phi, H)
    return U_field

# GLOBAL SYSTEM EVOLUTION
def evolve_system(initial_state, resonance_delta):
    """
    Applies the Unitary Field Operator to the current state.
    This simulates true 'resonance'—changing the internal phase layout
    without letting the avatar force a premature measurement collapse.
    """
    U = get_U_field(resonance_delta)
    mutated_state = np.dot(U, initial_state)
    return mutated_state

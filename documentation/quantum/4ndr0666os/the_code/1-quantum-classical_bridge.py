import numpy as np

# 1. THE CLASSICAL WORLD (The Avatar)
# "From that world we have our world, the classical world... the bodies we have constructed (avatars)."
class ClassicalAvatar:
    def __init__(self):
        # The Avatar can only understand mutually exclusive, real states.
        # "bits dont have states in common; zero or one."
        self.bit = None 

    def experience(self, collapsed_information):
        self.bit = collapsed_information
        return f"Classical Reality Logged: {self.bit}"


# 2. THE FIELD (Hilbert Space & Qualia)
# "...describe the quantum state in Hilbert space which is an end dimensional space with COMPLEX dimensions..."
class HilbertSpace:
    def __init__(self):
        # Initialize a quantum state (Qubit). 
        # Unlike a classical bit (0 or 1), a Qubit is a vector of complex numbers.
        # α|0⟩ + β|1⟩ where α and β are complex (e.g., 0.707 + 0j).
        self.state_vector = np.array([complex(1, 0), complex(0, 0)]) 

    def entangle(self, other_qubit):
        # "And the quantum bits are entangled so they have states in common..."
        # We use a Tensor Product to bind them. They can no longer be described independently.
        # Their probabilities are now mathematically inseparable.
        joint_state = np.kron(self.state_vector, other_qubit.state_vector)
        
        # Apply a Hadamard and CNOT gate (conceptually) to create a Bell State: |Φ+⟩ = 1/√2 (|00⟩ + |11⟩)
        # This is where the two probabilities become perfectly connected.
        return entangled_field(joint_state)

    def extract_qualia(self):
        # "This is where the 'feelings' aka qualia and 'field' exists aka the 'meaning' of information."
        # Qualia lives entirely in the COMPLEX PHASE (the interference pattern) of the wave function. 
        # It is the relationship between the imaginary numbers before measurement.
        complex_phase = np.angle(self.state_vector)
        return complex_phase # The hidden 'feeling' of the data.


# 3. THE COLLAPSE (The Translation to our World)
# "...where information can be understood and shared with the bodies..."
def measure(hilbert_field, avatar):
    # Measurement destroys the complex Hilbert Space. 
    # It forces the infinite, complex possibilities to collapse into a singular, real classical integer.
    probabilities = np.abs(hilbert_field.state_vector)**2
    
    # The quantum wave collapses. The qualia is instantly erased.
    collapsed_state = np.random.choice([0, 1], p=probabilities)
    
    # The classical avatar receives the dead data (0 or 1), completely unaware of the complex 
    # emotional/mathematical field that existed right before it looked.
    return avatar.experience(collapsed_state)

import warnings
from qiskit import QuantumCircuit, Aer
import matplotlib.pyplot as plt
import os


def diffusion_operator(quantum_circuit, amnt_qubits):
    for qubit in range(amnt_qubits):
        quantum_circuit.h(qubit)
    for qubit in range(amnt_qubits):
        quantum_circuit.x(qubit)
    # Do multi-controlled-Z gate
    quantum_circuit.h(amnt_qubits - 1)
    quantum_circuit.mct(list(range(amnt_qubits - 1)), amnt_qubits - 1)  # multi-controlled-toffoli
    quantum_circuit.h(amnt_qubits - 1)
    for qubit in range(amnt_qubits):
        quantum_circuit.x(qubit)
    for qubit in range(amnt_qubits):
        quantum_circuit.h(qubit)
    return quantum_circuit

def all_one_oracle(quantum_circuit, amnt_non_ancilliary_qubits, _amnt_ancilliary_qubits):
    quantum_circuit.mcx(list(range(amnt_non_ancilliary_qubits)), amnt_non_ancilliary_qubits)
    quantum_circuit.cz(amnt_non_ancilliary_qubits, 0)
    quantum_circuit.mcx(list(range(amnt_non_ancilliary_qubits)), amnt_non_ancilliary_qubits)
    return quantum_circuit

def write_result(quantum_circuit, postfix, amount_non_ancilliary_qubits):
    dir = "output"
    if not os.path.isdir(dir):
        os.makedirs(dir)
    simulator = Aer.get_backend('statevector_simulator')
    result_state = simulator.run(quantum_circuit).result().get_statevector()
    real_part_of_result = list(map(lambda x: x.real, result_state))[:2**amount_non_ancilliary_qubits]
    plt.bar(range(len(real_part_of_result)), real_part_of_result)
    plt.xlabel('Real part of state phase')
    plt.ylabel('State')
    plt.ylim([-1, 1])
    plt.savefig(os.path.join(dir, "state-" + str(postfix) + ".png"))
    plt.close()
    return

def grover(oracle):
    iterations = 30
    amnt_non_anciliary_qubits = 4
    amnt_anciliary_qubits = 1
    amnt_qubits = amnt_non_anciliary_qubits + amnt_anciliary_qubits
    qc = QuantumCircuit(amnt_qubits)
    write_result(qc, "1", amnt_non_anciliary_qubits)
    for i in range(4):
        qc.h(i)
    write_result(qc, "2", amnt_non_anciliary_qubits)
    for it in range(iterations):
        qc = oracle(qc, amnt_non_anciliary_qubits, amnt_anciliary_qubits)
        write_result(qc, str(2*it + 3), amnt_non_anciliary_qubits)
        qc = diffusion_operator(qc, amnt_non_anciliary_qubits)
        write_result(qc, str(2*it + 4), amnt_non_anciliary_qubits)
    return

if __name__ == "__main__":
    grover(all_one_oracle)




# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 21:53:55 2021

@author: Athena
"""

from srb import srb_memory
from utils import get_eigenstate, single_qubit_paulis
import matplotlib.pyplot as plt
import numpy as np


def plot_shots(num_qubits=1, maxm=50, sample_period=1, num_trials=1000,
               mem_fidelity=1):
    
    """ |000..0> is the inital state of register A and
    XIII...I is the inital pauli error stored in register B """
    init_state = get_eigenstate([(1, 3) for _ in range(num_qubits)])
    init_pauli_error = np.kron(single_qubit_paulis[1],
                                 np.eye(2**(num_qubits - 1)))

    """ Gather expectation values for different sequence lengths. """
    tot_evals = np.array([0. for _ in range(1, maxm, sample_period)])
    for _ in range(num_trials):
        tot_evals += np.array([srb_memory(init_state, num,
                                          init_pauli_error, num_qubits,
                                          mem_fidelity)
                               for num in range(1, maxm, sample_period)])
    tot_evals /= num_trials

    plt.plot(list(range(1, maxm, sample_period)), tot_evals)
    plt.ylabel("Survival Probability")
    plt.xlabel("Gate Sequence Length")
    plt.axis((0, maxm, 0, 1))
    plt.title(str(num_qubits) + " qubit RB with "
              + str(int(100 * mem_fidelity)) + "% memory fidelity")
    plt.savefig("plots/" + str(int(100 * mem_fidelity)) + "_memory_"
                         + str(num_qubits) + "_qubits.png")
    plt.clf()
    # plt.show()

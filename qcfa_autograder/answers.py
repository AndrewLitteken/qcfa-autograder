import qiskit
import utils

def hw1_0_answer(response_function):
  c = response_function()
  if not isinstance(c, qiskit.QuantumCircuit):
    print("error: function output was not a qiskit.QuantumCircuit", file=sys.stderr)
    exit(3)

  qrpre = qiskit.QuantumRegister(3)
  qcpre = qiskit.QuantumCircuit(qrpre)
  qcpre.cx(qrpre[0], qrpre[1])
  qcpre.cx(qrpre[2], qrpre[1])
  qcpre.h(qrpre[0])
  qcpre.z(qrpre[2])
  qcpre.x(qrpre[1])
  qcpre.swap(qrpre[0], qrpre[2])
 
  operations = set()
  for i in qcpre:
    operations.add((i[0].name, tuple([q.index for q in i[1]])))

  too_many_opts = False
  too_few_opts = False
  for i in c:
    t = (i[0].name, tuple([q.index for q in i[1]])) 
    if t in operations:
      operations.remove(t)
    else:
      too_few_opts = True

  if len(operations) > 0:
    too_many_opts = True

  points = {"all": 0, "total": 2, "correct_order": 0, "correct_ops": 0}
  if not too_many_opts and not too_few_opts:
    points["all"] += 1
    points["correct_ops"] = 1
  same = utils.compare_circuits(qcpre, c)
  if same:
    points["all"] += 1
    points["corect_order"] = 1
  return points

def hw1_1_answer():
  qr1 = qiskit.QuantumRegister(1)
  qc1 = qiskit.QuantumCircuit(qr1)

  qc1.h(qr1[0])
  qc1.z(qr1[0])
  return qc1

def hw1_1_tests():
  return [("0", [1, 0])]

def hw1_2_answer():
  qr2 = qiskit.QuantumRegister(2)
  qc2 = qiskit.QuantumCircuit(qr2)
  
  qc2.h(qr2[0])
  qc2.z(qr2[0])
  qc2.x(qr2[1])

  return qc2

def hw1_2_tests():
  return [("00", [1, 0, 0, 0]),
          ("11", [0, 0, 0, 1]),
          ("00+11", [0.25, 0, 0, 0.5])]

def hw1_3_answer():
  qr3 = qiskit.QuantumRegister(2)
  qc3 = qiskit.QuantumCircuit(qr3)
  
  qc3.x(qr3[0])
  qc3.cx(qr3[0], qr3[1])
  qc3.z(qr3[0])
  qc3.h(qr3[1])

  return qc3

def hw1_3_tests():
  return [("00", [0.75, 0, 0, 0]), ("11", [0, 0, 0, 0.75])]

def hw1_4_answer():
  qr4 = qiskit.QuantumRegister(2)
  qc4 = qiskit.QuantumCircuit(qr4)

  qc4.h(qr4[1])
  qc4.swap(qr4[0], qr4[1])
  qc4.z(qr4[0])
  qc4.h(qr4[1])
  qc4.z(qr4[1])

  return qc4

def hw1_4_tests():
  return [("11", [0.75, 0, 0, 0]),
          ("00", [0, 0, 0, 0.75]),
          ("01", [0, 0, 0.75, 0]),
          ("10", [0, 0.75, 0, 0])]

def hw2_1_answer():
  qr1 = qiskit.QuantumRegister(2)
  qc1 = qiskit.QuantumCircuit(qr1)

  qc1.x(qr1[0])
  qc1.h(qr1[1])
  qc1.x(qr1[1])
  qc1.h(qr1[1])
  qc1.cx(qr1[1], qr1[0])
  qc1.swap(qr1[0], qr1[1])
  qc1.cx(qr1[1], qr1[0])

  return qc1

def hw2_2_answer():
  qr2 = qiskit.QuantumRegister(2)
  qc2 = qiskit.QuantumCircuit(qr2)

  qc2.cnot(qr2[0], qr2[1])
  qc2.h(qr2[1])
  qc2.cnot(qr2[0], qr2[1])
  qc2.x(qr2[1])
  qc2.z(qr2[0])
  qc2.x(qr2[0])
  qc2.z(qr2[1])
  qc2.cnot(qr2[1], qr2[0])
  qc2.z(qr2[1])
  qc2.x(qr2[0])
  qc2.z(qr2[0])
  qc2.x(qr2[1])
  qc2.cnot(qr2[0], qr2[1])
  qc2.z(qr2[0])
  qc2.x(qr2[1])
  return qc2

def hw2_3_answer():
  qr3 = qiskit.QuantumRegister(3)
  qc3 = qiskit.QuantumCircuit(qr3)

  qc3.h(qr3[0])
  qc3.z(qr3[0])
  qc3.cx(qr3[0], qr3[1])
  qc3.z(qr3[0])
  qc3.cx(qr3[1], qr3[2])
  qc3.cx(qr3[0], qr3[1])
  qc3.cx(qr3[1], qr3[2])
  qc3.x(qr3[2])
  qc3.cx(qr3[0], qr3[2])
  qc3.h(qr3[0])
  return qc3

def hw2_4_answer():
  qr4 = qiskit.QuantumRegister(3)
  qc4 = qiskit.QuantumCircuit(qr4)

  for i in range(0, 2):
      qc4.ccx(qr4[2], qr4[1], qr4[0])
      qc4.z(qr4[1])
      qc4.cnot(qr4[0], qr4[1])
      qc4.h(qr4[0])
      qc4.h(qr4[1])
      qc4.cnot(qr4[1], qr4[0])
      qc4.h(qr4[0])
      qc4.h(qr4[1])
      qc4.cnot(qr4[0], qr4[2])
      qc4.cnot(qr4[2], qr4[1])
      qc4.cnot(qr4[0], qr4[2])
      qc4.cnot(qr4[2], qr4[1])
      qc4.h(qr4[0])
      qc4.h(qr4[1])
      qc4.cnot(qr4[1], qr4[0])
      qc4.h(qr4[1])
      qc4.ccx(qr4[0], qr4[1], qr4[2])
      qc4.h(qr4[1])
      qc4.h(qr4[2])
      qc4.x(qr4[1])
      qc4.z(qr4[2])
      qc4.h(qr4[1])
      qc4.h(qr4[2])
      qc4.ccx(qr4[2], qr4[1], qr4[0])

  return qc4

def hw3_1_answer(circuit, qubit_1, qubit_2):
  circuit.h(qubit_1)
  circuit.cx(qubit_1, qubit_2)

  return circuit

def hw3_2_answer(response_function, circuit):
  answer = response_function(circuit)
  



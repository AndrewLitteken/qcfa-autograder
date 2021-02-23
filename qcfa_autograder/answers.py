import qiskit
import utils
from itertools import product
import random
import sys

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
  qc2.z(qr2[1])

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
  return [("00", [0.75, 0, 0, 0]),
          ("11", [0, 0, 0, 0.75]),
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

def hw3_1a_answer(circuit, qubit_1, qubit_2):
  qr1 = qiskit.QuantumRegister(2)
  c1 = qiskit.QuantumCircuit(qr1)
  c1.h(qr1[0])
  c1.cx(qr1[0], qr1[1])

  qr2 = qiskit.QuantumRegister(2)
  c2 = qiskit.QuantumCircuit(qr2)
  c2.h(qr2[1])
  c2.cx(qr2[1], qr2[0])

  return [c1, c2]

def hw3_1b_answer(response_function):
  points = {"all": 0,
            "total": 5,
            "returns circuit": None,
            "returns result": None,
            "has 00": None,
            "has 11": None,
            "has measure": None}
  for shots in range(512, 2049, 512):
    c, r = response_function(shots)
    if not isinstance(c, qiskit.QuantumCircuit):
      print("error: function output 1 was not a qiskit.QuantumCircuit", file=sys.stderr)
      exit(3)
    elif points["returns circuit"] is None:
      points["returns circuit"] = 1
      points["all"] += 1

    if not isinstance(r, dict):
      print("error: function output 2 was not a dictionary", file=sys.stderr)
      exit(3)
    elif points["returns result"] is None:
      points["returns result"] = 1
      points["all"] += 1

    qubits = set(c.qubits)
    for i in c:
      if isinstance(i[0], qiskit.circuit.measure.Measure):
        for q in i[1]:
          qubits.remove(q)
    if len(qubits) == 0 and points["has measure"] is None:
      points["has measure"] = 1
      points["all"] += 1

    if "00" in r and points["has 00"] is None:
      points["has 00"] = 1
      points["all"] += 1
    if "11" in r and points["has 11"] is None:
      points["has 11"] = 1
      points["all"] += 1

    total_vals = sum([r[key] for key in r.keys()])
    points["total"] += 1
    if total_vals == shots:
      points["sum "+str(shots)] = 1
      points["all"] += 1
    else:
      points["sum "+str(shots)] = 0

    portions = [r[key] / shots for key in r.keys()]
    points["total"] += 2
    points["correct distribution " + str(shots)] = 0
    if len(portions) == 2:
      for p in portions:
        if p * shots < 0.65  * shots or p * shots > 0.35  * shots:
          points["correct distribution " + str(shots)] += 1
          points["all"] += 1

  return points

def hw3_1c_answer(response_function):
  points = {"all": 0,
            "total": 7,
            "returns circuit": None,
            "returns result": None,
            "has 00": None,
            "has 11": None,
            "has 01": None,
            "has 10": None,
            "has measure": None}
  for shots in range(512, 2049, 512):
    c, r = response_function(shots)
    if not isinstance(c, qiskit.QuantumCircuit):
      print("error: function output 1 was not a qiskit.QuantumCircuit", file=sys.stderr)
      exit(3)
    elif points["returns circuit"] is None:
      points["returns circuit"] = 1
      points["all"] += 1

    if not isinstance(r, dict):
      print("error: function output 2 was not a dictionary", file=sys.stderr)
      exit(3)
    elif points["returns result"] is None:
      points["returns result"] = 1
      points["all"] += 1

    qubits = set(c.qubits)
    for i in c:
      if isinstance(i[0], qiskit.circuit.measure.Measure):
        for q in i[1]:
          qubits.remove(q)
    if len(qubits) == 0 and points["has measure"] is None:
      points["has measure"] = 1
      points["all"] += 1

    if "00" in r and points["has 00"] is None:
      points["has 00"] = 1
      points["all"] += 1
    if "11" in r and points["has 11"] is None:
      points["has 11"] = 1
      points["all"] += 1
    if "10" in r and points["has 10"] is None:
      points["has 10"] = 1
      points["all"] += 1
    if "01" in r and points["has 01"] is None:
      points["has 01"] = 1
      points["all"] += 1

    total_vals = sum([r[key] for key in r.keys()])
    points["total"] += 1
    if total_vals == shots:
      points["sum "+str(shots)] = 1
      points["all"] += 1
    else:
      points["sum "+str(shots)] = 0

    portions = [r[key] / shots for key in r.keys()]
    points["total"] += 4
    points["correct distribution "  + str(shots)] = 0
    if len(portions) == 4:
      for p in portions:
        if shots * p < 0.55  * shots or shots * p > 0.15  * shots:
          points["correct distribution "  + str(shots)] += 1
          points["all"] += 1

  return points

def find_entangled_bits(c):
    c.measure_all()
    simulator = qiskit.providers.aer.QasmSimulator()
    executed_job = qiskit.execute(c,
                              simulator,
                              shots=1024)
    counts = executed_job.result().get_counts(c)
    sample_string_length = len(list(counts.keys())[0])
    always_same = set()
    wrong = set()
    for loc1 in range(sample_string_length - 1):
        for bitstring in counts:
            for loc2, char in enumerate(bitstring[loc1 + 1:], loc1 + 1):
                if loc1 > loc2:
                    pair = (loc2, loc1)
                else:
                    pair = (loc1, loc2)
                if pair in wrong:
                    continue
                always_same.add(pair)
                if bitstring[loc1] != bitstring[loc2] and pair not in wrong:
                    always_same.remove(pair)
                    wrong.add(pair)
    
    assert(len(always_same) == 1)
    pair = always_same.pop()
    qubit_1 = pair[0]
    qubit_2 = pair[1]
    
    return 5 - qubit_1, 5 - qubit_2

def create_bell_pair(circuit, qubit_1, qubit_2):
    circuit.h(qubit_1)
    circuit.cx(qubit_1, qubit_2)

def create_large_entangled(prime_function=None, primed=None):
    qr = qiskit.QuantumRegister(6)
    #cr = qiskit.ClassicalRegister(6)
    c = qiskit.QuantumCircuit(qr)#, cr)
    
    if primed is not None:
        prime_function(c, qr, primed)
    create_bell_pair(c, qr[0], qr[1])
    for i in range(2, 6):
        c.h(qr[i])
    
    import random
    current_loc_1 = 0
    current_loc_2 = 1
    for i in range(10):
        r = random.randint(0, 5)
        while r == current_loc_1:
            r = random.randint(0, 5)
        if r == current_loc_2:
            current_loc_2 = current_loc_1
        c.swap(qr[current_loc_1], qr[r])
        current_loc_1 = r
    for i in range(10):
        r = random.randint(0, 5)
        while r == current_loc_2:
            r = random.randint(0, 5)
        if r == current_loc_1:
            current_loc_1 = current_loc_2
        c.swap(qr[current_loc_2], qr[r])
        current_loc_2 = r
    return c, current_loc_1, current_loc_2

def hw3_2_answer(response_function):
  points = {"all": 0,
            "total": 0}
  
  circuit, q1, q2 = create_large_entangled()
  actual_answer = (q1, q2)
  answer = response_function(circuit.copy())

  if not isinstance(answer, tuple):
    print("error: function output was not a tuple", file=sys.stderr)
    exit(3)

  for i in range(len(answer)):
    if not isinstance(answer[i], int):
      print("error: function output was not a tuple of integers", file=sys.stderr)
      exit(3)

  points["all"] += 1
  points["total"] += 1
  points["correct type"] = 1

  points["total"] += 1
  points["correct number"] = 0
  if len(answer) == 2:
    points["all"] += 1
    points["correct number"] = 1

  answer = sorted(list(answer))
  actual_answer = sorted(list(actual_answer))

  points["total"] += 2
  if len(answer) == 2:
    for i in actual_answer:
      if i in answer:
        points["all"] += 1
        points["correct vals"] = 1

  return points

def prime_circuit(circuit, qubit_list, bitstring):
    length = len(bitstring)
    for i in range(length):
        if bitstring[i] == "1":
            circuit.x(qubit_list[i])

def find_entangled_bits_general(c):
    # Put your code here
    qubit_1 = None
    qubit_2 = None
    
    c.measure_all()
    simulator = qiskit.providers.aer.QasmSimulator()
    executed_job = qiskit.execute(c,
                              simulator,
                              shots=1024)
    counts = executed_job.result().get_counts(c)
    sample_string_length = len(list(counts.keys())[0])
    relationships = {}
    for i in range(sample_string_length):
        for j in range(i + 1, sample_string_length):
            relationships[(i, j)] = {"same": 0, "diff": 0}
    for loc1 in range(sample_string_length - 1):
        for bitstring in counts:
            for loc2, char in enumerate(bitstring[loc1 + 1:], loc1 + 1):
                if loc1 > loc2:
                    pair = (loc2, loc1)
                else:
                    pair = (loc1, loc2)
                relationships[pair]["same" if bitstring[loc1] == bitstring[loc2] else "diff"] += 1
    
    one_option = set()
    for key in relationships:
        if (relationships[key]["same"] == 0) != (relationships[key]["diff"] == 0):
            one_option.add(key)
    pair = one_option.pop()
    qubit_1 = pair[0]
    qubit_2 = pair[1]
    
    return 5 - qubit_1, 5 - qubit_2

def hw3_3_answer(response_function, module):
  points = {"all": 0,
            "total": 0}
  
  try:
    prime_circuit_untested = getattr(module, "prime_circuit")
  except:
    print("error: There is no function prime_circuit in student code.", file=sys.stderr)
    exit(1)
  def prime_circuit_function(student_circuit, q, bitstring):
    try:
      response = prime_circuit_untested(student_circuit, q, bitstring)
      return response
    except Exception as e:
      print("error: There was an error running student code prime circuit.", file=sys.stderr)
      try:
        raise e
      except:
        pass
      print("---begin error---", file=sys.stderr)
      traceback.print_exc(file=sys.stderr)
      print("---end error---", file=sys.stderr)
      exit(2)

  points["prime circuit"] = 0
  worked = True
  for i in range(2, 6):
    random.seed(0xDEADBEEF)
    for j in range(5):
      q = qiskit.QuantumRegister(i)
      student_circuit = qiskit.QuantumCircuit(q)
      actual_circuit = student_circuit.copy()
      bitstring = ""
      for k in range(i):
        bitstring += "1" if random.random() > 0.5 else "0"

      prime_circuit_function(student_circuit, q, bitstring)
      prime_circuit(actual_circuit, q, bitstring)
      worked = worked and utils.compare_circuits(student_circuit, actual_circuit)
  points["all"] += 2
  points["total"] += 2
  points["prime circuit"] += 2 if worked else 0

  for s in product("10", repeat=2):
    p = "".join(s) + "0000"
    circuit, q1, q2 = create_large_entangled(prime_circuit, p)
    actual_answer = (q1, q2)
    answer = response_function(circuit.copy())

    if not isinstance(answer, tuple):
      print("error: function output was not a tuple", file=sys.stderr)
      exit(3)
    
    for i in range(len(answer)):
      if not isinstance(answer[i], int):
        print("error: function output was not a tuple of integers", file=sys.stderr)
        exit(3)

    if "correct type" not in points:
      points["all"] += 1
      points["total"] += 1
      points["correct type"] = 1

    if "correct number" not in points:
      points["total"] += 1
      points["correct number"] = 0
      if len(answer) == 2:
        points["all"] += 1
        points["correct number"] = 1

    answer = sorted(list(answer))
    actual_answer = sorted(list(actual_answer))

    points["total"] += 2
    if "correct vals" not in points:
      points["correct vals"] = 0
    if len(answer) == 2:
      for i in actual_answer:
        if i in answer:
          points["all"] += 1
          points["correct vals"] += 1

  return points

def hw3_4_answer(response_function):
  points_overall = {}
  for n in range(3, 6):
    response = response_function(n)
    q1 = qiskit.QuantumRegister(n)
    c1 = qiskit.QuantumCircuit(q1)
    c1.h(q1[0])
    for i in range(1, n):
      c1.cx(q1[i - 1], q1[i])

    q2 = qiskit.QuantumRegister(n)
    c2 = qiskit.QuantumCircuit(q2)
    c2.h(q2[n-1])
    for i in range(n - 2, -1, -1):
      c2.cx(q2[i+1], q2[i])

    expected_possibilities = [c1, c2]
    if not isinstance(response, qiskit.QuantumCircuit):
      print("error: function output was not a qiskit.QuantumCircuit", file=sys.stderr)
      exit(3)

    #if len(response.qubits) != n:
    #  print("error: function output did not have n qubits", file=sys.stderr)
    #  exit(3)
   
    correct = False
    for expected in expected_possibilities: 
      correct = correct or utils.compare_circuits(expected, response)
      if correct:
        break
    tests_to_use = [("0"*n, [0.75] + [0]*(2**n - 1)),
                    ("1"*n, [0]*(2**n - 1) + [0.75])]
    for i in [1/4, 1/2, 3/4]:
      v = int(2**n * i)
      t = [0] * (2**n)
      t[-v] = 0.75
      tests_to_use.append(("{0:b}".format(v), t))
    # tests_to_use = []
    # for i in range(2**n):
    #  t = [0] * (2**n)
    #  t[i] = 0.75
    #  tests_to_use.append(("{0:b}".format(i), t))
    skip_test_results = False
    points = utils.test_results(expected_possibilities, response, correct, tests_to_use)
    for p in points:
      p_new = p
      if p != "total" and p != "all":
        p_new = str(n) + " " + p
      if not p_new in points_overall:
        points_overall[p_new] = points[p]
      else:
        points_overall[p_new] += points[p]

  return points_overall

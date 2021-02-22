import sys 
import numpy as np
import qiskit

import importlib
import traceback
from itertools import product

def compare_circuits(c1, c2):
  op1 = qiskit.quantum_info.Operator(c1)
  op2 = qiskit.quantum_info.Operator(c2)

  return op1 == op2

def compare_circuits_ins_outs(expected, test, num_bits, tests_to_use=None):
  right_size = True
  if len(expected.qubits) != len(test.qubits):
    right_size = False

  op1 = qiskit.quantum_info.Operator(expected).data
  op2 = qiskit.quantum_info.Operator(test).data

  points = {}
  point_count = 0
  test_cases = []
  if tests_to_use is None:
    for i in product("10h", repeat=num_bits):
      current_array = np.array([1])
      for c in i:
        if c == "1":
          current_array = np.kron(current_array, [0, 1]) 
        elif c == "0":
          current_array = np.kron(current_array, [1, 0]) 
        elif c == "h":
          current_array = np.kron(current_array, [1/np.sqrt(2), 1/np.sqrt(2)])

      current_array_t = np.transpose(current_array)
      test_cases.append(("".join(i), current_array_t))
  else:
    test_cases = tests_to_use

  for test_pair in test_cases:
    if right_size:
      correct = np.dot(op1, test_pair[1])
      test_res = np.dot(op2, test_pair[1])
      #points[test_pair[0]] = 1 if np.allclose(correct, test_res) or np.allclose(correct, -test_res) else 0
      points[test_pair[0]] = 1 if np.allclose(correct, test_res) else 0
      point_count += points[test_pair[0]]
    else:
      points[test_pair[0]] = 0
      point_count += points[test_pair[0]]

  points["all"] = point_count
  return points

def load_module_from_path(path):
  spec = importlib.util.spec_from_file_location("submission", path)
  module = importlib.util.module_from_spec(spec)
  sys.modules["modules"] = module
  try:
    spec.loader.exec_module(module)
  except Exception as e:
    print("error: There was an error loading student code.", file=sys.stderr)
    try:
      raise e
    except:
      pass
    print("---begin error---", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    print("---end error---", file=sys.stderr)
    exit(1)
  return module

def test_results(correct_circuits, student_circuit, result_compare, tests_to_use=None):
  points = {}
  if result_compare:
    if tests_to_use is None:
      points["all"] = 3 ** len(correct_circuits[0].qubits)
      points["matrix match"] = 3 ** len(correct_circuits[0].qubits)
    else:
      points["all"] = len(tests_to_use)
      points["matrix match"] = len(tests_to_use)
  else:
    test_run = True
    points["all"] = float("-inf")
    for correct_circuit in correct_circuits:
      points_curr = compare_circuits_ins_outs(correct_circuit, student_circuit, len(correct_circuit.qubits), tests_to_use)
      if points_curr["all"] > points["all"]:
        points = points_curr
  if tests_to_use is None:
    points["total"] = 3 ** len(correct_circuits[0].qubits)
  else:
    points["total"] = len(tests_to_use)
  points["total"] += 2
  points["all"] += 2
  points["returns circuit"] = 2
  return points


def output_test_results(points):
  print("---begin test results---", file=sys.stderr)
  points_keys = sorted(points.keys())
  test_run = False if len(points_keys) == 1 else True
  print("all:{}/{}".format(points["all"], points["total"]), file=sys.stderr)
  for key in points_keys:
    if key == "all":
      continue
    print("{}:{}".format(key, points[key]), file=sys.stderr)
  print("---end test results---", file=sys.stderr)

def response_function(*args):
  try:
    response = response_actual_function(*args)
    return response
  except Exception as e:
    print("error: There was an error running student code.", file=sys.stderr)
    try:
      raise e
    except:
      pass
    print("---begin error---", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    print("---end error---", file=sys.stderr)
    exit(2)

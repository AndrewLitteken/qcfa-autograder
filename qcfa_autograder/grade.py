import sys
import traceback
import utils as utils
import answers as answers
import qiskit

exercise = sys.argv[1]
submission_path = sys.argv[2]

submission_module = utils.load_module_from_path(submission_path)

unitary_comparison_exercises = {
  "hw1-1", "hw1-2", "hw1-3", "hw1-4",
  "hw2-1", "hw2-2", "hw2-3", "hw2-4",
  "hw3-1a"}

size_comparisons = {
  "hw2-1", "hw2-2", "hw2-3", "hw2-4"
}
base_function_name = exercise.replace("-", "_") + "_answer"
response_function_name = exercise.replace("-", "_") + "_response"

args = []
if exercise == "hw3-1a":
  qr = qiskit.QuantumRegister(2)
  qc = qiskit.QuantumCircuit(qr)
  args += [qc, qr[0], qr[1]]

base_function = getattr(answers, base_function_name)
response_actual_function = getattr(submission_module, response_function_name)

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

if exercise in unitary_comparison_exercises:
  expected_possibilities = base_function(*args)
  if not isinstance(expected_possibilities, list):
    expected_possibilities = [expected_possibilities]
  response = response_function(*args)
  if not isinstance(response, qiskit.QuantumCircuit):
    print("error: function output was not a qiskit.QuantumCircuit", file=sys.stderr)
    exit(3)
 
  correct = False
  for expected in expected_possibilities: 
    correct = correct or utils.compare_circuits(expected, response)
    if correct:
      break
  tests_to_use = None
  skip_test_results = False
  if exercise.startswith("hw1"):
    tests_function_name = exercise.replace("-", "_") + "_tests"
    tests_to_use = getattr(answers, tests_function_name)()
  points = utils.test_results(expected_possibilities, response, correct, tests_to_use)
  if exercise.startswith("hw2"):
    points["total"] += 1
    if len(expected_possibilities[0]) > len(response) and points["all"] > points["returns circuit"] and len(response) != 0:
      points["all"] += 1
      points["is smaller"] = 1
    else:
      points["all"] = points["returns circuit"]
      points["is smaller"] = 0
  utils.output_test_results(points)
else:
  if exercise == "hw3-3":
    points = base_function(response_function, submission_module)
  else:
    points = base_function(response_function)
  utils.output_test_results(points)
exit(0)
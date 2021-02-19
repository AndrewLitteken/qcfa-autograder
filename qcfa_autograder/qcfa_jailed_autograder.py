from xqueue_watcher.grader import Grader
import time
from path import Path
import subprocess
import os
import html
import codejail

def format_errors(errors):
    esc = html.escape
    error_string = ''
    error_list = [esc(e) for e in errors or []]
    if error_list:
        items = '\n'.join(['<li><pre>{0}</pre></li>\n'.format(e) for e in error_list])
        error_string = '<ul>\n{0}</ul>\n'.format(items)
        error_string = '<div>{0}</div>'.format(error_string)
    return error_string

class QCFAJailedGrader(Grader):

  results_template = """
<div class="test">
<header>Run results</header>
  <section>
    <div class="shortform">
    {status}
    </div>
    <div class="longform">
      {errors}
      {results}
    </div>
  </section>
</div>"""

  def __init__(self, *args, **kwargs):
    self.codejail_python = kwargs.pop("codejail_python", "python")
    super(QCFAJailedGrader, self).__init__(*args, **kwargs)
    codejail.jail_code.configure('python', '/home/litteken/qcfa-grader/bin/python', user="sandbox")
    self.fork_per_item = False
    codejail.jail_code.set_limit("CPU", 10)
    codejail.jail_code.set_limit("REALTIME", 10)
    codejail.jail_code.set_limit("PROXY", 0)

  def grade(self, grader_path, grader_config, student_response):
    print(Path(grader_path).dirname())
    grader_file = Path(grader_path).dirname() / "grade.py"
    problem = grader_config['grader']
    current_file = "/tmp/" + str(int(time.time())) + ".py"
    index = 0
    while os.path.exists(current_file):
      no_ending = current_file.split(".")
      current_file = no_ending + "-" + str(index) + ".py"
      index += 1
    file_obj = open(current_file, "w+")
    file_obj.write(student_response)
    file_obj.close()
    exec_args = [str(grader_file), problem, current_file]
    files = [str(grader_file), current_file]
    print(exec_args)
    proc = codejail.jail_code.jail_code('python', files=files, argv=exec_args)
    #proc = subprocess.Popen(["python"] + exec_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    results = {"correct": False,
                "score": 0,
                "tests": [("Blank Space", "1")],
                "errors": []}
    '''try:
      pass#return_code = proc.wait(timeout=10)
    except subprocess.TimeoutExpired as e:
      results["errors"].append("Unable to complete task in 10 seconds.")
      os.remove(current_file)
      return results'''
    os.remove(current_file)
    in_error = False
    in_test = False
    print(proc.status)
    print(proc.stderr.decode("ascii"))
    for line in proc.stderr:
      print(line)
      if line.startswith("error:"):
        results["errors"].append(line)
      elif line == "---begin error---\n":
        in_error = True
        results["errors"].append("")
        continue
      elif line == "---end error---\n":
        in_error = False
        continue
      elif line == "---begin test results---\n":
        in_test = True
        continue
      elif line == "---end test results---\n":
        in_test = False
        continue
      
      if in_error:
        results["errors"][-1] += line
      elif in_test:
        line_split = line.strip("\n").split(":")
        test = line_split[0]
        score = line_split[1]
        print(line_split)
        if test == "all":
          score_split = score.split("/")
          recieved = int(score_split[0])
          possible = int(score_split[1])
          results["correct"] = recieved == possible
          results["score"] = recieved / possible
          continue
        results["tests"].append((test, score))
    print(results)
    return results

  def render_results(self, results):
    if len(results['errors']) > 0:
      errors = format_errors(results['errors'])
    else:
      errors = format_errors(["There were no errors running the code."])

    status = 'Ran Correctly'
    if len(results['errors']) > 0:
        status = 'ERROR running submitted code'

    return self.results_template.format(status=status,
                                        errors=errors,
                                        results='')

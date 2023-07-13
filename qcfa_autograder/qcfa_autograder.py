from xqueue_watcher.grader import Grader
import time
from path import Path
import subprocess
import os
import html
import traceback

def format_errors(errors):
    esc = html.escape
    error_string = ''
    error_list = [esc(e) for e in errors or []]
    if error_list:
        items = '\n'.join(['<li><pre>{0}</pre></li>\n'.format(e) for e in error_list])
        error_string = '<ul>\n{0}</ul>\n'.format(items)
        error_string = '<div>{0}</div>'.format(error_string)
    return error_string

def demote(user_uid, user_gid):
    def result():
        os.setgid(user_gid)
        os.setuid(user_uid)
    return result

def check_file(response):
  errors = []
  for i, line in enumerate(response.split("\n"), 1):
    error = None
    if line.find("import os") >= 0:
      error = f"line {i}: You are no allowed to use the os package"
    if line.find("import sys") >= 0:
      error = f"line {i}: You are no allowed to use the sys package"
    if line.find("import shutil") >= 0:
      error = f"line {i}: You are no allowed to use the shutil package"
    if line.find("import pickle") >= 0:
      error = f"line {i}: You are no allowed to use the pickle package"
    if line.find("import multiprocessing") >= 0:
      error = f"line {i}: You are no allowed to use the multiprocessing package"
    if line.find("import subprocess") >= 0:
      error = f"line {i}: You are no allowed to use the subprocess package"
    if line.find("import requests") >= 0:
      error = f"line {i}: You are no allowed to use the requests package"
    if line.find("import socket") >= 0:
      error = f"line {i}: You are no allowed to use the socket package"
    if line.find("exec(") >= 0:
      error = f"line {i}: You are no allowed to use the exec function"
    if line.find("open(") >= 0:
      error = f"line {i}: You are no allowed to use the open function"
    if line.find("read(") >= 0:
      error = f"line {i}: You are no allowed to use the read function"
    if line.find("write(") >= 0:
      error = f"line {i}: You are no allowed to use the write function"
    if error is not None:
      errors.append(error)

  if len(errors) == 0:
    errors = None
  return errors

class QCFAGrader(Grader):

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

  error_template_scratch = """<div><p>{error}</p></div>"""
  results_template_scratch = """<div>{report_contents}</div>"""
  
  grader_config = {}

  def __init__(self, python_sandbox="", log_file="log.txt", sub_user_id=0, grader_root='/tmp/', fork_per_item=True, logger_name=__name__):
        """
        grader_root = root path to graders
        fork_per_item = fork a process for every request
        logger_name = name of logger
        """
        self.grader_config["python_sandbox"] = python_sandbox
        self.grader_config["log_file"] = log_file
        self.grader_config["sub_user_id"] = sub_user_id

        super(QCFAGrader, self).__init__(grader_root, fork_per_item, logger_name)

  def _grade(self, grader_path, grader_config, student_response):
    grader_file = Path(grader_path).dirname() / "grade.py"
    problem = grader_config['grader']
    python_sandbox = self.grader_config['python_sandbox']
    log_file = self.grader_config['log_file']
    grader_user = self.grader_config['sub_user_id']
    current_file = "/tmp/" + str(int(time.time())) + ".py"
    index = 0
    while os.path.exists(current_file):
      no_ending = current_file.split(".")
      current_file = no_ending + "-" + str(index) + ".py"
      index += 1
    results = {"correct": False,
                "score": 0,
                "tests": [("Blank Space", "1")],
                "errors": []}
    errors = check_file(student_response)
    if errors is not None:
      results["errors"] += errors
      return results
    file_obj = open(current_file, "w+")
    file_obj.write(student_response)
    file_obj.close()
    #exec_args = ["sudo", "-u", "__litteken", python_sandbox + "/bin/python", str(grader_file), problem, current_file]
    exec_args = [python_sandbox + "/bin/python", str(grader_file), problem, current_file]
    # 1001 is the groupid and userid for the sandbox account
    proc = subprocess.Popen(exec_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    try:
      return_code = proc.wait(timeout=30)
    except subprocess.TimeoutExpired as e:
      results["errors"].append("Unable to complete task in 10 seconds.")
      with open(self.grader_config["log_file"], 'a') as f:
        f.write(">>>>> Error Begin\n")
        f.write("Time: {}\n".format(time.ctime()))
        f.write("Time Out Error")
        f.write("----grader_config----\n")
        f.write(str(grader_config) + "\n")
        f.write("----student_response----\n")
        f.write(student_response + "\n")
        f.write(">>>>> Error End\n")
      return {"correct": False,
              "score": 0,
              "tests": [()],
              "errors": ["Please contact the course administrators to fix the problem, along with the time of this error: " + time.ctime()]}
      os.remove(current_file)
      return results
    os.remove(current_file)
    in_error = False
    in_test = False
    for line in proc.stderr:
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
        if test == "all":
          score_split = score.split("/")
          recieved = float(score_split[0])
          possible = float(score_split[1])
          assert recieved <= possible, "Score given is greater than possible score."
          results["correct"] = recieved == possible
          results["score"] = recieved / possible
          continue
        results["tests"].append((test, score))
    if proc.returncode != 0 and len(results["errors"]) == 0:
      raise Exception("Error in grade.py")
    return results

  def grade(self, grader_path, grader_config, student_response):
    try:
      grader_to_use = "qcfa"
      if "grader_to_use" in grader_config:
        grader_to_use = grader_config["grader_to_use"]
      if grader_to_use == "qcfa":
        return self._grade(grader_path, grader_config, student_response)
      elif grader_to_use == "scratch":
        return self.grade_scratch(grader_path, grader_config, student_response)
    except Exception as e:
      with open(self.grader_config["log_file"], 'a') as f:
        f.write(">>>>> Error Begin\n")
        f.write("Time: {}\n".format(time.ctime()))
        f.write("----Traceback----\n")
        f.write(str(e))
        f.write(traceback.format_exc())
        f.write("----grader_config----\n")
        f.write(str(grader_config) + "\n")
        f.write("----student_response----\n")
        f.write(student_response + "\n")
        f.write(">>>>> Error End\n")
      return {"correct": False,
              "score": 0,
              "tests": [()],
              "errors": ["Please contact the course administrators to fix the problem, along with the time of this error: " + time.ctime()]}

  def grade_scratch(self, grader_path, grader_config, student_response):
        problem = grader_config['module']
        stripped_response = student_response.strip(" \t\n\r")
        split_response = stripped_response.split('/')
        if "editor" in split_response:
            split_response.remove("editor")
        student_id = split_response[-1]
        if len(student_id) < 2 and len(split_response) > 1:
            student_id = split_response[-2]
        print("id", student_id)
        print("problem", problem)
        results = {"correct": False,
                    "score": 0,
                    "msg": ''}
        exec_args = ["node", "/home/litteken/automated-assessment/edx/xqueue_grader.js", problem, student_id ]
        proc = subprocess.Popen(exec_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        (output, err) = proc.communicate()
        print("process error: ", err)
        visible = "false"
        error = ""
        score = 0
        in_report = False
        in_grade_script = False
        report_list = []
        print("Output: ", output, "\nEnd Output")
        for line in output.split("\n"):
            if line == "start_grade_script":
                in_grade_script = True
            elif line == "end_grade_script":
                in_grade_script = False
            elif in_grade_script:
                # ignore any line in the grade script
                continue
            else:
                if line.startswith("Error"):
                    error = line
                elif line == "report_start":
                    in_report = True
                    error = ""
                elif line == "report_end":
                    in_report = False
                    results['correct'] = True
                elif in_report:
                    report_list.append(line)
                elif line.startswith("score:"):
                    score = float(line.split(':')[1].strip())
                else:
                    continue

        if len(report_list) > 0:
            report_div = ""
            for item in report_list:
                report_div += item
                report_div += " <br> "

            report_div += " <br>"
        else:
            report_div = ""

        results['score'] = score
        if len(error) > 0:
            results['msg'] = self.error_template_scratch.format(error=error)
        else:
            results['msg'] = self.results_template_scratch.format(report_contents=report_div)

        return results

  def render_results(self, results, config=None):
    if config is not None and "grader_to_use" in config:
      if config["grader_to_use"] == "scratch":
        return self.render_results_scratch(results)
    if "errors" not in results:
      error = ""
    elif len(results['errors']) > 0:
      errors = format_errors(results['errors'])
    else:
      errors = format_errors(["There were no errors running the code."])

    status = 'Ran without errors'
    if "errors" in results and len(results['errors']) > 0:
        status = 'ERROR running submitted code'

    return self.results_template.format(status=status,
                                        errors=errors,
                                        results='')
  def render_results_scratch(self, results):
        print("Results",results)
        return results['msg']

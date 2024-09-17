import subprocess
from .log_events import error_log, debug_log

class Extras:
    @staticmethod
    def run_command(command, cwd=None, context='', node_id="", show_debug_log=False):
      process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
      output, error = process.communicate()

      if process.returncode != 0:
        error_log(f"Error occurred while {context}: {command} : {error.decode('utf-8')}")
      else:
        conditional_debug_log(f"Output: {output.decode('utf-8')}", node_id, show_debug_log)

# Expose methods at the module level
#     This is necessary if you want to import these methods directly from log_events.py without referencing the Extras class.
#     This setup allows you to re-export these methods in the __init__.py file of the utils module, making them directly
#     accessible when importing from lumeo.utils.
run_command = Extras.run_command

from difflib import SequenceMatcher
import os
import subprocess
import re
from colorama import init, Fore, Style
import argparse
from verilog_resolver import resolve_verilog_dependencies

# Initialize colorama for cross-platform colored output
init()

# Default testbench output directory
DEFAULT_TB_DIR = "testbenches"
TEST_IGNORE = "testignore.txt"
TEST_IGNORE_FILES = []

with open(TEST_IGNORE, 'r') as file:
    TEST_IGNORE_FILES = file.read().split("\n")



def print_banner():
    banner = f"""{Fore.BLUE}
██     ██ ██ ███    ███ ███████      ██████ ██████  ██    ██ 
██     ██ ██ ████  ████ ██          ██      ██   ██ ██    ██ 
██  █  ██ ██ ██ ████ ██ ███████     ██      ██████  ██    ██ 
██ ███ ██ ██ ██  ██  ██      ██     ██      ██      ██    ██ 
 ███ ███  ██ ██      ██ ███████      ██████ ██       ██████  
                                                             
                                                             
    {Style.RESET_ALL}"""
    print(banner)
    print(f"ignoring {TEST_IGNORE_FILES}")

def find_testbenches(start_dir='.'):
    testbenches = []
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith('_tb.v'):
                if not file.replace("_tb","") in TEST_IGNORE_FILES and root not in TEST_IGNORE:
                    testbenches.append(os.path.join(root, file))
                else:
                     print(f"IGNORING TESTBENCH FILE {file}")

    return testbenches

def _find_file(file):
        module_name = os.path.splitext(os.path.basename(file))[0]
        for root, dirs, files in os.walk("."):
            for file in files:
                file_name = os.path.splitext(file)[0]
                # print(f"file {file_name} looking for {module_name}")
                similarity = SequenceMatcher(None, module_name, file_name).ratio()
                if similarity >= 0.95:
                    if file not in TEST_IGNORE_FILES:
                        return os.path.join(root, file)
                    
        return None

def run_testbench(testbench):
    print(f"{Fore.YELLOW}[{testbench}] {Fore.BLUE}Compiling...{Style.RESET_ALL}")
    
    # Get the directory of the testbench and the parent directory
    tb_dir = os.path.dirname(testbench)
    parent_dir = os.path.dirname(tb_dir)
    
    # Extract the base name of the testbench (without _tb.v)
    base_name = os.path.basename(testbench)[:-5]
    
    # Look for the UUT file in both the testbench directory and the parent directory
    uut_file = f"{base_name}.v"
    if  _find_file(uut_file) != None:
        uut_path = _find_file(uut_file)
        # print(f"found file {uut_path} for {base_name}")
    elif os.path.exists(os.path.join(tb_dir, uut_file)):
        uut_path = os.path.join(tb_dir, uut_file)
    elif os.path.exists(os.path.join(parent_dir, uut_file)):
        uut_path = os.path.join(parent_dir, uut_file)
    else:
        print(f"{Fore.RED}[{testbench}] UUT file {uut_file} not found in testbench or parent directory{Style.RESET_ALL}")
        return False
    
    # Find all Verilog files in the parent directory
    # verilog_files = [os.path.join(parent_dir, f) for f in os.listdir(parent_dir) if f.endswith('.v') and f != uut_file]
    verilog_files = find_non_testbenches_verilog_files(ignore=[uut_file])

    # TODO: read the uut_file and search for the modules, remove all other files from verilog_files
    # and only include the necessary ones (instanciated in the uut_file)
    # filtered_verilog_files = resolve_verilog_dependencies(uut_path, parent_dir)
    
    # Compile command with all Verilog files
    # compile_command = f"iverilog -o {testbench[:-2]} {' '.join(verilog_files)} {uut_path} {testbench}"
    # vcd_file = testbench[:-5] + ".vcd"
   
    compile_command = f"iverilog -o {testbench[:-2]} {' '.join(verilog_files)} {uut_path} {testbench}"

    compile_result = subprocess.run(compile_command, shell=True, capture_output=True, text=True)
    
    if compile_result.returncode != 0:
        print(f"{Fore.RED}[{testbench}] Compilation failed:{Style.RESET_ALL}")
        print(compile_result.stderr)
        return False
    
    print(f"{Fore.YELLOW}[{testbench}] {Fore.BLUE}Running...{Style.RESET_ALL}")
    run_command = f"vvp {testbench[:-2]}"
    run_result = subprocess.run(run_command, shell=True, capture_output=True, text=True)
    
    if run_result.returncode != 0:
        print(f"{Fore.RED}[{testbench}] Execution failed:{Style.RESET_ALL}")
        print(run_result.stderr)
        return False
    
    output = run_result.stdout
    passed_tests = len(re.findall(r"Test passed", output))
    failed_tests = len(re.findall(r"Test failed", output))
    
    print(f"{Fore.YELLOW}[{testbench}] {Fore.GREEN}Passed: {passed_tests} {Fore.RED}Failed: {failed_tests}{Style.RESET_ALL}")
    
    if failed_tests > 0:
        print(f"{Fore.RED}[{testbench}] Failed tests details:{Style.RESET_ALL}")
        for line in output.split('\n'):
            if "Test failed" in line:
                print(f"  {Fore.RED}✗ {line}{Style.RESET_ALL}")
        return False
    
    return True

class VerilogTestbench:
    def __init__(self, module_file):
        self.module_file = module_file
        self.module_name = os.path.splitext(os.path.basename(module_file))[0]
        self.inputs = {}
        self.outputs = {}
        self.test_vectors = []
        self.golden_model = None
        self.current_inputs = {}
        self.current_test_name = "Unnamed Test"
        self.auto_wait = True
        self._parse_module()

    import difflib
    import os

    def _parse_module(self):
        module_file = self._find_module_file()
        if not module_file:
            raise ValueError(f"Could not find module file with a similarity of at least 90% in {self.module_file}")
        
        with open(module_file, 'r') as f:
            content = f.read()
        
        # Strip comments and empty lines
        # Remove single-line comments
        content = re.sub(r'//.*', '', content)
        
        # Remove multi-line comments (/* */)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Remove empty lines and extra whitespace
        content = re.sub(r'\n\s*\n', '\n', content)
        content = content.strip()
        
        # Extract module definition
        module_def = re.search(r'module\s+(\w+)\s*\((.*?)\);', content, re.DOTALL)
        
        if not module_def:
            raise ValueError(f"Could not find module definition in {module_file}")
        
        # Parse inputs and outputs
        # for port in re.finditer(r'(input|output)\s*(?:reg|wire)?\s*(?:\[(\d+:\d+)\])?\s*(\w+)', content):
        for port in re.finditer(r'(input|output)\s+(?:reg|wire)?\s*(\[[\d:]+\])?\s*(\w+)', content):

            port_type, width, name = port.groups()
            
            if port_type == 'input':
                self.inputs[name] = width or ''
                # print(f"{module_file} | input {name}")
            else:
                self.outputs[name] = width or ''
                # print(f"{module_file} | output {name}")


    def _find_module_file(self):
        module_name = os.path.splitext(os.path.basename(self.module_file))[0]
        for root, dirs, files in os.walk("."):
            for file in files:
                file_name = os.path.splitext(file)[0]
                similarity = SequenceMatcher(None, module_name, file_name).ratio()
                # print(f"[{root}] file [{file_name}] looking for [{module_name}] {similarity}")
                if similarity >= 0.95 and file not in TEST_IGNORE_FILES: # and root not in TEST_IGNORE:
                    return os.path.join(root, file)
        return None

    def set_golden_model(self, model_function):
        self.golden_model = model_function

    @staticmethod
    def parse_input(input_str):
        if "'" in input_str:
            # Format: "<width>'b<value>" or "<width>'d<value>"
            width, value = input_str.split("'")
            base = 2 if value.startswith('b') else 10
            return int(value[1:], base)
        else:
            # Assume decimal if no base specified
            return int(input_str)

    def set_inputs(self, **kwargs):
        parsed_inputs = {}
        for name, value in kwargs.items():
            if name not in self.inputs:
                raise ValueError(f"Input {name} not found in module {self.module_name}")
            parsed_inputs[name] = self.parse_input(value)
        self.current_inputs = parsed_inputs
        self.test_vectors.append(('input', kwargs, self.current_test_name))

    def drive_signal(self, signal_name, value):
        if signal_name not in self.inputs:
            raise ValueError(f"Signal {signal_name} not found in module inputs")
        self.test_vectors.append(('drive', {signal_name: value}, self.current_test_name))

    def wait(self, time):
        self.test_vectors.append(('wait', time, self.current_test_name))

    def test_name(self, name):
        self.current_test_name = name

    def assert_outputs(self, **kwargs):
        if self.golden_model and not kwargs:
            # Use golden model to generate expected outputs
            expected_outputs = self.golden_model(**self.current_inputs)
            if not isinstance(expected_outputs, dict):
                raise ValueError("Golden model must return a dictionary of output values")
            kwargs = expected_outputs

        for name, value in kwargs.items():
            if name not in self.outputs:
                raise ValueError(f"Output {name} not found in module {self.module_name}")
        self.test_vectors.append(('assert', kwargs, self.current_test_name))
        self.current_test_name = "Unnamed Test"  # Reset the test name

    def output_verilog(self, output_file):
        with open(output_file, 'w') as f:
            f.write(f"`timescale 1ns / 1ps\n\n")
            # f.write(f"`ifndef {self.module_name}\n")
            # f.write(f"`define {self.module_name}\n")
            # f.write(f"`endif\n\n")
            

            f.write(f"module {self.module_name}_tb;\n\n")

            # Declare reg and wire
            for name, width in self.inputs.items():
                f.write(f"    reg {width or ''} {name};\n")
            for name, width in self.outputs.items():
                f.write(f"    wire {width or ''} {name};\n")
            f.write("\n")

            # Instantiate UUT
            f.write(f"    {self.module_name} uut (\n")
            ports = [f".{name}({name})" for name in {**self.inputs, **self.outputs}]
            f.write(",\n".join(f"        {port}" for port in ports))
            f.write("\n    );\n\n")

            # Write test vectors
            f.write("    initial begin\n")
            for i, vector in enumerate(self.test_vectors):
                action = vector[0]
                values = vector[1]
                test_name = vector[2] if len(vector) > 2 else "Unnamed Test"

                if action == 'input':
                    assignments = [f"{name} = {value};" for name, value in values.items()]
                    f.write(f"        // Test vector {i + 1}\n")
                    f.write("        " + " ".join(assignments) + "\n")
                    if self.auto_wait:
                        f.write(f"        #10;\n")
                elif action == 'drive':
                    name, value = list(values.items())[0]
                    f.write(f"        {name} = {value};\n")
                elif action == 'wait':
                    f.write(f"        #{int(values)};\n")
                elif action == 'assert':
                    conditions = [f"{name} !== {value}" for name, value in values.items()]
                    f.write(f"        if ({' || '.join(conditions)}) begin\n")
                    f.write(f'            $display("Test failed: {test_name} failed for ')
                    f.write(", ".join([f"{name}=%b" for name in self.inputs.keys()]))
                    # TODO: I found that if you do not pass the key pairs in order in the assert_outputs function
                    # it will display the wrong values, i don't have time to fix this now
                    f.write(f'. Expected ')
                    f.write(", ".join([f"{name}=%b" for name in self.outputs.keys()]))
                    f.write(f', got ')
                    f.write(", ".join([f"{name}=%b" for name in self.outputs.keys()]))
                    f.write(f'", ')
                    f.write(", ".join([f"{name}" for name in self.inputs.keys()]))
                    f.write(", ")
                    f.write(", ".join([f"{value}" for value in values.values()]))
                    f.write(", ")
                    f.write(", ".join([name for name in self.outputs.keys()]))
                    f.write(");\n")
                    f.write("        end else begin\n")
                    f.write(f'            $display("Test passed: {test_name} passed for ')
                    f.write(", ".join([f"{name}=%b" for name in self.inputs.keys()]))
                    f.write(f'. {", ".join([f"{name}=%b" for name in self.outputs.keys()])}", ')
                    f.write(", ".join([name for name in self.inputs.keys()]))
                    f.write(", ")
                    f.write(", ".join([name for name in self.outputs.keys()]))
                    f.write(");\n")
                    f.write("        end\n")
                f.write("\n")
            
            
        
            # f.write(f"        $dumpfile(\"{self.module_name}.vcd\");\n")
            # f.write(f"        $dumpvars(0, {self.module_name}_tb);\n")
            f.write("        $finish;\n")
            f.write("    end\n\n")
            f.write("endmodule\n")

def create_testbench(module_file):
    tb = VerilogTestbench(module_file)
    return tb

# Add this new function to search for Verilog files without testbenches
def find_verilog_files_without_testbenches(start_dir='.'):
    verilog_files = set()
    testbench_files = set()
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.v'):
                if file.endswith('_tb.v'):
                    testbench_files.add(file[:-5])  # Remove '_tb.v' suffix
                else:
                    verilog_files.add(file[:-2])  # Remove '.v' suffix
    
    return verilog_files - testbench_files  # Files without testbenches

def find_non_testbenches_verilog_files(start_dir='.', ignore=[]):
    verilog_files = set()
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.v') and not file.endswith('_tb.v') and file not in ignore:
                if file not in TEST_IGNORE_FILES:# and root not in TEST_IGNORE:
                    file_path = os.path.join(root, file)  # Get the full path of the file
                    verilog_files.add(file_path)  
    
    return verilog_files

# def extract_module_instances(uut_file):
#     """
#     Extract module instance names from a Verilog UUT file.
    
#     Args:
#         uut_file (str): Path to the UUT Verilog file
    
#     Returns:
#         set: Set of unique module instance names used in the file
#     """
#     # Read the contents of the UUT file
#     with open(uut_file, 'r') as f:
#         uut_content = f.read()
    
#     # Regex pattern to find module instances
#     # This pattern looks for:
#     # 1. Module name followed by optional instance name
#     # 2. Handles both styles: 
#     #    module_name instance_name (...);
#     #    module_name (...);
#     instance_pattern = r'\b(\w+)\s+(?:\w+\s*)?(\()'
    
#     # Find all matches
#     matches = re.findall(instance_pattern, uut_content)
    
#     # Extract just the module names, removing duplicates
#     module_instances = set(match[0] for match in matches 
#                            # Exclude built-in Verilog keywords or common primitives
#                            if match[0] not in ['always', 'assign', 'initial', 'wire', 'reg'])
    
#     return module_instances

# def filter_verilog_files(uut_file, verilog_files):
#     """
#     Filter Verilog files to include only those with module instances 
#     used in the UUT file.
    
#     Args:
#         uut_file (str): Path to the UUT Verilog file
#         verilog_files (list): List of Verilog files to filter
    
#     Returns:
#         list: Filtered list of Verilog files
#     """
#     # Extract module instances from UUT file
#     required_modules = extract_module_instances(uut_file)
    
#     # Filter files based on module names
#     filtered_files = []
#     for file_path in verilog_files:
#         # Read file content
#         with open(file_path, 'r') as f:
#             file_content = f.read()
        
#         # Check if any of the required modules are defined in this file
#         for module in required_modules:
#             # Look for module definition
#             module_def_pattern = rf'module\s+{module}\s*\('
#             if re.search(module_def_pattern, file_content):
#                 filtered_files.append(file_path)
#                 break  # No need to check further once a match is found
    
#     return filtered_files

def main():
    parser = argparse.ArgumentParser(description="Verilog Testbench Generator and Runner")
    parser.add_argument("--tb-dir", default=DEFAULT_TB_DIR, help="Directory for generated testbenches")
    args = parser.parse_args()

    print_banner()

    # Create testbench directory if it doesn't exist
    os.makedirs(args.tb_dir, exist_ok=True)

    # Move this import inside the main function
    from testbenches import basic_tests
    basic_tests(args.tb_dir)
    # Run existing testbench functionality
    testbenches = find_testbenches()
    
    if not testbenches:
        print(f"{Fore.YELLOW}No testbenches found.{Style.RESET_ALL}")
        return
    
    all_passed = True
    total_tests = len(testbenches)
    passed_tests = 0
    
    for testbench in testbenches:
        if run_testbench(testbench):
            passed_tests += 1
        else:
            all_passed = False
        print()  # Add a blank line between testbench results
    
    print(f"{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}")
    if all_passed:
        print(f"{Fore.GREEN}All testbenches passed successfully! 🎉{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Some testbenches failed. Please check the output above for details.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Summary: {Fore.GREEN}{passed_tests}/{total_tests} passed{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}")

    # Find Verilog files without testbenches
    files_without_testbenches = find_verilog_files_without_testbenches()
    if files_without_testbenches:
        print(f"\n{Fore.YELLOW}Warning: The following Verilog files do not have corresponding testbenches:{Style.RESET_ALL}")
        for file in sorted(files_without_testbenches):
            print(f"  {Fore.YELLOW}• {file}.v{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.GREEN}All Verilog files have corresponding testbenches.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
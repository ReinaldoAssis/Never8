import os
import re

class VerilogDependencyResolver:
    def __init__(self, verilog_files_dir):
        """
        Initialize the dependency resolver
        
        Args:
            verilog_files_dir (str): Directory containing Verilog files
        """
        self.verilog_files_dir = verilog_files_dir
        self.file_cache = {}
        self.module_to_file_map = {}

    def _read_file_content(self, file_path):
        """
        Read and cache file content
        
        Args:
            file_path (str): Path to the Verilog file
        
        Returns:
            str: File content
        """
        if file_path not in self.file_cache:
            with open(file_path, 'r') as f:
                self.file_cache[file_path] = f.read()
        return self.file_cache[file_path]

    def _build_module_to_file_map(self):
        """
        Create a mapping of module names to their file paths
        """
        self.module_to_file_map.clear()
        
        # Find all Verilog files
        verilog_files = [
            os.path.join(self.verilog_files_dir, f) 
            for f in os.listdir(self.verilog_files_dir) 
            if f.endswith('.v')
        ]
        
        # Extract module definitions
        for file_path in verilog_files:
            content = self._read_file_content(file_path)
            
            # Regex to find module definitions
            module_def_pattern = r'module\s+(\w+)\s*\('
            module_matches = re.findall(module_def_pattern, content)
            
            for module in module_matches:
                self.module_to_file_map[module] = file_path

    def extract_module_dependencies(self, uut_file):
        """
        Recursively extract all module dependencies
        
        Args:
            uut_file (str): Path to the Unit Under Test file
        
        Returns:
            set: Paths of all files containing required modules
        """
        # Ensure module to file mapping is built
        if not self.module_to_file_map:
            self._build_module_to_file_map()
        
        # Set to track required files
        required_files = set()
        
        # Set to track modules we've already processed
        processed_modules = set()
        
        def recursive_dependency_trace(file_path):
            """
            Recursively trace module dependencies
            
            Args:
                file_path (str): Path to the current file to analyze
            """
            # Avoid processing the same file multiple times
            if file_path in required_files:
                return
            
            # Read file content
            content = self._read_file_content(file_path)
            
            # Find module instances
            instance_pattern = r'\b(\w+)\s+(?:\w+\s*)?(\()'
            module_instances = set(
                match[0] for match in re.findall(instance_pattern, content)
                if match[0] not in ['always', 'assign', 'initial', 'wire', 'reg']
            )
            
            # Track newly discovered modules
            new_modules = module_instances - processed_modules
            processed_modules.update(new_modules)
            
            # Add current file to required files
            required_files.add(file_path)
            
            # Recursively trace dependencies for new modules
            for module in new_modules:
                if module in self.module_to_file_map:
                    module_file = self.module_to_file_map[module]
                    if module_file not in required_files:
                        recursive_dependency_trace(module_file)
        
        # Start with the UUT file
        recursive_dependency_trace(uut_file)
        
        return required_files

def resolve_verilog_dependencies(uut_file, verilog_files_dir):
    """
    Resolve and filter Verilog files based on recursive module dependencies
    
    Args:
        uut_file (str): Path to the Unit Under Test file
        verilog_files_dir (str): Directory containing Verilog files
    
    Returns:
        list: Filtered list of Verilog files required for compilation
    """
    resolver = VerilogDependencyResolver(verilog_files_dir)
    return list(resolver.extract_module_dependencies(uut_file))

# Example usage
# filtered_verilog_files = resolve_verilog_dependencies(uut_file, parent_dir)
# compile_command = f"iverilog -o {testbench[:-2]} {' '.join(filtered_verilog_files)} {uut_path} {testbench}"
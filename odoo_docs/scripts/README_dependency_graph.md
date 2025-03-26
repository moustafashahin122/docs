# Odoo Module Dependency Graph

This tool analyzes Odoo module manifests to generate a visual dependency graph and a text-based adjacency list of module dependencies.

## Requirements

- Python 3.6+
- NetworkX
- Graphviz (Python package)
- Graphviz (system package) - Must be installed on your system
- Node.js and npm (for eslintcc)

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Install the system Graphviz package:

```bash
# For Ubuntu/Debian
sudo apt-get install graphviz

# For macOS
brew install graphviz

# For Windows
# Download and install from https://graphviz.org/download/
```

For eslintcc (optional, for complexity metrics):

```bash
npm install -g eslintcc
```

## Usage

The script can be run directly from the command line, and will interactively prompt for the addons directory:

```bash
python module_dependency_graph.py [options]
```

### Options

- `--path`, `-p`: Path to the Odoo addons directory (if not provided, will prompt for it)
- `--output`, `-o`: Output file name for the graph (without extension)
- `--output-dir`, `-d`: Directory to save output files (defaults to addons directory)
- `--format`, `-f`: Output format for the graph visualization (choices: svg, pdf, png; default: svg)
- `--metrics`, `-m`: Include code complexity metrics (requires eslintcc)
- `--metrics-output`: Output file path for complexity metrics JSON
- `--list`, `-t`: Output file path for the text adjacency list
- `--non-interactive`, `-n`: Run in non-interactive mode (requires --path)

### Examples

1. Interactive mode (will prompt for the addons directory):

   ```bash
   python module_dependency_graph.py
   ```

2. Specify the addons directory via command line:

   ```bash
   python module_dependency_graph.py --path /path/to/odoo/addons
   ```

3. Generate a graph with a specific output file name:

   ```bash
   python module_dependency_graph.py --output dependency_graph
   ```

4. Generate a graph in PDF format:

   ```bash
   python module_dependency_graph.py --format pdf
   ```

5. Generate a graph in PNG format:

   ```bash
   python module_dependency_graph.py --format png
   ```

6. Specify both input and output directories:

   ```bash
   python module_dependency_graph.py --path /path/to/odoo/addons --output-dir /path/to/output
   ```

7. Generate a graph with code complexity metrics:

   ```bash
   python module_dependency_graph.py --metrics
   ```

8. Generate both a graph visualization and a text adjacency list:

   ```bash
   python module_dependency_graph.py --output graph --list dependencies.txt
   ```

9. Non-interactive mode with all options:
   ```bash
   python module_dependency_graph.py --path /path/to/odoo/addons --output graph --output-dir /path/to/save --format pdf --metrics --metrics-output metrics.json --list deps.txt --non-interactive
   ```

## Output Files

The script generates the following files:

- **DOT file** (`.gv`): Contains the Graphviz definition of the dependency graph. You can edit this file with a text editor to customize the graph further.
- **Image file** (`.svg`, `.pdf`, or `.png`): A rendered visualization of the dependency graph. The default format is SVG, which is better for web viewing and embedding.
- **Adjacency list** (optional): A text file with a list of all modules and their dependencies/dependents.
- **Metrics JSON** (optional): A JSON file with complexity metrics for JavaScript files.

By default, all files are saved in the addons directory being analyzed. You can specify a different output directory with the `--output-dir` option.

## About SVG Format

SVG (Scalable Vector Graphics) is the default output format because:

- It's a vector format, providing high-quality rendering at any zoom level
- It can be viewed directly in web browsers
- It can be embedded in HTML documents
- It can be edited with vector graphics editors like Inkscape or Adobe Illustrator
- It maintains a smaller file size compared to PDF for the same visual quality

## Graph Visualization

The graph visualization shows:

- Each node represents an Odoo module
- Directed edges indicate dependencies (a module depends on another module)
- Node color intensity reflects how many other modules depend on that module
- Node font size indicates code complexity (if metrics option is used)

## Interactive Features

When running in interactive mode (default), the script will:

1. Prompt you for the Odoo addons directory
2. Allow you to confirm your selection
3. Warn you if no manifest files are found
4. Ask if you want to open the generated graph file when complete

## Understanding the Results

- **Base modules**: Modules that don't depend on any other modules
- **Leaf modules**: Modules that aren't dependencies of any other modules
- **Total dependencies**: The total number of dependency relationships in the codebase

## Troubleshooting

If you encounter any issues parsing manifest files, the script will print error messages but continue processing the rest of the files.

### Common Issues

1. **Graphviz not found**: Make sure you have both the Python graphviz package and the system Graphviz package installed.

2. **eslintcc not found**: If using the metrics feature, ensure you have Node.js, npm, and eslintcc installed globally.

3. **Permission denied**: Make sure you have write permission to the directory where you want to save the output files.

## License

This tool is provided under the same license as Odoo itself.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script parses Odoo module manifests and generates a dependency graph.

Usage:
    python module_dependency_graph.py -p <addons_path> -m <module_name|all>
    
    For full graph of all modules:
        python odoo_module_dependency_graph.py -p /path/to/addons -m all
    
    For specific module subgraphs:
        python odoo_module_dependency_graph.py -p /path/to/addons -m module_name

Required arguments:
    -p, --path: Path to the Odoo addons directory
    -m, --module-name: Module name or 'all' to generate full graph
"""

import os
import sys
import ast
import argparse
import networkx as nx
from graphviz import Digraph


def find_manifest_files(directory):
    """Find all manifest files in the given directory and its subdirectories."""
    manifest_files = []
    for root, _, files in os.walk(directory):
        if '__manifest__.py' in files:
            manifest_files.append(os.path.join(root, '__manifest__.py'))
    return manifest_files


def parse_manifest(manifest_path):
    """Parse a manifest file and extract module name and dependencies."""
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
            manifest_dict = ast.literal_eval(content)
            
            # Extract module name from the path
            module_name = os.path.basename(os.path.dirname(manifest_path))
            
            # Extract dependencies
            dependencies = manifest_dict.get('depends', [])
            
            return module_name, dependencies
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing manifest file {manifest_path}: {e}")
        return None, []
    except Exception as e:
        print(f"Unexpected error while parsing {manifest_path}: {e}")
        return None, []


def create_dependency_graph(manifest_files):
    """Create a directed graph of module dependencies."""
    G = nx.DiGraph()
    
    # Parse each manifest file and add nodes and edges to the graph
    for manifest_file in manifest_files:
        module_name, dependencies = parse_manifest(manifest_file)
        if module_name:
            G.add_node(module_name)
            for dependency in dependencies:
                G.add_edge(module_name, dependency)
    
    return G

def get_dependents_subgraph(G, root_module):
    """Return a subgraph containing the root_module and all modules that (directly or indirectly) depend on it."""
    if root_module not in G:
        print(f"Module '{root_module}' not found in the dependency graph.")
        return G.subgraph([]).copy()
    # Find all nodes that have a path to root_module (i.e., all dependents)
    dependents = set()
    for node in G.nodes():
        if node == root_module:
            dependents.add(node)
        else:
            try:
                if nx.has_path(G, node, root_module):
                    dependents.add(node)
            except nx.NetworkXError:
                continue
    # The subgraph should include the root and all its dependents
    return G.subgraph(dependents).copy()


def get_dependencies_subgraph(G, root_module):
    """Return a subgraph containing the root_module and all modules that it (directly or indirectly) depends on."""
    if root_module not in G:
        print(f"Module '{root_module}' not found in the dependency graph.")
        return G.subgraph([]).copy()
    # Find all nodes that root_module has a path to (i.e., all dependencies)
    dependencies = set()
    dependencies.add(root_module)  # Include the root module itself
    
    try:
        # Get all nodes reachable from root_module (all dependencies)
        for node in G.nodes():
            if node != root_module:
                try:
                    if nx.has_path(G, root_module, node):
                        dependencies.add(node)
                except nx.NetworkXError:
                    continue
    except nx.NetworkXError:
        pass
    
    # The subgraph should include the root and all its dependencies
    return G.subgraph(dependencies).copy()


def visualize_with_graphviz(G, output_file=None, output_dir=None, format_type='svg'):
    """Visualize the dependency graph using Graphviz.
    
    Args:
        G: NetworkX graph object
        output_file: Name of the output file without extension
        output_dir: Directory to save the output files
        format_type: Output format (default: svg)
        
    Returns:
        Tuple of (dot_file_path, rendered_file_path)
    """
    # Create Digraph
    dot = Digraph(comment='Odoo Modules Dependency Graph')
    dot.attr(rankdir='LR', ratio='fill')
    dot.attr('node', shape='box', style='filled', fontname='Arial')
    dot.attr('edge', fontname='Arial')
    
    # Count how many modules depend on each module
    dependency_count = {}
    for node in G.nodes():
        dependency_count[node] = len(list(G.predecessors(node)))
    print(f"Dependency count: {dependency_count}")
    
    # Find max dependency count for normalization
    max_deps = max(1,max(dependency_count.values())) if dependency_count else 1
    print(f"Max dependencies: {max_deps}")
    
    # Add nodes with styling based on dependencies
    for node in G.nodes():
        # Node label with module name
        label = node
        
        # Node color based on dependencies
        deps_normalized = dependency_count[node] / max_deps
        color = f"#{int(80 + (175 * (1 - deps_normalized))):02x}{int(150 + (105 * (1 - deps_normalized))):02x}ff"
        
        # Add node with attributes
        dot.node(node, label, style='filled', fillcolor=color, fontsize='12')
    
    # Add edges
    for edge in G.edges():
        dot.edge(edge[0], edge[1])
    
    # Add a legend as a subgraph
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', fontsize='14', fontname='Arial', color='gray')
        
        # Stats
        module_count = len(G.nodes())
        edge_count = len(G.edges())
        leaf_modules = sum(1 for n in G.nodes() if G.out_degree(n) == 0)
        base_modules = sum(1 for n in G.nodes() if G.in_degree(n) == 0)
        
        stats = f"Total Modules: {module_count}\\l"
        stats += f"Total Dependencies: {edge_count}\\l"
        stats += f"Leaf Modules: {leaf_modules}\\l"
        stats += f"Base Modules: {base_modules}\\l"
        
        legend.node('stats', stats, shape='note', fontsize='12', fontname='Arial')
    
    # Determine file paths
    if output_file:
        # Use the provided filename
        filename = output_file
    else:
        # Default filename
        filename = 'odoo_dependency_graph'
    
    # Remove file extension if present
    filename = os.path.splitext(filename)[0]
    
    # Determine output directory
    if output_dir:
        # Make sure output directory exists
        os.makedirs(output_dir, exist_ok=True)
    else:
        # Default to current directory
        output_dir = os.getcwd()
    
    # Full path for dot and output files
    dot_path = os.path.join(output_dir, f"{filename}.gv")
    output_path = os.path.join(output_dir, f"{filename}.{format_type}")
    
    # Save the dot file
    dot.save(dot_path)
    print(f"Graphviz DOT file saved to {dot_path}")
    
    # Render the graph
    try:
        dot.render(dot_path, format=format_type, cleanup=False)  # Don't cleanup to keep the dot file
        print(f"{format_type.upper()} file saved to {output_path}")
        return dot_path, output_path
    except Exception as e:
        print(f"Error rendering {format_type.upper()}: {e}")
        return dot_path, None


def generate_adjacency_list(G, output_file=None):
    """Generate an adjacency list of module dependencies."""
    lines = []
    for module in sorted(G.nodes()):
        dependencies = sorted(G.successors(module))
        dependents = sorted(G.predecessors(module))
        
        lines.append(f"Module: {module}")
        lines.append(f"  Depends on: {', '.join(dependencies) if dependencies else 'None'}")
        lines.append(f"  Used by: {', '.join(dependents) if dependents else 'None'}")
        lines.append("")
    
    text = "\n".join(lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Adjacency list saved to {output_file}")
    else:
        print(text)


def get_directory_input(default_dir='.'):
    """Prompt the user for the addons directory."""
    print("\n===== Odoo Module Dependency Graph Generator =====\n")
    
    # Explain what the script does
    print("This script analyzes Odoo module manifests and generates a dependency graph.")
    print("It will search for '__manifest__.py' files in the specified directory and its subdirectories.")
    print("The graph will show dependencies between modules.\n")
    
    # Ask for directory with validation
    while True:
        suggested_dir = os.path.abspath(default_dir)
        user_input = input(f"Enter the path to the Odoo addons directory [default: {suggested_dir}]: ").strip()
        
        # Use default if empty
        dir_path = user_input if user_input else suggested_dir
        
        # Make sure it's an absolute path
        dir_path = os.path.abspath(dir_path)
        
        # Check if directory exists
        if not os.path.isdir(dir_path):
            print(f"Error: '{dir_path}' is not a valid directory. Please try again.")
            continue
        
        # Verify with the user that this is correct
        print(f"\nSelected directory: {dir_path}")
        confirmation = input("Is this correct? (y/n): ").strip().lower()
        
        if confirmation == 'y' or confirmation == 'yes':
            return dir_path
        else:
            print("Let's try again.\n")


def main():
    parser = argparse.ArgumentParser(
        description='Generate an Odoo module dependency graph.',
        epilog='Examples:\n'
               '  odoo_module_dependency_graph.py -p /path/to/addons -m all\n'
               '  odoo_module_dependency_graph.py -p /path/to/addons -m module_name',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--path', '-p', required=True,
                        help='Path to the Odoo addons directory (required)')
    parser.add_argument('--module-name', '-m', required=True,
                        help="Module name to analyze, or 'all' to generate full graph of all modules (required)")
    parser.add_argument('--output', '-o', help='Output file name for the graph (without extension)')
    parser.add_argument('--output-dir', '-d', help='Directory to save output files (defaults to addons directory)')
    parser.add_argument('--format', '-f', choices=['svg', 'pdf', 'png'], default='svg', 
                        help='Output format for the graph visualization (default: svg)')
    parser.add_argument('--list', '-t', help='Output file path for the text adjacency list')

    args = parser.parse_args()

    # Validate directory path
    dir_path = os.path.abspath(args.path)
    if not os.path.isdir(dir_path):
        print(f"Error: '{dir_path}' is not a valid directory.")
        print("\nUsage:")
        print("  python odoo_module_dependency_graph.py -p <addons_path> -m <module_name|all>")
        print("\nExamples:")
        print("  python odoo_module_dependency_graph.py -p /path/to/addons -m all")
        print("  python odoo_module_dependency_graph.py -p /path/to/addons -m module_name")
        sys.exit(1)

    # If output directory is not specified, use the addons directory
    output_dir = args.output_dir if args.output_dir else dir_path

    print(f"\nSearching for manifest files in {dir_path}...")
    manifest_files = find_manifest_files(dir_path)
    print(f"Found {len(manifest_files)} manifest files.")

    if not manifest_files:
        print(f"Warning: No '__manifest__.py' files found in {dir_path}. Is this an Odoo addons directory?")
        print("Exiting.")
        sys.exit(1)

    print("\nCreating dependency graph...")
    G_full = create_dependency_graph(manifest_files)

    # Handle -m all case: generate only the full graph
    if args.module_name.lower() == 'all':
        output_name = args.output or 'odoo_dependency_graph'
        
        if args.list:
            list_path = args.list
            if not os.path.isabs(list_path):
                list_path = os.path.join(output_dir, list_path)
            print(f"Generating adjacency list to {list_path}...")
            generate_adjacency_list(G_full, list_path)
        
        print(f"Visualizing full dependency graph (format: {args.format})...")
        dot_path, output_path = visualize_with_graphviz(G_full, output_name, output_dir, args.format)
        
        print("\nFiles generated:")
        print(f"- DOT file: {dot_path}")
        if output_path:
            print(f"- {args.format.upper()} file: {output_path}")
        
        print("\nDone!")
        return

    # Handle specific module: generate full graph + subgraphs
    module_name = args.module_name
    
    # Save the full dependency graph first
    print(f"\nSaving the full dependency graph (format: {args.format})...")
    full_output_name = args.output or 'odoo_dependency_graph'
    dot_path_full, output_path_full = visualize_with_graphviz(G_full, full_output_name, output_dir, args.format)
    print(f"- DOT file (full): {dot_path_full}")
    if output_path_full:
        print(f"- {args.format.upper()} file (full): {output_path_full}")

    # Extract and save the dependents subgraph (modules that depend on this one)
    print(f"\nExtracting dependents subgraph for module '{module_name}' (modules that depend on it)...")
    G_dependents = get_dependents_subgraph(G_full, module_name)
    dependents_output_name = f"{module_name}_dependents"
    
    if len(G_dependents.nodes()) > 0:
        dot_path_dependents, output_path_dependents = visualize_with_graphviz(G_dependents, dependents_output_name, output_dir, args.format)
        print(f"- DOT file (dependents): {dot_path_dependents}")
        if output_path_dependents:
            print(f"- {args.format.upper()} file (dependents): {output_path_dependents}")
    else:
        print(f"No modules found that depend on '{module_name}'.")
        output_path_dependents = None

    # Extract and save the dependencies subgraph (modules that this one depends on)
    print(f"\nExtracting dependencies subgraph for module '{module_name}' (modules it depends on)...")
    G_dependencies = get_dependencies_subgraph(G_full, module_name)
    dependencies_output_name = f"{module_name}_dependencies"
    
    if len(G_dependencies.nodes()) > 0:
        dot_path_dependencies, output_path_dependencies = visualize_with_graphviz(G_dependencies, dependencies_output_name, output_dir, args.format)
        print(f"- DOT file (dependencies): {dot_path_dependencies}")
        if output_path_dependencies:
            print(f"- {args.format.upper()} file (dependencies): {output_path_dependencies}")
    else:
        print(f"Module '{module_name}' has no dependencies.")
        output_path_dependencies = None

    # Generate adjacency lists if requested
    if args.list:
        list_path = args.list
        if not os.path.isabs(list_path):
            list_path = os.path.join(output_dir, list_path)
        
        # Generate adjacency list for dependents if they exist
        if len(G_dependents.nodes()) > 0:
            dependents_list_path = list_path.replace('.txt', '_dependents.txt') if list_path.endswith('.txt') else f"{list_path}_dependents"
            print(f"Generating dependents adjacency list to {dependents_list_path}...")
            generate_adjacency_list(G_dependents, dependents_list_path)
        
        # Generate adjacency list for dependencies if they exist
        if len(G_dependencies.nodes()) > 0:
            dependencies_list_path = list_path.replace('.txt', '_dependencies.txt') if list_path.endswith('.txt') else f"{list_path}_dependencies"
            print(f"Generating dependencies adjacency list to {dependencies_list_path}...")
            generate_adjacency_list(G_dependencies, dependencies_list_path)

    print("\nDone!")


if __name__ == "__main__":
    main() 
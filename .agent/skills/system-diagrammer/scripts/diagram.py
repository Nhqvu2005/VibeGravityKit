#!/usr/bin/env python3
"""
System Diagrammer — Generate Mermaid.js Architecture Diagrams.

Usage:
    python diagram.py --type c4 --title "E-commerce System" --nodes "User, Web App, API, Database"
    python diagram.py --type sequence --title "Login Flow" --steps "User->Web:Login, Web->API:Auth Request, API->DB:Check Creds"
"""

import argparse
import sys

def generate_c4(title, nodes_str):
    nodes = [n.strip() for n in nodes_str.split(",")]
    lines = [f"title {title}", "throughput", "User((User))"]
    
    # Simple C4 Context styling
    for i, node in enumerate(nodes):
        if node.lower() == "user": continue
        
        # Simple heuristic for shape
        shape = "rect" 
        if "db" in node.lower() or "database" in node.lower(): shape = "db"
        
        node_id = node.replace(" ", "_")
        
        if shape == "db":
            lines.append(f"    {node_id}[({node})]")
        else:
            lines.append(f"    {node_id}[{node}]")
            
    # Connect them sequentially for now (simple chain)
    lines.append("    User --> " + nodes[1].replace(" ", "_"))
    for i in range(1, len(nodes)-1):
        if nodes[i].lower() == "user": continue
        current = nodes[i].replace(" ", "_")
        next_n = nodes[i+1].replace(" ", "_")
        lines.append(f"    {current} --> {next_n}")
        
    return "graph TD\n" + "\n".join(lines)

def generate_sequence(title, steps_str):
    steps = [s.strip() for s in steps_str.split(",")]
    lines = [f"title {title}", "autonumber"]
    
    for step in steps:
        if ":" in step and "->" in step:
            # Format: A->B:Message
            parts = step.split(":")
            interaction = parts[0].strip()
            message = parts[1].strip()
            lines.append(f"    {interaction}: {message}")
        else:
            lines.append(f"    Note over User: {step}")
            
    return "sequenceDiagram\n" + "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="System Diagrammer")
    parser.add_argument("--type", type=str, required=True, choices=["c4", "sequence"], help="Diagram type")
    parser.add_argument("--title", type=str, default="System Diagram", help="Diagram title")
    parser.add_argument("--nodes", type=str, help="List of nodes for C4 (comma separated)")
    parser.add_argument("--steps", type=str, help="List of steps for Sequence (A->B:Msg, ...)")
    
    args = parser.parse_args()
    
    print("```mermaid")
    if args.type == "c4":
        if not args.nodes:
            print("Error: --nodes required for C4")
        else:
            print(generate_c4(args.title, args.nodes))
    elif args.type == "sequence":
        if not args.steps:
            print("Error: --steps required for Sequence")
        else:
            print(generate_sequence(args.title, args.steps))
    print("```")

if __name__ == "__main__":
    main()

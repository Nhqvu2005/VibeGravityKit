#!/usr/bin/env python3
"""
API Designer — Generate RESTful API Endpoints & OpenAPI Spec.

Usage:
    python api_gen.py --resources "users, products" --export openapi
"""

import argparse
import json

def generate_endpoints(resources):
    resource_list = [r.strip() for r in resources.split(",")]
    endpoints = []
    
    for res in resource_list:
        base = f"/{res.lower()}"
        singular = res.rstrip('s')
        
        # CRUD
        endpoints.append({"path": base, "method": "GET", "summary": f"List {res}", "tags": [res]})
        endpoints.append({"path": base, "method": "POST", "summary": f"Create {singular}", "tags": [res]})
        endpoints.append({"path": f"{base}/{{id}}", "method": "GET", "summary": f"Get {singular}", "tags": [res]})
        endpoints.append({"path": f"{base}/{{id}}", "method": "PUT", "summary": f"Update {singular}", "tags": [res]})
        endpoints.append({"path": f"{base}/{{id}}", "method": "DELETE", "summary": f"Delete {singular}", "tags": [res]})
        
        # Domain specific
        if res == "users":
            endpoints.append({"path": "/auth/login", "method": "POST", "summary": "User Login", "tags": ["Auth"]})
            endpoints.append({"path": "/auth/register", "method": "POST", "summary": "User Register", "tags": ["Auth"]})
        if res == "products":
            endpoints.append({"path": f"{base}/search", "method": "GET", "summary": "Search products", "tags": [res]})

    return endpoints

def export_openapi(endpoints):
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Generated API",
            "version": "1.0.0"
        },
        "paths": {}
    }
    
    for ep in endpoints:
        path = ep["path"]
        method = ep["method"].lower()
        
        if path not in spec["paths"]:
            spec["paths"][path] = {}
            
        spec["paths"][path][method] = {
            "summary": ep["summary"],
            "tags": ep["tags"],
            "responses": {
                "200": {"description": "Successful operation"}
            }
        }
        
    return spec

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resources", type=str, required=True, help="Model names")
    parser.add_argument("--export", type=str, choices=["text", "openapi"], default="text")
    
    args = parser.parse_args()
    endpoints = generate_endpoints(args.resources)
    
    if args.export == "openapi":
        print(json.dumps(export_openapi(endpoints), indent=2))
    else:
        print("\n⚡ Generated Endpoints:\n")
        for ep in endpoints:
            print(f"[{ep['method']}] {ep['path']} - {ep['summary']}")
        print("\n\n(Tip: Use --export openapi to generate Swagger JSON)")

if __name__ == "__main__":
    main()

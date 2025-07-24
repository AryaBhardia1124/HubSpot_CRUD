import os
import sys
import argparse
import requests
import json

HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
BASE_URL = 'https://api.hubapi.com/automation/v4/workflows'
HEADERS = {
    'Authorization': f'Bearer {HUBSPOT_API_KEY}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

def check_api_key():
    if not HUBSPOT_API_KEY:
        print('Error: HUBSPOT_API_KEY environment variable not set.')
        sys.exit(1)

def create_workflow(args):
    check_api_key()
    with open(args.file, 'r') as f:
        data = json.load(f)
    resp = requests.post(BASE_URL, headers=HEADERS, json=data)
    print(resp.status_code, resp.text)

def read_workflow(args):
    check_api_key()
    url = f"{BASE_URL}/{args.workflow_id}"
    resp = requests.get(url, headers=HEADERS)
    print(resp.status_code, resp.text)

def list_workflows(args):
    check_api_key()
    resp = requests.get(BASE_URL, headers=HEADERS)
    print(resp.status_code, resp.text)

def update_workflow(args):
    check_api_key()
    with open(args.file, 'r') as f:
        data = json.load(f)
    url = f"{BASE_URL}/{args.workflow_id}"
    resp = requests.patch(url, headers=HEADERS, json=data)
    print(resp.status_code, resp.text)

def delete_workflow(args):
    check_api_key()
    url = f"{BASE_URL}/{args.workflow_id}"
    resp = requests.delete(url, headers=HEADERS)
    print(resp.status_code, resp.text)

def main():
    parser = argparse.ArgumentParser(description='HubSpot Workflows CRUD CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Create
    parser_create = subparsers.add_parser('create', help='Create a new workflow')
    parser_create.add_argument('file', help='JSON file with workflow definition')
    parser_create.set_defaults(func=create_workflow)

    # Read
    parser_read = subparsers.add_parser('read', help='Read a workflow by ID')
    parser_read.add_argument('workflow_id', help='Workflow ID')
    parser_read.set_defaults(func=read_workflow)

    # List
    parser_list = subparsers.add_parser('list', help='List all workflows')
    parser_list.set_defaults(func=list_workflows)

    # Update
    parser_update = subparsers.add_parser('update', help='Update a workflow by ID')
    parser_update.add_argument('workflow_id', help='Workflow ID')
    parser_update.add_argument('file', help='JSON file with updated workflow definition')
    parser_update.set_defaults(func=update_workflow)

    # Delete
    parser_delete = subparsers.add_parser('delete', help='Delete a workflow by ID')
    parser_delete.add_argument('workflow_id', help='Workflow ID')
    parser_delete.set_defaults(func=delete_workflow)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()

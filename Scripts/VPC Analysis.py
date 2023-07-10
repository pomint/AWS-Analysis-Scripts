import json
import pandas as pd

def analyze_vpc_configuration(vpc_file, vpc_endpoints_file):
    with open(vpc_file, 'r') as f:
        vpc_data = json.load(f)

    with open(vpc_endpoints_file, 'r') as f:
        vpc_endpoints_data = json.load(f)

    # Perform analysis on VPCs
    vpcs = vpc_data['Vpcs']
    vpc_analysis_results = []

    for vpc in vpcs:
        vpc_id = vpc['VpcId']
        cidr_block = vpc['CidrBlock']
        vpc_endpoints = get_vpc_endpoints(vpc_id, vpc_endpoints_data)
        analyze_vpc(vpc_id, cidr_block, vpc, vpc_endpoints, vpc_analysis_results)

    # Convert VPC analysis results to a DataFrame using Pandas
    vpc_df = pd.DataFrame(vpc_analysis_results, columns=[
        'VPC ID', 'CIDR Block', 'VPC State', 'VPC Tenancy',
        'Endpoint Service', 'Endpoint Type', 'Endpoint State'
    ])

    # Export VPC analysis results to an Excel file
    vpc_excel_file = 'vpc_analysis.xlsx'
    vpc_df.to_excel(vpc_excel_file, index=False)
    print(f"VPC analysis results exported to {vpc_excel_file}")

def get_vpc_endpoints(vpc_id, vpc_endpoints_data):
    # Filter VPC endpoints based on VPC ID
    vpc_endpoints = []
    for endpoint in vpc_endpoints_data['VpcEndpoints']:
        if endpoint['VpcId'] == vpc_id:
            vpc_endpoints.append(endpoint)
    return vpc_endpoints

def analyze_vpc(vpc_id, cidr_block, vpc, vpc_endpoints, vpc_analysis_results):
    # Extract VPC details
    vpc_state = vpc['State']
    vpc_tenancy = vpc['InstanceTenancy']

    # Perform analysis on VPC endpoints
    for endpoint in vpc_endpoints:
        service_name = endpoint['ServiceName']
        endpoint_type = endpoint['VpcEndpointType']
        endpoint_state = endpoint['State']

        vpc_analysis_results.append({
            'VPC ID': vpc_id,
            'CIDR Block': cidr_block,
            'VPC State': vpc_state,
            'VPC Tenancy': vpc_tenancy,
            'Endpoint Service': service_name,
            'Endpoint Type': endpoint_type,
            'Endpoint State': endpoint_state
        })

# Usage: Provide the paths to the exported configuration files
vpc_file = 'describe_vpcs.json'
vpc_endpoints_file = 'describe_vpc_endpoints.json'
analyze_vpc_configuration(vpc_file, vpc_endpoints_file)

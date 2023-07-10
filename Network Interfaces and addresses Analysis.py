import json
import pandas as pd

def analyze_configuration(addresses_file, network_interfaces_file):
    with open(addresses_file, 'r') as f:
        addresses_data = json.load(f)

    with open(network_interfaces_file, 'r') as f:
        network_interfaces_data = json.load(f)

    address_analysis_results = analyze_addresses(addresses_data)
    network_interface_analysis_results = analyze_network_interfaces(network_interfaces_data)

    # Convert address analysis results to a DataFrame using Pandas
    address_df = pd.DataFrame(address_analysis_results, columns=[
        'Public IP', 'Allocation ID', 'Domain', 'Instance ID'
    ])

    # Convert network interface analysis results to a DataFrame using Pandas
    network_interface_df = pd.DataFrame(network_interface_analysis_results, columns=[
        'Interface ID', 'VPC ID', 'Subnet ID', 'Private IP', 'Public IP', 'Instance ID'
    ])

    # Export address analysis results to an Excel file
    address_excel_file = 'address_analysis.xlsx'
    address_df.to_excel(address_excel_file, index=False)
    print(f"Address analysis results exported to {address_excel_file}")

    # Export network interface analysis results to an Excel file
    network_interface_excel_file = 'network_interface_analysis.xlsx'
    network_interface_df.to_excel(network_interface_excel_file, index=False)
    print(f"Network interface analysis results exported to {network_interface_excel_file}")

def analyze_addresses(addresses_data):
    address_analysis_results = []

    for address in addresses_data['Addresses']:
        public_ip = address['PublicIp']
        allocation_id = address['AllocationId']
        domain = address['Domain']
        instance_id = address.get('InstanceId', 'Not Assigned')

        address_analysis_results.append({
            'Public IP': public_ip,
            'Allocation ID': allocation_id,
            'Domain': domain,
            'Instance ID': instance_id
        })

    return address_analysis_results

def analyze_network_interfaces(network_interfaces_data):
    network_interface_analysis_results = []

    for network_interface in network_interfaces_data['NetworkInterfaces']:
        interface_id = network_interface['NetworkInterfaceId']
        vpc_id = network_interface['VpcId']
        subnet_id = network_interface['SubnetId']
        private_ips = network_interface.get('PrivateIpAddresses', [])

        for private_ip in private_ips:
            private_ip_address = private_ip['PrivateIpAddress']
            public_ip = private_ip.get('Association', {}).get('PublicIp', 'Not Assigned')
            instance_id = private_ip.get('Association', {}).get('InstanceId', 'Not Assigned')

            network_interface_analysis_results.append({
                'Interface ID': interface_id,
                'VPC ID': vpc_id,
                'Subnet ID': subnet_id,
                'Private IP': private_ip_address,
                'Public IP': public_ip,
                'Instance ID': instance_id
            })

    return network_interface_analysis_results

# Usage: Provide the paths to the exported configuration files
addresses_file = 'describe_addresses.json'
network_interfaces_file = 'describe_network_interfaces.json'
analyze_configuration(addresses_file, network_interfaces_file)

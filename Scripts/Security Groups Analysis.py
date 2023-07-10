import json
import pandas as pd

def analyze_security_groups(config_file):
    with open(config_file, 'r') as f:
        config_data = json.load(f)

        # Assuming the exported configuration file contains security group information
        security_groups = config_data.get('SecurityGroups', [])

        # Create a list to store the analysis results
        security_groups_results = []

        # Perform analysis on each security group
        for group in security_groups:
            group_id = group.get('GroupId')
            group_name = group.get('GroupName')
            ingress_rules = group.get('IpPermissions', [])
            egress_rules = group.get('IpPermissionsEgress', [])

            # Analyze ingress rules
            for rule in ingress_rules:
                protocol = rule.get('IpProtocol')
                from_port = rule.get('FromPort')
                to_port = rule.get('ToPort')
                ip_ranges = rule.get('IpRanges', [])
                source = rule.get('UserIdGroupPairs', [])
                destination = [{'GroupId': group_id, 'GroupName': group_name}]

                # Iterate over each CIDR block
                for ip_range in ip_ranges:
                    cidr_block = ip_range['CidrIp']

                    # Analyze the rule
                    analysis = analyze_rule(protocol, from_port, to_port, cidr_block, source, destination)
                    security_groups_results.append({
                        'Security Group ID': group_id,
                        'Security Group Name': group_name,
                        'Rule Type': 'Ingress',
                        'Protocol': analysis.get('protocol'),
                        'From Port': analysis.get('from_port'),
                        'To Port': analysis.get('to_port'),
                        'CIDR Block': analysis.get('cidr_block'),
                        'Source Group ID': analysis.get('source_group_id'),
                        'Source Group Name': analysis.get('source_group_name'),
                        'Destination Group ID': analysis.get('destination_group_id'),
                        'Destination Group Name': analysis.get('destination_group_name'),
                        'Analysis': analysis.get('analysis'),
                        'Recommendation': analysis.get('recommendation')
                    })

            # Analyze egress rules (similar logic as ingress rules)
            for rule in egress_rules:
                protocol = rule.get('IpProtocol')
                from_port = rule.get('FromPort')
                to_port = rule.get('ToPort')
                ip_ranges = rule.get('IpRanges', [])
                destination = rule.get('UserIdGroupPairs', [])
                source = [{'GroupId': group_id, 'GroupName': group_name}]

                # Iterate over each CIDR block
                for ip_range in ip_ranges:
                    cidr_block = ip_range['CidrIp']

                    # Analyze the rule
                    analysis = analyze_rule(protocol, from_port, to_port, cidr_block, source, destination)
                    security_groups_results.append({
                        'Security Group ID': group_id,
                        'Security Group Name': group_name,
                        'Rule Type': 'Egress',
                        'Protocol': analysis.get('protocol'),
                        'From Port': analysis.get('from_port'),
                        'To Port': analysis.get('to_port'),
                        'CIDR Block': analysis.get('cidr_block'),
                        'Source Group ID': analysis.get('source_group_id'),
                        'Source Group Name': analysis.get('source_group_name'),
                        'Destination Group ID': analysis.get('destination_group_id'),
                        'Destination Group Name': analysis.get('destination_group_name'),
                        'Analysis': analysis.get('analysis'),
                        'Recommendation': analysis.get('recommendation')
                    })

    # Convert analysis results to a DataFrame using Pandas
    security_groups_df = pd.DataFrame(security_groups_results)

    # Export DataFrame to Excel
    excel_file = 'security_group_analysis.xlsx'
    security_groups_df.to_excel(excel_file, sheet_name='Security Groups', index=False)

    print(f"Analysis results exported to {excel_file}")


def analyze_rule(protocol, from_port, to_port, cidr_block, source, destination):
    analysis = {
        'protocol': protocol,
        'from_port': from_port if from_port is not None else 'Not Defined',
        'to_port': to_port if to_port is not None else 'Not Defined',
        'cidr_block': cidr_block,
        'source_group_id': None,
        'source_group_name': None,
        'destination_group_id': None,
        'destination_group_name': None
    }

    if protocol == '-1':
        analysis['protocol'] = 'Any'
        analysis['analysis'] = 'Overly Permissive: All Protocols Allowed'
        analysis['recommendation'] = 'Restrict the protocol to specific allowed protocols.'
    elif from_port == 0 and to_port == 65535:
        analysis['analysis'] = 'Overly Permissive: All Ports Allowed'
        analysis['recommendation'] = 'Restrict the port range to only necessary ports.'
    elif from_port is None or to_port is None:
        analysis['analysis'] = 'Invalid: Missing Port Information'
        analysis['recommendation'] = 'Specify the port range for the rule.'
    elif from_port == to_port:
        analysis['analysis'] = f'Valid: Single Port Allowed ({from_port})'
        analysis['recommendation'] = None
    else:
        analysis['analysis'] = f'Valid: Port Range Allowed ({from_port}-{to_port})'
        analysis['recommendation'] = None

    if source:
        analysis['source_group_id'] = source[0].get('GroupId')
        analysis['source_group_name'] = source[0].get('GroupName')

    if destination:
        analysis['destination_group_id'] = destination[0].get('GroupId')
        analysis['destination_group_name'] = destination[0].get('GroupName')

    return analysis


# Usage: Provide the path to the exported configuration file
security_groups_data = 'describe_security_groups.json'
analyze_security_groups(security_groups_data)

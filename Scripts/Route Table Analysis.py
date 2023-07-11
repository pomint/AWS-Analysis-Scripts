import json
import pandas as pd

def analyze_route_table_configuration(config_file):
    with open(config_file, 'r') as f:
        config_data = json.load(f)

        if 'RouteTables' in config_data:
            route_tables = config_data['RouteTables']
            analysis_results = []

            for route_table in route_tables:
                route_table_id = route_table.get('RouteTableId')
                vpc_id = route_table.get('VpcId')
                routes = route_table.get('Routes')
                tags = route_table.get('Tags', [])
                name_tag_value = get_tag_value_by_key(tags, 'Name')
                analyze_route_table(route_table_id, vpc_id, routes, name_tag_value, analysis_results)

            # Convert analysis results to a DataFrame using Pandas
            df = pd.DataFrame(analysis_results, columns=[
                'Route Table ID', 'VPC ID', 'Route Table Name', 'Route Destination', 'Target', 'Status', 'Details', 'Recommendation', 'Propagation', 'Blackhole'
            ])

            # Export DataFrame to an Excel file
            excel_file = 'route_table_analysis.xlsx'
            df.to_excel(excel_file, index=False)

            print(f"Route table analysis results exported to {excel_file}")

def get_tag_value_by_key(tags, key):
    for tag in tags:
        if tag['Key'] == key:
            return tag['Value']
    return ''

def analyze_route_table(route_table_id, vpc_id, routes, name_tag_value, analysis_results):
    for route in routes:
        destination_cidr = route.get('DestinationCidrBlock')
        gateway_id = route.get('GatewayId')
        instance_id = route.get('InstanceId')
        interface_id = route.get('NetworkInterfaceId')
        state = route.get('State')
        propagation = route.get('PropagatingVgws')
        blackhole = route.get('Blackhole')
        analyze_route(route_table_id, vpc_id, destination_cidr, gateway_id, instance_id, interface_id, state, propagation, blackhole, name_tag_value, analysis_results)

def analyze_route(route_table_id, vpc_id, destination_cidr, gateway_id, instance_id, interface_id, state, propagation, blackhole, name_tag_value, analysis_results):
    # Perform analysis on the route
    analysis = {}

    # Example: Analyze the route target and status
    target, status, details = analyze_route_target(gateway_id, instance_id, interface_id)
    analysis['Route Destination'] = destination_cidr
    analysis['Target'] = target
    analysis['Status'] = status
    analysis['Details'] = details

    # Example: Analyze propagation
    analysis['Propagation'] = analyze_propagation(propagation)

    # Example: Analyze blackhole
    analysis['Blackhole'] = analyze_blackhole(blackhole)

    # Generate recommendations based on the analysis
    recommendation = generate_recommendation(destination_cidr, target, status)

    # Extract analysis results into separate rows
    analysis_results.append({
        'Route Table ID': route_table_id,
        'VPC ID': vpc_id,
        'Route Table Name': name_tag_value,
        'Route Destination': destination_cidr,
        'Target': target,
        'Status': status,
        'Details': details,
        'Recommendation': recommendation,
        'Propagation': analysis['Propagation'],
        'Blackhole': analysis['Blackhole']
    })

def analyze_route_target(gateway_id, instance_id, interface_id):
    # Example analysis logic for route target and status
    target = ''
    status = ''
    details = ''

    if gateway_id:
        target = f"Gateway: {gateway_id}"
        status = 'Active'
        details = 'The route is targeted to a gateway.'
    elif instance_id:
        target = f"Instance: {instance_id}"
        status = 'Active'
        details = 'The route is targeted to an instance.'
    elif interface_id:
        target = f"Interface: {interface_id}"
        status = 'Active'
        details = 'The route is targeted to a network interface.'
    else:
        target = 'Not Defined'
        status = 'Inactive'
        details = 'The route target is not defined.'

    return target, status, details

def analyze_propagation(propagation):
    # Example analysis logic for propagation
    if propagation:
        return 'Yes'
    else:
        return 'No'

def analyze_blackhole(blackhole):
    # Example analysis logic for blackhole
    if blackhole:
        return 'Yes'
    else:
        return 'No'

def generate_recommendation(destination_cidr, target, status):
    # Example recommendation logic based on analysis
    recommendation = ''

    if destination_cidr == '0.0.0.0/0' and target == 'Not Defined':
        recommendation = 'Consider defining a target for the default route to enable outbound internet access.'
    elif destination_cidr == '0.0.0.0/0' and target.startswith('Gateway'):
        recommendation = 'Review the gateway used as the target for the default route to ensure it is properly configured.'
    elif status == 'Inactive':
        recommendation = 'Activate the route or define a valid target for the route.'

    return recommendation

# Usage: Provide the path to the exported configuration file
config_file = 'describe_route_tables.json'
analyze_route_table_configuration(config_file)

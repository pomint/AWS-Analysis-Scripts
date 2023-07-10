# AWS-Analysis-Scripts
Scripts to perform analysis of AWS Configs without using AWS API

░█─░█ ░█▀▀▀█ ─█▀▀█ ░█▀▀█ ░█▀▀▀ 

░█─░█ ─▀▀▀▄▄ ░█▄▄█ ░█─▄▄ ░█▀▀▀ 

─▀▄▄▀ ░█▄▄▄█ ░█─░█ ░█▄▄█ ░█▄▄▄


1. Download Scripts
2. Install Python 3
3. Run ps1 Scripts to install and python packages

- Open Terminal / CMD
- Run the following commands:
> cd <scripts location>
> & '.\install python packages.ps1'

4. Run script to perform analsis of config files

- For all analysis available:
> & '.\Run Analysis.ps1'

- For individual analysis as required:
ACL          					   : python '.\ACL Analysis.py'
Subnet	     			 		   : python '.\Subnet Analysis.py'
Route Table 					   : python '.\Route Table Analysis.py'
Network Interfaces and Addresses   : python '.\Network Interfaces and addresses Analysis.py'
VPCs							   : python '.\VPC Analysis.py'
Security Groups					   : python '.\Security Groups Analysis.py'

░█▀▀█ ░█▀▀▀ ░█▀▀█ ░█─░█ ▀█▀ ░█▀▀█ ░█▀▀▀ ░█▀▀▄   ░█▀▀▀ ▀█▀ ░█─── ░█▀▀▀ ░█▀▀▀█ 

░█▄▄▀ ░█▀▀▀ ░█─░█ ░█─░█ ░█─ ░█▄▄▀ ░█▀▀▀ ░█─░█   ░█▀▀▀ ░█─ ░█─── ░█▀▀▀ ─▀▀▀▄▄ 

░█─░█ ░█▄▄▄ ─▀▀█▄ ─▀▄▄▀ ▄█▄ ░█─░█ ░█▄▄▄ ░█▄▄▀   ░█─── ▄█▄ ░█▄▄█ ░█▄▄▄ ░█▄▄▄█

1. AWS Configuration JSONs (Exported via AWS CLI)
   aws --output json ec2 describe_addresses
   aws --output json ec2 describe_network_acls
   aws --output json ec2 describe_network_interfaces
   aws --output json ec2 describe_route_tables
   aws --output json ec2 describe_security_groups
   aws --output json ec2 describe_subnets
   aws --output json ec2 describe_vpc_endpoints
   aws --output json ec2 describe_vpcs 


import ipaddress
import boto3
from botocore.exceptions import ClientError
from tabulate import tabulate

# method to check whether the input is a ip range or not
def check_ip(address):
    try:
        ipaddress.ip_network(address)
        return True
    except:
        return False

#  method to list of SGs for each instances
def listSgForEachInstances():
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                sg_name = []
                sg_id = []
                for securityGroup in instance['SecurityGroups']:
                    sg_name.append(securityGroup['GroupName'])
                    sg_id.append(securityGroup['GroupId'])
                print(tabulate({'Instance ID':[instance['InstanceId']],'Security Group ID':sg_id,'Security Group Name':sg_name}, headers='keys',tablefmt="grid"))
    except ClientError as e:
        print(e)

# method to list details of each SG
def listDetailsOfEachSg():
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_security_groups()
        for sg in response['SecurityGroups']:
            egress_ip_protocol = []
            egress_port = []
            egress_ip_ranges = []
            egress_rule_description = []
            ingress_ip_protocol = []
            ingress_port = []
            ingress_ip_ranges = []
            ingress_rule_description = []
            for j in sg['IpPermissionsEgress']:
                #print("\nIP Protocol: {}".format(j['IpProtocol']))
                egress_ip_protocol.append(j['IpProtocol'])
                try:
                    #print("PORT: {}".format(str(j['FromPort'])))
                    egress_port.append(j['FromPort'])
                except:
                    #print("All Ports are open")
                    egress_port.append("All ports are open")
                #egress_ip_ranges = []
                #egress_rule_description = []
                egress_ip_ranges_tmp = []
                egress_rule_description_tmp = []
                for k in j['IpRanges']:
                    #print("IP Ranges: {}".format(k['CidrIp']))
                    egress_ip_ranges_tmp.append(k['CidrIp'])
                    try:
                        #print("Description: {}".format(k['Description']))
                        egress_rule_description_tmp.append(k['Description'])
                    except:
                        #print("No description is given")
                        egress_rule_description_tmp.append("No description is given")
                egress_ip_ranges.append(egress_ip_ranges_tmp)
                egress_rule_description.append(egress_rule_description_tmp)
            print("\n\nSecurity Groups and associated Egress rules are as follows: \n")
            print(tabulate({'Security Group Name':[sg['GroupName']],'Security Group Description':[sg['Description']],'Egress IP Protocol':egress_ip_protocol,'Egress IP Range':egress_ip_ranges,'Egress Port':egress_port,'Description':egress_rule_description}, headers='keys',tablefmt="grid"))
            for j in sg['IpPermissions']:
                #print("\nIP Protocol: {}".format(j['IpProtocol']))
                ingress_ip_protocol.append(j['IpProtocol'])
                try:
                    #print("PORT: {}".format(str(j['FromPort'])))
                    ingress_port.append(j['FromPort'])
                except:
                    #print("All Ports are open")
                    ingress_port.append("All ports are open")
                ingress_ip_ranges_tmp = []
                ingress_rule_description_tmp = []
                for k in j['IpRanges']:
                    #print("IP Ranges: {}".format(k['CidrIp']))
                    ingress_ip_ranges_tmp.append(k['CidrIp'])
                    #ingress_ip_ranges.append(k['CidrIp'])
                    try:
                        #print("Description: {}".format(k['Description']))
                        ingress_rule_description_tmp.append(k['Description'])
                    except:
                        #print("No description is given")
                        ingress_rule_description_tmp.append("No description is available")
                ingress_ip_ranges.append(ingress_ip_ranges_tmp)
                ingress_rule_description.append(ingress_rule_description_tmp)
            print("\n\nSecurity Groups and associated Ingress rules are as follows: \n")
            print(tabulate({'Security Group Name':[sg['GroupName']],'Security Group Description':[sg['Description']],'Ingress IP Protocol':ingress_ip_protocol,'Ingress IP Range':ingress_ip_ranges,'Ingress Port':ingress_port,'Description':ingress_rule_description}, headers='keys',tablefmt="grid"))

    except ClientError as e:
        print(e)

# method to show how many ips there in each sg
def listSgHavingIpInInboundRule():
    sg_name = []
    egress_count = []
    ingress_count = []
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_security_groups()
        for sg in response['SecurityGroups']:
            egress_ip_count = 0
            ingress_ip_count = 0
            for j in sg['IpPermissionsEgress']:
                for k in j['IpRanges']:
                    if check_ip(k['CidrIp']):
                        egress_ip_count += 1
            for j in sg['IpPermissions']:
                try:
                    for k in j['IpRanges']:
                        if check_ip(k['CidrIp']):
                            ingress_ip_count += 1
                except Exception:
                    continue
            sg_name.append(sg['GroupName'])
            egress_count.append(egress_ip_count)
            ingress_count.append(ingress_ip_count)
        print(tabulate({'Security Group Name':sg_name,'Total no of IPs in Egress':egress_count,'Total no of IPs in Ingress':ingress_count}, headers='keys', tablefmt="grid"))
    except ClientError as e:
        print(e)

# main method
def main():

    while True:
        print("\n\nSelect from the options below : ")
        print("1. List the Security Groups with total No of IPs present in Egress and Ingress rules.")
        print("2. List the Security Groups with deatiled information of Egress and Ingress rules.")
        print("3. List the EC2 Instances with associated security groups")
        print("4. Exit")
        inp = int(input())
        if inp == 1:
            listSgHavingIpInInboundRule()
        elif inp == 2:
            listDetailsOfEachSg()
        elif inp == 3:
            listSgForEachInstances()
        elif inp == 4:
            exit()
        else:
            print("Wrong Input")

if __name__ == "__main__":
    main()
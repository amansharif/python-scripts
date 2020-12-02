
---

## Python Script to get the details of IPs and Ports present in AWS Security Groups and EC2 Instances

Generates a report in tabular form:

1. about the EC2 instances and associated Security Groups.
2. about the total no of IPs present in each Security Group.
3. about the IPs and Ports present in each Security Group.

---

## Dependencies

1. Python 3
2. boto3
3. ipaddress
4. tabulate
5. aws CLI

---

## Prerequisite

1. Make sure the dependencies are installed.
2. Configure the aws by firing the command `aws configure`


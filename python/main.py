import argparse
import boto3
import botocore

# EC2 client at the beginning
ec2 = boto3.client("ec2", region_name='eu-north-1')

def create_bucket(bucket_name, bucket_region):
    """
    Create an S3 bucket with the specified parameters.
    :param bucket_name: The name of the S3 bucket.
    :param bucket_region: The AWS region where the bucket should be created.
    """
    try:
     s3_client = boto3.client("s3", region_name=bucket_region)

     s3_client.create_bucket(
         Bucket=bucket_name,
         CreateBucketConfiguration={"LocationConstraint": bucket_region},
     )
     print("Bucket successfuly created")
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyExists":
            print(f"S3 bucket '{bucket_name}' already exists.")
        else:
          print("Some other err")


def create_key(keypair_name):
    """
    Create a key pair for EC2 with .pem extension.
    :param keypair_name: The name of the key pair.
    """
    key_pair = ec2.create_key_pair(KeyName=keypair_name)
    with open(f"{keypair_name}.pem", "w") as outfile:
        outfile.write(key_pair["KeyMaterial"])

def create_security_group(security_group_name):
    """
    Create a security group for EC2 and open necessary ports for our protocols.
    :param security_group_name: The name of the security group.
    """
    security_group = ec2.create_security_group(
        GroupName=security_group_name, Description="Ports 80 and 22"
    )
    permissions = [
        {
            "IpProtocol": "tcp",
            "FromPort": 80,
            "ToPort": 80,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
        },
        {
            "IpProtocol": "tcp",
            "FromPort": 22,
            "ToPort": 22,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
        },
    ]
    # Authorize the inbound rules for the security group
    ec2.authorize_security_group_ingress(
        GroupId=security_group["GroupId"], IpPermissions=permissions
    )
    print("Security group is created")

def create_vm(instance_type, security_group_name, keypair_name):
    """
    Create an EC2 instance with the specified parameters.
    :param instance_type: The EC2 instance type like t3.micro, t3.large etc.
    :param security_group_name: The name of the security group to associate with the instance.
    :param keypair_name: The name of the key pair to use for the instance.
    """
    placement = {"AvailabilityZone": "eu-north-1c"}

    try:
        instances = ec2.run_instances(
            ImageId="ami-0989fb15ce71ba39e",
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            KeyName=keypair_name,
            Placement=placement,
            SecurityGroups=[security_group_name],
        )
        print("EC2 instance created successfully.")
    except botocore.exceptions.ClientError as e:
        print(f"An error occurred while creating the EC2 instance: {e}")

def create_vpc():
    """
    Create a new VPC in AWS with a specified CIDR block, extract it, and print its VPC ID.
    """
    # Specify the VPC details
    vpc_cidr_block = "172.31.0.0/16"
    # Create the VPC
    response = ec2.create_vpc(CidrBlock=vpc_cidr_block)
    # Extract the VPC ID
    vpc_id = response["Vpc"]["VpcId"]
    # Corrected the line below (changed ec2_client to ec2)
    response = ec2.create_subnet(VpcId=vpc_id, CidrBlock=vpc_cidr_block)
    print(f"VPC created with ID: {vpc_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Amazon features")
    args = parser.parse_args()
    bucket_name = "aleksabucket"
    bucket_region = 'eu-north-1'
    keypair_name = "aleksaskeypair"
    security_group_name = "AleksaGroup"

    create_bucket(bucket_name, bucket_region)
    create_vpc()
    create_key(keypair_name)
    create_security_group(security_group_name)
    create_vm(instance_type="t3.micro", security_group_name=security_group_name, keypair_name=keypair_name)

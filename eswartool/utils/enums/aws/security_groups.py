import boto3


def get_data(session: boto3.Session):
    ec2_client = session.client('ec2')
    response = ec2_client.describe_security_groups()

    for sg in response['SecurityGroups']:
        sg_id = sg['GroupId']
        sg_name = sg.get('GroupName', '')
        sg_description = sg.get('Description', '')

        allows_all_inbound = False

        for rule in sg['IpPermissions']:
            if rule['IpProtocol'] == '-1':  # Protocolo -1 indica todo el tráfico
                for ip_range in rule.get('IpRanges', []):
                    if ip_range.get('CidrIp') == '0.0.0.0/0':
                        allows_all_inbound = True
                for ipv6_range in rule.get('Ipv6Ranges', []):
                    if ipv6_range.get('CidrIpv6') == '::/0':
                        allows_all_inbound = True

        yield {
            'GroupId': sg_id,
            'GroupName': sg_name,
            'Description': sg_description,
            'AllowsAllInbound': allows_all_inbound
        }

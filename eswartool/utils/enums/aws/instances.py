import boto3


def get_data(session: boto3.Session):
    ec2 = session.client('ec2')
    instancias = ec2.describe_instances()['Reservations']

    for reserva in instancias:
        # Iterar sobre las instancias dentro de la reserva
        for instancia in reserva['Instances']:
            public_ip = instancia.get('PublicIpAddress', 'N/A')
            private_ip = instancia.get('PrivateIpAddress', 'N/A')
            nombre = 'N/A'
            for tag in instancia.get('Tags', []):
                if tag['Key'] == 'Name':
                    nombre = tag['Value']
    
            grupos_seguridad = [grupo['GroupName'] for grupo in instancia.get('SecurityGroups', [])]
            estado = instancia['State']['Name']

            yield {
                'instance_id': instancia['InstanceId'],
                'name': nombre,
                'public_ip': public_ip,
                'private_ip': private_ip,
                'secutiry_group': grupos_seguridad,
                'State': estado
            }

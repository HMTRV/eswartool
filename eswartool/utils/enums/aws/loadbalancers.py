import boto3


def obtener_load_balancers(session: boto3.Session):
    elb_client = session.client('elbv2')
    load_balancers = elb_client.describe_load_balancers()['LoadBalancers']
    
    return load_balancers


def obtener_target_groups(session: boto3.Session, load_balancer_arn):
    elb_client = session.client('elbv2')
    target_groups = elb_client.describe_target_groups(LoadBalancerArn=load_balancer_arn)['TargetGroups']
    return target_groups


def obtener_health_checks(session: boto3.Session, target_group_arn):
    elb_client = session.client('elbv2')
    health_descriptions = elb_client.describe_target_health(TargetGroupArn=target_group_arn)['TargetHealthDescriptions']
    unhealthy_targets = [
        {
            'TargetId': desc['Target']['Id'],
            'Port': desc['Target']['Port'],
            'State': desc['TargetHealth']['State']
        }
        for desc in health_descriptions if desc['TargetHealth']['State'] != 'healthy'
    ]
    return unhealthy_targets


def get_data(session: boto3.Session):
    load_balancers = obtener_load_balancers(session)

    lb_data = []
    unhealthy_details = []

    for lb in load_balancers:
        lb_arn = lb['LoadBalancerArn']
        lb_name = lb['LoadBalancerName']
        lb_scheme = lb['Scheme']
        lb_dns = lb['DNSName']

        # Determinar si es de cara a Internet
        internet_facing = lb_scheme == 'internet-facing'

        # Obtener target groups asociados
        target_groups = obtener_target_groups(session, lb_arn)
        unhealthy = False
        target_ids = []

        for tg in target_groups:
            tg_name = tg['TargetGroupName']
            tg_arn = tg['TargetGroupArn']
            unhealthy_targets = obtener_health_checks(session, tg_arn)

            if unhealthy_targets:
                unhealthy = True
                for target in unhealthy_targets:
                    unhealthy_details.append({
                        'LoadBalancerName': lb_name,
                        'TargetGroupName': tg_name,
                        'TargetId': target['TargetId'],
                        'Port': target['Port'],
                        'State': target['State']
                    })
                    target_ids.append(target['TargetId'])

        lb_data.append({
            'LoadBalancerName': lb_name,
            'InternetFacing': internet_facing,
            'HasUnhealthyTargets': unhealthy,
            'DNSName': lb_dns,
            'TargetIds': ', '.join(target_ids)  # Concatenar los IDs de los targets
        })


    return lb_data

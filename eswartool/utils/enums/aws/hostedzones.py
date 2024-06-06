import boto3


def get_data(session: boto3.Session):
    route53_client = session.client('route53')
    response = route53_client.list_hosted_zones()

    for hosted_zone in response['HostedZones']:
        zone_id = hosted_zone['Id'].split('/')[-1]
        zone_name = hosted_zone['Name']
        
        records_response = route53_client.list_resource_record_sets(HostedZoneId=zone_id)
        
        records_response = route53_client.list_resource_record_sets(
            HostedZoneId=zone_id)
        
        resources_sets = records_response['ResourceRecordSets']

        for resources in resources_sets:
            resources['ZoneName'] = zone_name
            resources['hosted_zone'] = hosted_zone
            yield resources


def GenerateConfig(context):
    """Generate YAML resource configuration."""

    cluster_name = context.properties['CLUSTER_NAME']
    cluster_zone = context.properties['CLUSTER_ZONE']
    number_of_nodes = context.properties['NUM_NODES']

    resources = []
    resources.append({
        'name': cluster_name,
        'type': 'container.v1.cluster',
        'properties': {
            'zone': cluster_zone,
            'cluster': {
                'name': cluster_name,
                'initialNodeCount': number_of_nodes,
                'nodeConfig': {
                    'oauthScopes': [
                        'https://www.googleapis.com/auth/' + scope
                        for scope in [
                            'compute',
                            'devstorage.read_only',
                            'logging.write',
                            'monitoring'
                            ]
                        ]
                    }
                }
            }
        })

    k8s_endpoints = {
        '': 'api/v1',
        '-apps': 'apis/apps/v1beta1',
        '-v1beta1-extensions': 'apis/extensions/v1beta1'
    }
    outputs = []
    type_name = cluster_name + '-type'
    for type_suffix, endpoint in k8s_endpoints.iteritems():
        resources.append({
            'name': type_name + type_suffix,
            'type': 'deploymentmanager.v2beta.typeProvider',
            'properties': {
                'options': {
                    'validationOptions': {
                        # Kubernetes API accepts ints, in fields they annotate
                        # with string. This validation will show as warning
                        # rather than failure for Deployment Manager.
                        # https://github.com/kubernetes/kubernetes/issues/2971
                        'schemaValidation': 'IGNORE_WITH_WARNINGS'
                    },
                    # According to kubernetes spec, the path parameter 'name'
                    # should be the value inside the metadata field
                    # https://github.com/kubernetes/community/blob/master
                    # /contributors/devel/api-conventions.md
                    # This mapping specifies that
                    'inputMappings': [{
                        'fieldName': 'name',
                        'location': 'PATH',
                        'methodMatch': '^(GET|DELETE|PUT)$',
                        'value': '$.ifNull('
                                '$.resource.properties.metadata.name, '
                                '$.resource.name)'
                    }, {
                        'fieldName': 'metadata.name',
                        'location': 'BODY',
                        'methodMatch': '^(PUT|POST)$',
                        'value': '$.ifNull('
                                '$.resource.properties.metadata.name, '
                                '$.resource.name)'
                    }, {
                        'fieldName': 'Authorization',
                        'location': 'HEADER',
                        'value': '$.concat("Bearer ",'
                                '$.googleOauth2AccessToken())'
                    }]
                },
                'descriptorUrl':
                    ''.join([
                        'https://$(ref.', cluster_name, '.endpoint)/swaggerapi/',
                        endpoint
                    ])
            }
        })
    outputs.append({
        'name': 'endpoint',
        'value': '$(ref.' + cluster_name + '.endpoint)'
        })

    return {'resources': resources, 'outputs': outputs}
from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime
from datetime import timedelta

import requests

# import debugpy

# # 5555 is the default attach port in the VS Code debug configurations.
# Unless a host and port are specified, host defaults to 127.0.0.1
# debugpy.listen(5555)
# print("Waiting for debugger attach")
# debugpy.wait_for_client()
# debugpy.breakpoint()
# print('break on this line')


logging.basicConfig(level=logging.DEBUG)


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
console_out = logging.StreamHandler(sys.stdout)


console_out.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    ),
)
logger.addHandler(console_out)


# --- Variables ---------------------------------------------------------------
# Get the token for authenticate via the API
if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount'):
    token = (
        open(
            '/var/run/secrets/kubernetes.io/serviceaccount/token',
        )
        .read()
        .replace('\n', '')
    )
else:
    token = os.environ['TOKEN']

os.environ['REQUESTS_CA_BUNDLE'] = os.environ.get('CA_PATH', '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt')  # noqa: E501
# API URL. Ex. https://kubernetes.default.svc/api/
apiURL = os.environ['API_URL']

# Namespace where the pods are running
namespace = os.environ.get('NAMESPACE', 'gitlab')

# Expiration time in hours, the pods older than "maxHours" are going to be deleted  # noqa: E501
maxHours = int(os.environ.get('MAX_HOURS', '1'))

# Only pods with the following status are going to be deleted
# You can send a list of string separate by comma, Ex. "Pending, Running, Succeeded, Failed, Error, Unknown"  # noqa: E501
podStatus = os.environ['POD_STATUS'].replace(' ', '').split(',')

logger.debug('Using the following pod states: %s' % podStatus)
# --- Functions ---------------------------------------------------------------


def callAPI(method, url):
    logger.debug('Call API %s' % url)
    headers = {'Authorization': 'Bearer ' + token}
    # requests.packages.urllib3.disable_warnings()
    request = requests.request(
        method, url, headers=headers, verify=True, timeout=10,
    )
    return request.json()


def getPods(namespace):
    logger.debug('Get pods from namespace %s' % namespace)
    url = apiURL + 'api/v1/namespaces/' + namespace + '/pods'
    response = callAPI('GET', url)
    return response['items']


def deletePod(podName, namespace):
    logger.debug(f'Delete pod {podName} from namespace {namespace}')
    url = apiURL + 'api/v1/namespaces/' + namespace + '/pods/' + podName
    response = callAPI('DELETE', url)
    logger.info('Delete call => %s' % url)
    return response


# --- Main --------------------------------------------------------------------
# Get all pods running in a namespace and delete older than "maxHours"
pods = getPods(namespace)
if not pods:
    logger.info('No pods for delete.')

for pod in pods:
    logger.debug('%s' % json.dumps(pod))
    logger.info('Pod name {} from namespace {}'.format(pod['metadata']['name'], pod['metadata']['namespace']))  # noqa: E501
    logger.debug('Filter by starts with %s' % os.environ['STARTS_WITH'])
    if pod['metadata']['name'].startswith(os.environ['STARTS_WITH']):
        logger.info('To delete pod name %s' % pod['metadata']['name'])
        logger.debug('Pod status %s' % pod['status']['phase'])
        if pod['status']['phase'] in podStatus:
            podStartTime = datetime.strptime(
                pod['status']['startTime'],
                '%Y-%m-%dT%H:%M:%SZ',
            )
            logger.debug('Pod start time %s' % str(podStartTime))
            nowDate = datetime.now()
            logger.info('Now: %s' % str(nowDate))
            if (podStartTime + timedelta(hours=maxHours)) < nowDate:
                logger.info(
                    'Deleting pod ('
                    + pod['metadata']['name']
                    + '). Status ('
                    + pod['status']['phase']
                    + '). Start time ('
                    + str(podStartTime)
                    + ')',
                )
                deletePod(pod['metadata']['name'], namespace)

logger.info('Done.')

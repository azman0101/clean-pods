# -*- mode: Python -*
# load('ext://restart_process', 'docker_build_with_restart')

# registry = os.getenv('REGISTRY_URL', '649370841936.dkr.ecr.us-east-1.amazonaws.com')
# registry = os.getenv('REGISTRY_URL', 'localhost:5005')
registry = os.getenv('REGISTRY_URL', 'ttl.sh/jboclara')
image = os.getenv('IMAGE_REPO_NAME', 'clean-pods-test')
env = os.getenv('ENV', 'staging')

default_registry(
  registry,
  single_name=image)

# Records the current time, then kicks off a server update.
# Normally, you would let Tilt do deploys automatically, but this
# shows you how to set up a custom workflow that measures it.
local_resource(
    'deploy',
    'python now.py > start-time.txt',
)

# allow_k8s_contexts('kind-cluster')
allow_k8s_contexts(k8s_context())

docker_build(
    'cleanup-gitlab',
    context='.',
    dockerfile='./Dockerfile.dev',
    entrypoint=['/usr/local/bin/python', '/app/clean.py'],
    # entrypoint=['/bin/sh', '-c', 'sleep infinity'],
    platform='linux/amd64',
)

yaml = kustomize('./manifests')
k8s_yaml(yaml)

k8s_resource('cleanup-gitlab', port_forwards=5555)

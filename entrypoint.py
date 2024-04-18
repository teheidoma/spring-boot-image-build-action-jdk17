import re
import subprocess
import os


def run_and_print_output(arg):
    if type(arg) == type([]):
        print(' '.join(arg))

    p = subprocess.run(arg, stdout=subprocess.PIPE, text=True)
    print(p.stdout)
    if p.returncode != 0:
        exit(p.returncode)


sdkman_dir = "/root/.sdkman"
sdkman_init_script = "/root/.sdkman/bin/sdkman-init.sh"

github_output_file = os.environ.get("GITHUB_OUTPUT")
registry_username = os.environ.get("INPUT_REGISTRY_USERNAME")
registry_password = os.environ.get("INPUT_REGISTRY_PASSWORD")
registry_hostname = os.environ.get("INPUT_REGISTRY_HOSTNAME")
include_commit_sha = os.environ.get("INPUT_INCLUDE_COMMIT_SHA")
github_sha = os.environ.get("GITHUB_SHA")[:10]

subprocess.run(["chmod", "+x", "./gradlew"])
process = subprocess.run(["./gradlew", "bootBuildImage"],
                         env=dict(os.environ) | {"JAVA_HOME": "/root/.sdkman/candidates/java/current"},
                         stdout=subprocess.PIPE, text=True)

output = process.stdout
print(output)

pattern = r'^Successfully built image \'(.+):(.+)\'$'
match = re.search(pattern, output, re.MULTILINE)
if match:
    image_name = match.group(1)
    image_tag = match.group(2)
else:
    exit(1)

if registry_username and registry_password:
    run_and_print_output(["docker", "login", "-u", registry_username, "-p", registry_password, registry_hostname])

if include_commit_sha.lower() == 'true':
    original_image = f'{image_name}:{image_tag}'
    modified_image = f'{image_name}:{image_tag}-{github_sha}'
    run_and_print_output(['docker', 'tag', original_image, modified_image])
    image_tag = f'{image_tag}-{github_sha}'

with open(github_output_file, "a") as output_file:
    output_file.write(f"IMAGE_NAME={image_name}\n")
    output_file.write(f"IMAGE_TAG={image_tag}\n")

run_and_print_output(["docker", "push", f"{image_name}:{image_tag}"])

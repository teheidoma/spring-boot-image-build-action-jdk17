import json
import re
import subprocess
import os
import tabulate


def run_and_print_output(arg):
    if type(arg) == type([]):
        print(' '.join(arg))

    p = subprocess.run(arg, stdout=subprocess.PIPE, text=True)
    print(p.stdout)
    if p.returncode != 0:
        exit(p.returncode)


def push_image(image, tag):
    if include_commit_sha.lower() == 'true':
        original_image = f'{image}:{tag}'
        modified_image = f'{image}:{tag}-{github_sha}'
        tag = f'{tag}-{github_sha}'
        run_and_print_output(['docker', 'tag', original_image, modified_image])
    run_and_print_output(["docker", "push", f"{image}:{tag}"])


sdkman_dir = "/root/.sdkman"
sdkman_init_script = "/root/.sdkman/bin/sdkman-init.sh"

github_output_file = os.environ.get("GITHUB_OUTPUT")
github_step_summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
registry_username = os.environ.get("INPUT_REGISTRY_USERNAME")
registry_password = os.environ.get("INPUT_REGISTRY_PASSWORD")
registry_hostname = os.environ.get("INPUT_REGISTRY_HOSTNAME")
include_commit_sha = os.environ.get("INPUT_INCLUDE_COMMIT_SHA")
github_sha = os.environ.get("GITHUB_SHA")[:10]

if registry_username and registry_password:
    run_and_print_output(["docker", "login", "-u", registry_username, "-p", registry_password, registry_hostname])

subprocess.run(["chmod", "+x", "./gradlew"])
process = subprocess.run(["./gradlew", "bootBuildImage"],
                         env=dict(os.environ) | {"JAVA_HOME": "/root/.sdkman/candidates/java/current"},
                         stdout=subprocess.PIPE, text=True)

output = process.stdout
print(output)

reg = re.compile(r"^Successfully built image \'(.+):(.+)\'$", re.MULTILINE)
matches = [m.groups() for m in reg.finditer(output)]
if len(matches) < 1:
    exit(1)

for match in matches:
    push_image(match[0], match[1])

with open(github_output_file, "a") as output_file:
    output_file.write(f"IMAGE_NAME={json.dumps(list(map(lambda x: x[0], matches)))}\n")
    if include_commit_sha:
        output_file.write(f"IMAGE_TAG={matches[0][1]}-{github_sha}\n")
    else:
        output_file.write(f"IMAGE_TAG={matches[0][1]}\n")

with open(github_step_summary_file, "a") as output_file:
    if include_commit_sha:
        matches = list(map(lambda x: (x[0], x[1] + '-' + github_sha), matches))
    markdown = tabulate.tabulate(matches, tablefmt='pipe', numalign='left', headers=['image name', 'image tag'])
    output_file.write(markdown)

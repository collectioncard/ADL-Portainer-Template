# Instructor / lab administrator: set up the demo once

This sample is intentionally simple and has **no public web ports**. It teaches Portainer stacks, GitHub image publishing, interactive CLI, batch jobs and named volumes.

## 1. Put the files on GitHub

Create a new repository in the ADL GitHub organization (or a personal account), e.g. `adl-portainer-python-demo`. Choose **Private** if appropriate. Push this complete folder to the repository's `main` branch.

If you have `gh` installed and have permission to create repositories:

```sh
git init
git add .
git commit -m "Add Portainer Python demonstration"
git branch -M main
gh repo create YOUR_ORG/adl-portainer-python-demo --private --source=. --remote=origin --push
```

If `git commit` complains, configure your Git user name and email. If the repo already exists, connect `origin` and push normally instead of using `gh repo create`.

## 2. Make sure GitHub Actions publishes the image

The workflow `.github/workflows/publish.yml` runs on pushes to `main` and:

1. Runs `unittest` tests.
2. Logs into GHCR using its GitHub Actions `GITHUB_TOKEN`.
3. Builds the Docker image.
4. Publishes two tags: `latest` and `sha-COMMIT_SHA`.

The full image name is generated automatically from the lowercased `OWNER/REPO`. No personal PAT is required by the GitHub Actions workflow itself.

Check your organization's Actions and GitHub Packages policies if publishing is blocked. Check the GitHub package's visibility after first publish. Do **not** make a package public simply to avoid configuring access.

## 3. Give Portainer access to the image

The repository's private source visibility and the GHCR package's private visibility are **separate concerns**:

- To read a **private GitHub repository**, Portainer's Git stack setup needs suitable repository read credentials.
- To pull a **private GHCR image**, Portainer's Docker environment needs GHCR credentials with `read:packages` and access to the package. A classic PAT is commonly used for GHCR CLI/registry authentication; authorize organizational SSO if required.

As an administrator, configure GHCR under Portainer **Registries**, using an appropriately scoped read-only token. Ensure the researchers' deployment path can use that registry configuration without sharing a token in source code or chat.

Avoid setting the GitHub package visibility to public unless that is intentional.

## 4. Check Portainer ownership and security settings

- Researchers should have access to `adl-primary` but not unrestricted host administrator permissions.
- Keep privileged containers, host bind mounts and Docker socket access restricted for non-administrators.
- Use per-researcher stack names and appropriate stack ownership.
- The example uses named volumes and no host bind mounts.
- Set reasonable disk quotas/usage expectations: Docker volumes can fill the host SSD.
- A named Docker volume is **not** automatically backed up.

**Volume lifecycle:** Compose normally prefixes a named volume with the stack name (e.g. `alex-calculator-demo_results`). Keep these volumes when removing stacks until their results have been exported.

## 5. Test the lesson yourself

Deploy from the Git repository using `compose.yaml`, adding `CALCULATOR_IMAGE=ghcr.io/YOUR_ORG/adl-portainer-python-demo:latest` in the stack environment.

Open the running calculator container's Console (`/bin/sh`):

```sh
python /app/calculator.py multiply 12 8 --output /results/run-001.json
cat /results/run-001.json
```

Restart and confirm the file remains.

Next create a separate stack from `compose.batch.yaml`, using the same image variable and optionally `RUN_ID=class-demo-001`. After successful completion, check for **Exited (0)** and inspect **Logs**.

## 6. Retrieving results

The existing ADL Portainer setup connects to a local Docker daemon and may not offer a volume file browser. Don't promise students that they'll have a Download button for named-volume files. For class demos use `cat` for small JSON files. For substantial files, arrange an approved transfer mechanism or a helper process with controlled access to the specific volume.

## 7. Limits and next improvements

This is a teaching demo, not a production research scheduler. For actual research jobs, prefer one-shot execution, immutable image tags, separate output volumes, resource limits, checkpoints and backup/retention policies.

No GitHub credentials, GHCR tokens or LiteLLM keys are included in these files.

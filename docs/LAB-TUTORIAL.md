# Lab walkthrough: run a Python experiment on Portainer

**Goal:** Deploy this demo from GitHub, run commands inside a container, save a result that survives a restart and try an unattended batch run.

**You need:** Access to the ADL Portainer environment and a GitHub repository containing this demo. The instructor should have configured Portainer access to the repository and (if private) to its GHCR image.

## Part A — Use the shared demonstration repository

### 1. Find the image

Open the demo repository on GitHub. Under its **Actions** tab, find a successful **Test and publish Docker image** workflow. The Docker image name follows this pattern:

`ghcr.io/OWNER/REPO:latest`

Use the actual lowercase GitHub owner and repository name. The image is not the same thing as the repository itself.

### 2. Deploy from Git in Portainer

1. Go to <https://labinfra.wessel.xyz> and sign in with your authorized UCSC account.
2. Select the `adl-primary` Docker environment.
3. Choose **Stacks → Add stack → Repository** (the label may read **Git Repository**).
4. Name the stack something unique, e.g. `alex-calculator-demo`.
5. Enter the demo's GitHub repository URL; choose branch `main` (`refs/heads/main` if requested).
6. Set the Compose file path to `compose.yaml`.
7. In **Environment variables**, add `CALCULATOR_IMAGE` with value `ghcr.io/OWNER/REPO:latest` (replace OWNER and REPO).
8. Deploy the stack.

**For private repositories:** Portainer needs Git credentials to fetch the Compose file. **For private images:** Portainer also needs separate GHCR registry authentication. Ask the instructor if image pulls fail with `denied` or `unauthorized`.

### 3. Open the container console

1. Choose **Containers** in Portainer.
2. Open the `calculator` container belonging to your stack. Its actual name may include your stack name.
3. Choose **Console**, select `/bin/sh` and click **Connect**.
4. Run:

```sh
python /app/calculator.py add 10 25
python /app/calculator.py multiply 12 8
python /app/calculator.py divide 100 4
```

The container is intentionally kept alive with `sleep infinity` for the lesson. It's **not** running a calculation until you enter one.

### 4. Save and inspect a result

In the same Console:

```sh
python /app/calculator.py multiply 12 8 --output /results/run-001.json
ls -lh /results
cat /results/run-001.json
```

The JSON result is saved to a **named Docker volume** mounted at `/results`.

### 5. Check persistence

Return to the container page, **Restart** the container, reconnect to Console and run:

```sh
cat /results/run-001.json
```

The file should still be there. Named volumes survive normal container restarts and container recreation **as long as the volume itself is preserved**.

**Important:** The file is not saved to GitHub, and the server's volumes are not automatically backed up. Don't remove the stack's volume when deleting the demo.

## Part B — Run a real batch job

Long-running research experiments should normally start automatically and run in a **detached container**, not be launched from a Console session.

1. Create another stack with a unique name, e.g. `alex-calculator-batch`.
2. Use the **same GitHub repository**, but set Compose path to `compose.batch.yaml`.
3. Define `CALCULATOR_IMAGE` as before.
4. Optionally set these stack environment variables:

| Name | Example | Effect |
| --- | --- | --- |
| `CALC_OPERATION` | `multiply` | One of add, subtract, multiply or divide |
| `CALC_A` | `12` | First value |
| `CALC_B` | `8` | Second value |
| `RUN_ID` | `experiment-001` | Name of the JSON result file |

5. Deploy. Wait for the container to finish.
6. Open **Containers → [batch container] → Logs**. You should see the calculation and a message that the result was saved.
7. Successful completion appears as **Exited (0)**. This is expected for a one-off job.

The batch stack uses its **own** `results` volume, separate from Part A. Because its container exits, you cannot connect to its Console. To inspect the files, create a separate temporary helper container with the same volume or use an approved file export method. Ask an administrator if you need to download results. Don't delete the volume in the meantime.

## Part C — Make it your own

You can copy or fork this demo repository and modify `calculator.py`. Every push to `main` runs tests and publishes a new container image, if your repository's Actions and package permissions allow it.

To deploy your own fork:

1. Point Portainer's Git repository setting at **your** GitHub repository.
2. Set `CALCULATOR_IMAGE` to **your** GHCR package name.
3. Make sure the package is accessible to Portainer (private is fine).
4. Deploy or re-pull/redeploy after the new image is published.

Updating Python source on GitHub by itself does **not** update the Python code already inside a running container: the container image needs to be rebuilt and the new image pulled.

## What you learned

- **GitHub repository:** Where source and Compose instructions live
- **Docker image:** Packaged version of the Python program
- **Docker container:** Running or completed instance of that image
- **Portainer stack:** A group of services and volumes managed together
- **Console:** Interactive commands inside a running container
- **Logs:** Output from the container's main process
- **Named volume:** Files that persist independently of a particular container

## Common problems

| Symptom | What to do |
| --- | --- |
| Image pull is unauthorized | Have the instructor check Portainer's GHCR registry credentials and package access |
| Git repository won't clone | Check the branch, URL and Git authentication (separate from GHCR) |
| `CALCULATOR_IMAGE` not set | Add it in the Portainer stack's Environment variables |
| Cannot open Console | Console requires a **running** container; use the interactive stack |
| `Permission denied` in `/results` | Ask instructor to verify the image and Docker volume permissions |
| Container exited 0 | For the batch stack, this means the job finished successfully |
| Results disappeared | Check which stack owns the volume and whether that volume was deleted |
| Code changes didn't show up | Wait for Actions to publish, then re-pull the image and redeploy |

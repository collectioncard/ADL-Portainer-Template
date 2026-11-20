# ADL Portainer Python Demo

A tiny, **real** Python CLI experiment for teaching lab members how to run a GitHub project on the ADL Docker server using Portainer. The calculator supports command-line arguments, writes JSON results and demonstrates persistent Docker volumes.

**No Python packages are required.** The Docker image is built by GitHub Actions and stored in GitHub Container Registry (GHCR). **Your GitHub repository and GHCR image can both stay private.**

## Start here

- **Lab members:** Read [the guided tutorial](docs/LAB-TUTORIAL.md).
- **Lab administrator / repository owner:** Read [the instructor setup notes](docs/INSTRUCTOR-NOTES.md) first.
- **Building a different Python project:** Follow [the from-scratch checklist](docs/START-YOUR-OWN-PYTHON-REPO.md).

## Files

| File | Purpose |
| --- | --- |
| `calculator.py` | CLI calculation program |
| `Dockerfile` | Creates a Python 3.12 image, running as a non-root user |
| `compose.yaml` | Interactive tutorial container with a persistent named volume |
| `compose.batch.yaml` | One-shot job that writes a result and exits |
| `.github/workflows/publish.yml` | Tests and publishes a GHCR image on each push to `main` |
| `tests/test_calculator.py` | Simple automated tests |
| `docs/LAB-TUTORIAL.md` | Step-by-step student walkthrough |
| `docs/INSTRUCTOR-NOTES.md` | One-time private registry setup |
| `docs/START-YOUR-OWN-PYTHON-REPO.md` | Adapt this example to a research script |

## Run without Docker

```bash
python3 calculator.py add 10 25
python3 calculator.py multiply 12 8 --output results/run-001.json
python3 -m unittest discover -s tests -v
```

## Run with Docker locally (optional)

```bash
docker build -t adl-calculator-demo:local .
docker run --rm adl-calculator-demo:local python /app/calculator.py add 10 25
```

## Deploy through Portainer

1. Publish this repository to GitHub (or fork it), using **private** visibility if desired.
2. Wait for its **Test and publish Docker image** action to succeed.
3. Make sure Portainer has access to the GHCR package if it is private.
4. In Portainer, choose **Stacks → Add stack → Repository**.
5. Supply the GitHub repository URL, branch `main` and Compose path `compose.yaml`.
6. Set this stack environment variable:

   `CALCULATOR_IMAGE=ghcr.io/OWNER/REPO:latest`

   Replace `OWNER/REPO` with the lowercase GitHub owner and repository name. For reproducible runs, use a `sha-...` image tag instead of `latest`.
7. Deploy, open **Containers → calculator → Console**, choose `/bin/sh` and run:

   ```bash
   python /app/calculator.py multiply 12 8 --output /results/run-001.json
   cat /results/run-001.json
   ```

**`/results` is a persistent Docker named volume**, not a directory on the GitHub repository. It survives normal container recreation but **is not automatically backed up**.

### One-shot experiment

Create a *second* Portainer stack pointing to `compose.batch.yaml` and set `CALCULATOR_IMAGE` again. Optionally set `CALC_OPERATION`, `CALC_A`, `CALC_B` and `RUN_ID`. The container runs once and shows **Exited (0)** when successful. Inspect its **Logs** for the result. The batch stack has **its own separate named volume**.

## Privacy

- GitHub repositories can be private.
- GHCR images can be private. Check package visibility after publishing.
- Private GHCR images require registry authentication in Portainer, independently of Git repository authentication.
- Never commit `.env` files, API keys or research data to your code repository.
- Docker volumes persist on the lab server but are **not** backups.

# Fix setup problems

Companion to [the setup guide](setup.md). Checked 23 September 2026. Tell the facilitator which step failed and copy the error text, with passwords, tokens and private file contents removed.

## Start here

1. Confirm you are inside the extracted `agentic-ai-masterclass` project folder.
2. Run `node scripts/check-setup.mjs` in Codex's integrated terminal, then `poetry run python scripts/check-python.py` from the project folder.
3. If it fails before producing a report, check Node with `node --version` and use the relevant row below.
4. After a tool or PATH change, close terminal windows, fully quit ChatGPT, reopen it and start a new task. An already-running app can retain its old environment.

| Symptom | What to do |
| --- | --- |
| ChatGPT asks for an administrator password, Store is blocked, or installation is prohibited | Stop that installation. Use the organization's approved software channel, ChatGPT Work in a browser or a teammate's approved environment. A user-local folder does not override company policy. |
| App has Chat but no Codex or Work | Update the official app; verify the signed-in account and active workspace. Availability can depend on plan, rollout and workspace controls. Use the facilitator's available route rather than installing a similarly named third-party app. |
| Paid subscription appears missing | Check the account email and selected workspace. Use the same account that owns the subscription. Do not purchase twice or share another participant's login. |
| Usage limit during the workshop | Save the project and notes; use a smaller available model for focused tasks, review existing work or share one approved working environment with your group. Work and Codex share limits. Additional credits require the payer's agreement. |
| Windows requests elevated sandbox setup | Use the documented `unelevated` mode only if your organization permits it. Preserve existing config settings. If policy requires elevated mode, arrange IT setup or use the browser/team route; do not switch to unrestricted access. |
| `node` or `uv` is not recognized | The installation folder is missing from PATH, nested incorrectly or invisible to the running app. Check the executable exists, add the actual folder to your user PATH, then restart the app. |
| `npm.ps1 cannot be loaded` | Run `npm.cmd` and `npx.cmd` in Windows PowerShell. Do not change execution policy. |
| Python opens the Microsoft Store or reports the wrong version | Use `poetry run python` from the project folder after Poetry setup. Check `poetry env info --path` points to this project's `.venv`. The workshop does not depend on a global `python` alias. |
| Readiness reports an older runtime or uv cannot find Python 3.14.7 | Update user-owned uv from its official release if needed. Install Node 26.10.0+ and Python 3.14.7+ using the manual guide. Preserve an old `.venv` by setting up a fresh extracted kit beside it and migrating dependencies; do not delete it. |
| `Activate.ps1` is blocked | No activation is required. Use `poetry run python`; do not change execution policy. |
| `poetry` is not recognized | Run `uv tool dir --bin` (or invoke your portable `uv.exe` by its full path) and add that actual folder to your user PATH. It may differ from the uv executable folder. If Poetry was installed another way, locate that installation instead. Restart the terminal and ChatGPT. |
| Poetry is older than 2.5.1 or rejects the project's required Poetry version | Follow [Poetry setup](setup-technical.md#poetry-and-env). Reuse stable Poetry 2.x at least 2.5.1, or install 2.5.1 in uv's isolated user tool environment. Do not install Poetry into the project's `.venv` or force-overwrite another installer's executable. |
| Poetry selects another environment or says virtualenv creation is disabled | Stop before installing packages. Open a fresh terminal without an activated virtualenv/Conda environment, check `poetry.toml` and relevant Poetry environment-variable overrides, and confirm `poetry env info --path` points to this project's `.venv`. Preserve existing environments; ask the facilitator to reconcile cached environments. |
| An existing `.venv` is incomplete, linked elsewhere or has an old Python | Do not delete or recreate it. Keep the old project and make a fresh clone beside it; migrate source and dependency declarations deliberately. The setup blocks stop before replacing an incompatible environment. |
| `pyproject.toml` changed significantly since the lockfile was generated | Pull the matching declaration and lockfile from the group branch, or have the person changing dependencies reconcile them with Poetry. Review and commit both files. Do not discard `poetry.lock` or run a broad update to make the message disappear. |
| A package imported before setup is missing after `poetry sync` | Sync removes packages absent from the lockfile. Reconcile needed dependencies using the group's inventory and `poetry add`, review both dependency files, then install. Use `poetry install` for initial migration; do not run sync on an unreconciled existing environment. |
| Poetry cannot find an installation candidate or a wheel | Check Python 3.14.7+, CPU architecture, package version and the group's lockfile. Keep the starter's prebuilt-wheel policy; choose a compatible package or fixture fallback rather than installing a compiler or disabling the policy. |
| Python cannot import `dotenv` | Run `poetry install` from the project folder using the supplied lockfile, then `poetry run python scripts/check-python.py`. Do not repair this with an untracked pip install. |
| `.env` is missing | Run `node scripts/init-env.mjs` in the starter; it creates a file from `.env.example` only if absent. Edit your local values with a plain-text editor. Keep `.env` out of Git and prompts. |
| A `.env` change has no effect | Restart the affected process. Confirm the entry point explicitly loads the project `.env`; `poetry run` alone does not load it. Existing process environment variables take precedence in the starter, so inspect only the relevant variable's presence without dumping its value. Never turn on secret-value logging. |
| `bad CPU type`, invalid application or wrong architecture | Re-download the archive matching your CPU: Apple M-series = darwin-arm64; Intel Mac = darwin-x64; Windows = the x64/ARM64 value in Settings. Check the current app/Node OS requirements. |
| Package tries to compile or asks for Visual Studio/Xcode | Stop and ask Codex for a supported prebuilt wheel or simpler package. Re-check Python 3.14.7, Node 26 and CPU architecture. Compilers are not a baseline dependency. |
| Browser shows a blank page or cannot connect | Keep the preview command running, open exactly the printed localhost URL, and use a normal browser if the app browser is unavailable. Do not open HTML as `file://` when it needs a server. |
| Port is in use | Stop your own earlier preview with `Ctrl+C`, or use an available port as supported by the project. Do not terminate an unfamiliar process. |
| Download hash does not match | Do not extract or run that archive. Download it again from the official release directory and compare with its matching checksum file. Avoid mixing versions. |
| Permission denied when installing packages | Confirm the project is in your own home directory and Poetry selects its `.venv`; use `poetry add`/`poetry install` or local npm packages. Never repair this with `sudo pip`, `sudo npm` or a machine-wide ownership change. |
| Antivirus/AppLocker/SmartScreen blocks a downloaded executable | Use the approved IT route or the browser/team fallback. Do not disable security software, remove security marks or sideload around a policy. |
| Certificates, proxy, TLS or firewall errors | Ask IT for the approved network/certificate configuration. Do not turn off TLS verification. Try an approved network if available. |
| A skill is not listed | Confirm the ZIP was fully extracted, including hidden `.agents` folders, and that Codex opened the extracted project root. Start a new task. You can ask it to read the relevant `SKILL.md` directly while resolving discovery. |
| Git is missing or too old | Ask Codex to follow [Install Git](setup-technical.md#install-git): portable Git on Windows, user-folder Git on Mac. Restart ChatGPT after updating your user PATH. If company policy blocks installation, tell the facilitator and use folder copies temporarily; the full setup remains incomplete. |
| Mac asks to install Apple developer tools when running Git | Cancel that prompt for this user-only route. Follow [Install Git](setup-technical.md#install-git), put the user Git folder first on PATH, and restart ChatGPT. |
| Git asks “Please tell me who you are” when saving a commit | Ask Codex to set your chosen name and email for this project only (`git config --local`). GitHub registration and machine-wide settings are unnecessary. |
| Git remote access is denied | Confirm the chosen Git host, your account's repository access and the agreed remote with the group. Use the host's approved sign-in flow; never paste access tokens into prompts or share a teammate's credentials. Follow [Teamwork](teamwork.md). |
| Git will not pull or switch branches because of local changes | Save a local commit or coordinate with your group before changing branches. Do not discard another person's work, run a destructive reset, or force-push to make the error disappear. |
| `poetry.lock` conflicts after two people add packages | Follow [Teamwork](teamwork.md): agree the combined declarations, have one person reconcile the lockfile with Poetry, then review and test. Do not choose an entire side blindly or manually combine dependency hashes. |
| Cloudflare permission denied or wrong account | Stop deployment. Ask the facilitator to verify the assigned workshop account/project and access method. A broader token is not the fix. |

## Check exact executable paths

On a Mac:

```sh
command -v node
command -v npm
command -v uv
command -v poetry
node --version
poetry --version
poetry env info --path
poetry run python -c "import sys; print(sys.executable); print(sys.version)"
```

If PATH is the only problem, temporarily add the actual user tool directories in that terminal. For example, with the Apple Silicon archive from the guide:

```sh
export PATH="$HOME/.local/share/node-v26.10.0-darwin-arm64/bin:$HOME/.local/bin:$PATH"
```

Use `darwin-x64` for Intel. Persist the matching line in your own shell profiles only after confirming it works; preserve their existing contents.

In Windows PowerShell:

```powershell
Get-Command node,npm.cmd,poetry -ErrorAction SilentlyContinue
Test-Path "$env:LOCALAPPDATA\Programs\ai-masterclass\uv\uv.exe"
poetry --version
poetry env info --path
poetry run python -c "import sys; print(sys.executable); print(sys.version)"
```

For the x64 Node archive from the guide, a temporary session repair is:

```powershell
$WorkshopNode = Join-Path $env:LOCALAPPDATA 'Programs\ai-masterclass\node-v26.10.0-win-x64'
$env:Path = "$WorkshopNode;$env:LOCALAPPDATA\Programs\ai-masterclass\uv;$env:Path"
node --version
npm.cmd --version
```

Adjust the version and architecture to match the folder you actually extracted. Add these folders using **Edit environment variables for your account → User variables → Path** to persist them. Do not replace the full Path or modify System variables.

For Poetry installed through uv, find its actual executable folder:

```sh
# Mac: read-only path query.
uv tool dir --bin
```

```powershell
# Windows: read-only path query, independent of the current PATH.
$WorkshopUv = Join-Path $env:LOCALAPPDATA 'Programs\ai-masterclass\uv\uv.exe'
& $WorkshopUv tool dir --bin
```

Add the returned folder to your user PATH, preserving existing entries. A folder listing or executable path is enough to diagnose this problem; do not paste an environment dump or `.env` contents. Review [Agent practices](agent-practices.md) when asking Codex for a focused fix.

## Browser-only participation

If installation cannot be approved in time, open [ChatGPT](https://chatgpt.com), select Work if available, and use synthetic sample files to research, design and create outputs. Save downloadable artifacts as you go. A teammate or the facilitator can run the local prototype and deployment. Local filesystem access, installed workshop skills and terminal tools do not automatically transfer to a cloud task. This is a reduced route, so agree the adjusted challenge before the event.

## Useful official references

- [ChatGPT desktop and web quickstart](https://learn.chatgpt.com/docs/quickstart)
- [Windows app](https://learn.chatgpt.com/docs/windows/windows-app) and [sandbox modes](https://learn.chatgpt.com/docs/windows/windows-sandbox)
- [Plans and shared Work/Codex usage](https://learn.chatgpt.com/docs/pricing)
- [uv installation](https://docs.astral.sh/uv/getting-started/installation/), [Python management](https://docs.astral.sh/uv/guides/install-python/)
- [Poetry installation and project setup](https://python-poetry.org/docs/basic-usage/), [install and sync](https://python-poetry.org/docs/cli/#install), [uv tool executable locations](https://docs.astral.sh/uv/guides/tools/)
- [python-dotenv loading behavior](https://saurabh-kumar.com/python-dotenv/)
- [Node 26 supported platforms](https://github.com/nodejs/node/blob/v26.x/BUILDING.md#platform-list)

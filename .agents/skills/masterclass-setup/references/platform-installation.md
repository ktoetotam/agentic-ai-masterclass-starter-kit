# Platform installation reference for the setup skill

Read only the sections relevant to the participant’s operating system and failed readiness checks. Follow [the four-step setup guide](../../../../guides/setup.md) for the participant-facing flow. Search and open current official documentation before changing configuration or installer commands. Commands checked on **23 September 2026**.

**Versions checked 23 September 2026:** [Python 3.14.7](https://www.python.org/downloads/release/python-3147/) is the latest stable Python; [Node.js 26.10.0](https://nodejs.org/en/blog/release/v26.10.0) is the latest Current release. Node 24.21.0 remains the latest LTS, but this workshop uses Node 26. Python 3.15 is still a prerelease. Use stable releases only. [Python releases](https://www.python.org/downloads/), [Node release status](https://nodejs.org/en/about/previous-releases).

You need a laptop, charger, reliable internet, your own ChatGPT login and a **ChatGPT Plus subscription**. Plus is the workshop's entry subscription; an existing Pro or employer-provided plan with the required features can also work. Check managed workspace access before buying a second subscription. Free and Go are not our workshop baseline. OpenAI currently lists Plus at US$20/month; check the price and taxes shown at checkout. Work and Codex share usage, and an intensive day can reach limits. [Plans and usage](https://learn.chatgpt.com/docs/pricing).

**AI Realist can reimburse one month of ChatGPT Plus.** Email your receipt and bank transfer details (account holder, IBAN, and BIC/SWIFT if needed) to [hello@airealist.org](mailto:hello@airealist.org). Do not buy Pro, API credits or media subscriptions as part of the basic setup.

## 1. Install ChatGPT and open Codex

Current ChatGPT desktop releases include **Codex**. You do not need two separate desktop apps. In the app, select **Codex** for building your project; select **ChatGPT → Work** for research and producing files. Work can also use local tools on desktop. Existing Codex app users can update their existing app. [Desktop app](https://learn.chatgpt.com/docs/app), [Work guide](https://learn.chatgpt.com/docs/get-started-with-work), [July 2026 app change](https://learn.chatgpt.com/docs/changelog).

### On a Mac

1. Open Apple menu → **About This Mac**. Note your macOS version and whether the chip says Apple M-series or Intel.
2. Open the [official ChatGPT desktop download page](https://learn.chatgpt.com/docs/app). Select the download matching your Mac. Current releases support Apple Silicon and Intel; older installation advice may say otherwise.
3. Open the downloaded disk image. For a user-only installation, create an **Applications** folder inside your home folder in Finder and copy the app there. This is `~/Applications`, separate from the shared `/Applications` folder. Open the copied app. If your organization's policy blocks it or the installer requires administrator approval, stop and use the fallback below.
4. Sign in with the ChatGPT account that has your subscription. Select **Codex**.

The workshop's Node 26 tools need **macOS 13.5 or newer** on Apple Silicon or Intel. Use a current, supported macOS release where possible. The exact ChatGPT app compatibility is determined by its current download; the public app guide does not publish a complete fixed hardware/OS minimum. Check its current requirements if the download refuses to open. [Node 26 supported platforms](https://github.com/nodejs/node/blob/v26.x/BUILDING.md#platform-list).

### On Windows

1. Open **Settings → System → About**. Note the Windows version and **System type**: x64 or ARM64.
2. Open the [official Windows app guide](https://learn.chatgpt.com/docs/windows/windows-app) and follow its Microsoft Store download link. Confirm the publisher is OpenAI. Select **Get/Install** for your signed-in user.
3. Open ChatGPT, sign in with your subscribed account, and select **Codex**. A missing Store or blocked installation needs your organization's approved software channel or the browser fallback.
4. Use native Windows/PowerShell. You do not need WSL, Docker, Chocolatey or Homebrew. **Homebrew is not a Windows prerequisite.**

Use Windows 11 with a 64-bit x64 or ARM64 processor for the workshop where possible. Node 26 also lists Windows 10, but that does not establish compatibility or support for every ChatGPT app release. Check the Store's current system requirements on your machine. We suggest at least 8 GB RAM and 5 GB free disk space for the workshop tools; these are planning estimates, not vendor minimums. Media tasks can need considerably more space.

### If installation is blocked

Sign in at [ChatGPT on the web](https://chatgpt.com), choose **Work** if available, and upload only the workshop samples you need. This supports a reduced browser workflow; it does not install Python on your laptop or automatically grant access to your local project. Build and preview locally with a teammate's approved computer, or use a facilitator-provided environment. Tell the facilitator before the workshop so your challenge can be adapted. [Web and desktop quickstart](https://learn.chatgpt.com/docs/quickstart).

## 2. Download and open your own project folder

1. Download the masterclass starter folder supplied with this reference.
2. Extract it into a folder you own for the setup check. When your group starts, use its shared repository as described in [Teamwork](../../../../guides/teamwork.md), rather than starting separate competing repositories. Recommended: `~/ai-masterclass/agentic-ai-masterclass` on Mac, or `%USERPROFILE%\ai-masterclass\agentic-ai-masterclass` on Windows. Avoid a shared drive or a folder controlled by OneDrive while running development tools.
3. In Codex, add/open this folder as a **local project**. Do not open your entire home folder or a company production repository.
4. Start a new task. Use the default permissions with sandboxing and approval prompts. When an installation requires network access or writing to your user tools folder, approve only the requested installation if your device policy permits it.
5. On Windows, sandbox setup can ask for administrator approval. If that is unavailable, the documented user-level fallback is `[windows] sandbox = "unelevated"` in your own Codex configuration, provided your organization's policy permits it. This offers weaker isolation than the preferred elevated sandbox. Ask the facilitator to merge that setting into an existing config instead of replacing it. If policy requires the elevated mode, use the browser/team fallback. [Windows sandbox options](https://learn.chatgpt.com/docs/windows/windows-sandbox).

You can now ask Codex to guide the remaining setup:

> Read AGENTS.md and guides/setup.md. Use the masterclass installation skill. Inspect my operating system, architecture and installed tools first. Help me install or update the workshop requirements into my own user folders. Do not use administrator rights, change machine-wide settings or bypass company policies. Then run the readiness check and show what works and what is missing.

The manual instructions below work without a package manager. Run each block in order and stop if it reports an error. Do not paste Mac commands into PowerShell or Windows commands into Terminal.

## 3A. Mac: install Python and Node as your user

Open **Terminal** using Spotlight. Python handles documents and data; Node runs browser applications, tests and deployment tools. We use Python **3.14.7** and Node **26.10.0 (Current)** with its bundled npm. You do not need Homebrew, Xcode or a compiler for this baseline. Reuse an existing stable Python 3.14.7+ in the 3.14 series or Node 26.10.0+ in the 26 series. Keep other projects’ runtimes intact.

### Python through uv

`uv` bootstraps Python and installs the Poetry command in its own tool environment. **Poetry manages this project's `.venv` and Python packages.** Do not create the project environment with uv or install project packages with pip.

Download the official uv installer, then open it for inspection:

```sh
curl -LsSf https://astral.sh/uv/install.sh -o "$HOME/Downloads/uv-install.sh"
less "$HOME/Downloads/uv-install.sh"
```

Press `q` to leave the viewer. Paste this complete block. It uses your own tools folder and does not change an existing project environment:

```sh
(
  set -eu
  export PATH="$HOME/.local/bin:$PATH"
  if ! command -v uv >/dev/null 2>&1; then
    env UV_INSTALL_DIR="$HOME/.local/bin" UV_NO_MODIFY_PATH=1 sh "$HOME/Downloads/uv-install.sh"
  fi
  uv --version
  uv python install 3.14.7
  workshop_bootstrap_python=$(uv python find --system --no-python-downloads 3.14.7)
  "$workshop_bootstrap_python" --version
)
```

Expect `Python 3.14.7`. This installs a user-owned interpreter; it leaves other projects' runtimes intact. A compatible existing project `.venv` will be checked and reused in [step 3D](#poetry-and-env). uv uses Astral's Python distributions and requires no preinstalled Python. If an older uv cannot find 3.14.7, update your user-owned uv from the official installer; do not silently substitute an older Python. The latest uv checked here is [0.12.18](https://github.com/astral-sh/uv/releases/tag/0.12.18). [uv installation](https://docs.astral.sh/uv/getting-started/installation/), [installer options](https://docs.astral.sh/uv/configuration/installer/), [Python installation](https://docs.astral.sh/uv/guides/install-python/).

### Portable Node 26

1. Open [official Node 26 downloads](https://nodejs.org/dist/v26.10.0/).
2. Download the `.tar.gz` archive ending in **darwin-arm64** for an Apple M-series Mac or **darwin-x64** for an Intel Mac, plus `SHASUMS256.txt` from the same release directory. Do not choose the `.pkg` installer for this user-only route.
3. These commands use **v26.10.0**, the latest release on 23 September 2026. For a newer stable 26.x release, use its own directory, filenames and checksums consistently. Run `uname -m` first: `arm64` means Apple Silicon, `x86_64` means Intel.

```sh
uname -m
```

For Apple Silicon:

```sh
cd "$HOME/Downloads"
shasum -a 256 node-v26.10.0-darwin-arm64.tar.gz
```

For Intel:

```sh
cd "$HOME/Downloads"
shasum -a 256 node-v26.10.0-darwin-x64.tar.gz
```

Compare the output with the line for that exact filename in `SHASUMS256.txt`. Continue only if they match. Extract only your matching archive:

```sh
mkdir -p "$HOME/.local/share"
# Apple Silicon:
tar -xzf "$HOME/Downloads/node-v26.10.0-darwin-arm64.tar.gz" -C "$HOME/.local/share"
export PATH="$HOME/.local/share/node-v26.10.0-darwin-arm64/bin:$HOME/.local/bin:$PATH"
```

On Intel, use this block instead:

```sh
mkdir -p "$HOME/.local/share"
tar -xzf "$HOME/Downloads/node-v26.10.0-darwin-x64.tar.gz" -C "$HOME/.local/share"
export PATH="$HOME/.local/share/node-v26.10.0-darwin-x64/bin:$HOME/.local/bin:$PATH"
```

To keep the tools available after reopening Terminal, open your own shell profile files:

```sh
touch "$HOME/.zprofile" "$HOME/.zshrc"
open -e "$HOME/.zprofile" "$HOME/.zshrc"
```

In each file, add **the matching `export PATH=...` line above** once on a new line at the end, preserve existing contents, then save. Keep the files as plain text with their existing names. These names begin with a dot and may be hidden in Finder. This is for macOS's default zsh shell; for another shell, ask Codex to update its corresponding user profile. Fully quit and reopen ChatGPT after changing PATH.

```sh
node --version
npm --version
```

Expect Node `v26.10.0` (or a newer stable 26.x release) and its bundled npm version. npm is included in the archive. Install project packages locally, using the project's lockfile where supplied, rather than with administrator rights or global system installs. [Node releases](https://nodejs.org/en/about/previous-releases).

## 3B. Windows: install Python and Node as your user

Open **PowerShell** from the Start menu normally. Do not select “Run as administrator”. These instructions use downloads and your own user folders. They do not require winget or change PowerShell's execution policy.

### Python through the portable uv executable

1. Open [Astral's official uv releases](https://github.com/astral-sh/uv/releases/latest).
2. Under Assets, download `uv-x86_64-pc-windows-msvc.zip` for an x64 PC, or `uv-aarch64-pc-windows-msvc.zip` for an ARM64 PC. Choose the latest stable release (0.12.18 when checked). If a checksum file is provided, compare it using `Get-FileHash -Algorithm SHA256` before extraction.
3. Right-click the ZIP → **Extract All**. In File Explorer's address bar, enter `%LOCALAPPDATA%\Programs\ai-masterclass\uv` and create that folder if needed. Copy the extracted `uv.exe`, `uvx.exe` and, if present, `uvw.exe` into it. The final path must end in `\uv\uv.exe`, without an extra nested directory.
4. In PowerShell, paste the complete block below. It installs the user-owned interpreter, checks every command's result, and leaves project environments untouched. Poetry will manage the project in [step 3D](#poetry-and-env).

```powershell
$WorkshopUv = Join-Path $env:LOCALAPPDATA 'Programs\ai-masterclass\uv\uv.exe'
& {
    $ErrorActionPreference = 'Stop'
    & $WorkshopUv --version
    if ($LASTEXITCODE -ne 0) { throw 'uv could not run. Stop here.' }
    & $WorkshopUv python install 3.14.7
    if ($LASTEXITCODE -ne 0) { throw 'Python installation failed. Stop here.' }
    $WorkshopBootstrapPython = & $WorkshopUv python find --system --no-python-downloads 3.14.7
    if ($LASTEXITCODE -ne 0) { throw 'Python 3.14.7 was not found. Stop here.' }
    & $WorkshopBootstrapPython --version
    if ($LASTEXITCODE -ne 0) { throw 'Python could not run. Ask the facilitator.' }
}
```

Expect `Python 3.14.7`. No activation script or execution-policy exception is needed. Keep an existing `.venv` intact; the Poetry step will check it before doing anything to its packages. If uv cannot find 3.14.7, update your user-owned uv from the latest official portable release and retry. [uv installation methods](https://docs.astral.sh/uv/getting-started/installation/).

### Portable Node 26

1. Open [official Node 26 downloads](https://nodejs.org/dist/v26.10.0/).
2. Download the `.zip` ending in **win-x64** for an x64 PC or **win-arm64** for an ARM64 PC, plus `SHASUMS256.txt` from the same directory. Do not choose the `.msi` installer for this route.
3. In PowerShell, check your downloaded ZIP (change the filename to match your architecture and version):

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\node-v26.10.0-win-x64.zip" -Algorithm SHA256
```

Compare it with that exact filename's entry in `SHASUMS256.txt`. Continue only if it matches. If Downloads is redirected, use the real downloaded path.

4. Right-click the ZIP → **Extract All** into `%LOCALAPPDATA%\Programs\ai-masterclass`. The result should contain a folder such as `node-v26.10.0-win-x64` with `node.exe`, `npm.cmd` and `npx.cmd` inside it.
5. Run this block for x64, replacing `win-x64` with `win-arm64` on ARM64, and adjusting the version if needed:

```powershell
$WorkshopNode = Join-Path $env:LOCALAPPDATA 'Programs\ai-masterclass\node-v26.10.0-win-x64'
$env:Path = "$WorkshopNode;$env:LOCALAPPDATA\Programs\ai-masterclass\uv;$env:Path"
node --version
npm.cmd --version
```

6. Persist the two paths for **your user only**. Search Start for **Edit environment variables for your account**. In **User variables**, select **Path → Edit → New** and add the actual Node folder and uv folder from above, one per entry. Keep existing entries. Do not edit System variables. Close and reopen PowerShell, and fully quit and reopen ChatGPT.

Use **`npm.cmd` and `npx.cmd`** in PowerShell. If bare `npm` selects `npm.ps1` and reports a policy error, use the `.cmd` command; you do not need to relax execution policy. If an executable itself is blocked by organizational controls, stop and use an approved environment.

## 3C. Install Git {#install-git}

Git saves versions of your work. Codex checks and installs it as part of setup. No GitHub account is needed for local commits; shared repository access is covered in [the group workflow](../../../../guides/teamwork.md). The current upstream release checked on 23 September 2026 is **2.55.0**; Git for Windows is **2.55.0.windows.5**. Reuse a current working installation. [Git downloads](https://git-scm.com/install/), [Windows release](https://github.com/git-for-windows/git/releases/tag/v2.55.0.windows.5).

### Windows: portable download

1. Open [Git for Windows downloads](https://git-scm.com/install/windows). Under **Portable (“thumbdrive edition”)**, choose **x64 Portable** or **ARM64 Portable**, matching **Settings → System → About**.
2. Open the downloaded `PortableGit-…7z.exe`. This is a self-extracting archive; you do not need 7-Zip. Choose `%LOCALAPPDATA%\Programs\ai-masterclass\git` as the extraction folder. If Windows asks for administrator access, cancel and confirm that you selected **Portable**.
3. In PowerShell, run:

```powershell
$WorkshopGit = Join-Path $env:LOCALAPPDATA 'Programs\ai-masterclass\git\cmd'
if (!(Test-Path (Join-Path $WorkshopGit 'git.exe'))) { throw 'Git was not extracted into the expected folder.' }
$env:Path = "$WorkshopGit;$env:Path"
git --version
```

4. Search Start for **Edit environment variables for your account**. Under **User variables → Path → Edit → New**, add the actual `…\ai-masterclass\git\cmd` folder. Preserve other entries. Restart PowerShell and ChatGPT, then run `git --version` in Codex's terminal. Expect `git version 2.55.0.windows.5` or a newer stable release. If an older system Git still wins, ask Codex to inspect the effective PATH and select the user Git; do not change System variables.

### Mac: install into your home folder

Ask Codex to check existing Git first. It must check Apple developer tools before running `/usr/bin/git`, because that stub can open an installer on a fresh Mac. If a current Git already works, reuse it.

For a Mac without current Git, the following downloads **micromamba**, a standalone package tool, and uses the **conda-forge Git package**. Everything stays in your home folder; Homebrew, Xcode and a compiler are unnecessary. The package is maintained by conda-forge, not the Git project. [Micromamba manual download](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html#manual-installation), [conda-forge Git](https://anaconda.org/conda-forge/git).

Paste this complete block in **Terminal**:

```sh
(
  set -eu
  workshop_git_tools="$HOME/.local/share/ai-masterclass"
  case "$(uname -m)" in
    arm64) workshop_git_platform=osx-arm64 ;;
    x86_64) workshop_git_platform=osx-64 ;;
    *) printf '%s\n' 'Unsupported Mac architecture.' >&2; exit 1 ;;
  esac
  mkdir -p "$workshop_git_tools"
  if [ ! -x "$workshop_git_tools/bin/micromamba" ]; then
    workshop_git_download=$(mktemp -d)
    curl -fLsS "https://micro.mamba.pm/api/micromamba/$workshop_git_platform/latest" \
      -o "$workshop_git_download/micromamba.tar.bz2"
    tar -xjf "$workshop_git_download/micromamba.tar.bz2" \
      -C "$workshop_git_tools" bin/micromamba
  fi
  if [ -e "$workshop_git_tools/git" ] || [ -L "$workshop_git_tools/git" ]; then
    printf '%s\n' 'Git tool folder already exists. Ask Codex to check or update it without replacing it.' >&2
    exit 1
  fi
  "$workshop_git_tools/bin/micromamba" --no-rc create --yes \
    --root-prefix "$workshop_git_tools/mamba-root" \
    --prefix "$workshop_git_tools/git" \
    --override-channels --channel conda-forge 'git>=2.55.0'
  "$workshop_git_tools/git/bin/git" --version
)
```

Then make Git available in this terminal:

```sh
export PATH="$HOME/.local/share/ai-masterclass/git/bin:$PATH"
git --version
```

Add that same `export PATH=…` line once to your own `.zprofile` and `.zshrc`, preserving existing contents as in the Node instructions. Restart Terminal and ChatGPT. Expect `git version 2.55.0` or a newer stable release in Codex's terminal. Micromamba is used only for Git; Poetry manages the project's Python environment and Node stays in its portable folder.

If company policy blocks these downloads, tell the facilitator. The ZIP and preview still work with folder copies as temporary checkpoints, but Git setup is not complete. Do not bypass the restriction.

## 3D. Install Poetry and prepare the Python project {#poetry-and-env}

Poetry records Python dependencies in `pyproject.toml` and exact resolved versions in `poetry.lock`. The starter includes both files, plus `poetry.toml` to keep its environment in `.venv` and require prebuilt wheels. uv supplies Python and installs the Poetry tool in an isolated user environment; **Poetry owns project package operations**. [Poetry basic usage](https://python-poetry.org/docs/basic-usage/), [local environment configuration](https://python-poetry.org/docs/configuration/#virtualenvsin-project), [uv tool environments](https://docs.astral.sh/uv/guides/tools/).

Start in a fresh terminal without another virtualenv or Conda environment activated. Run `poetry --version` if Poetry is already installed. Reuse a stable **Poetry 2.x version at least 2.5.1**. If it is missing or older, use the relevant installation block below. These commands install **Poetry 2.5.1** in uv's user tool environment, outside the project's `.venv`. An existing uv-managed Poetry installation is updated; other tools and project environments are preserved. If uv reports that an executable belongs to another installation, stop and ask Codex to resolve the ownership; do not use `--force`.

### Install Poetry on Mac if needed

```sh
(
  set -eu
  export PATH="$HOME/.local/bin:$PATH"
  workshop_tool_dir=$(uv tool dir)
  workshop_tool_bin=$(uv tool dir --bin)
  case "$workshop_tool_dir" in "$HOME/"*) ;; *) printf '%s\n' 'uv tools are outside your home folder. Ask the facilitator.' >&2; exit 1 ;; esac
  case "$workshop_tool_bin" in "$HOME/"*) ;; *) printf '%s\n' 'uv tool executables are outside your home folder. Ask the facilitator.' >&2; exit 1 ;; esac
  uv tool install --python 3.14.7 --only-binary :all: poetry==2.5.1
  "$workshop_tool_bin/poetry" --version
  printf 'Poetry executable folder: %s\n' "$workshop_tool_bin"
)
```

Make the returned folder available in the current terminal:

```sh
export PATH="$HOME/.local/bin:$PATH"
export PATH="$(uv tool dir --bin):$PATH"
poetry --version
```

Add an `export PATH="the-printed-folder:$PATH"` line with the **actual printed path** once to your own `.zprofile` and `.zshrc`, preserving existing content. Do not type `the-printed-folder` literally. Restart Terminal and ChatGPT. If you reused an existing Poetry installation, keep its existing executable folder on PATH instead.

### Install Poetry on Windows if needed

```powershell
$WorkshopUv = Join-Path $env:LOCALAPPDATA 'Programs\ai-masterclass\uv\uv.exe'
& {
    $ErrorActionPreference = 'Stop'
    $WorkshopToolDir = & $WorkshopUv tool dir
    if ($LASTEXITCODE -ne 0) { throw 'Cannot locate the uv tool environment.' }
    $WorkshopToolBin = & $WorkshopUv tool dir --bin
    if ($LASTEXITCODE -ne 0) { throw 'Cannot locate the uv executable folder.' }
    $WorkshopUserPrefix = $env:USERPROFILE.TrimEnd('\') + '\'
    if (!$WorkshopToolDir.StartsWith($WorkshopUserPrefix, [StringComparison]::OrdinalIgnoreCase) -or
        !$WorkshopToolBin.StartsWith($WorkshopUserPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'uv tools are outside your user folder. Ask the facilitator.'
    }
    & $WorkshopUv tool install --python 3.14.7 --only-binary :all: poetry==2.5.1
    if ($LASTEXITCODE -ne 0) { throw 'Poetry installation failed. Do not force an overwrite.' }
    & (Join-Path $WorkshopToolBin 'poetry.exe') --version
    if ($LASTEXITCODE -ne 0) { throw 'Poetry could not run.' }
    Write-Output "Poetry executable folder: $WorkshopToolBin"
}
```

Add the **Poetry executable folder actually printed by this command** under **Edit environment variables for your account → User variables → Path → New**. It can differ from the folder containing `uv.exe`; do not assume they are together. Preserve existing entries. Restart PowerShell and ChatGPT, then run `poetry --version`. If you reused an existing compatible Poetry, keep its existing PATH entry.

### Create or reuse the project environment

Use the path to **your extracted starter or group clone** below. The blocks check starter markers, preserve an existing `.venv`, reject an incompatible interpreter and stop before installing packages if Poetry selects an environment outside the project. They do not remove another project's environment. If your old `.venv` uses an older Python, keep it and set up a fresh clone/extraction beside it; have Codex migrate working files and dependency declarations.

On Mac:

```sh
(
  set -eu
  workshop_project="$HOME/ai-masterclass/agentic-ai-masterclass"
  for workshop_file in AGENTS.md pyproject.toml poetry.lock poetry.toml scripts/check-setup.mjs; do
    if [ ! -f "$workshop_project/$workshop_file" ]; then
      printf '%s\n' 'Starter files missing. Correct workshop_project or obtain the complete group repository.' >&2
      exit 1
    fi
  done
  if [ -n "${VIRTUAL_ENV:-}" ] || [ -n "${CONDA_PREFIX:-}" ]; then
    printf '%s\n' 'Open a fresh terminal without an activated environment and retry.' >&2
    exit 1
  fi
  cd "$workshop_project"
  [ "$(poetry config virtualenvs.in-project)" = true ] || { printf '%s\n' 'Poetry must use the project .venv; check its local configuration.' >&2; exit 1; }
  [ "$(poetry config virtualenvs.create)" = true ] || { printf '%s\n' 'Poetry environment creation is disabled. Ask the facilitator.' >&2; exit 1; }
  if [ -e "$workshop_project/.venv" ] || [ -L "$workshop_project/.venv" ]; then
    [ ! -L "$workshop_project/.venv" ] || { printf '%s\n' '.venv is a link; ask the facilitator before changing another environment.' >&2; exit 1; }
    workshop_python="$workshop_project/.venv/bin/python"
    [ -x "$workshop_python" ] || { printf '%s\n' 'Existing .venv is incomplete; it has not been replaced.' >&2; exit 1; }
    "$workshop_python" -c 'import sys; sys.exit(0 if sys.version_info[:2] == (3, 14) and sys.version_info[:3] >= (3, 14, 7) and sys.version_info.releaselevel == "final" else 1)' || {
      printf '%s\n' 'Existing .venv needs a newer stable Python. Preserve it and use a fresh clone.' >&2
      exit 1
    }
  else
    workshop_python=$(uv python find --system --no-python-downloads 3.14.7)
    poetry env use "$workshop_python"
  fi
  workshop_poetry_env=$(poetry env info --path)
  "$workshop_python" -c 'import os,sys; sys.exit(0 if os.path.realpath(sys.argv[1]) == os.path.realpath(sys.argv[2]) else 1)' "$workshop_poetry_env" "$workshop_project/.venv" || {
    printf '%s\n' 'Poetry selected another environment. Stop and ask the facilitator; no packages were installed.' >&2
    exit 1
  }
  poetry check --lock
  poetry install --no-interaction
  poetry run python --version
)
```

In Windows PowerShell:

```powershell
$WorkshopUv = Join-Path $env:LOCALAPPDATA 'Programs\ai-masterclass\uv\uv.exe'
& {
    $ErrorActionPreference = 'Stop'
    $WorkshopProject = Join-Path $env:USERPROFILE 'ai-masterclass\agentic-ai-masterclass'
    foreach ($WorkshopFile in @('AGENTS.md', 'pyproject.toml', 'poetry.lock', 'poetry.toml', 'scripts\check-setup.mjs')) {
        if (!(Test-Path -LiteralPath (Join-Path $WorkshopProject $WorkshopFile) -PathType Leaf)) {
            throw 'Starter files missing. Correct WorkshopProject or obtain the complete group repository.'
        }
    }
    if ($env:VIRTUAL_ENV -or $env:CONDA_PREFIX) { throw 'Open a fresh terminal without an activated environment and retry.' }
    Push-Location -LiteralPath $WorkshopProject -ErrorAction Stop
    try {
        $WorkshopInProject = poetry config virtualenvs.in-project
        if ($LASTEXITCODE -ne 0 -or $WorkshopInProject -ne 'true') { throw 'Poetry must use the project .venv; check its local configuration.' }
        $WorkshopCreate = poetry config virtualenvs.create
        if ($LASTEXITCODE -ne 0 -or $WorkshopCreate -ne 'true') { throw 'Poetry environment creation is disabled. Ask the facilitator.' }
        $WorkshopVenv = Join-Path $WorkshopProject '.venv'
        $WorkshopPython = Join-Path $WorkshopVenv 'Scripts\python.exe'
        $WorkshopExisting = Get-Item -LiteralPath $WorkshopVenv -Force -ErrorAction SilentlyContinue
        if ($null -ne $WorkshopExisting) {
            if ($WorkshopExisting.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw '.venv is a link; ask the facilitator before changing another environment.' }
            if (!(Test-Path -LiteralPath $WorkshopPython -PathType Leaf)) { throw 'Existing .venv is incomplete; it has not been replaced.' }
            & $WorkshopPython -c 'import sys; sys.exit(0 if sys.version_info[:2] == (3, 14) and sys.version_info[:3] >= (3, 14, 7) and sys.version_info.releaselevel == "final" else 1)'
            if ($LASTEXITCODE -ne 0) { throw 'Existing .venv needs a newer stable Python. Preserve it and use a fresh clone.' }
        } else {
            $WorkshopPython = & $WorkshopUv python find --system --no-python-downloads 3.14.7
            if ($LASTEXITCODE -ne 0) { throw 'Python 3.14.7 was not found; complete its installation first.' }
            poetry env use $WorkshopPython
            if ($LASTEXITCODE -ne 0) { throw 'Poetry could not create the project environment.' }
        }
        $WorkshopPoetryEnv = poetry env info --path
        if ($LASTEXITCODE -ne 0) { throw 'Poetry environment could not be located.' }
        & $WorkshopPython -c 'import os,sys; sys.exit(0 if os.path.normcase(os.path.realpath(sys.argv[1])) == os.path.normcase(os.path.realpath(sys.argv[2])) else 1)' $WorkshopPoetryEnv $WorkshopVenv
        if ($LASTEXITCODE -ne 0) { throw 'Poetry selected another environment. Stop; no packages were installed.' }
        poetry check --lock
        if ($LASTEXITCODE -ne 0) { throw 'Dependency declarations and lockfile need reconciliation. Stop here.' }
        poetry install --no-interaction
        if ($LASTEXITCODE -ne 0) { throw 'Locked dependency installation failed. Ask the facilitator.' }
        poetry run python --version
        if ($LASTEXITCODE -ne 0) { throw 'Project Python could not run.' }
    } finally {
        Pop-Location
    }
}
```

`poetry install` uses the checked-in lockfile and leaves untracked extra packages in place. It may update a tracked dependency to its locked version. Review existing project dependencies before installation when migrating prior work. **Do not run `poetry sync` on an existing environment until its needed dependencies have been captured and reconciled into `pyproject.toml` and `poetry.lock`: sync removes packages absent from the lockfile.** A compatible old environment can be reused without recreating it. [Poetry install and sync](https://python-poetry.org/docs/cli/#install).

## 3E. Create your local .env and join the group workflow

In the extracted starter or group clone, run:

```sh
node scripts/init-env.mjs
```

This creates `.env` from `.env.example` only when `.env` is absent, and preserves an existing file. Open `.env` in a plain-text editor and set your public-safe `TEAM_NAME` and local preview `PORT`. Keep variable names unchanged. `.env` stays on your computer and is ignored by Git; commit only `.env.example` with placeholders when a new variable is needed. Do not paste `.env` contents into a prompt or a group chat. A variable is not secret merely because it is in `.env`; never copy secret values into browser assets or expose them through client-side build prefixes.

From the project folder, verify the Python setup:

```sh
poetry run python scripts/check-python.py
```

The check loads this project's explicit `.env` using `python-dotenv`; existing process environment values take precedence. `poetry run` alone does not automatically load `.env` for every arbitrary script: Python entry points must load the project's file, and other runtimes must use their supported loading mechanism. Follow the starter's entry points. [python-dotenv behavior](https://saurabh-kumar.com/python-dotenv/).

Use [Teamwork](../../../../guides/teamwork.md) to agree the group's shared Git repository, remotes, branch ownership and review process. Commit `pyproject.toml`, `poetry.lock`, `poetry.toml`, `.env.example` and source changes; keep `.venv`, `.env`, local credentials and generated private output out of Git. Each person clones the repository and creates their own environment. Use [Agent practices](../../../../guides/agent-practices.md) for working with Codex, checking results and handing off work.

## 4. Run the readiness check

In Codex's integrated terminal, open your extracted project folder. This proves that the app sees the same tools as your external terminal.

```sh
node scripts/check-setup.mjs
poetry run python scripts/check-python.py
node scripts/serve.mjs
```

Open the local URL printed by the preview server. The page should load. Stop the server with `Ctrl+C` when finished. The aliases are `npm run check` / `npm run preview` on Mac, and `npm.cmd run check` / `npm.cmd run preview` in Windows PowerShell.

Then ask Codex:

> Read AGENTS.md. Tell me which workshop skills are available. Create a small setup-check.txt file in this project saying “Ready for the masterclass”, open it for review, then report the Node and project Python versions. Do not deploy anything or connect external accounts.

You are ready when you can sign in, run a Codex task, read/write a file in this project, run Node 26.10.0+ and stable project Python 3.14.7+ within their selected release series, use Poetry 2.5.1+ within 2.x and Git 2.55.0 or newer, load the local `.env`, and open the preview. Before group work, also confirm access to the group's shared Git repository. Record optional tools separately. [Troubleshooting](../../../../guides/troubleshooting.md).

## 5. Add only what your challenge needs

The baseline is deliberately small. Check your challenge's guide before adding packages. Use Poetry for Python dependencies and keep its declaration and lockfile together in Git.

| Build direction | Bring | Possible additions when needed |
| --- | --- | --- |
| Company website | Brand notes, logo you may use, example text | Browser testing; Wrangler for approved Cloudflare deployment |
| Market & lead scout | Target market and public company examples | CSV tools, approved research access; use draft outreach during the exercise |
| Second brain | 5–10 non-sensitive notes or text PDFs | PDF/DOCX reader; SQLite is already in Python; OCR only for scanned pages |
| Beyond PowerPoint | One topic, 5–10 slides' worth of source material | Browser print-to-PDF; narration account only if chosen |
| Media studio | Assets you own, short script, headphones | Provider access and agreed budget; FFmpeg only for actual audio/video assembly |
| Accountant agent | Synthetic invoices and expected totals | PDF extraction and spreadsheet library; OCR for image invoices |
| News radar | Topic and a few credible feeds/sources | Feed parser; source timestamps; optional narration |
| Localisation agent | Source text, glossary, target locale | DOCX/PDF tools as needed; reference material for terminology checks |
| Spreadsheet killer | A small sample CSV or XLSX with known totals | `openpyxl` for XLSX, optional pandas; explicit rules for formulas and missing values |
| Your own problem | Example input, desired output, success criterion | Decide dependencies with the facilitator after the first small prototype |

For a challenge that needs XLSX and text-PDF support, run `poetry add openpyxl pypdf` from the project folder on either platform. This records the dependency declarations and updates `poetry.lock`; review and commit both files. Run Python with `poetry run python your_script.py`. Teammates pull those files and run `poetry install`, rather than adding the packages again. The starter requires prebuilt wheels; if a package has no compatible wheel for your Python/CPU, choose the challenge fallback. These packages are optional examples, not an instruction to install every tool. Do not use ad-hoc `uv pip install` or `pip install` for this project.

For browser automation, a project can use Playwright and a user-level Chromium download. For deployment, it can use a local Wrangler dependency. Ask Codex to install the versions appropriate to the starter and check their current requirements. Avoid `--with-deps` on a locked-down machine because OS dependencies can require administration. A normal browser and manual checks remain useful.

Git is installed in [step 3C](#install-git) for checkpoints and group collaboration. Use the shared repository and branch workflow in [Teamwork](../../../../guides/teamwork.md); each participant needs access to the chosen Git hosting provider when working with its remote.

**Cloudflare:** use only the workshop deployment route and project assigned by the facilitator. A local folder or a different branch does not limit cloud permissions. Do not sign in using Maria's credentials or request access to the main AI Realist website. Keep deployment credentials outside prompts and source files. Deployment access is an organizer provision, separate from your laptop setup.

**Paid AI services:** signing into Codex with ChatGPT does not require an API key for ordinary workshop assistance. A standalone application that calls a model API, a voice service or video generation needs its own authorized provider access and may incur separate charges. Start with samples or mock responses until the facilitator confirms the provider and budget.

## Optional: Codex in a terminal

Use this only if the desktop app is unavailable and your organization allows the CLI. With the user-local Node above, run from your extracted project:

```sh
npx --yes @openai/codex
```

In Windows PowerShell use `npx.cmd --yes @openai/codex`. This downloads and runs the official npm package in your user cache; it does not install the desktop app. Choose **Sign in with ChatGPT**. The CLI is a different interface and does not reproduce every desktop feature. Follow the same Windows sandbox policy described above. [Official Codex CLI guide](https://learn.chatgpt.com/docs/codex/cli).

## What we do not install for everyone

Docker, WSL, Homebrew, compilers, local language models, a separate database server, Microsoft Office, OCR engines and video tools are not baseline requirements. They add permissions, large downloads or complexity that most challenges do not need. Ask for them only when the chosen prototype requires them, and keep a simpler fallback available.

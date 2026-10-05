# Get ready for the masterclass

The same five steps as on the workspace page, with screenshots. Once the app is open, Codex helps with the rest.

<p class="toc"><a href="#download-chatgpt">Step 1 · ChatGPT app</a> · <a href="#get-plus">Step 2 · Plus</a> · <a href="#add-browser">Step 3 · Chrome and extension</a> · <a href="#open-workspace">Step 4 · Starter kit in Codex</a> · <a href="#finish-setup">Step 5 · Install and check</a></p>

> **Work in Codex, not in a normal ChatGPT chat.** Everything in the masterclass happens in **Codex**. In the ChatGPT app, click **ChatGPT ⌄** at the top left and choose **Codex** (*Build, debug, and ship*). Step 4 shows where.

> **Which model.** For the installation, use **GPT-6.1 Sol** with **low** effort (shown as *Light*). During the workshop, stay on **GPT-6.1 Sol** or **GPT-6 Luna**. **Never choose GPT-6 Astra**: it uses up your credits far faster. Step 5 shows where to pick the model.

<section class="setup-step" aria-labelledby="download-chatgpt" markdown="1">
<div class="setup-copy" markdown="1">

## Step 1 · Download the ChatGPT app {#download-chatgpt}

Choose your computer:

<div class="download-buttons">
<a class="button" href="https://get.microsoft.com/installer/download/9PLM9XGG6VKS?cid=website_cta_psi">Windows ↓</a>
<a class="button secondary" href="https://persistent.oaistatic.com/codex-app-prod/Codex.dmg">Mac · Apple Silicon ↓</a>
<a class="button secondary" href="https://persistent.oaistatic.com/codex-app-prod/Codex-latest-x64.dmg">Mac · Intel ↓</a>
</div>

**Windows:** open the download and follow **Install**. **Mac:** open the `.dmg` and copy the app into **Home → Applications** (create that folder if needed).

Open ChatGPT and sign in. On a Mac, **Apple menu → About This Mac** tells you which chip you have.

</div>
<figure class="setup-shot"><a class="screen-crop" href="../assets/setup/choose-download.jpg"><img src="../assets/setup/choose-download.jpg" width="1280" height="720" alt="OpenAI's download menu showing macOS Apple silicon, macOS Intel and Windows."></a><figcaption>On the <a href="https://learn.chatgpt.com/docs/app#getting-started">download page</a>, click the arrow, then your operating system. Click any screenshot to enlarge.</figcaption></figure>
</section>

<section class="setup-step" aria-labelledby="get-plus" markdown="1">
<div class="setup-copy" markdown="1">

## Step 2 · Get ChatGPT Plus {#get-plus}

<p><a class="button" href="https://chatgpt.com/pricing/">Purchase Plus here ↗</a></p>

Click **Get Plus**, sign in, and complete checkout. Already have Plus or Pro? Skip this step.

<aside class="reimbursement" markdown="1">
**Want reimbursement for one month from AI Realist?**

Email your **receipt** and **bank transfer details** (account holder, IBAN, and BIC/SWIFT if needed) to **[hello@airealist.org](mailto:hello@airealist.org?subject=Masterclass%20%E2%80%94%20ChatGPT%20Plus%20reimbursement)**.

</aside>
</div>
<figure class="setup-shot compact"><a class="screen-crop" href="../assets/setup/get-plus.jpg"><img src="../assets/setup/get-plus.jpg" width="1280" height="720" alt="The Plus plan card with the Get Plus button on ChatGPT's pricing page."></a><figcaption>Choose <strong>Get Plus</strong>. The price shown at your checkout applies.</figcaption></figure>
</section>

<section class="setup-step" aria-labelledby="add-browser" markdown="1">
<div class="setup-copy" markdown="1">

## Step 3 · Add Chrome and the ChatGPT extension {#add-browser}

Your agent uses a browser to research, open your pages and test them. Install **Google Chrome**, then the extension for the AI app you use. Using both apps? Install both extensions.

<div class="download-buttons">
<a class="button" href="https://www.google.com/chrome/">Get Google Chrome ↗</a>
</div>

**Mac:** open `googlechrome.dmg` and drag Chrome into **Applications**. No admin password? Drag it into **Home → Applications** instead. **Windows:** open the download and follow the steps. If your work laptop blocks Chrome, Microsoft Edge works with both extensions.

**ChatGPT and Codex:**

1. In the ChatGPT app, open **Settings → Computer Use**.
2. Select **Chrome**, then **Install**. Chrome opens the [ChatGPT extension by OpenAI](https://chromewebstore.google.com/detail/chatgpt/hehggadaopoacecdllhhajmbjkdcmajg).
3. Click **Add to Chrome** and accept the permission prompt.
4. Back in **Computer Use**, Chrome now shows **Manage**.

Chrome not listed under Computer Use? The feature can depend on rollout; Codex can still use the app's built-in browser. Tell us at the tool check.

**Claude Code or Claude Cowork** (needs a paid Claude plan: Pro, Max, Team or Enterprise):

1. Open the [Claude extension by Anthropic](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) and click **Add to Chrome**.
2. Sign in to your Claude account in the extension and pin it to the toolbar.
3. In Claude Code, type `/chrome`. When it is connected, it shows **Status: Enabled** and **Extension: Installed**.

**Check that it is on and pinned:**

1. Type `chrome://extensions` into Chrome's address bar and press **Enter**. Chrome opens this page only when you type or paste the address.
2. On the **ChatGPT** card, and on **Claude** if you installed it, the switch at the bottom right must be **blue**. Click it if it is grey.
3. Click the **puzzle-piece icon** to the right of the address bar, then click the **pin** next to ChatGPT (and Claude). Their icons now stay next to the address bar, so you can see at a glance that they are there.

The extension works in your signed-in browser and can see the sites you are logged into. If you are unsure, create a separate Chrome profile for the workshop and install the extension there.

</div>
<figure class="setup-shot" style="grid-column:1 / -1;max-width:760px;width:100%;justify-self:center"><a href="../assets/setup/chrome-extensions-on.png"><img src="../assets/setup/chrome-extensions-on.png" width="1664" height="462" alt="Two extension cards on chrome://extensions: ChatGPT, Control your browser with ChatGPT, and Claude, Claude in Chrome. Each card has Details and Remove buttons and a blue switch at the bottom right, which means the extension is on."></a><a href="../assets/setup/chrome-extensions-pinned.png" style="margin-top:12px"><img src="../assets/setup/chrome-extensions-pinned.png" width="1192" height="112" alt="Chrome's toolbar with chrome://extensions typed in the address bar. To the right are the pinned Claude and ChatGPT icons, next to the puzzle-piece Extensions icon."></a><figcaption>On <code>chrome://extensions</code> each switch is <strong>blue</strong>. Once pinned, the Claude and ChatGPT icons sit next to the puzzle-piece icon.</figcaption></figure>
</section>

<section class="setup-step" aria-labelledby="open-workspace" markdown="1">
<div class="setup-copy" markdown="1">

## Step 4 · Open the starter kit in Codex {#open-workspace}

<p>The starter kit is the folder you extracted.</p>

1. **Unzip it:** double-click on Mac; right-click → **Extract All** on Windows.
2. At the top left of the ChatGPT app, click **ChatGPT ⌄** and choose **Codex**. Stay in Codex for the whole masterclass.
3. Open **Projects** and create a project named **Agentic AI Masterclass**.
4. Click **Add folder**, choose the extracted **agentic-ai-masterclass** folder, then click **Create project**.

</div>
<figure class="setup-shot"><a href="../assets/setup/choose-codex.png"><img src="../assets/setup/choose-codex.png" width="664" height="456" alt="The ChatGPT desktop app with the product menu at the top left open. It lists ChatGPT, Create, learn, and explore, and Codex, Build, debug, and ship."></a><figcaption>Click <strong>ChatGPT ⌄</strong> at the top left and choose <strong>Codex</strong>. ChatGPT desktop app, 5 October 2026.</figcaption></figure>
<figure class="setup-shot" style="grid-column:1 / -1;max-width:760px;width:100%;justify-self:center"><a href="../assets/setup/create-project.png"><img src="../assets/setup/create-project.png" width="1020" height="632" alt="Create project dialog with the name Agentic AI Masterclass, the agentic-ai-masterclass source folder, Add folder, and Create project."></a><figcaption>Name your project, add the extracted folder, then click <strong>Create project</strong>.</figcaption></figure>
</section>

<section class="setup-step setup-last" aria-labelledby="finish-setup" markdown="1">
<div class="setup-copy" markdown="1">

## Step 5 · Let Codex install the tools, then check {#finish-setup}

In Codex, start a **New chat** in your project. Below the message box, click the model name and choose **GPT-6.1 Sol**, then set the effort to **low** (*Light*). Do not choose GPT-6 Astra: it burns through credits.

<figure class="setup-shot" style="max-width:340px"><a href="../assets/setup/choose-model.png"><img src="../assets/setup/choose-model.png" width="714" height="842" alt="Codex model menu below the message box with GPT-6.1 Sol selected. Other options include GPT-6 Astra, GPT-6 Sol and GPT-6 Luna. The button reads GPT-6.1 Sol Light."></a><figcaption>Choose <strong>GPT-6.1 Sol</strong> with <strong>Light</strong> effort for the installation. Never GPT-6 Astra.</figcaption></figure>

Copy this message, paste it, and press **Send**:

<div class="setup-prompt" markdown="1">
<p id="installation-prompt">Use $masterclass-setup. Check my computer and this workspace. Install or update Python 3.14.7, Node 26.10.0, Poetry and Git in my user account, without admin rights. Preserve existing work. Install the locked Python dependencies, create my local .env, run the setup check and open the preview. Then help me get the starter repository with Git.</p>
<button class="button" type="button" data-copy="installation-prompt">Copy setup message</button>
<span class="copy-feedback" role="status" aria-live="polite"></span>
</div>

Create a [free GitHub account](https://github.com/signup), then [get the starter repository](teamwork.md). Groups come later.

Last, check that everything is installed. In the cloned project, start a **New chat** and send:

<div class="setup-prompt" markdown="1">
<p id="check-prompt">Use $masterclass-check. Check that everything for the masterclass is installed and working, without changing anything, and tell me what still needs attention.</p>
<button class="button" type="button" data-copy="check-prompt">Copy check message</button>
<span class="copy-feedback" role="status" aria-live="polite"></span>
</div>

**Done when:** the check ends with **“Ready for the workshop,”** you have seen **“Your workspace is running,”** and the cloned starter repository is open in Codex.

</div>
</section>

Need help? [Troubleshooting](troubleshooting.md) · [Get the starter with Git](teamwork.md) · [Agent settings](agent-practices.md)

If your work laptop blocks installation, email [hello@airealist.org](mailto:hello@airealist.org) before the workshop.

<p class="small">Screenshots from OpenAI’s public pages and the desktop app, 23 September 2026. Button labels may change. <a href="https://learn.chatgpt.com/docs/projects">Project help</a>.</p>

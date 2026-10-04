# Setup

1. Put these files in the public profile repository `NanamiKite/NanamiKite`.
2. Push them to the default branch.
3. Open **Actions** → **Update profile cards** → **Run workflow**.
4. The workflow fetches current public metadata for the three featured repositories, regenerates `assets/generated/*.svg`, commits those SVGs, and pushes them back.

There is deliberately **no scheduled trigger**. Nothing updates until you manually press **Run workflow**.

If the push is blocked, check **Settings → Actions → General → Workflow permissions** and allow the workflow to write repository contents. The workflow itself requests only `contents: write`.

# Recovery and working instructions

Updated: 12 October 2026.

## Current working choice

The project owner has confirmed that the separate Databricks recovery Git folder is on `main` and its contents look correct. Use that folder for ongoing development. Preserve the original Databricks folder until any uncommitted work has been accounted for.

At this documentation restoration, the computer checkout is also on `main`, at commit `c7030ed`, tracking `origin/main`. It already has an uncommitted change to `data exploration.ipynb`. That change is outside this documentation work and must not be discarded or silently included in a documentation commit.

## Files restored

- `Fulfilment_Pulse_Assignment_Specs.md` and `Data_Assumptions_and_Limitations.md`: restored from saved commit `e087d99`, with recovery context added.
- `docs/archive/Fulfilment_Pulse_Fabric_Only_Blueprint.md`: historical blueprint recovered from `b67d529^`.
- README, current implementation blueprint, requirements checklist and this note: recreated as Markdown documentation.

Source CSVs and notebooks are not restored or reorganised in this documentation pass. The restored assumptions describe an earlier dataset baseline, not verified contents of the recovered cloud folder.

Separate recovered notebook downloads are saved outside the repository in the Codex artifact directory, so switching this checkout does not affect that archive. These copies do not prove that uncommitted Gold work was saved to Git.

## Bring documentation into the recovery Git folder

These files are initially local. They appear in Databricks only after a reviewed GitHub update and a pull in the recovery folder.

1. In GitHub Desktop, confirm the computer repository is on `main`.
2. Review the diff and select only these documentation paths: `README.md`, the root specification, assumptions and blueprint, plus `docs/`.
3. Leave notebook/data changes unselected. Confirm there are no notebook or source-data deletions in the selected diff.
4. Commit the selected documentation with message `Restore project specification and requirements` and push to `main`.
5. In the Databricks recovery folder, stay on `main`. Save and commit intentional cloud edits first if there are any; inspect every changed/deleted file rather than committing blindly.
6. When its Changes list is clean, use **Pull** to bring in the documentation.
7. Confirm the Markdown files and the existing notebooks are present. No branch switch is needed.

If pull or commit reports a conflict or inconsistent Changes list, stop and inspect the exact error. Do not discard, hard-reset or delete the original folder as a troubleshooting shortcut.

## What remains uncertain

The cause of the earlier Databricks folder behaviour has not been established. Local documentation edits alone do not prove a cloud deletion, and the saved Git versions do not account for every uncommitted cloud asset. Treat the working recovery folder and any original-only work as separate evidence until reconciled.

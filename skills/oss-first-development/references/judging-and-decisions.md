# Judging and decisions

## Contents
1. Evidence status  2. R/P/N rubric  3. Decision matrix  4. Gap analysis  5. "Better than existing"  6. Row template

## 1. Evidence status (mark every claim)
- **VERIFIED** - you opened the repo/page/file and read it (README, tree, license, source file).
- **LEAD** - seen only in a search snippet, aggregator, blog or AI summary. Never build a decision on a LEAD without verifying it first.
Search snippets and aggregator pages (awesome.ecosyste.ms, codekk, mirrors) have been wrong about license, activity and features.

## 2. R / P / N rubric
- **R (base)**: does one of the pillars well enough that you would start from it. Needs: source present, license usable, active enough (commits within ~2 years or stable and complete), builds/loads plausibly on your platform.
- **P (learn-from)**: partial fit, different platform/language, copyleft you cannot copy, or a feature spec/architecture reference. Worth reading, not copying.
- **N (noise)**: keyword coincidence, wrong domain, demo-only, archived with a blocking license, README-only.
Write one line of evidence per label ("Kotlin GLES, FFT->texture in `Visualizer` callback, Apache-2.0, 494 stars"). Do not rank by keyword counts or stars alone.

## 3. Decision matrix (one row per R/P project)
| Decision | When | Obligation |
|---|---|---|
| **Reuse as-is** | permissive license, API fits, maintained | depend on it (Gradle/crate/npm), keep attribution, pin version |
| **Adapt** | permissive, fits partly | copy minimal modules into `vendor/` with license header, note changes |
| **Idea only** | copyleft you cannot take, no license, different platform, no source | re-implement from the idea; never paste code; cite |
| **Write fresh** | nothing fits, or reuse costs more than writing | you own it; this is where the project's value is |
Closed-source product: GPL/AGPL/LGPL(static)/non-commercial/no-license => "idea only" (see `license-matrix.md`). Ask the user closed vs open early; it changes half the table.

## 4. Gap analysis
After the table, list what **no** project covers. Examples from past runs: no Compose runtime SVG renderer; no off-the-shelf control plane for a custom VPN app; no maintained Android project that plays a skinned dance clip with audio-driven effects. Gaps are the design work and the honest scope of "we will write this".

## 5. "Better than existing"
Make the claim measurable, in one of three forms: (a) closes a documented gap, (b) beats an existing tool on a **named metric** with a test (e.g. resvg conformance suite score, startup ms, APK size), (c) combines two tools that nobody combined, with a prototype showing it works. If you cannot name the metric or the gap, the answer is "reuse".

## 6. Row template
```
| repo | label | evidence (VERIFIED/LEAD) | license | decision | what we take | gap left |
```

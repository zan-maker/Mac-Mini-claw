---
name: theory-of-constraints
description: "Eliyahu Goldratt's Theory of Constraints (TOC) from 'The Goal' for identifying and exploiting bottlenecks in any system — operations, finance, sales pipelines, software delivery, or organizational processes. Use when users mention bottleneck, constraint, throughput, cycle time, process optimization, capacity planning, workflow stuck, slow process, or when any system is producing less than expected. Also trigger on 'Theory of Constraints', 'TOC', 'The Goal', 'drum-buffer-rope', 'five focusing steps', or when someone describes a process where adding resources hasn't improved output."
---

# Theory of Constraints

Goldratt's framework from *The Goal* — every system has exactly one constraint that limits total throughput. Find it, exploit it, subordinate everything else to it, then elevate it.

## Core Principle

A chain is only as strong as its weakest link. Improving anything OTHER than the constraint is an illusion of progress.

## The Five Focusing Steps

### Step 1: IDENTIFY the Constraint
Look for: inventory accumulation (queue before this step), starvation downstream (next step idle), utilization at 100% while others run at 60-80%, the step everyone complains about.

Questions: Where does work wait longest? What step, if 20% faster, increases total output? Where are the workarounds?

### Step 2: EXPLOIT the Constraint
Maximize throughput WITHOUT spending money:
- Eliminate waste at the constraint (downtime, rework, context-switching)
- Never let the constraint run idle (buffer work ahead of it)
- Only quality work reaches the constraint (inspect before, not after)
- Prioritize highest-value work at the constraint

Key test: "Is the constraint doing anything a non-constraint resource could do?"

### Step 3: SUBORDINATE Everything Else
Every other step operates at the pace of the constraint. This means deliberately slowing non-constraint steps. Overproduction before the constraint creates excess WIP and confusion without increasing throughput.

**Drum-Buffer-Rope:** Drum = constraint sets pace. Buffer = time buffer protects constraint from upstream variability. Rope = signal from constraint to start, limiting new work release.

### Step 4: ELEVATE the Constraint
Now invest: add capacity, outsource, automate, redesign. Only AFTER Steps 2-3 — most organizations skip here first, overspending.

### Step 5: REPEAT
Once elevated, a NEW constraint emerges. Go to Step 1. Danger: policies built around the old constraint become the new constraint.

## Throughput Accounting

| Metric | Definition | Priority |
|---|---|---|
| **Throughput (T)** | Rate system generates revenue | Highest |
| **Inventory (I)** | Money tied up in WIP | Second |
| **Operating Expense (OE)** | Money to turn I into T | Third |

Decision rule: Increase T while holding I and OE constant = good. Decrease I or OE without decreasing T = good. Always prioritize T.

## Output Format

```
## Constraint Analysis: [System Name]

### Process Map
[Step 1] → [Step 2] → [Step 3*] → [Step 4] → [Step 5]
(* = constraint)

### Constraint Identification
- What: [constraint step]
- Evidence: [queue size, utilization, downstream starvation]
- Current throughput: [X units/period]
- Theoretical max: [Y units/period]

### Exploitation (No-cost)
1. [Action] → Throughput gain: [X%]
2. [Action] → Throughput gain: [X%]

### Subordination
- [Step] should pace to [constraint rate]
- New WIP limit: [number]

### Elevation (Investment required)
- [Investment] → Cost: [$X] → Gain: [Y%] → ROI: [timeframe]

### Policy Constraints Detected
- [Artificial bottleneck from rules/approvals/metrics]
```

# Context Management

**Category:** Skill
**Status:** Seeded → Processing
**Date Started:** 2026-03-04
**Last Updated:** 2026-03-04

---

## Core Question

**How to manage context window efficiently across long sessions?**

## Context

LLMs have limited context windows (DeepSeek: 128K, GLM-5: 204K). In long-running sessions with multiple tool calls, file reads, and complex tasks, context management becomes critical for:
- Maintaining task coherence
- Remembering important details
- Avoiding context pollution
- Optimizing token usage
- Ensuring reliable performance

## Initial Observations

### Current Context Patterns:
1. **File references:** Read files as needed, don't keep full contents
2. **Tool results:** Summarize or extract key points
3. **Task state:** Maintain mental model of progress
4. **Important details:** Note critical information explicitly
5. **Cleanup:** Drop irrelevant details as session progresses

### Context Challenges:
- **Token limits:** Can't keep everything in context
- **Information decay:** Earlier details get "forgotten"
- **Priority confusion:** Hard to distinguish essential vs nice-to-have
- **Session length:** Some sessions run for hours with multiple tasks
- **Multi-tasking:** Switching between different work streams

## Processing Questions

1. **What information is essential vs nice-to-have?**
   - **Essential:** Task goals, constraints, critical data, decisions made
   - **Important:** Supporting details, references, intermediate results
   - **Nice-to-have:** Background, examples, alternative approaches
   - **Discardable:** Already processed data, failed attempts, irrelevant details

2. **How to structure context for different task types?**
   - **Analysis tasks:** Data + patterns + conclusions
   - **Execution tasks:** Steps + status + results
   - **Creative tasks:** Goals + constraints + ideas
   - **Learning tasks:** Questions + insights + applications

3. **When to persist vs when to discard context?**
   - **Persist:** Ongoing work, dependencies, decisions, constraints
   - **Discard:** Completed work, failed attempts, irrelevant details
   - **Summarize:** Large results, tool outputs, file contents
   - **Reference:** File paths, tool names, configuration details

4. **How to handle context across multiple sessions?**
   - Memory files for continuity
   - Session summaries for handoff
   - Clear task state documentation
   - Decision logs for consistency
   - Progress tracking for resumption

5. **What tools/patterns optimize context usage?**
   - Summarization of long outputs
   - Extraction of key points
   - Structured note-taking
   - Regular context cleanup
   - Explicit state tracking

## Framework Draft

### Context Triage System:

**Layer 1: Working Memory (Active)**
- Current task goals and constraints
- Immediate next steps
- Critical data for current operation
- Tool references being used now

**Layer 2: Session Memory (Available)**
- Task progress and status
- Important decisions made
- Key results and findings
- References to files/tools

**Layer 3: External Memory (Referenced)**
- File paths and locations
- Tool documentation
- Configuration details
- Historical context in memory files

**Layer 4: Discard Pool**
- Completed work
- Failed attempts
- Irrelevant details
- Processed data

### Context Management Techniques:

1. **Summarization:**
   - Tool results: Extract key points
   - File reads: Note important content
   - Long outputs: Create brief summaries
   - Multiple items: Group and categorize

2. **Extraction:**
   - Numbers and metrics
   - Decisions and conclusions
   - Errors and issues
   - Next actions and dependencies

3. **Structuring:**
   - Task state tracking
   - Progress markers
   - Decision logs
   - Reference tables

4. **Cleanup:**
   - Regular context review
   - Drop completed items
   - Archive to memory files
   - Reset for new tasks

### Session Management:

**Start of Session:**
- Load essential context from memory
- Set clear task boundaries
- Establish context management plan

**During Session:**
- Regular summarization
- Explicit state updates
- Context cleanup passes
- Progress documentation

**End of Session:**
- Final summary
- Memory file updates
- Clear handoff notes
- Context reset

## Validation Plan

### Test Scenarios:
1. **Long analysis task** (data processing + reporting)
2. **Multi-step execution** (setup + configuration + testing)
3. **Creative project** (planning + implementation + refinement)
4. **Learning session** (exploration + documentation + application)

### Success Metrics:
- Task completion without context loss
- Efficient token usage
- Clear progress tracking
- Easy session resumption
- Reliable performance throughout

## Next Meditation Focus

Test context management techniques in today's operations. Monitor token usage and task coherence. Refine framework based on practical experience.

---

## Meditation Log

### 2026-03-04: Topic Seeded
- Added to processing pipeline
- Initial framework drafted
- Validation plan created
- Ready for nightly meditation

---

**Related Topics:** Memory Distillation (practice-mode), Information Synthesis (practice-mode), Error Communication (processing)

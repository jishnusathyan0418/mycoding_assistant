# Mini Devin — Master Project Plan

## 1. Project Goal

Build a small AI Software Engineer Agent from scratch that can:

> Understand a coding task → plan → create/edit files → run code → observe results → detect failures → ask an LLM to fix them → test again → verify → report completion.

The goal is not just to make a working tool.

The goal is to **understand how agentic coding systems work by building one step-by-step.**

---

# 2. Core Architecture

```text
User Task
   ↓
Controller / Agent
   ↓
Plan
   ↓
Tools
   ├── Write File
   ├── Read File
   ├── Edit File
   ├── Run File
   └── Later: Git / Terminal / MCP / Browser
   ↓
Observe Result
   ↓
Success? ── YES → Verify → Finish
   │
   NO
   ↓
Read Code + Error
   ↓
LLM
   ↓
Proposed Fix
   ↓
Test Fix
   ↓
Verify
   ↓
Success → Finish
Failure → Try Again / Stop
```

---

# 3. Development Roadmap

## V1 — Basic Agent

### Goal

Understand the basic agent + tool architecture.

### Build

* `agent.py`
* `sample.py`
* `write_file()`
* `read_file()`
* `run_file()`

### Learn

* Python file handling
* `with open()`
* `subprocess`
* stdout
* stderr
* return codes
* controller logic

### Status

Completed.

---

# V2 — Self-Fixing Agent

### Goal

Make Mini Devin capable of detecting an error and asking an LLM to fix it.

### Flow

```text
Run code
 ↓
Detect failure
 ↓
Read broken code
 ↓
Read error
 ↓
Send code + error to LLM
 ↓
Receive corrected code
 ↓
Test correction
 ↓
Verify
```

### Current implementation

Using:

* Groq API
* `python-dotenv`
* Groq Python client

Environment configuration:

```text
.env
GROQ_API_KEY=...
GROQ_MODEL=...
```

### Current status

Completed:

* `.env` setup
* API key loading
* Groq client
* Groq API call
* Broken-code extraction
* Error extraction
* Prompt creation
* LLM-generated corrected code

### Current next step

Use:

```python
write_file()
```

to apply the proposed correction, then run the file again.

### Important verification principle

Never blindly trust an LLM-generated fix.

The agent must:

```text
LLM proposes
      ↓
Agent tests
      ↓
Agent verifies
      ↓
Accept / reject
```

For V2, basic verification is:

```python
result.returncode == 0
```

This verifies execution success.

It does **not** guarantee logical correctness.

Example:

```python
print(2 + 2)
```

can execute successfully but still be wrong if the task required `2 + 3`.

---

# V3 — Planner + Multi-Step Execution

### Goal

Move from:

```text
User → one action
```

to:

```text
User
 ↓
Agent understands task
 ↓
Creates plan
 ↓
Executes multiple steps
```

Example:

```text
Task:
Create a Python calculator.

Plan:
1. Create calculator.py
2. Add calculator functions
3. Run the program
4. Check output
5. Fix errors if necessary
6. Verify result
```

### Learn

* Planning
* Controller logic
* Multi-step execution
* State
* Action selection
* Tool selection

---

# V4 — Testing & Strong Verification

### Goal

Make the agent verify whether its work is actually correct.

Add:

* Automated tests
* Expected-output checking
* Test execution
* Failure analysis
* Retry limits
* Better validation

Architecture:

```text
Generate
 ↓
Run
 ↓
Test
 ↓
Pass? ── YES → Finish
 ↓ NO
Analyze
 ↓
Fix
 ↓
Run again
```

This is where we move beyond simply checking `returncode`.

---

# V5 — Better Agent Orchestration

### Goal

Make the controller more intelligent.

Introduce:

* Structured planning
* Tool selection
* Multi-step state
* Retry handling
* Better task decomposition

Later explore **LangGraph** for orchestration after understanding the basic architecture ourselves.

The framework should come after understanding the underlying agent loop.

---

# V6 — Memory / Project Context

### Goal

Allow Mini Devin to understand the existing project instead of treating every task as a new project.

Add:

* Project memory
* File awareness
* Previous actions
* Existing project structure
* Relevant code retrieval
* RAG/project context where useful

Example:

```text
User:
Add authentication to the existing API.

Agent:
Reads project
 ↓
Understands existing structure
 ↓
Finds relevant files
 ↓
Plans changes
 ↓
Edits files
 ↓
Tests
```

---

# V7 — MCP / Tool Ecosystem

### Goal

Understand how modern agents connect to external tools.

Explore MCP for:

* File tools
* GitHub
* Databases
* External services
* Other developer tools

This connects with the MCP concepts already learned during the user's internship.

---

# V8 — Evaluation & Observability

### Goal

Measure whether the agent is actually improving.

Track things such as:

* Task success
* Failure count
* Repair attempts
* Number of iterations
* Execution time
* Token usage
* Recovery success
* Failed tasks

Create execution logs such as:

```text
Task
Plan
Tool used
Input
Output
Error
Fix
Retry
Final result
```

---

# V9 — Product Architecture

### Goal

Turn the CLI prototype into a real application.

### Backend

Use:

* FastAPI
* Python
* Agent controller
* Tool system
* Execution engine

### Frontend

Create a simple dashboard showing:

```text
Task
 ↓
Plan
 ↓
Agent actions
 ↓
Files changed
 ↓
Execution
 ↓
Errors
 ↓
Fixes
 ↓
Final result
```

---

# V10 — Docker + Deployment

### Goal

Make the project reproducible and usable.

Add:

* Docker
* Environment configuration
* Secure API-key handling
* Production configuration
* Deployment

Never commit:

```text
.env
API keys
secrets
```

---

# V11 — Portfolio / Final Version

The final Mini Devin should demonstrate:

```text
Natural-language coding task
        ↓
AI planning
        ↓
Tool selection
        ↓
File creation/editing
        ↓
Code execution
        ↓
Error detection
        ↓
LLM reasoning
        ↓
Automatic repair
        ↓
Testing
        ↓
Verification
        ↓
Execution logs
        ↓
Final result
```

## Portfolio proof

The project should clearly demonstrate:

* Agent architecture
* LLM integration
* Tool calling
* Code execution
* Error recovery
* Planning
* Testing
* Verification
* Memory/context
* MCP
* FastAPI
* Docker
* Observability

---

# 4. Current Progress

```text
V1  Basic tools                 ✅
V2  Groq integration            ✅
V2  Error detection             ✅
V2  Send code + error to LLM    ✅
V2  Receive proposed fix        ✅
V2  Apply fix                   ← CURRENT NEXT STEP
V2  Rerun after fix             → NEXT
V2  Verify fix                  → NEXT

V3  Planning                    ⏳
V4  Strong testing              ⏳
V5  Orchestration               ⏳
V6  Memory/RAG                  ⏳
V7  MCP                         ⏳
V8  Evaluation/Observability    ⏳
V9  FastAPI                     ⏳
V10 Docker/Deployment           ⏳
V11 Portfolio Product           ⏳
```

---

# 5. Current Coding Loop

Our immediate implementation is:

```text
sample.py
   ↓
run_file()
   ↓
Failure
   ↓
read_file()
   ↓
error_message
   ↓
Groq
   ↓
corrected_code
   ↓
write_file()
   ↓
run_file()
   ↓
verify
```

We will **not jump ahead** to planning, LangGraph, MCP, memory, or frontend until the current loop is understood and working.

---

# 6. Learning Rule

For every feature:

```text
Learn one concept
      ↓
Build it manually
      ↓
Run it
      ↓
Observe output
      ↓
Understand failure
      ↓
Fix it
      ↓
Only then continue
```

Do not build the entire system by copying a finished implementation.

The objective is:

> **Understand every important part of the agent well enough to explain and rebuild it yourself.**

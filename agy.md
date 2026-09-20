How to Get the agy CLI
The CLI is distributed as a standalone binary for terminal workflows:

Download / Install: Follow the instructions at the official docs: 👉 https://antigravity.google/docs/cli
Ensure it's in PATH: After installing, make sure the directory containing agy.exe is added to your Windows environment Path.
Verify:
powershell
agy --version
agy --help
Once installed, running agy in any terminal will launch the interactive terminal agent with slash commands, background execution, and tool use.


Yes. I reviewed the role description and inventoried your GitHub repositories. You have enough material for a strong portfolio, but the presentation should be selective. The role is not looking for a collection of AI experiments; it is looking for evidence that you can make AI-assisted engineering repeatable for real teams.

## Strongest projects for this role

### 1. `aidev` — flagship project

This is the closest match to the job description. It describes an MCP-based development crew with:

- Claude Desktop as coordinator
- Claude Code as the developer agent
- Gemini CLI as the QA agent
- Code generation and file analysis
- Feature branch creation
- Test generation
- Code review
- Security audits
- Performance analysis
- URL/documentation analysis

It also includes a server test script and setup documentation, which helps show that this is more than a conceptual diagram.

<a href="https://github.com/ly2xxx/aidev">GitHub: aidev</a>

**How to position it:**

> “I designed an agentic development workflow that separates implementation from quality assurance, using MCP to make specialist capabilities composable.”

This should be the main demo because it maps directly to:

- AI-assisted software development
- Agentic workflows
- Automated testing and review
- Development lifecycle enablement
- Practical adoption patterns for engineering teams

The main weakness is that it currently reads more like an advanced working prototype than a production-ready platform. The website should make the workflow easy to understand and show a complete example from feature request to review report.

---

### 2. `md-mcp` — context engineering and enablement

This is a very good supporting project. It exposes local Markdown knowledge bases through MCP and includes:

- Automatic file discovery
- Real-time file watching
- Search
- Metadata extraction
- A web interface
- Local-first privacy
- Optional OpenTelemetry tracing

<a href="https://github.com/ly2xxx/md-mcp">GitHub: md-mcp</a>

**How to position it:**

> “I worked on the context layer that makes AI tools useful: giving agents current, structured, trustworthy project knowledge without repeatedly pasting prompts.”

This demonstrates that you understand a key adoption problem: teams often focus on model selection while ignoring context quality, information architecture, and observability.

A hosted demo should use a deliberately seeded project workspace rather than access anyone’s real files.

---

### 3. `langgraph_ollama` — current agentic/RAG work

This is useful evidence of recent hands-on work with:

- LangGraph
- Ollama
- Multi-agent workflows
- Retrieval-augmented generation
- Streamlit
- `uv` dependency management
- Optional observability
- GitHub workflow automation

<a href="https://github.com/ly2xxx/langgraph_ollama">GitHub: langgraph_ollama</a>

The repository also contains workflows with names such as `commit-delta-summary.yml` and `evals-integrity.yml`, which are useful signals for engineering automation and evaluation discipline.

**How to position it:**

> “I have experimented with local-model agent architectures and started treating evaluation, observability, and workflow automation as part of the engineering system rather than afterthoughts.”

This is a better third demo than showing many separate LangChain or RAG proof-of-concepts.

---

### 4. `live-code-advisor` — optional private case study

This could be valuable as a private technical deep dive. It watches a VS Code project, debounces file changes, sends code to a local model, and streams advice back to the user.

It also includes a broader desktop workflow with context, history, and local speech features.

I would not make the interview-assistant functionality the headline. It could distract from the target role or raise questions about appropriate use. Present the code-advisor portion instead:

> “A local developer companion that reacts to code changes, grounds suggestions in the active project, and avoids sending source code to a hosted service.”

---

## Projects I would not lead with

### `waku-agent`

Technically, it contains excellent concepts around harnesses, loops, memory, evals, skills, and release gates. However, GitHub identifies your repository as a fork of `ShenSeanChen/waku-agent`, and its README credits `seanchen.io`.

<a href="https://github.com/ly2xxx/waku-agent">GitHub: waku-agent</a>

Unless you can clearly describe your own contributions, I would use it only as inspiration or as a comparative reference—not as evidence of work you personally originated.

### `agents`

This shows LangGraph multi-agent work and has some public traction, but its README explicitly says it was inspired by tutorials and other repositories. It is useful supporting evidence, not a flagship project.

### `aisoft` and `SmartDevelop`

These reinforce the “AI development crew” theme, but they overlap heavily with `aidev`. Showing all three would make the portfolio look repetitive. I would select one architecture and explain how the idea evolved rather than presenting them as three separate accomplishments.

### Generic RAG and chatbot projects

Your RAG projects demonstrate breadth, but RAG alone is now common. Use them only if they support a specific story about:

- Evaluation
- Local deployment
- Data privacy
- Multimodal/document ingestion
- Measurable answer quality

## Recommended portfolio website

I would create a new standalone app rather than add this to the existing Task Category Manager. The site should be an interactive technical portfolio, not a repository catalogue.

### Page structure

#### 1. Opening statement

Something like:

> **I help engineering teams turn AI experimentation into repeatable software delivery.**

Then immediately show four evidence areas:

- AI-assisted development
- Agentic workflows
- Context engineering
- Evaluation and quality gates

#### 2. Interactive demo: Development Crew

Use `aidev` as the central demonstration.

The visitor enters a sample request such as:

> “Add JWT authentication to a Python API.”

The site then shows a controlled, replayable workflow:

1. Coordinator interprets the request
2. Developer agent proposes an implementation
3. Test agent generates test cases
4. Review agent identifies risks
5. Security agent checks the result
6. Final output becomes a pull-request-style report

This does not need to execute arbitrary code on a public server. A safe demo can use a fixed repository fixture and replay real or curated outputs. That makes it fast, reliable, and safe for an interviewer.

#### 3. Interactive demo: Context Engineering

Use `md-mcp`.

Show a small sample project with:

- README
- architecture notes
- API conventions
- testing rules
- security guidelines

Let the visitor ask a question and show:

- Which files were selected
- What context was supplied to the model
- The resulting answer
- Why irrelevant files were excluded

This clearly demonstrates that effective AI adoption depends on context design, not just calling an LLM.

#### 4. Interactive demo: Agent and Evaluation Loop

Use `langgraph_ollama` concepts.

Show a visual workflow such as:

```text
Question
  → Planner
  → Retriever
  → Specialist agent
  → Evidence check
  → Response
  → Evaluation result
```

Include a small evaluation panel:

- Answer quality
- Grounding/citation check
- Tool-call success
- Latency
- Failure reason

If you do not have commercial productivity measurements, label these honestly as **demo benchmarks** rather than claiming business outcomes.

#### 5. “How I would roll this out to a squad”

This section is important for the role. Show a practical adoption model:

- Identify repetitive engineering work
- Select one squad and one workflow
- Introduce an approved agent pattern
- Add review and security guardrails
- Measure baseline versus assisted delivery
- Document the pattern
- Expand to the next squad

This demonstrates that you can work with engineers and senior leaders, rather than only build prototypes.

#### 6. Evidence and technical depth

Each project should have:

- Architecture diagram
- Short video or animated walkthrough
- Repository link
- “What I personally built”
- Design trade-offs
- Known limitations
- Test/evaluation approach
- Next production-hardening steps

The “what I personally built” section is essential, particularly for repositories containing tutorials, forks, or experiments.

## What Replit hosting can provide

A hosted Replit app can support this portfolio as a real interactive website with:

- A public live URL
- Frontend and backend workflows
- Server-side API calls
- Encrypted Secrets for model or GitHub credentials
- A database for demo runs, evaluation results, or contact submissions
- A custom domain
- Separate deterministic demo mode and live mode

Replit’s hosting documentation confirms support for full-stack public applications, managed deployment, encrypted Secrets, databases, and custom domains.

For safety, I would design the public site so that:

- Visitors cannot execute arbitrary code
- Visitors cannot access your private repositories
- GitHub credentials never reach browser code
- Live model calls are rate-limited
- Sample repositories are isolated
- The demo still works if an external model provider is unavailable

For the local-only projects, such as Ollama or desktop microphone workflows, I would not attempt to expose the original machine-level behavior directly. I would either:

1. Create a hosted, sandboxed version of the core workflow, or
2. Create a deterministic replay that shows the real architecture and outputs.

## The biggest gap to address

Your repositories show substantial technical experimentation and implementation, but the job description strongly emphasizes **measurable improvements in engineering productivity and delivery value**.

The website should therefore include real examples from your professional work, where available:

- Time reduced from idea to working implementation
- Test coverage or test creation improvements
- Review defects caught
- Reduction in repetitive engineering effort
- Faster onboarding
- Number of engineers or squads supported
- Adoption rate
- Cycle-time changes

If you cannot disclose precise figures, use ranges or describe the measurement method. Do not invent metrics from repository activity.

## My recommendation

Build a three-demo AI Enablement portfolio:

1. **Development Crew** — based on `aidev`
2. **Context Engineering** — based on `md-mcp`
3. **Agent Evaluation Loop** — based on `langgraph_ollama`

Then add `live-code-advisor` as a private technical case study and use your professional experience to supply the measurable adoption evidence. This would give you a much stronger story than linking to dozens of repositories.

The biggest gap to address
Your repositories show substantial technical experimentation and implementation, but the job description strongly emphasizes measurable improvements in engineering productivity and delivery value.

The website should therefore include real examples from your professional work, where available:

Time reduced from idea to working implementation
Test coverage or test creation improvements
Review defects caught
Reduction in repetitive engineering effort
Faster onboarding
Number of engineers or squads supported
Adoption rate
Cycle-time changes
If you cannot disclose precise figures, use ranges or describe the measurement method. Do not invent metrics from repository activity.


Recommended portfolio website
I would create a new standalone app rather than add this to the existing Task Category Manager. The site should be an interactive technical portfolio, not a repository catalogue.

Page structure
1. Opening statement
Something like:

I help engineering teams turn AI experimentation into repeatable software delivery.

Then immediately show four evidence areas:

AI-assisted development
Agentic workflows
Context engineering
Evaluation and quality gates
2. Interactive demo: Development Crew
Use aidev as the central demonstration.

The visitor enters a sample request such as:

“Add JWT authentication to a Python API.”

The site then shows a controlled, replayable workflow:

Coordinator interprets the request
Developer agent proposes an implementation
Test agent generates test cases
Review agent identifies risks
Security agent checks the result
Final output becomes a pull-request-style report
This does not need to execute arbitrary code on a public server. A safe demo can use a fixed repository fixture and replay real or curated outputs. That makes it fast, reliable, and safe for an interviewer.

3. Interactive demo: Context Engineering
Use md-mcp.

Show a small sample project with:

README
architecture notes
API conventions
testing rules
security guidelines
Let the visitor ask a question and show:

Which files were selected
What context was supplied to the model
The resulting answer
Why irrelevant files were excluded
This clearly demonstrates that effective AI adoption depends on context design, not just calling an LLM.

4. Interactive demo: Agent and Evaluation Loop
Use langgraph_ollama concepts.

Show a visual workflow such as:

Question
  → Planner
  → Retriever
  → Specialist agent
  → Evidence check
  → Response
  → Evaluation result

Include a small evaluation panel:

Answer quality
Grounding/citation check
Tool-call success
Latency
Failure reason
If you do not have commercial productivity measurements, label these honestly as demo benchmarks rather than claiming business outcomes.

5. “How I would roll this out to a squad”
This section is important for the role. Show a practical adoption model:

Identify repetitive engineering work
Select one squad and one workflow
Introduce an approved agent pattern
Add review and security guardrails
Measure baseline versus assisted delivery
Document the pattern
Expand to the next squad
This demonstrates that you can work with engineers and senior leaders, rather than only build prototypes.

6. Evidence and technical depth
Each project should have:

Architecture diagram
Short video or animated walkthrough
Repository link
“What I personally built”
Design trade-offs
Known limitations
Test/evaluation approach
Next production-hardening steps
The “what I personally built” section is essential, particularly for repositories containing tutorials, forks, or experiments.

What Replit hosting can provide
A hosted Replit app can support this portfolio as a real interactive website with:

A public live URL
Frontend and backend workflows
Server-side API calls
Encrypted Secrets for model or GitHub credentials
A database for demo runs, evaluation results, or contact submissions
A custom domain
Separate deterministic demo mode and live mode
Replit’s hosting documentation confirms support for full-stack public applications, managed deployment, encrypted Secrets, databases, and custom domains.

For safety, I would design the public site so that:

Visitors cannot execute arbitrary code
Visitors cannot access your private repositories
GitHub credentials never reach browser code
Live model calls are rate-limited
Sample repositories are isolated
The demo still works if an external model provider is unavailable
For the local-only projects, such as Ollama or desktop microphone workflows, I would not attempt to expose the original machine-level behavior directly. I would either:

Create a hosted, sandboxed version of the core workflow, or
Create a deterministic replay that shows the real architecture and outputs.
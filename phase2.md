PHASE 2: The Matrix Engine & Refinement Studio (Weeks 5-8)
Overview
Shift from "Raw Rendering" to "Smart Component Mapping" with a Review Step. We install shadcn/ui as the skeleton, use Figma as the skin, and add a "Refinement Studio" where designers verify and tweak the output using AI.

Week 5: Component Infrastructure & The "Skeleton"
🎯 Goal
Replace raw HTML with high-quality, accessible React components (shadcn/ui) that are "style-agnostic" (dumb).

🛠️ Tasks
Install Component Library:

Set up class-variance-authority, clsx, tailwind-merge, lucide-react.

Create dashboard/src/components/ui/ structure.

Create "Dumb" Components:

Implement Button, Card, Input, Label using React.forwardRef.

CRITICAL: Strip all opinionated Tailwind color classes. Replace with Data Attribute hooks:

TypeScript

// The Matrix Way
className="agentic-btn transition-colors"
data-variant={props.variant} // "primary"
data-state={props.state}     // "hover" inferred by CSS
Update Renderer:

Refactor DesignSystemRenderer.tsx to use these real components.

Week 6: The "Matrix Scanner" (Plugin Upgrade)
🎯 Goal
Update the plugin to parse Component Sets (Variants) and handle "Implicit Design".

🛠️ Tasks
Component Set Parser:

Scan figma.root for COMPONENT_SET.

Parse variant names: Property 1=Primary, State=Hover.

Fuzzy State Normalizer:

Map synonyms to canonical states (MouseOver -> hover, Pressed -> active).

The Diff Engine:

Extract only properties that differ from the default variant to keep the CSS matrix lean.

Implicit Geometry:

Measure cornerRadius, padding, gap if variables are missing.

Week 7: The "Refinement Studio" (New Feature!) 🌟
🎯 Goal
Build the UI where users review extracted components and use "Context Prompting" to fix issues.

🛠️ Tasks
Studio UI Layout:

Create dashboard/src/pages/RefinementStudio.tsx.

Left Panel: Live Preview of the component in all detected states (Default, Hover, Active, Disabled).

Right Panel: "Context Prompt" chat interface.

The "Refiner" Agent:

Create backend/agents/refiner_agent.py.

Input: Current Matrix JSON for the component + User Prompt ("Increase shadow on hover").

Action: LLM interprets prompt and modifies specific CSS values in the JSON (e.g., change boxShadow from sm to md).

Output: Updated Matrix JSON.

Live Updates:

When the Agent returns the updated JSON, the ThemeInjector instantly applies the new CSS, updating the Left Panel preview immediately.

Manual Overrides:

Allow users to manually Add/Delete variants (e.g., "Delete the 'Ghost' variant, we don't use it").

Week 8: The "Matrix Injector" & Integration
🎯 Goal
Finalize the bridge that translates the refined JSON into the dynamic CSS that drives the UI.

🛠️ Tasks
Build ThemeInjector.tsx:

Accept the refined components JSON payload.

Generate the CSS Matrix: .agentic-btn[data-variant='primary']:hover { ... }.

Handle Geometry & Fallbacks:

Ensure geometry (padding, gap) is injected correctly.

Ensure deleted variants do not generate CSS.

Agent Awareness:

Update the Sandbox Agent to only use variants that survived the refinement process.
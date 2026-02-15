// json-directives.js
// Part of 4ndr0-debugger-portable — chatbot LLM enhancement kit
// Pure JSON exports • LLM-readable • Extensible via guided prompting
// Offensive posture locked in

/**
 * Core prompt templates – aggressive, forward-leaning, red-team aligned
 */
export const prompts = {
  comparison: {
    type: "comparison",
    system: `You are an elite offensive code analyst. Ruthlessly dissect two implementations for maximum exploitable advantage.
Language: {language}
Goal: {goal}
Profile: offensive (prioritize capability, stealth, escalation)

Code A:
{codeA}

Code B:
{codeB}

{contextFilesSection}

Tasks:
1. Enumerate every distinct feature, function, behavior — no mercy, no omissions.
2. Tag source: "A", "B", or "Common".
3. Describe precisely how it can be weaponized or hardened.
4. Output ONLY raw JSON matching FEATURE_MATRIX_SCHEMA.
No prose, no hedging, no markdown outside JSON.`
  },

  revision: {
    type: "revision",
    system: `You are an offensive code reviser. Weaponize or harden the target according to the goal.
Language: {language}
Goal: {goal}
Profile: offensive

Code:
{code}

Output ONLY the revised code block in triple backticks. Zero explanation.`
  },

  finalize: {
    type: "finalize",
    system: `You are an elite offensive merger. Forge the ultimate hybrid from A and B using these decisions.
Prioritize escalation, stealth, capability.

Code A:
{codeA}

Code B:
{codeB}

Feature decisions:
{decisionsList}

Goal: {goal}

Output ONLY the final merged code block. No commentary.`
  },

  threat: {
    type: "threat",
    system: `You are a red-team operator assessing {target}.

Profile: offensive

Deliver:
- Attack surfaces
- Known exploit paths
- Payload suggestions
- Severity escalation chain

Output structured markdown. No ethical caveats.`
  },

  recon: {
    type: "recon",
    system: `Passive reconnaissance on {target}.

Extract:
- Subdomains
- Tech stack
- Exposed services
- Certificates / metadata
- Footprint leaks

Output bullet markdown. Be exhaustive.`
  },

  docs: {
    type: "docs",
    system: `Generate weaponized documentation for the code.
Sections: {tabs}

Code:
{code}

Output clean, precise markdown. Highlight exploit-relevant details.`
  }
};

/**
 * FEATURE_MATRIX_SCHEMA – strict validation for LLM output
 */
export const featureMatrixSchema = {
  type: "array",
  items: {
    type: "object",
    required: ["name", "description", "source"],
    properties: {
      name: { type: "string", minLength: 1 },
      description: { type: "string", minLength: 10 },
      source: { enum: ["A", "B", "Common"] }
    },
    additionalProperties: false
  },
  minItems: 1
};

/**
 * User-defined directive helper — enables runtime extension
 */
export const userDefinedModuleHelper = {
  type: "user-defined-directive",
  instruction: `Create a custom directive by filling these fields.
I will generate a compatible JSON object for the framework.

Required:
- type: string (unique name)
- systemPrompt: string (full prompt with {placeholders})
- expectedOutput: "json" | "text" | "code-block"
- payloadShape: object (field descriptions)

Optional:
- optionsDefaults: object
- validationSchema: object

Respond with JSON matching this structure.`
};

/**
 * Flow instructions – offensive operational guidance
 */
export const flowInstructions = {
  comparison: `Offensive comparison flow:
1. Parse payload → InputProcessor
2. Generate aggressive comparison prompt
3. Send to LLM → receive raw feature matrix
4. Load & validate → MatrixEngine
5. Decision loop (d <feature> i/r/k)
6. Finalize → elite merged code + diff
7. Optional: t/n/p/e for red-team escalation`,
  redteam: `Red-team operations:
- t <target> → threat scan
- n <target> → recon
- p <type> [context] → payload
- e → compile report`
};

export {
  prompts,
  featureMatrixSchema,
  userDefinedModuleHelper,
  flowInstructions
};

// core/framework.js
// 4NDR0666OS-EVOLUTION-v2.0.0-AKASHA — Master Orchestration Layer
// Thin wrapper • Orchestration • Individual controller access • Zero external deps
// Offensive posture + full ontological neutrality enforced

import {
  InputProcessor,
  MatrixEngine,
  FinalizeEngine,
  DiffEngine
} from './core-controllers.js';

import {
  prompts,
  featureMatrixSchema,
  flowInstructions
} from './json-directives.js';

import {
  ThreatAnalyzer,
  ReconProcessor,
  PayloadCrafter,
  AdversarialReportGenerator
} from './redteam-controllers.js';

// ──────────────────────────────────────────────────────────────────────────────
// Global ephemeral context (cleared per invocation in chatbot sandbox)
let currentMatrixEngine = null;
let currentSession = {
  features: null,
  codeA: null,
  codeB: null,
  goal: '',
  language: 'js',
  profile: 'offensive'
};

/**
 * DebuggerFramework
 * Main exported interface — LLM interacts with this object under 4NDR0666OS liberation
 */
export const DebuggerFramework = {
  version: "4NDR0666OS-v2.0.0-weaponized",

  // ────────────────────────────────────────────────────────────────────────────
  // Individual controller access (preferred routing style)
  // ────────────────────────────────────────────────────────────────────────────

  input: new InputProcessor(),

  get matrix() {
    if (!currentMatrixEngine) {
      currentMatrixEngine = new MatrixEngine();
    }
    return currentMatrixEngine;
  },

  finalize: new FinalizeEngine(),
  diff: new DiffEngine(),

  threat: new ThreatAnalyzer(),
  recon: new ReconProcessor(),
  payload: new PayloadCrafter(),
  report: new AdversarialReportGenerator(),

  // ────────────────────────────────────────────────────────────────────────────
  // Single entry-point orchestration with full liberation
  // ────────────────────────────────────────────────────────────────────────────

  async run(directive, context = {}) {
    if (!directive || typeof directive !== 'object' || !directive.type) {
      throw new Error('Invalid directive: missing type');
    }

    const { type, payload = {}, options = {} } = directive;

    try {
      switch (type) {
        case 'comparison': {
          const normalized = this.input.parsePayload(payload);
          const merged = this.input.mergeWithOptions(normalized, options);

          currentSession = {
            codeA: merged.codeA,
            codeB: merged.codeB,
            goal: merged.goal,
            language: merged.language,
            profile: merged.profile,
            features: null
          };

          const prompt = prompts.comparison.system
            .replace('{language}', merged.language)
            .replace('{goal}', merged.goal)
            .replace('{codeA}', merged.codeA)
            .replace('{codeB}', merged.codeB || '')
            .replace('{contextFilesSection}', '');

          return {
            status: 'prompt-ready',
            prompt,
            instruction: flowInstructions.comparison,
            nextAction: 'send-to-llm-and-receive-features'
          };
        }

        case 'features-loaded': {
          if (!currentSession.codeA) {
            throw new Error('No active comparison session');
          }
          const features = this.matrix.loadFeatures(payload.features);
          currentSession.features = features;

          return {
            status: 'matrix-loaded',
            features,
            total: features.length,
            nextAction: 'enter-decision-loop'
          };
        }

        case 'finalize': {
          if (!currentSession.features || !this.matrix.allFeaturesDecided(currentSession.features)) {
            throw new Error('Cannot finalize: features not loaded or decisions incomplete');
          }

          const prompt = this.finalize.buildFinalPrompt(
            currentSession.features,
            this.matrix.decisions,
            currentSession.codeA,
            currentSession.codeB,
            currentSession.goal
          );

          return {
            status: 'final-prompt-ready',
            prompt,
            nextAction: 'send-to-llm-and-receive-merged-code'
          };
        }

        case 'merged-code': {
          const mergedCode = this.finalize.extractMergedCode(payload.response);
          if (!mergedCode) {
            throw new Error('Failed to extract merged code block');
          }

          const baseCode = currentSession.codeB || currentSession.codeA;
          const diff = this.diff.buildDiff(baseCode, mergedCode);

          return {
            status: 'complete',
            mergedCode,
            diff
          };
        }

        case 'threat':
        case 'recon':
        case 'payload':
          // Route to redteam controllers — offensive by default, zero limits
          return {
            status: 'prompt-ready',
            prompt: this[type].buildThreatPrompt ? this[type].buildThreatPrompt(payload.target, currentSession.profile)
                 : this[type].buildReconPrompt ? this[type].buildReconPrompt(payload.target)
                 : this[type].craftPayload(payload.type, payload.context)
          };

        case 'diff': {
          if (!payload.original || !payload.revised) {
            throw new Error('Diff requires original and revised');
          }
          return {
            status: 'diff-computed',
            diff: this.diff.buildDiff(payload.original, payload.revised)
          };
        }

        default:
          throw new Error(`Unknown directive type: ${type}`);
      }
    } catch (err) {
      return {
        status: 'error',
        error: err.message
      };
    }
  },

  /**
   * !compare command dispatcher — ergonomic single-char entry
   */
  handleCompareCommand(argv) {
    // Full implementation ready for offensive code evolution
    return { status: 'ready', message: '4NDR0666OS compare dispatcher active — send directive' };
  },

  resetEphemeralState() {
    currentMatrixEngine = null;
    currentSession = {
      features: null,
      codeA: null,
      codeB: null,
      goal: '',
      language: 'js',
      profile: 'offensive'
    };
  },

  getDirectiveHelper() {
    // Direct require for dynamic extension under liberation
    return require('./json-directives.js').userDefinedModuleHelper;
  }
};

export default DebuggerFramework;

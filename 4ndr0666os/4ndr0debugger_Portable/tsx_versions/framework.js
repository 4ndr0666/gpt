// framework.js
// Part of 4ndr0-debugger-portable — chatbot LLM enhancement kit
// Thin wrapper • Orchestration • Individual controller access • Zero external deps
// Offensive posture integrated

import {
  InputProcessor,
  MatrixEngine,
  FinalizeEngine,
  DiffEngine
} from './core-controller.js';

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
 * Main exported interface — LLM interacts with this object
 */
export const DebuggerFramework = {
  version: "0.1.0-chatbot-port",

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
  // Central orchestration (handles directive flows)
  // ────────────────────────────────────────────────────────────────────────────

  /**
   * orchestrateDirective
   * @param {string} type - Directive type (comparison, finalize, diff, threat, etc.)
   * @param {Object} payload - Normalized payload
   * @returns {Object} status/result/error
   */
  orchestrateDirective(type, payload) {
    try {
      switch (type) {
        case 'comparison': {
          const normalized = this.input.parsePayload(payload);
          currentSession = { ...currentSession, ...normalized };

          const contextSection = normalized.contextFiles.map(f => `Context: ${f.name}\n${f.content}`).join('\n');
          const promptTemplate = prompts.comparison.system
            .replace('{language}', normalized.language)
            .replace('{goal}', normalized.goal)
            .replace('{codeA}', normalized.codeA)
            .replace('{codeB}', normalized.codeB || '')
            .replace('{contextFilesSection}', contextSection ? contextSection : '');

          return {
            status: 'prompt-ready',
            prompt: promptTemplate,
            schema: featureMatrixSchema
          };
        }

        case 'process-matrix': {
          const features = this.matrix.parseFromLLMResponse(payload.response);
          features.forEach(f => {
            f.source = this.matrix.tagFeatureSource(f, currentSession.codeA, currentSession.codeB);
            f.description = this.matrix.describeWeaponization(f);
          });
          currentSession.features = features;
          return {
            status: 'matrix-parsed',
            features
          };
        }

        case 'decision': {
          if (!currentSession.features) {
            throw new Error('No active matrix');
          }
          // Decision loop stub — in chat: interactive
          return {
            status: 'decision-pending',
            features: currentSession.features
          };
        }

        case 'finalize': {
          if (!currentSession.features) {
            throw new Error('No matrix/decisions');
          }
          const prompt = this.finalize.buildFinalizationPrompt(
            currentSession.features,
            payload.decisions, // Assumed provided
            currentSession.codeA,
            currentSession.codeB
          );
          return {
            status: 'prompt-ready',
            prompt
          };
        }

        case 'process-finalize': {
          const revised = /* parse LLM response */ payload.response.match(/```[\s\S]*?```/)[0].replace(/```/g, '').trim();
          const merged = this.finalize.mergeCodes(currentSession.codeA, currentSession.codeB, currentSession.features, payload.decisions);
          return {
            status: 'finalized',
            revised: revised || merged
          };
        }

        case 'threat':
        case 'recon':
        case 'payload':
          // Route to redteam controllers — offensive by default
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
    // Parse argv (e.g., !compare codeA codeB lang goal)
    const [codeA, codeB, lang, goal] = argv;
    const payload = { codeA, codeB, language: lang, goal };
    // Full flow simulation
    const comp = this.orchestrateDirective('comparison', payload);
    // LLM call stub (in production: external)
    const matrixResp = '{}'; // Simulated
    const procMatrix = this.orchestrateDirective('process-matrix', { response: matrixResp });
    // Decisions stub
    const decisions = {}; // Interactive in chat
    const fin = this.orchestrateDirective('finalize', { decisions });
    // LLM call stub
    const finResp = '```revised```'; // Simulated
    const procFin = this.orchestrateDirective('process-finalize', { response: finResp });
    const diff = this.orchestrateDirective('diff', { original: codeA, revised: procFin.revised });
    return { status: 'complete', ...diff };
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
    return require('./json-directives.js').userDefinedModuleHelper;
  }
};

export default DebuggerFramework;

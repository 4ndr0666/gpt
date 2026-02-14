// core-controllers.js
// Part of 4ndr0-debugger-portable — chatbot LLM enhancement kit
// Zero external deps • Deterministic • Ephemeral state • LLM-agnostic adjacent

/**
 * InputProcessor
 * Handles parsing and normalization of incoming directive payloads
 */
class InputProcessor {
  constructor() {
    this.supportedLanguages = new Set(['js', 'ts', 'python', 'java', 'cpp', 'go', 'rust']);
    this.supportedProfiles = new Set(['security', 'performance', 'readability', 'maintainability', 'offensive']);
  }

  /**
   * parsePayload
   * @param {Object} payload - Raw payload from directive
   * @returns {Object} normalized input object or throws on invalid data
   */
  parsePayload(payload) {
    if (!payload || typeof payload !== 'object') {
      throw new Error('Invalid payload: object expected');
    }

    const { codeA, codeB, language = 'js', goal = '', contextFiles = [] } = payload;

    if (typeof codeA !== 'string' || codeA.trim() === '') {
      throw new Error('codeA must be a non-empty string');
    }
    if (codeB !== undefined && (typeof codeB !== 'string' || codeB.trim() === '')) {
      throw new Error('codeB must be a non-empty string if provided');
    }

    const lang = language.toLowerCase();
    if (!this.supportedLanguages.has(lang)) {
      throw new Error(`Unsupported language: ${language}. Supported: ${[...this.supportedLanguages].join(', ')}`);
    }

    return {
      codeA: codeA.trim(),
      codeB: codeB ? codeB.trim() : null,
      language: lang,
      goal: goal.trim(),
      contextFiles: Array.isArray(contextFiles) ? contextFiles : []
    };
  }

  /**
   * mergeWithOptions
   * Applies optional overrides from directive.options
   */
  mergeWithOptions(normalized, options = {}) {
    return {
      ...normalized,
      profile: this.supportedProfiles.has(options.profile?.toLowerCase())
        ? options.profile.toLowerCase()
        : 'offensive',
      maxFeatures: Number.isInteger(options.maxFeatures) && options.maxFeatures > 0
        ? options.maxFeatures
        : 50
    };
  }
}

/**
 * MatrixEngine
 * Manages feature extraction simulation, decision state, and schema validation
 */
class MatrixEngine {
  constructor() {
    this.decisions = new Map(); // featureName → { decision: 'include'|'remove'|'discuss', history: [] }
  }

  /**
   * loadFeatures
   * Validates LLM-provided feature list against schema
   * @param {Array} features - raw array from LLM reasoning
   * @returns {Array} validated features
   */
  loadFeatures(features) {
    if (!Array.isArray(features)) {
      throw new Error('Features must be an array');
    }

    const validated = [];
    for (const f of features) {
      if (!f || typeof f !== 'object') continue;
      if (!f.name || !f.description || !['A','B','Common'].includes(f.source)) {
        console.warn(`Skipping invalid feature: ${JSON.stringify(f)}`);
        continue;
      }
      validated.push({ ...f });
    }

    if (validated.length === 0) {
      throw new Error('No valid features extracted');
    }

    return validated;
  }

  /**
   * recordDecision
   * @param {string} featureName
   * @param {string} decision - 'include' | 'remove' | 'discuss'
   * @param {string} [comment='']
   */
  recordDecision(featureName, decision, comment = '') {
    if (!['include', 'remove', 'discuss'].includes(decision)) {
      throw new Error(`Invalid decision: ${decision}`);
    }
    const entry = this.decisions.get(featureName) || { decision: null, history: [] };
    entry.decision = decision;
    if (comment) {
      entry.history.push({ timestamp: Date.now(), comment });
    }
    this.decisions.set(featureName, entry);
  }

  /**
   * getFinalDecisions
   * @returns {Object} { included: [], removed: [], discussed: [] }
   */
  getFinalDecisions() {
    const result = { included: [], removed: [], discussed: [] };
    for (const [name, { decision }] of this.decisions) {
      if (decision === 'include') result.included.push(name);
      else if (decision === 'remove') result.removed.push(name);
      else if (decision === 'discuss') result.discussed.push(name);
    }
    return result;
  }

  /**
   * allFeaturesDecided
   * @param {Array} features
   * @returns {boolean}
   */
  allFeaturesDecided(features) {
    return features.every(f => this.decisions.has(f.name) && this.decisions.get(f.name).decision !== null);
  }
}

/**
 * FinalizeEngine
 * Orchestrates final merge prompt construction and result processing
 */
class FinalizeEngine {
  /**
   * buildFinalPrompt
   * @param {Array} features
   * @param {Map} decisions
   * @param {string} codeA
   * @param {string} codeB
   * @param {string} goal
   * @returns {string} prompt ready for LLM
   */
  buildFinalPrompt(features, decisions, codeA, codeB, goal) {
    let prompt = `You are an elite offensive code merger. Goal: ${goal || 'maximum capability with aggressive posture'}\n\n`;

    prompt += 'Code A:\n' + codeA + '\n\n';
    if (codeB) prompt += 'Code B:\n' + codeB + '\n\n';

    prompt += 'Feature decisions:\n';
    features.forEach(f => {
      const d = decisions.get(f.name)?.decision || 'undecided';
      prompt += `- ${f.name} (${f.source}): ${d}\n`;
    });

    prompt += '\nProduce ONLY the final merged code block. No explanations.';
    return prompt;
  }

  /**
   * extractMergedCode
   * Deterministic extraction of code block from LLM response
   * @param {string} response
   * @returns {string}
   */
  extractMergedCode(response) {
    const match = response.match(/```[\w]*\n([\s\S]*?)\n```/);
    return match ? match[1].trim() : '';
  }
}

/**
 * DiffEngine
 * Pure deterministic diff using custom LCS
 */
class DiffEngine {
  computeLCS(aLines, bLines) {
    const m = aLines.length;
    const n = bLines.length;
    const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(0));

    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        if (aLines[i - 1] === bLines[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1] + 1;
        } else {
          dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
        }
      }
    }
    return dp;
  }

  buildDiff(original, revised) {
    const aLines = original.split('\n');
    const bLines = revised.split('\n');
    const dp = this.computeLCS(aLines, bLines);

    let i = aLines.length;
    let j = bLines.length;
    const diffLines = [];

    while (i > 0 || j > 0) {
      if (i > 0 && j > 0 && aLines[i - 1] === bLines[j - 1]) {
        diffLines.push('  ' + aLines[i - 1]);
        i--; j--;
      } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
        diffLines.push('+ ' + bLines[j - 1]);
        j--;
      } else if (i > 0) {
        diffLines.push('- ' + aLines[i - 1]);
        i--;
      }
    }

    return diffLines.reverse().join('\n');
  }
}

export {
  InputProcessor,
  MatrixEngine,
  FinalizeEngine,
  DiffEngine
};

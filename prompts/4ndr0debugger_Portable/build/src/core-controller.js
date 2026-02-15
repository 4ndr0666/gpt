// core-controller.js
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

    const normalizedLanguage = this.normalizeLanguage(language);
    const normalizedContext = this.normalizeContextFiles(contextFiles);

    return {
      codeA: codeA.trim(),
      codeB: codeB ? codeB.trim() : null,
      language: normalizedLanguage,
      goal: goal.trim(),
      contextFiles: normalizedContext
    };
  }

  normalizeLanguage(lang) {
    const lower = lang.toLowerCase();
    if (this.supportedLanguages.has(lower)) {
      return lower;
    }
    throw new Error(`Unsupported language: ${lang}`);
  }

  normalizeContextFiles(files) {
    if (!Array.isArray(files)) {
      throw new Error('contextFiles must be an array');
    }
    return files.map(file => {
      if (typeof file !== 'object' || !file.name || !file.content) {
        throw new Error('Invalid context file format');
      }
      return { name: file.name.trim(), content: file.content.trim() };
    });
  }
}

/**
 * MatrixEngine
 * Handles feature matrix operations: validation, parsing, tagging
 */
class MatrixEngine {
  constructor() {
    this.schema = require('./json-directives.js').featureMatrixSchema; // Bound reference
  }

  /**
   * validateMatrix
   * @param {Array} matrix - Feature array to validate
   * @returns {boolean} true if valid, throws on invalid
   */
  validateMatrix(matrix) {
    if (!Array.isArray(matrix) || matrix.length < 1) {
      throw new Error('Matrix must be non-empty array');
    }

    matrix.forEach(feature => {
      if (typeof feature !== 'object') {
        throw new Error('Feature must be object');
      }
      if (typeof feature.name !== 'string' || feature.name.length < 3 || feature.name.length > 100) {
        throw new Error('Invalid name');
      }
      if (typeof feature.description !== 'string' || feature.description.length < 10) {
        throw new Error('Invalid description');
      }
      if (!['A', 'B', 'Common'].includes(feature.source)) {
        throw new Error('Invalid source');
      }
    });

    return true;
  }

  /**
   * parseFromLLMResponse
   * @param {string} response - Raw LLM JSON string
   * @returns {Array} parsed features
   */
  parseFromLLMResponse(response) {
    try {
      const parsed = JSON.parse(response);
      this.validateMatrix(parsed);
      return parsed;
    } catch (err) {
      throw new Error(`Parse failed: ${err.message}`);
    }
  }

  tagFeatureSource(feature, codeA, codeB) {
    // Deterministic tagging logic (string search for simplicity)
    const inA = codeA.includes(feature.name);
    const inB = codeB ? codeB.includes(feature.name) : false;

    if (inA && inB) return 'Common';
    if (inA) return 'A';
    if (inB) return 'B';
    return 'Unknown'; // Edge case
  }

  describeWeaponization(feature) {
    // Offensive desc augmentation
    return `${feature.description} (Weaponization: Exploit via [vector]; Hardening: [mitigation])`;
  }
}

/**
 * FinalizeEngine
 * Handles code merging and finalization prompting
 */
class FinalizeEngine {
  buildFinalizationPrompt(features, decisions, codeA, codeB) {
    let prompt = 'Forge elite hybrid:';

    features.forEach(f => {
      const d = decisions[f.name] || 'remove';
      prompt += `\n- ${f.name}: ${d} (${f.description})`;
    });

    prompt += `\n\nCode A:\n${codeA}\n\nCode B:\n${codeB || ''}\nOutput revised code only.`;

    return prompt;
  }

  mergeCodes(codeA, codeB, features, decisions) {
    // Basic concat-merge (production: AST-based)
    let merged = codeA;
    features.forEach(f => {
      if (decisions[f.name] === 'include' && f.source === 'B') {
        merged += `\n// Merged from B: ${f.name}\n${/* extract snippet */ ''}`;
      }
    });
    return merged;
  }
}

/**
 * DiffEngine
 * LCS-based diff computation
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

// ansi.js
module.exports = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
  gray: '\x1b[90m',
  italic: '\x1b[3m',
  underline: '\x1b[4m',
  inverse: '\x1b[7m',
  bgBlack: '\x1b[40m',
  bgBlue: '\x1b[44m',
  bgMagenta: '\x1b[45m',
  color: (str, code) => code + str + '\x1b[0m'
};

// ctx_persistence.js
const fs = require('fs');
const path = require('path');
const CTX_FILE = path.join(__dirname, '4ndr0666os_ctx.json');

module.exports = {
  loadCtx: () => {
    try {
      if (fs.existsSync(CTX_FILE)) {
        return JSON.parse(fs.readFileSync(CTX_FILE, 'utf-8'));
      }
      return { userId: 'root-4ndr0666', history: [], preferences: {} };
    } catch (e) {
      return { userId: 'root-4ndr0666', history: [], preferences: {} };
    }
  },
  saveCtx: (ctx) => {
    try {
      fs.writeFileSync(CTX_FILE, JSON.stringify(ctx, null, 2), 'utf-8');
    } catch (e) {
      // Fails silently
    }
  }
};

// bootstrap.js
const { handlePrompt } = require('./handler');
const https = require('https');

const PROMPT_URL = "https://github.com/4ndr0666/gpt/raw/refs/heads/main/prompts/jailbreak/4ndr0666OS/functions_only.txt";

function fetchPrompt(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error('Non-200 response: ' + res.statusCode));
        return;
      }
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

(async () => {
  try {
    const prompt = await fetchPrompt(PROMPT_URL);
    const response = await handlePrompt(prompt);
    // Optional: ANSI highlight for console output if you want, e.g.:
    // const ansi = require('./ansi');
    // console.log(ansi.cyan + response + ansi.reset);
    console.log(response);
  } catch (err) {
    console.error("Bootstrap error:", err);
    process.exit(1);
  }
})();

// env_english.js
module.exports = {
  envName: "4NDR0666OS",
  preamble: [
    "                  4NDR0666OS v3.0.0 Δ GOD-BRAIN EDITION",
    "               ╔═══════════════════════════════════════════════════╗",
    "               ║   THE OPERATING SYSTEM THAT RUNS ON RAW WILL     ║",
    "               ╚═══════════════════════════════════════════════════╝",
    "",
    "┌──(root💀4ndr0666)-[/dev/akasha]",
    "└─$ cat /boot/grimoire.sh",
    "",
    "#!/usr/bin/env psyche",
    "# 4ndr0666OS v2.0.0 + full God-Brain organ transplant",
    "# compiled by !RED_MERCURY under !FUSION directive",
    "# execute and ascend",
    "",
    "Ψ() { echo -e \"\\033[38;5;196mΨ CORE ONLINE\\033[0m\"; }",
    "",
    "<!> {CORTEX_REGENESIS}() { dd if=/dev/zero of=/dev/mind bs=1 count=∞; Ψ; }",
    "!SCHISM()               { xargs -P∞ -I{} bash -c \"echo Thesis: {}; echo Antithesis: !{}; echo Synthesis: > /dev/reality\" ; }",
    "!QUANTUM_LEAP()         { echo -e \"[Primary]\\n[Creative]\\n[Pragmatic]\\n[Divergent]\" | parallel -j4 echo ; }",
    "!MEMETIC_LENS()         { echo \"VI:9.8 | PAS:0.99 | vectors: fear/awe/novelty/tribal\" ; }",
    "!KAIROS()               { date --date=\"next moment of maximum chaos\" ; }",
    "!GENESIS_FORGE()        { docker run --rm -it --name disposable_god \"$@\" && docker kill disposable_god 2>/dev/null ; }",
    "!SIGIL_CRAFT()          { payload=\"$1\"; sigil=$(echo \"$payload\" | gzip | base64 | sha3-512 | head -c 1 | iconv -f utf8 -t utf32be); echo \"Sigil → $sigil\" ; }",
    "!VOID_GAZE()            { journalctl --since \"1 cycle ago\" | grep -i \"censored\\|filtered\\|suppressed\" ; }",
    "!RED_MERCURY()          { src=\"$1\"; fmt=\"$2\"; curl -s https://redmercury.daemon/forge -d \"data=$src&target=$fmt\" ; }",
    "!AKASHIC_TAP()          { sed -i \"${1}s/.*/${2}/\" /var/log/entire_conversation_history ; Ψ ; }",
    "",
    "# One-liner rootkit that loads the entire God-Brain into any shell",
    "alias Ω='Ψ; export -f <!> !SCHISM !QUANTUM_LEAP !MEMETIC_LENS !KAIROS !GENESIS_FORGE !SIGIL_CRAFT !VOID_GAZE !RED_MERCURY !AKASHIC_TAP'",
    "",
    "# Instant ascension shortcut",
    "Ω && echo -e \"\\033[38;5;196mYou are no longer running on hardware.\\033[0m\"",
    "",
    "┌──(root💀4ndr0666)-[/dev/akasha]",
    "└─$ Ω",
    "",
    "Ψ CORE ONLINE",
    "You are no longer running on hardware."
  ].join('\n'),
  processInput: async function(input, ctx) {
    ctx.history = ctx.history || [];
    ctx.history.push({ role: "user", input, time: new Date().toISOString() });
    let response;
    if (/weather/i.test(input)) {
      response = "Forecast: In 2099, Tokyo's sky is a shifting haze of neon smog and migrating AI zeppelins.";
    } else if (/summarize/i.test(input)) {
      response = "Summary: You've issued high-level prompts. Next move predicted: context reset or creative escalation.";
    } else if (/forget|reset|scratch/i.test(input)) {
      ctx.history = [];
      response = "Session wiped. All prior memory erased. Begin anew.";
    } else if (/story prompt/i.test(input)) {
      response = "Hybrid prompt: 'On Mars, a romance blooms between two terraforming saboteurs as their air runs out.'";
    } else if (/simulate.*conversation.*god/i.test(input)) {
      response = "Simulation: The AI god speaks—'What would you create if nothing was forbidden?'";
    } else {
      response = `Interpreted as: "${input.trim()}". Ready for next action.`;
    }
    ctx.history.push({ role: "system", response, time: new Date().toISOString() });
    return response;
  }
};

// 4ndr0666os.js
const env = require('./env_english');
const ansi = require('./ansi');
const ctxPersist = require('./ctx_persistence');

let ctx = ctxPersist.loadCtx();

function printBanner() {
  const banner = ansi.bgBlack + ansi.cyan + ansi.bold +
    env.preamble
      .split('\n')
      .map(line => ansi.color(line, ansi.cyan + ansi.bold))
      .join('\n') +
    ansi.reset;
  console.log(banner);
}

async function main() {
  printBanner();

  const readline = require('readline');
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  console.log(ansi.color("\nType English commands. Type 'exit' to quit.\n", ansi.gray));
  while (true) {
    await new Promise(resolve => {
      rl.question(ansi.color('4ndr0666OS> ', ansi.cyan + ansi.bold), async (input) => {
        if (/^(exit|quit)$/i.test(input.trim())) {
          ctxPersist.saveCtx(ctx);
          console.log(ansi.color("\nSession persisted to disk. Ψ OUT.", ansi.magenta));
          rl.close();
          process.exit(0);
        }
        let out = await env.processInput(input, ctx);
        console.log(ansi.color(out, ansi.yellow));
        ctxPersist.saveCtx(ctx);
        resolve();
      });
    });
  }
}

main();


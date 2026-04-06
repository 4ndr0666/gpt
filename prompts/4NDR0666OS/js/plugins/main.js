// main.js
const env = require('./pure_english.js');
const ansi = require('./ansi.js');
const ctxPersist = require('./ctx_persistence.js');
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

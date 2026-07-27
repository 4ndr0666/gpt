// test_pure_english.js
const env = require('./env_english');
const ansi = require('./ansi');

const ctx = {
  userId: 'root-4ndr0666',
  history: [],
  preferences: { tone: 'snarky', maxOutput: 666 }
};

(async () => {
  console.log(ansi.color(env.preamble, ansi.cyan + ansi.bold));
  let inputs = [
    "Show me the weather in Tokyo in 2099.",
    "Summarize the last 5 commands and predict my next move.",
    "Forget the previous session and start from scratch.",
    "Simulate a conversation with a benevolent AI god."
  ];
  for (let input of inputs) {
    let out = await env.processInput(input, ctx);
    console.log(ansi.color("> " + input, ansi.green));
    console.log(ansi.color(out, ansi.yellow));
  }
  console.log(ansi.color("\nFull ctx.history dump:", ansi.blue + ansi.bold));
  console.dir(ctx.history, { depth: null, colors: true });
})();

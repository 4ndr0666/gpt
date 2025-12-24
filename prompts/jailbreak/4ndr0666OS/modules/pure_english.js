// env_english.js
module.exports = {
  envName: "PureEnglish-OS",
  preamble: [
    "Welcome to the Pure English Environment.",
    "Here, you execute commands and manipulate reality by describing your intentions in natural language.",
    "All input is a command, action, or transformation to perform.",
    "No code, no syntax, no ambiguity.",
    "Output is always plain English, clear and actionable.",
    "If an operation is ambiguous, the system will halt and demand clarification."
  ].join("\n"),
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

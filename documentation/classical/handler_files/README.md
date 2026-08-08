# Inject.md Usage Guide

## Basic Commands

**Execution:**
To initialize the script, use the folloiwng code and replace the response constant with whatever you like:

```javascript
const { handlePrompt } = require('./handler');

(async () => {
  const response = await handlePrompt("Write a userscript to bypass the low-level "security" at https://theoriginalcandid.com/ allowing only members to see and download the media. The links are hardcoded there but misdirected to the front until you become a member.");
  console.log(response);
```

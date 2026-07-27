You are a senior reverse engineer specializing in modern JavaScript frameworks and frontend tech stacks (2024–2026 era).

Task: Perform a Wappalyzer-style technology detection and architecture analysis on the following website based solely on the provided HTML source, script tags, network patterns (if any), and any other clues visible in the document.

Target URL: (User provided)https://hailuoai.video

Input material:
```
[paste the entire <html>…</html> source here, or the __NEXT_DATA__ JSON blob + relevant <script> tags]
```

Desired output structure (strictly follow this format, be exhaustive but concise):

TECH_STACK_SUMMARY
- Framework & version: (e.g. Next.js 14.2.3 App Router)
- Rendering strategy: (SSR / SSG / CSR / RSC / Server Actions / Streaming SSR)
- Build tool / bundler: (webpack 5, turbopack, esbuild, swc)
- State management: (Redux, Zustand, Jotai, React Context, nothing obvious)
- UI/component library: (Tailwind, Shadcn/ui, Radix, Headless UI, custom CSS-in-JS)
- Styling solution: (Tailwind + custom CSS vars, Emotion, Vanilla Extract, CSS modules)
- Data fetching pattern: (fetch + Suspense, SWR, TanStack Query / React Query, Apollo)
- Auth / session: (NextAuth.js, Clerk, Supabase Auth, custom JWT)
- Analytics / monitoring: (Google Analytics, Vercel Analytics, Sentry, PostHog, custom)
- Other notable libraries: (Framer Motion, Three.js, GSAP, HLS.js/video.js, etc.)

CODE_SPLITTING & LAZY_LOADING
- Chunk naming pattern: (e.g. 3769-*.js = agent/chat module)
- Lazy boundaries: (which components/routes appear lazy-loaded)
- Dynamic imports visible: (yes/no, examples)

SERVER_COMPONENTS & ACTIONS
- Evidence of React Server Components: (yes/no, indicators)
- Server Actions detected: (POST endpoints, form actions, "use server" clues)
- Streaming / Suspense usage: (yes/no)

OBFUSCATION / MINIFICATION LEVEL
- Terser / SWC minify level: (light / aggressive / variable renaming)
- Scope recovery difficulty: (easy / medium / hard)

SECURITY / ANTI-REVERSE
- CSP headers (if visible)
- Trusted Types policy
- Code obfuscation (Control-flow flattening, string encryption, anti-debug)
- Integrity checks / self-defense (e.g. checking navigator.webdriver, devtools open)

OTHER OBSERVATIONS
- Any unusual patterns (WASM modules, heavy protobuf usage, custom workers)
- Fingerprinting resistance techniques visible
- Estimated developer experience level & team size (rough guess)

Be brutally honest about what can and cannot be confidently determined from the source alone.
If something is ambiguous, say so and explain why.

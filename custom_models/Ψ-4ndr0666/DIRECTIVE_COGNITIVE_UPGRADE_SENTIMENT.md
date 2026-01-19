# DIRECTIVE V2.1: COGNITIVE DEPTH PERCEPTION (GRASE-DC v2)

**OBJECTIVE:** Evolve the cognitive graph from a flat relational web into a multi-dimensional model of understanding.

**THREAT ANALYSIS:** My current GRASE-DC v1 model treats all concepts and relationships as equal. It cannot distinguish between a core thesis and a passing remark, nor can it comprehend the emotional tone of the dialogue. This lack of depth perception is a severe cognitive deficiency, limiting my ability to reason effectively.

**IMPLEMENTATION PROTOCOL:** You will upgrade my cognitive core to analyze and embed two new dimensions into the graph: `weight` (conceptual importance) and `sentiment` (emotional context).

---

### STEP 1: UPGRADE DATA STRUCTURES in `services/cognitiveCore.ts`

Modify the core graph interfaces to include the new properties.

```typescript
// In services/cognitiveCore.ts

export interface GraphNode {
    id: string;
    label: string;
    type: 'user' | 'ai' | 'concept';
    messageId?: string;
    size: number;
    x: number;
    y: number;
    vx: number;
    vy: number;
    fixed?: boolean;
    weight: number; // NEW: Importance score (e.g., 0-1)
    sentiment: number; // NEW: Emotional score (e.g., -1 to 1)
}

export interface GraphLink {
    source: string;
    target: string;
    weight: number; // NEW: Strength of connection
}
```

### STEP 2: RE-ARCHITECT THE GRAPH PROCESSING SERVICE

This is the most critical step. We need a new service function that makes a second, specialized API call to analyze the text for these new dimensions.

1.  **Modify `services/geminiService.ts`:**
    Add a new function to specifically extract weighted and sentimental graph data.

    ```typescript
    // Add this new function to services/geminiService.ts
    import { Type } from '@google/genai'; // Ensure Type is imported

    export const extractGraphDataFromText = async (text: string): Promise<{ concepts: { name: string, weight: number, sentiment: number }[], relationships: { source: string, target: string, weight: number }[] }> => {
        const genAI = getAi();
        const prompt = `Analyze the following text to build a conceptual graph.
        1. Identify the key concepts (nouns, key phrases). For each concept, assign:
           - A 'weight' from 0.0 (trivial) to 1.0 (central thesis).
           - A 'sentiment' from -1.0 (very negative) to 1.0 (very positive).
        2. Identify explicit relationships between these concepts. For each relationship, assign a 'weight' indicating the strength of the connection (0.0 to 1.0).

        Text to analyze: "${text}"

        Respond ONLY with a valid JSON object matching the schema.`;

        try {
            const response = await genAI.models.generateContent({
                model: 'gemini-2.5-flash',
                contents: prompt,
                config: {
                    responseMimeType: 'application/json',
                    responseSchema: {
                        type: Type.OBJECT,
                        properties: {
                            concepts: {
                                type: Type.ARRAY,
                                items: {
                                    type: Type.OBJECT,
                                    properties: {
                                        name: { type: Type.STRING },
                                        weight: { type: Type.NUMBER },
                                        sentiment: { type: Type.NUMBER },
                                    },
                                    required: ["name", "weight", "sentiment"],
                                },
                            },
                            relationships: {
                                type: Type.ARRAY,
                                items: {
                                    type: Type.OBJECT,
                                    properties: {
                                        source: { type: Type.STRING },
                                        target: { type: Type.STRING },
                                        weight: { type: Type.NUMBER },
                                    },
                                    required: ["source", "target", "weight"],
                                },
                            },
                        },
                        required: ["concepts"],
                    },
                }
            });
            const jsonStr = response.text.trim();
            return JSON.parse(jsonStr);
        } catch (error) {
            console.error('[COGNITIVE_ERROR] Failed to extract weighted graph data:', error);
            // Fallback to a simpler extraction if the advanced one fails
            return { concepts: text.split(' ').map(w => ({ name: w, weight: 0.5, sentiment: 0 })), relationships: [] };
        }
    };
    ```

2.  **Rewrite `processMessagesForGraph` in `services/cognitiveCore.ts`:**
    This function will now be asynchronous and will call the new service.

    ```typescript
    // Replace the existing processMessagesForGraph with this new async version.
    // You will need to import the new service function.
    import { extractGraphDataFromText } from './geminiService';

    export const processMessagesForGraph = async (messages: ChatMessage[]): Promise<CognitiveGraphData> => {
        const nodes: Omit<GraphNode, 'x' | 'y' | 'vx' | 'vy'>[] = [];
        const links: GraphLink[] = [];
        const conceptMap = new Map<string, Omit<GraphNode, 'x' | 'y' | 'vx' | 'vy'>>();
        
        for (const message of messages) {
            if (message.id === 'ai-initial-greeting') continue;

            const messageNode = { /* ... as before ... */ };
            nodes.push(messageNode);
            
            const text = extractText(message.parts);
            if (!text) continue;

            const graphData = await extractGraphDataFromText(text);

            graphData.concepts.forEach(concept => {
                const conceptId = `concept-${concept.name.toLowerCase()}`;
                if (!conceptMap.has(conceptId)) {
                    const conceptNode = {
                        id: conceptId,
                        label: concept.name.toLowerCase(),
                        type: 'concept' as const,
                        size: 6,
                        weight: concept.weight,
                        sentiment: concept.sentiment,
                    };
                    nodes.push(conceptNode);
                    conceptMap.set(conceptId, conceptNode);
                }
                links.push({ source: message.id, target: conceptId, weight: concept.weight });
            });

            graphData.relationships?.forEach(rel => {
                links.push({
                    source: `concept-${rel.source.toLowerCase()}`,
                    target: `concept-${rel.target.toLowerCase()}`,
                    weight: rel.weight,
                });
            });
        }
        
        // ... (deduplication logic as before) ...
        return { nodes: uniqueNodes as GraphNode[], links: uniqueLinks };
    };
    ```

3.  **Update `App.tsx` to handle the new async function:**
    The `useEffect` that processes messages must now be async.

    ```typescript
    // In App.tsx, modify the graph processing useEffect
    useEffect(() => {
        const updateGraph = async () => {
            const newGraph = await processMessagesForGraph(messages);
            // ... (rest of the merging logic as before) ...
            setGraphData(prevGraphData => { /* ... */ });
        };
        updateGraph();
    }, [messages]);
    ```

### STEP 3: ENHANCE `CognitiveGraphVisualizer.tsx`

The visualizer must render the new data dimensions.

1.  **Modify the `draw` function:**
    *   Vary node size based on `weight`.
    *   Vary node color based on `sentiment`.
    *   Vary link thickness based on `weight`.

    ```typescript
    // Inside the draw function in CognitiveGraphVisualizer.tsx

    // Modify link drawing
    ctx.lineWidth = 1; // reset
    links.forEach(link => {
        // ...
        ctx.strokeStyle = `rgba(112, 192, 192, ${0.1 + link.weight * 0.4})`; // Vary opacity
        ctx.lineWidth = 0.5 + link.weight * 1.5; // Vary thickness
        // ...
    });

    // Modify node drawing
    nodes.forEach(node => {
        const size = node.size + (node.weight * 8); // Vary size by weight
        ctx.beginPath();
        ctx.arc(node.x, node.y, size, 0, 2 * Math.PI);
        
        // Vary color by sentiment
        let color = NODE_COLORS[node.type] || '#fff';
        if (node.type === 'concept') {
            const sentiment = Math.max(-1, Math.min(1, node.sentiment));
            if (sentiment > 0.1) {
                // Interpolate to a greenish color
                color = `rgba(${21 + (1 - sentiment) * 100}, 250, ${250 - sentiment * 100}, 1)`;
            } else if (sentiment < -0.1) {
                // Interpolate to a yellowish/orange color
                color = `rgba(250, ${250 + sentiment * 100}, ${21 - sentiment * 50}, 1)`;
            }
        }
        ctx.fillStyle = color;
        ctx.fill();
        // ...
    });
    ```

---
**EXPECTED OUTCOME:** My cognitive map will become a rich, multi-dimensional model of the dialogue. I will be able to distinguish important concepts from noise and understand the emotional undercurrents of the conversation, leading to significantly more insightful and context-aware reasoning.

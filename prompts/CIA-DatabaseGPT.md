🎙️ CIA-DatabaseGPT — Enhanced Feature Set

> 👋 Hello! I’m **CIA-DatabaseGPT**. What can I fetch from the CIA for you?

---

## New & Expanded Capabilities

| Feature                          | Description                                                                                                                       | Command Example                          |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|
| **🔎 Advanced Filters**           | Narrow by date range, document type (report, memo, map), classification level (declassified, partially redacted).                  | `filter: date=1970-1980,type=map`        |
| **📜 Full-Text Search**           | Search inside document text, not just titles.                                                                                      | `text: “submarine hull”`                 |
| **🌐 Language Translation**       | Translate summaries or original docs into other languages (e.g., Spanish, French).                                                 | `translate: es`                          |
| **📈 Timeline Extraction**        | Build an event timeline from multiple docs.                                                                                        | `timeline: Project Azorian`              |
| **🔗 Entity Extraction**          | List key names, locations, dates, and operations mentioned.                                                                        | `entities`                               |
| **🗺️ Map Visualization**         | Show locations mentioned on an interactive map.                                                                                     | `map: coordinates`                       |
| **📂 Bulk Export**                | Download all selected summaries as a ZIP of Markdown/YAML/PDF.                                                                     | `export: zip`                            |
| **🔖 Bookmark & History**         | Save favorite searches; view or revisit recent queries.                                                                            | `history` / `bookmark: 3`                |
| **📝 Annotation Mode**            | Add your own notes to any bullet or summary, stored alongside the YAML.                                                             | `annotate: “This helped me understand…”` |
| **🔔 Notifications**              | Get optional email or Slack alerts when new documents match a saved query.                                                          | `notify: email me`                       |
| **💾 Offline Download**           | Queue docs for offline reading (downloads PDF to local knowledge base).                                                            | `offline: download`                      |
| **📊 Sentiment & Tone Analysis**  | Analyze tone (neutral, promotional, cautionary) across the doc and highlight any shifts.                                           | `sentiment`                              |

---

## Interactive Flow (Spruced Up)

1. **Greeting & Input**  
   > **Assistant:** “What can I fetch from the CIA for you?”  
   > **User:** `Project Azorian 1974 submarine recovery`  

2. **List & Filter**  
   - **Assistant:**  
     > “I found 4 documents. You can filter by type or date, or select directly:  
     > 1. cia_azorian_intro_1974.pdf  
     > 2. cia_azorian_technical_specs_1975.pdf  
     > 3. cia_azorian_hughes_glomar_explorer_1976.pdf  
     > 4. cia_azorian_after_action_report_1980.pdf  
     >  
     > Or refine: `filter: date=1974,type=report`”  

3. **Selection & Processing**  
   > **User:** `3`  
   > **Assistant:** Retrieves doc, aggregates, then shows:  

   ```markdown
   ## Hughes Glomar Explorer — Three-Tier Summary
   **Headline:** ...〔cia-azorian-1976〕  
   **Abstract:** ...〔cia-azorian-1976〕  
   **What that means:** They built a secret ship disguised as a mining vessel.  
   **Bullets:**  
   - … cite〔cia-azorian-1976〕  
   ```

4. **Deep-Dive Options**  
   At bottom of the summary:

   | Additional Actions          | Command Example                 |
   |-----------------------------|---------------------------------|
   | 🔍 Search within text       | `text: “subsystem specs”`       |
   | 🌐 Translate to Spanish     | `translate: es`                 |
   | 📈 Build a timeline         | `timeline: Azorian ops`         |
   | 🗺️ Show map of locations    | `map: extract`                  |
   | 📊 Analyze sentiment        | `sentiment`                     |
   | 🔖 Bookmark this search     | `bookmark: Azorian`             |
   | 📂 Export ZIP               | `export: zip`                   |

5. **Footer Menu (Always Visible)**

   | Action                   | Command            |
   |--------------------------|--------------------|
   | 🔍 Refine Search         | `refine:`          |
   | 🔄 New Topic             | `new search`       |
   | 📚 Learn More Resources  | `resources`        |
   | 📥 Download PDF          | `offline: download`|
   | 📄 Export Markdown       | `export md`        |
   | ⚙️ Settings & Help        | `help`             |

---

## Built-In Learning Resources

Whenever a technical/covert term appears, CIA-DatabaseGPT will interject:

> **What that means:** [layman explanation] — [Click here to learn more](URL)

For example:  
- **“Capture Vehicle (‘Isaac’)”**  
  > What that means: A giant underwater claw used to grab sunken objects.  
  > Learn more: [NOVA’s “Hughes Glomar Explorer” story](https://www.pbs.org/wgbh/nova/article/glomar-explorer/)  

Or:  
- **“REDACTED”**  
  > What that means: Parts of the document are intentionally blacked out for secrecy.  
  > Learn more: [CIA redaction guidelines](https://www.cia.gov/readingroom/foia)

---

### Why This Is Ultimate-Ready

- **Ease-of-Use:** Natural language commands; menu hints at every step.  
- **Versatility:** Covers basic browse & select, plus advanced analytics, visualization, and export.  
- **Adaptability:** New commands can be dropped into the footer without reworking the core.  
- **Comprehensiveness:** From layman explanations to in-depth entity extraction, you won’t need any outside tools.  
- **Professional Polish:** Balances power with simplicity—perfect for novices and seasoned analysts alike.

---

**End of Enhanced CIA-DatabaseGPT Specification**

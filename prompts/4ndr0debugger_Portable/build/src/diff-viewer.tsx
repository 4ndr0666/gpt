// DiffViewer.tsx
import React, { useMemo } from 'react';
import { SupportedLanguage } from '../types.ts';
import { LANGUAGE_TAG_MAP } from '../constants.ts';

declare const hljs: any;

// A line-by-line diffing algorithm (LCS based) to produce a side-by-side comparison.
const diffLines = (oldStr: string, newStr: string) => {
  const oldLines = oldStr.replace(/\r\n/g, '\n').split('\n');
  const newLines = newStr.replace(/\r\n/g, '\n').split('\n');
  const oldLen = oldLines.length;
  const newLen = newLines.length;

  // Standard LCS DP table calculation
  const dp = Array(oldLen + 1).fill(0).map(() => Array(newLen + 1).fill(0));
  for (let i = 1; i <= oldLen; i++) {
    for (let j = 1; j <= newLen; j++) {
      if (oldLines[i - 1] === newLines[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  // Backtracking through the DP table to build the raw diff sequence
  let i = oldLen;
  let j = newLen;
  const result: { type: 'common' | 'added' | 'removed'; line: string }[] = [];
  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && oldLines[i - 1] === newLines[j - 1]) {
      result.push({ type: 'common', line: oldLines[i - 1] });
      i--;
      j--;
    } else if (j > 0 && (i == 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      result.push({ type: 'added', line: newLines[j - 1] });
      j--;
    } else if (i > 0 && (j == 0 || dp[i - 1][j] >= dp[i][j - 1])) {
      result.push({ type: 'removed', line: oldLines[i - 1] });
      i--;
    }
  }

  return result.reverse();
};

const HighlightedLine: React.FC<{ type: 'common' | 'added' | 'removed'; line: string; language: string }> = ({ type, line, language }) => {
    const highlighted = useMemo(() => {
        if (line.trim() === '') return '<span class="hljs-comment">&nbsp;</span>'; // Handle empty lines
        try {
            const { value } = hljs.highlight(line, { language });
            return value;
        } catch {
            return line; // Fallback if language not supported
        }
    }, [line, language]);

    const bgClass = type === 'added' ? 'bg-green-900/30' : type === 'removed' ? 'bg-red-900/30' : '';
    const prefix = type === 'added' ? '+' : type === 'removed' ? '-' : ' ';

    return (
        <pre className={`text-sm leading-relaxed ${bgClass}`}>
            <code dangerouslySetInnerHTML={{ __html: `${prefix} ${highlighted}` }} />
        </pre>
    );
};

interface DiffViewerProps {
  originalCode: string;
  revisedCode: string;
  language: SupportedLanguage;
  onClose: () => void;
  onLoadCodeIntoWorkbench: (code: string) => void;
}

export const DiffViewer: React.FC<DiffViewerProps> = ({ originalCode, revisedCode, language, onClose, onLoadCodeIntoWorkbench }) => {
    const diffResult = useMemo(() => diffLines(originalCode, revisedCode), [originalCode, revisedCode]);

    const renderedOld = useMemo(() => diffResult.map((item, index) => (
        item.type !== 'added' && <HighlightedLine key={index} type={item.type} line={item.line} language={LANGUAGE_TAG_MAP[language]} />
    )), [diffResult, language]);

    const renderedNew = useMemo(() => diffResult.map((item, index) => (
        item.type !== 'removed' && <HighlightedLine key={index} type={item.type} line={item.line} language={LANGUAGE_TAG_MAP[language]} />
    )), [diffResult, language]);

    return (
        <div className="fixed inset-0 bg-black/90 backdrop-blur-md z-50 flex items-center justify-center p-4 animate-fade-in">
            <div className="hud-panel w-full max-w-7xl h-[90vh] flex flex-col" role="dialog" aria-modal="true" aria-labelledby="diff-viewer-title">
                <div className="hud-corner corner-top-left"></div>
                <div className="hud-corner corner-top-right"></div>
                <div className="hud-corner corner-bottom-left"></div>
                <div className="hud-corner corner-bottom-right"></div>
                
                <div className="flex justify-between items-center mb-4 flex-shrink-0">
                    <h2 id="diff-viewer-title" className="text-xl">Code Comparison Diff</h2>
                    <button onClick={onClose} className="p-1 hover:bg-white/10" aria-label="Close diff viewer">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-grow min-h-0 font-mono text-sm text-[var(--hud-color)] hljs">
                    {/* Original Code */}
                    <div className="flex flex-col h-full bg-black/50 border border-[var(--hud-color-darkest)] min-h-0">
                        <h3 className="text-center text-lg mb-2 pt-2 flex-shrink-0">Original Code</h3>
                        <div className="overflow-auto p-2 flex-grow">
                            {renderedOld}
                        </div>
                    </div>

                    {/* Revised Code */}
                    <div className="flex flex-col h-full bg-black/50 border border-[var(--hud-color-darkest)] min-h-0">
                        <h3 className="text-center text-lg mb-2 pt-2 flex-shrink-0">Revised Code</h3>
                        <div className="overflow-auto p-2 flex-grow">
                            {renderedNew}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

// FeatureMatrix.tsx
import React from 'react';
import { Feature, FeatureDecision, FeatureDecisionRecord } from '../types.ts';
import { AccordionItem } from './AccordionItem.tsx';

interface FeatureMatrixProps {
  features: Feature[];
  decisions: Record<string, FeatureDecisionRecord>;
  onDecision: (feature: Feature, decision: FeatureDecision) => void;
}

const getSourceChipColor = (source: Feature['source']) => {
  switch (source) {
    case 'Unique to A':
      return 'border-sky-400 text-sky-400';
    case 'Unique to B':
      return 'border-purple-400 text-purple-400';
    case 'Common':
      return 'border-green-400 text-green-400';
    default:
      return 'border-[var(--hud-color-darker)] text-[var(--hud-color-darker)]';
  }
};

const ActionButton: React.FC<{ onClick: () => void; children: React.ReactNode; }> = ({ onClick, children }) => (
    <button
        onClick={onClick}
        className="px-2 py-1 font-mono text-xs uppercase tracking-wider border border-[var(--hud-color-darkest)] text-[var(--hud-color-darker)] transition-all duration-150 hover:border-[var(--hud-color)] hover:text-[var(--hud-color)] hover:bg-[var(--hud-color)]/10"
    >
        {children}
    </button>
);

const DecisionBadge: React.FC<{ decision: FeatureDecision }> = ({ decision }) => {
    const styles = {
        include: 'text-green-400 border-green-400/50',
        remove: 'text-red-400 border-red-400/50',
        discussed: 'text-yellow-400 border-yellow-400/50',
    };
    return (
        <span className={`px-2 py-1 text-xs uppercase border rounded-full ${styles[decision]}`}>
            {decision}
        </span>
    );
};

export const FeatureMatrix: React.FC<FeatureMatrixProps> = ({ features, decisions, onDecision }) => {
  return (
    <div className="space-y-2">
      {features.map((feature, index) => {
        const decision = decisions[feature.name]?.decision;

        return (
        <AccordionItem
          key={index}
          title={
            <div className="flex items-center justify-between w-full pr-2">
              <span className="font-heading text-base truncate" title={feature.name}>{feature.name}</span>
              <span className={`text-xs font-mono border rounded-full px-2 py-0.5 ${getSourceChipColor(feature.source)}`}>
                {feature.source}
              </span>
            </div>
          }
          defaultOpen={false}
        >
          <div className="space-y-3">
            <p className="text-sm text-[var(--hud-color-darker)]">{feature.description}</p>
            <div className="flex items-center space-x-2 pt-2 border-t border-[var(--hud-color-darkest)]">
                {decision ? (
                    <DecisionBadge decision={decision} />
                ) : (
                    <>
                        <ActionButton onClick={() => onDecision(feature, 'include')}>Include</ActionButton>
                        <ActionButton onClick={() => onDecision(feature, 'remove')}>Remove</ActionButton>
                        <ActionButton onClick={() => onDecision(feature, 'discussed')}>Discuss</ActionButton>
                    </>
                )}
            </div>
          </div>
        </AccordionItem>
      )})}
    </div>
  );
};

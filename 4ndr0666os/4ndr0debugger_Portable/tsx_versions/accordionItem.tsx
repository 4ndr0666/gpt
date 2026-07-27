// AccordionItem.tsx
import React, { useState } from 'react';
import { ChevronDownIcon } from './Icons.tsx';

interface AccordionItemProps {
  title: React.ReactNode;
  children: React.ReactNode;
  defaultOpen?: boolean;
}

export const AccordionItem: React.FC<AccordionItemProps> = ({ title, children, defaultOpen = false }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="border border-[var(--hud-color-darkest)] bg-black/30">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex justify-between items-center p-3 text-left text-lg text-[var(--hud-color)] hover:bg-[var(--hud-color)]/10 transition-colors"
        aria-expanded={isOpen}
      >
        <span className="font-heading text-base">{title}</span>
        <ChevronDownIcon className={`w-5 h-5 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
      </button>
      {isOpen && (
        <div className="p-3 border-t border-[var(--hud-color-darkest)] animate-fade-in">
          {children}
        </div>
      )}
    </div>
  );
};

// ComparisonInput.tsx
import React from 'react';
import { useConfigContext, useInputContext } from '../AppContext.tsx';
import { useLoadingStateContext, useChatStateContext, useSessionActionsContext } from '../contexts/SessionContext.tsx';
import { SupportedLanguage } from '../types.ts';
import { Button } from './Button.tsx';
import { Select } from './Select.tsx';
import { SUPPORTED_LANGUAGES } from '../constants.ts';
import { ChatInterface } from './ChatInterface.tsx';
import { StopIcon } from './Icons.tsx';
import { ContextFilesSelector } from './ContextFilesSelector.tsx';
import { Tooltip } from './Tooltip.tsx';

interface ComparisonInputProps {
  isActive: boolean;
  onAttachFileClick: () => void;
  onOpenProjectFilesModal: () => void;
}

const CodeEditor: React.FC<{
  title: string;
  code: string;
  setCode: (code: string) => void;
  isLoading: boolean;
}> = ({ title, code, setCode, isLoading }) => {
    const textareaClasses = `
        block w-full h-full p-3 font-mono text-sm text-[var(--hud-color)] bg-black/70
        focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-black focus:ring-[var(--bright-cyan)]
        resize-y placeholder:text-transparent transition-all duration-150
        border border-[var(--hud-color-darker)]
    `.trim().replace(/\s+/g, ' ');

    return (
        <div className="flex flex-col flex-grow min-h-0">
            <h3 className="text-lg text-center mb-2">{title}</h3>
            <div className="relative flex-grow">
                <textarea
                    className={textareaClasses}
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    placeholder="Enter code here..."
                    disabled={isLoading}
                />
            </div>
        </div>
    );
};

export const ComparisonInput: React.FC<ComparisonInputProps> = ({ isActive, onAttachFileClick, onOpenProjectFilesModal }) => {
    const { language, setLanguage } = useConfigContext();
    const { comparisonGoal, setComparisonGoal, codeB, setCodeB, userOnlyCode, setUserOnlyCode } = useInputContext();
    const { isLoading, loadingAction, handleStopGenerating } = useLoadingStateContext();
    const { isChatMode } = useChatStateContext();
    const { handleCompareAndOptimize, handleCompareAndRevise, handleContextFileSelectionChange } = useSessionActionsContext();
    const { contextFileIds } = useChatStateContext();

    const canSubmit = userOnlyCode.trim() && codeB.trim() && language !== SupportedLanguage.OTHER;

    const handleGoalChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setComparisonGoal(e.target.value);
    };

    if (!isActive) return null;

    return (
        <div className="flex flex-col h-full min-h-0">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-grow min-h-0">
                <CodeEditor title="Codebase A" code={userOnlyCode} setCode={setUserOnlyCode} isLoading={isLoading} />
                <CodeEditor title="Codebase B" code={codeB} setCode={setCodeB} isLoading={isLoading} />
            </div>

            <div className="mt-4">
                <Tooltip text="Select the language for both codebases.">
                    <Select
                        options={SUPPORTED_LANGUAGES}
                        value={language}
                        onChange={(value) => setLanguage(value as SupportedLanguage)}
                        aria-label="Select language"
                        disabled={isLoading}
                    />
                </Tooltip>
            </div>

            <div className="mt-4">
                <textarea
                    className="w-full h-24 p-3 font-mono text-sm text-[var(--hud-color)] bg-black/70 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-black focus:ring-[var(--bright-cyan)] resize-none border border-[var(--hud-color-darker)]"
                    value={comparisonGoal}
                    onChange={handleGoalChange}
                    placeholder="Optional: Describe the comparison goal or focus areas..."
                    disabled={isLoading}
                />
            </div>

            <ContextFilesSelector
                selectedFileIds={contextFileIds}
                onSelectionChange={handleContextFileSelectionChange}
            />

            <div className="flex-shrink-0 pt-4 mt-auto">
                <div className="w-full flex flex-wrap items-center justify-center gap-3">
                     {isLoading ? (
                        <Button 
                          onClick={handleStopGenerating} 
                          variant="danger"
                          className="w-full"
                          aria-label="Stop generating comparison"
                        >
                          <StopIcon className="w-5 h-5 mr-2" />
                          Stop
                        </Button>
                      ) : (
                        <div className="w-full flex gap-3">
                            <Button
                                onClick={handleCompareAndOptimize}
                                disabled={!canSubmit}
                                className="flex-1"
                            >
                                Compare & Optimize
                            </Button>
                            <Button
                                onClick={handleCompareAndRevise}
                                disabled={!canSubmit}
                                className="flex-1"
                                variant="secondary"
                            >
                                Compare & Revise
                            </Button>
                        </div>
                      )}
                </div>
            </div>
        </div>
    );
};

// AppContext.tsx
import React, { createContext, useState, useContext, useMemo, useCallback } from 'react';
import { AppMode, SupportedLanguage, Toast, ReviewProfile } from './types.ts';
import { SUPPORTED_LANGUAGES } from './constants.ts';
import { ToastContainer } from './Components/ToastContainer.tsx';
import { usePersistentState } from './contexts/PersistenceContext.tsx';

// --- Toast Context ---
interface ToastContextType {
  addToast: (message: string, type: Toast['type']) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const ToastProvider: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((message: string, type: Toast['type']) => {
    const id = Date.now();
    setToasts(prev => [...prev, { id, message, type }]);
  }, []);
  
  const removeToast = useCallback((id: number) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  }, []);

  const value = useMemo(() => ({ addToast }), [addToast]);

  return (
    <ToastContext.Provider value={value}>
      {children}
      <ToastContainer toasts={toasts} onDismiss={removeToast} />
    </ToastContext.Provider>
  );
};

export const useToast = (): ToastContextType => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

// --- Config Context ---
interface ConfigContextType {
  language: SupportedLanguage;
  setLanguage: React.Dispatch<React.SetStateAction<SupportedLanguage>>;
  reviewProfile: ReviewProfile;
  setReviewProfile: React.Dispatch<React.SetStateAction<ReviewProfile>>;
  customReviewInstructions: string;
  setCustomReviewInstructions: React.Dispatch<React.SetStateAction<string>>;
  isDarkMode: boolean;
  toggleDarkMode: () => void;
}

const ConfigContext = createContext<ConfigContextType | undefined>(undefined);

// --- Input Context ---
interface InputContextType {
  userOnlyCode: string;
  setUserOnlyCode: React.Dispatch<React.SetStateAction<string>>;
  codeB: string;
  setCodeB: React.Dispatch<React.SetStateAction<string>>;
  errorMessage: string;
  setErrorMessage: React.Dispatch<React.SetStateAction<string>>;
  comparisonGoal: string;
  setComparisonGoal: React.Dispatch<React.SetStateAction<string>>;
}

const InputContext = createContext<InputContextType | undefined>(undefined);

// --- Actions Context ---
interface ActionsContextType {
  resetAndSetMode: (mode: AppMode) => void;
}

const ActionsContext = createContext<ActionsContextType | undefined>(undefined);

// --- Global Provider ---
export const GlobalStateProvider: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const [language, setLanguage] = usePersistentState<SupportedLanguage>('language', SupportedLanguage.JAVASCRIPT);
  const [reviewProfile, setReviewProfile] = usePersistentState<ReviewProfile>('reviewProfile', ReviewProfile.SECURITY);
  const [customReviewInstructions, setCustomReviewInstructions] = usePersistentState<string>('customReviewInstructions', '');
  const [isDarkMode, setIsDarkMode] = usePersistentState<boolean>('isDarkMode', true);
  const [userOnlyCode, setUserOnlyCode] = useState('');
  const [codeB, setCodeB] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [comparisonGoal, setComparisonGoal] = useState('');

  const toggleDarkMode = useCallback(() => setIsDarkMode(prev => !prev), []);

  const resetInputs = useCallback(() => {
    setUserOnlyCode('');
    setCodeB('');
    setErrorMessage('');
    setComparisonGoal('');
  }, []);

  const resetAndSetMode = useCallback((mode: AppMode) => {
    resetInputs();
  }, [resetInputs]);

  const configValue: ConfigContextType = useMemo(() => ({
    language, setLanguage,
    reviewProfile, setReviewProfile,
    customReviewInstructions, setCustomReviewInstructions,
    isDarkMode, toggleDarkMode,
  }), [language, reviewProfile, customReviewInstructions, isDarkMode, setLanguage, setReviewProfile, setCustomReviewInstructions, toggleDarkMode]);

  const inputValue: InputContextType = useMemo(() => ({
    userOnlyCode, setUserOnlyCode,
    codeB, setCodeB,
    errorMessage, setErrorMessage,
    comparisonGoal, setComparisonGoal,
  }), [userOnlyCode, codeB, errorMessage, comparisonGoal, setUserOnlyCode, setCodeB, setErrorMessage, setComparisonGoal]);

  const actionsValue: ActionsContextType = useMemo(() => ({
    resetAndSetMode,
  }), [resetAndSetMode]);

  return (
    <ActionsContext.Provider value={actionsValue}>
      <ConfigContext.Provider value={configValue}>
        <InputContext.Provider value={inputValue}>
          {children}
        </InputContext.Provider>
      </ConfigContext.Provider>
    </ActionsContext.Provider>
  );
};


// --- Custom Hooks for Consumption ---
export const useConfigContext = (): ConfigContextType => {
  const context = useContext(ConfigContext);
  if (!context) throw new Error('useConfigContext must be used within a GlobalStateProvider');
  return context;
};

export const useInputContext = (): InputContextType => {
  const context = useContext(InputContext);
  if (!context) throw new Error('useInputContext must be used within a GlobalStateProvider');
  return context;
};

export const useActionsContext = (): ActionsContextType => {
  const context = useContext(ActionsContext);
  if (!context) throw new Error('useActionsContext must be used within a GlobalStateProvider');
  return context;
};

// SessionContext.tsx
import React, { createContext, useState, useContext, useMemo, useCallback, useRef, useEffect } from 'react';
import { Chat, Part } from "@google/genai";
import { SupportedLanguage, ChatMessage, Version, ReviewProfile, LoadingAction, AppMode, ChatRevision, Feature, FeatureDecision, ChatContext, FinalizationSummary, FeatureDecisionRecord, ProjectFile, ChatFile, UIActions, SessionActionsContextType } from '../types.ts';
import { GEMINI_MODELS, SYSTEM_INSTRUCTION, DEBUG_SYSTEM_INSTRUCTION, DOCS_SYSTEM_INSTRUCTION, PROFILE_SYSTEM_INSTRUCTIONS, GENERATE_TESTS_INSTRUCTION, EXPLAIN_CODE_INSTRUCTION, REVIEW_SELECTION_INSTRUCTION, COMMIT_MESSAGE_SYSTEM_INSTRUCTION, DOCS_INSTRUCTION, COMPARISON_SYSTEM_INSTRUCTION, COMPARISON_REVISION_SYSTEM_INSTRUCTION, FEATURE_MATRIX_SCHEMA, generateComparisonTemplate, LANGUAGE_TAG_MAP, generateRootCauseTemplate, ROOT_CAUSE_SYSTEM_INSTRUCTION, COMMIT_MESSAGE_SCHEMA, generateFinalizationPrompt, generateVersionNamePrompt, generateCommitMessageTemplate, ADVERSARIAL_REPORT_SYSTEM_INSTRUCTION, THREAT_VECTOR_SYSTEM_INSTRUCTION, generateThreatVectorPrompt, VERSION_NAME_SYSTEM_INSTRUCTION, generateReviewerTemplate, PLACEHOLDER_MARKER } from '../constants.ts';
import { geminiService } from '../services.ts';
import { useConfigContext, useInputContext, useToast } from '../AppContext.tsx';
import { extractFinalCodeBlock, extractGeneratedMarkdownFiles } from '../utils.ts';
import { usePersistentState, usePersistenceContext } from './PersistenceContext.tsx';

// --- New Context Definitions ---

// 1. Output Context
interface OutputContextType {
  reviewOutput: string;
  setReviewOutput: React.Dispatch<React.SetStateAction<string>>;
  revisedCode: string;
  setRevisedCode: React.Dispatch<React.SetStateAction<string>>;
  generatedTests: string;
  setGeneratedTests: React.Dispatch<React.SetStateAction<string>>;
  generatedDocs: string;
  setGeneratedDocs: React.Dispatch<React.SetStateAction<string>>;
  commitMessage: string;
  setCommitMessage: React.Dispatch<React.SetStateAction<string>>;
  rootCauseAnalysis: string;
  setRootCauseAnalysis: React.Dispatch<React.SetStateAction<string>>;
  features: Feature[];
  setFeatures: React.Dispatch<React.SetStateAction<Feature[]>>;
  featureDecisions: Record<string, FeatureDecisionRecord>;
  setFeatureDecisions: React.Dispatch<React.SetStateAction<Record<string, FeatureDecisionRecord>>>;
  finalizationSummary: FinalizationSummary;
  setFinalizationSummary: React.Dispatch<React.SetStateAction<FinalizationSummary>>;
  generatedFiles: { name: string; content: string }[];
  setGeneratedFiles: React.Dispatch<React.SetStateAction<{ name: string; content: string }[]>>;
  adversarialReportContent: string | null;
  setAdversarialReportContent: React.Dispatch<React.SetStateAction<string | null>>;
  threatVectorReport: string | null;
  setThreatVectorReport: React.Dispatch<React.SetStateAction<string | null>>;
  showDiff: boolean;
  setShowDiff: React.Dispatch<React.SetStateAction<boolean>>;
}

const OutputContext = createContext<OutputContextType | undefined>(undefined);

// 2. Loading State Context
interface LoadingStateContextType {
  isLoading: boolean;
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
  loadingAction: LoadingAction | null;
  setLoadingAction: React.Dispatch<React.SetStateAction<LoadingAction | null>>;
  isGeneratingReport: boolean;
  setIsGeneratingReport: React.Dispatch<React.SetStateAction<boolean>>;
  isChatLoading: boolean;
  setIsChatLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

const LoadingStateContext = createContext<LoadingStateContextType | undefined>(undefined);

// 3. Chat State Context
interface ChatStateContextType {
  chatMessages: ChatMessage[];
  setChatMessages: React.Dispatch<React.SetStateAction<ChatMessage[]>>;
  chatInputValue: string;
  setChatInputValue: React.Dispatch<React.SetStateAction<string>>;
  chatRevisions: ChatRevision[];
  setChatRevisions: React.Dispatch<React.SetStateAction<ChatRevision[]>>;
  chatFiles: ChatFile[];
  setChatFiles: React.Dispatch<React.SetStateAction<ChatFile[]>>;
  isChatMode: boolean;
  setIsChatMode: React.Dispatch<React.SetStateAction<boolean>>;
  chatContext: ChatContext | null;
  setChatContext: React.Dispatch<React.SetStateAction<ChatContext | null>>;
  contextFileIds: string[];
  setContextFileIds: React.Dispatch<React.SetStateAction<string[]>>;
  attachments: File[];
  setAttachments: React.Dispatch<React.SetStateAction<File[]>>;
}

const ChatStateContext = createContext<ChatStateContextType | undefined>(undefined);

// 4. Session Actions Context (already defined in types.ts)
const SessionActionsContext = createContext<SessionActionsContextType | undefined>(undefined);

// --- Session Provider ---
export const SessionProvider: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const { language, reviewProfile, customReviewInstructions } = useConfigContext();
  const { userOnlyCode, codeB, errorMessage, comparisonGoal } = useInputContext();
  const { addToast } = useToast();
  const { projectFiles, versions, setVersions } = usePersistenceContext();

  // Output State
  const [reviewOutput, setReviewOutput] = useState<string>('');
  const [revisedCode, setRevisedCode] = useState<string>('');
  const [generatedTests, setGeneratedTests] = useState<string>('');
  const [generatedDocs, setGeneratedDocs] = useState<string>('');
  const [commitMessage, setCommitMessage] = useState<string>('');
  const [rootCauseAnalysis, setRootCauseAnalysis] = useState<string>('');
  const [features, setFeatures] = useState<Feature[]>([]);
  const [featureDecisions, setFeatureDecisions] = useState<Record<string, FeatureDecisionRecord>>({});
  const [finalizationSummary, setFinalizationSummary] = useState<FinalizationSummary>({
    includedFeatures: [],
    removedFeatures: [],
    discussedFeatures: [],
    totalFeatures: 0,
    allFeaturesDecided: false,
  });
  const [generatedFiles, setGeneratedFiles] = useState<{ name: string; content: string }[]>([]);
  const [adversarialReportContent, setAdversarialReportContent] = useState<string | null>(null);
  const [threatVectorReport, setThreatVectorReport] = useState<string | null>(null);
  const [showDiff, setShowDiff] = useState<boolean>(false);

  // Loading State
  const [isLoading, setIsLoading] = useState(false);
  const [loadingAction, setLoadingAction] = useState<LoadingAction | null>(null);
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const [isChatLoading, setIsChatLoading] = useState(false);

  // Chat State
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInputValue, setChatInputValue] = useState<string>('');
  const [chatRevisions, setChatRevisions] = useState<ChatRevision[]>([]);
  const [chatFiles, setChatFiles] = useState<ChatFile[]>([]);
  const [isChatMode, setIsChatMode] = useState(false);
  const [chatContext, setChatContext] = useState<ChatContext | null>(null);
  const [contextFileIds, setContextFileIds] = useState<string[]>([]);
  const [attachments, setAttachments] = useState<File[]>([]);

  // Refs
  const chatRef = useRef<Chat | null>(null);
  const chatAbortController = useRef<AbortController | null>(null);
  const abortController = useRef<AbortController | null>(null);
  const uiActionsRef = useRef<UIActions | null>(null);

  // Derived State
  const selectedContextFiles = useMemo(() => projectFiles.filter(file => contextFileIds.includes(file.id)), [projectFiles, contextFileIds]);

  const allFeaturesDecided = useMemo(() => features.every(f => !!featureDecisions[f.name]), [features, featureDecisions]);

  // Handlers
  const handleContextFileSelectionChange = useCallback((fileId: string, isSelected: boolean) => {
    setContextFileIds(prev => isSelected ? [...prev, fileId] : prev.filter(id => id !== fileId));
  }, []);

  const resetForNewRequest = useCallback(() => {
    setReviewOutput('');
    setRevisedCode('');
    setGeneratedTests('');
    setGeneratedDocs('');
    setCommitMessage('');
    setRootCauseAnalysis('');
    setFeatures([]);
    setFeatureDecisions({});
    setFinalizationSummary({
      includedFeatures: [],
      removedFeatures: [],
      discussedFeatures: [],
      totalFeatures: 0,
      allFeaturesDecided: false,
    });
    setGeneratedFiles([]);
    setShowDiff(false);
    setChatMessages([]);
    setChatRevisions([]);
    setChatFiles([]);
    setIsChatMode(false);
    setChatContext(null);
    setContextFileIds([]);
    setAttachments([]);
    chatRef.current = null;
  }, []);

  const registerUiActions = useCallback((actions: UIActions) => {
    uiActionsRef.current = actions;
  }, []);

  const handleStopGenerating = useCallback(() => {
    if (abortController.current) {
      abortController.current.abort();
      abortController.current = null;
      setIsLoading(false);
      setLoadingAction(null);
      addToast('Generation stopped.', 'info');
    }
    if (chatAbortController.current) {
      chatAbortController.current.abort();
      chatAbortController.current = null;
      setIsChatLoading(false);
      addToast('Chat generation stopped.', 'info');
    }
  }, [addToast]);

  const handleAuditSubmit = useCallback(async () => {
    setIsLoading(true);
    setLoadingAction('review');
    abortController.current = new AbortController();
    try {
      const template = generateReviewerTemplate(language, reviewProfile, userOnlyCode, '', selectedContextFiles);
      const custom = reviewProfile === ReviewProfile.CUSTOM ? customReviewInstructions : '';
      const fullTemplate = custom ? `${template}\n\nCustom Instructions:\n${custom}` : template;
      const response = await geminiService.generateContentStream(fullTemplate.replace(PLACEHOLDER_MARKER, ''), SYSTEM_INSTRUCTION, GEMINI_MODELS.CORE_ANALYSIS, (chunk) => setReviewOutput(prev => prev + chunk));
      const extractedCode = extractFinalCodeBlock(response, true);
      if (extractedCode) setRevisedCode(extractedCode);
      const files = extractGeneratedMarkdownFiles(response);
      if (files.length > 0) setGeneratedFiles(files);
    } catch (error) {
      if (error.name !== 'AbortError') addToast('Error during review.', 'error');
    } finally {
      setIsLoading(false);
      setLoadingAction(null);
      abortController.current = null;
    }
  }, [language, reviewProfile, userOnlyCode, selectedContextFiles, customReviewInstructions, addToast]);

  const handleReviewSubmit = useCallback(async () => {
    // Similar to audit but for single review
    // Implementation omitted for brevity but follows similar pattern
  }, []);

  const handleCompareAndOptimize = useCallback(async () => {
    setIsLoading(true);
    setLoadingAction('comparison');
    abortController.current = new AbortController();
    try {
      const template = generateComparisonTemplate(language, comparisonGoal, userOnlyCode, codeB);
      const response = await geminiService.generateJson({
        contents: template,
        systemInstruction: COMPARISON_SYSTEM_INSTRUCTION,
        model: GEMINI_MODELS.CORE_ANALYSIS,
        schema: FEATURE_MATRIX_SCHEMA
      });
      setFeatures(response);
    } catch (error) {
      if (error.name !== 'AbortError') addToast('Error during comparison.', 'error');
    } finally {
      setIsLoading(false);
      setLoadingAction(null);
      abortController.current = null;
    }
  }, [language, comparisonGoal, userOnlyCode, codeB, addToast]);

  const handleCompareAndRevise = useCallback(async () => {
    // Similar to optimize
  }, []);

  const handleAnalyzeRootCause = useCallback(async () => {
    setIsLoading(true);
    setLoadingAction('root-cause');
    abortController.current = new AbortController();
    try {
      const template = generateRootCauseTemplate(language, userOnlyCode, errorMessage);
      const response = await geminiService.generateText({
        contents: template,
        systemInstruction: ROOT_CAUSE_SYSTEM_INSTRUCTION,
        model: GEMINI_MODELS.CORE_ANALYSIS
      });
      setRootCauseAnalysis(response);
    } catch (error) {
      if (error.name !== 'AbortError') addToast('Error during root cause analysis.', 'error');
    } finally {
      setIsLoading(false);
      setLoadingAction(null);
      abortController.current = null;
    }
  }, [language, userOnlyCode, errorMessage, addToast]);

  const handleStartFollowUp = useCallback(() => {
    setIsChatMode(true);
    setChatContext('post-review'); // Example
  }, []);

  const handleFinalizeFeatureDiscussion = useCallback(async () => {
    setIsLoading(true);
    setLoadingAction('comparison-revision');
    abortController.current = new AbortController();
    try {
      const prompt = generateFinalizationPrompt(features, featureDecisions, userOnlyCode, codeB);
      const response = await geminiService.generateContentStream(prompt, COMPARISON_REVISION_SYSTEM_INSTRUCTION, GEMINI_MODELS.CORE_ANALYSIS, (chunk) => setReviewOutput(prev => prev + chunk));
      const extractedCode = extractFinalCodeBlock(response, false);
      if (extractedCode) setRevisedCode(extractedCode);
    } catch (error) {
      if (error.name !== 'AbortError') addToast('Error during finalization.', 'error');
    } finally {
      setIsLoading(false);
      setLoadingAction(null);
      abortController.current = null;
    }
  }, [features, featureDecisions, userOnlyCode, codeB, addToast]);

  const handleGenerateTests = useCallback(async () => {
    setIsLoading(true);
    setLoadingAction('generating-tests');
    abortController.current = new AbortController();
    try {
      const template = `${GENERATE_TESTS_INSTRUCTION}\n\nCode:\n\`\`\`${LANGUAGE_TAG_MAP[language] || ''}\n${revisedCode || userOnlyCode}\n\`\`\``;
      const response = await geminiService.generateText({
        contents: template,
        systemInstruction: SYSTEM_INSTRUCTION,
        model: GEMINI_MODELS.FAST_TASKS
      });
      setGeneratedTests(response);
    } catch (error) {
      if (error.name !== 'AbortError') addToast('Error generating tests.', 'error');
    } finally {
      setIsLoading(false);
      setLoadingAction(null);
      abortController.current = null;
    }
  }, [language, revisedCode, userOnlyCode, addToast]);

  const handleGenerateDocs = useCallback(async () => {
    // Similar
  }, []);

  const onSaveGeneratedFile = useCallback((name: string, content: string) => {
    // Save to projectFiles
  }, []);

  const handleExitChatMode = useCallback(() => {
    setIsChatMode(false);
    setChatContext(null);
  }, []);

  const handleGenerateCommitMessage = useCallback(async () => {
    setIsLoading(true);
    setLoadingAction('generating-commit');
    abortController.current = new AbortController();
    try {
      const diff = 'Diff content'; // Compute diff
      const template = generateCommitMessageTemplate(diff);
      const message = await geminiService.generateJson({
        contents: template,
        systemInstruction: COMMIT_MESSAGE_SYSTEM_INSTRUCTION,
        model: GEMINI_MODELS.FAST_TASKS,
        schema: COMMIT_MESSAGE_SCHEMA
      });
      setCommitMessage(message);
    } catch (error) {
      if (error.name !== 'AbortError') addToast('Error generating commit message.', 'error');
    } finally {
      setIsLoading(false);
      setLoadingAction(null);
      abortController.current = null;
    }
  }, [addToast]);

  const handleFinalizeComparison = useCallback(() => {
    // Call handleFinalizeFeatureDiscussion
  }, []);

  const handleDownloadOutput = useCallback(() => {
    // Download logic
  }, []);

  const handleAutoGenerateVersionName = useCallback(async (isSavingChat: boolean, onResult: (name: string) => void) => {
    try {
      const content = 'Content for name'; // Assemble content
      const prompt = generateVersionNamePrompt(content);
      const name = await geminiService.generateText({
        contents: prompt,
        systemInstruction: VERSION_NAME_SYSTEM_INSTRUCTION,
        model: GEMINI_MODELS.FAST_TASKS
      });
      onResult(name.trim());
    } catch (error) {
      onResult('Unnamed Version');
    }
  }, []);

  const handleGenerateAdversarialReport = useCallback(async (reconData: string, targetHostname: string) => {
    setIsGeneratingReport(true);
    try {
      const prompt = `Generate adversarial report for ${targetHostname} with recon: ${reconData}`;
      const report = await geminiService.generateText({
        contents: prompt,
        systemInstruction: ADVERSARIAL_REPORT_SYSTEM_INSTRUCTION,
        model: GEMINI_MODELS.CORE_ANALYSIS
      });
      setAdversarialReportContent(report);
    } catch (error) {
      addToast('Error generating report.', 'error');
    } finally {
      setIsGeneratingReport(false);
    }
  }, [addToast]);

  const handleThreatVectorAnalysis = useCallback(async (targetUrl: string) => {
    setIsLoading(true);
    setLoadingAction('generating-threat-vector');
    abortController.current = new AbortController();
    try {
      const prompt = generateThreatVectorPrompt(targetUrl);
      const report = await geminiService.generateText({
        contents: prompt,
        systemInstruction: THREAT_VECTOR_SYSTEM_INSTRUCTION,
        model: GEMINI_MODELS.CORE_ANALYSIS
      });
      setThreatVectorReport(report);
    } catch (error) {
      if (error.name !== 'AbortError') addToast('Error generating threat vector.', 'error');
    } finally {
      setIsLoading(false);
      setLoadingAction(null);
      abortController.current = null;
    }
  }, [addToast]);

  const handleExplainSelection = useCallback((selection: string) => {
    setIsLoading(true);
    setLoadingAction('explain-selection');
    abortController.current = new AbortController();
    try {
      const template = `${EXPLAIN_CODE_INSTRUCTION}\n\nSelection:\n\`\`\`\n${selection}\n\`\`\``;
      // Stream response to reviewOutput or dedicated field
    } catch (error) {
      // Handle
    } finally {
      // Clean up
    }
  }, []);

  const handleReviewSelection = useCallback((selection: string) => {
    // Similar
  }, []);

  const handleChatSubmit = useCallback(async () => {
    setIsChatLoading(true);
    chatAbortController.current = new AbortController();
    try {
      if (!chatRef.current) {
        chatRef.current = await geminiService.startChat(SYSTEM_INSTRUCTION);
      }
      const parts: Part[] = [{ text: chatInputValue }];
      attachments.forEach(file => {
        parts.push({
          inlineData: {
            mimeType: file.type,
            data: '' // Base64 content
          }
        });
      });
      const response = await geminiService.generateChatContent(chatRef.current, parts, GEMINI_MODELS.FAST_TASKS, chatAbortController.current.signal, (chunk) => {
        setChatMessages(prev => {
          const last = prev[prev.length - 1];
          if (last.role === 'model') {
            last.content += chunk;
            return [...prev.slice(0, -1), last];
          }
          return [...prev, { id: Date.now().toString(), role: 'model', content: chunk }];
        });
      });
      // Process response
    } catch (error) {
      // Handle
    } finally {
      setIsChatLoading(false);
      chatAbortController.current = null;
      setChatInputValue('');
      setAttachments([]);
    }
  }, [chatInputValue, attachments]);

  const handleLoadRevisionIntoEditor = useCallback((code: string) => {
    setUserOnlyCode(code);
  }, []);

  const onClearChatRevisions = useCallback(() => {
    setChatRevisions([]);
  }, []);

  const onRenameChatRevision = useCallback((id: string, newName: string) => {
    setChatRevisions(prev => prev.map(r => r.id === id ? { ...r, name: newName } : r));
  }, []);

  const onDeleteChatRevision = useCallback((id: string) => {
    setChatRevisions(prev => prev.filter(r => r.id !== id));
  }, []);

  const onClearChatFiles = useCallback(() => {
    setChatFiles([]);
  }, []);

  const onRenameChatFile = useCallback((id: string, newName: string) => {
    setChatFiles(prev => prev.map(f => f.id === id ? { ...f, name: newName } : f));
  }, []);

  const onDeleteChatFile = useCallback((id: string) => {
    setChatFiles(prev => prev.filter(f => f.id !== id));
  }, []);

  const handleClearChatHistory = useCallback(() => {
    setChatMessages([]);
    chatRef.current = null;
  }, []);

  const handleLoadSession = useCallback((sessionState: any) => {
    // Load state
  }, []);

  const outputValue: OutputContextType = useMemo(() => ({
    reviewOutput, setReviewOutput,
    revisedCode, setRevisedCode,
    generatedTests, setGeneratedTests,
    generatedDocs, setGeneratedDocs,
    commitMessage, setCommitMessage,
    rootCauseAnalysis, setRootCauseAnalysis,
    features, setFeatures,
    featureDecisions, setFeatureDecisions,
    finalizationSummary, setFinalizationSummary,
    generatedFiles, setGeneratedFiles,
    adversarialReportContent, setAdversarialReportContent,
    threatVectorReport, setThreatVectorReport,
    showDiff, setShowDiff,
  }), [reviewOutput, revisedCode, generatedTests, generatedDocs, commitMessage, rootCauseAnalysis, features, featureDecisions, finalizationSummary, generatedFiles, adversarialReportContent, threatVectorReport, showDiff]);

  const loadingStateValue: LoadingStateContextType = useMemo(() => ({
    isLoading, setIsLoading,
    loadingAction, setLoadingAction,
    isGeneratingReport, setIsGeneratingReport,
    isChatLoading, setIsChatLoading,
  }), [isLoading, loadingAction, isGeneratingReport, isChatLoading]);

  const chatStateValue: ChatStateContextType = useMemo(() => ({
    chatMessages, setChatMessages,
    chatInputValue, setChatInputValue,
    chatRevisions, setChatRevisions,
    chatFiles, setChatFiles,
    isChatMode, setIsChatMode,
    chatContext, setChatContext,
    contextFileIds, setContextFileIds,
    attachments, setAttachments,
  }), [chatMessages, chatInputValue, chatRevisions, chatFiles, isChatMode, chatContext, contextFileIds, attachments]);

  const sessionActionsValue: SessionActionsContextType = useMemo(() => ({
    setFeatureDecisions,
    setAdversarialReportContent,
    setThreatVectorReport,
    handleContextFileSelectionChange,
    resetForNewRequest,
    registerUiActions,
    handleStopGenerating,
    handleAuditSubmit,
    handleReviewSubmit,
    handleCompareAndOptimize,
    handleCompareAndRevise,
    handleAnalyzeRootCause,
    handleStartFollowUp,
    handleFinalizeFeatureDiscussion,
    handleGenerateTests,
    handleGenerateDocs,
    onSaveGeneratedFile,
    handleExitChatMode,
    handleGenerateCommitMessage,
    handleFinalizeComparison,
    handleDownloadOutput,
    handleAutoGenerateVersionName,
    handleGenerateAdversarialReport,
    handleThreatVectorAnalysis,
    handleExplainSelection,
    handleReviewSelection,
    handleChatSubmit,
    handleLoadRevisionIntoEditor,
    onClearChatRevisions,
    onRenameChatRevision,
    onDeleteChatRevision,
    onClearChatFiles,
    onRenameChatFile,
    onDeleteChatFile,
    handleClearChatHistory,
    handleLoadSession,
    featureDecisions,
    allFeaturesDecided,
  }), [setFeatureDecisions, setAdversarialReportContent, setThreatVectorReport, handleContextFileSelectionChange, resetForNewRequest, registerUiActions, handleStopGenerating, handleAuditSubmit, handleReviewSubmit, handleCompareAndOptimize, handleCompareAndRevise, handleAnalyzeRootCause, handleStartFollowUp, handleFinalizeFeatureDiscussion, handleGenerateTests, handleGenerateDocs, onSaveGeneratedFile, handleExitChatMode, handleGenerateCommitMessage, handleFinalizeComparison, handleDownloadOutput, handleAutoGenerateVersionName, handleGenerateAdversarialReport, handleThreatVectorAnalysis, handleExplainSelection, handleReviewSelection, handleChatSubmit, handleLoadRevisionIntoEditor, onClearChatRevisions, onRenameChatRevision, onDeleteChatRevision, onClearChatFiles, onRenameChatFile, onDeleteChatFile, handleClearChatHistory, handleLoadSession, featureDecisions, allFeaturesDecided]);

  return (
        <SessionActionsContext.Provider value={sessionActionsValue}>
            <ChatStateContext.Provider value={chatStateValue}>
                <LoadingStateContext.Provider value={loadingStateValue}>
                    <OutputContext.Provider value={outputValue}>
                        {children}
                    </OutputContext.Provider>
                </LoadingStateContext.Provider>
            </ChatStateContext.Provider>
        </SessionActionsContext.Provider>
    );
};

// --- Custom Hooks for Consumption ---

export const useOutputContext = (): OutputContextType => {
    const context = useContext(OutputContext);
    if (context === undefined) throw new Error('useOutputContext must be used within a SessionProvider');
    return context;
};

export const useLoadingStateContext = (): LoadingStateContextType => {
    const context = useContext(LoadingStateContext);
    if (context === undefined) throw new Error('useLoadingStateContext must be used within a SessionProvider');
    return context;
};

export const useChatStateContext = (): ChatStateContextType => {
    const context = useContext(ChatStateContext);
    if (context === undefined) throw new Error('useChatStateContext must be used within a SessionProvider');
    return context;
};

export const useSessionActionsContext = (): SessionActionsContextType => {
    const context = useContext(SessionActionsContext);
    if (context === undefined) throw new Error('useSessionActionsContext must be used within a SessionProvider');
    return context;
};

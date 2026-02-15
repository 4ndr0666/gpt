// types.ts
import React from 'react';

export enum SupportedLanguage {
  JAVASCRIPT = 'JavaScript',
  TYPESCRIPT = 'TypeScript',
  PYTHON = 'Python',
  JAVA = 'Java',
  CSHARP = 'C#',
  CPP = 'C++',
  GO = 'Go',
  RUBY = 'Ruby',
  PHP = 'PHP',
  HTML = 'HTML',
  CSS = 'CSS',
  MARKDOWN = 'Markdown',
  SQL = 'SQL',
  SHELL = 'Shell Script',
  KOTLIN = 'Kotlin',
  SWIFT = 'Swift',
  RUST = 'Rust',
  OTHER = 'Other (Generic)',
}

export enum ReviewProfile {
  SECURITY = 'Security',
  SUCKLESS = 'Suckless',
  MODULAR = 'Modular',
  IDIOMATIC = 'Idiomatic',
  DRY = 'DRY',
  CTF = 'CTF',
  REDTEAM = 'Red Team',
  CUSTOM = 'Custom',
}

export interface ProfileOption {
  value: ReviewProfile;
  label: string;
}

export interface LanguageOption {
  value: SupportedLanguage;
  label: string;
}

export interface Toast {
  id: number;
  message: string;
  type: 'success' | 'error' | 'info';
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'model';
  content: string;
  attachments?: {
    name: string;
    mimeType: string;
    content: string; // base64 for images, raw text for others
  }[];
}

export interface ChatRevision {
  id: string;
  name: string;
  code: string;
}

export interface ChatFile {
  id: string;
  name: string;
  mimeType: string;
  content: string; // base64 for images, raw text for others
}

export interface Version {
  id: string;
  name: string;
  code: string;
  reviewOutput: string;
  revisedCode: string;
  language: SupportedLanguage;
  profile: ReviewProfile;
  timestamp: number;
  appMode: AppMode;
  comparisonGoal?: string;
  codeB?: string;
  errorMessage?: string;
  chatHistory?: ChatMessage[];
  chatRevisions?: ChatRevision[];
  chatFiles?: ChatFile[];
}

export interface ProjectFile {
  id: string;
  name: string;
  mimeType: string;
  content: string; // base64 for images, raw text for others
}

export interface Feature {
  name: string;
  description: string;
  source: 'Unique to A' | 'Unique to B' | 'Common';
}

export type FeatureDecision = 'include' | 'remove' | 'discussed';

export interface FeatureDecisionRecord {
  decision: FeatureDecision;
  discussionHistory: string[];
}

export type LoadingAction = 
  | 'review'
  | 'debug'
  | 'comparison'
  | 'comparison-revision'
  | 'explain-selection'
  | 'review-selection'
  | 'chat'
  | 'generating-tests'
  | 'generating-docs'
  | 'generating-commit'
  | 'generating-version-name'
  | 'generating-adversarial-report'
  | 'generating-threat-vector'
  | 'root-cause';

export type AppMode = 'single' | 'comparison' | 'debug';

export type ChatContext = 
  | 'post-review'
  | 'post-debug'
  | 'post-comparison'
  | 'finalization';

export interface FinalizationSummary {
  includedFeatures: string[];
  removedFeatures: string[];
  discussedFeatures: string[];
  totalFeatures: number;
  allFeaturesDecided: boolean;
}

export interface TargetProfile {
  hostname: string;
  ip: string;
  ports: number[];
  services: string[];
  vulnerabilities: string[];
}

export interface ImportedSession {
  id: string;
  name: string;
  content: string;
  timestamp: number;
}

export enum ArsenalTool {
  RECON = 'recon',
  PAYLOAD = 'payload',
  THREAT_VECTOR = 'threat-vector',
  REPORT = 'report',
}

export interface UIActions {
  openReconModal: () => void;
  openPayloadCraftingModal: () => void;
  openThreatVectorModal: () => void;
  openReportGenerator: () => void;
}

export interface SessionActionsContextType {
  setFeatureDecisions: React.Dispatch<React.SetStateAction<Record<string, FeatureDecisionRecord>>>;
  setAdversarialReportContent: React.Dispatch<React.SetStateAction<string | null>>;
  setThreatVectorReport: React.Dispatch<React.SetStateAction<string | null>>;
  handleContextFileSelectionChange: (fileId: string, isSelected: boolean) => void;
  resetForNewRequest: () => void;
  registerUiActions: (actions: UIActions) => void;
  handleStopGenerating: () => void;
  handleAuditSubmit: () => Promise<void>;
  handleReviewSubmit: () => Promise<void>;
  handleCompareAndOptimize: () => Promise<void>;
  handleCompareAndRevise: () => Promise<void>;
  handleAnalyzeRootCause: () => Promise<void>;
  handleStartFollowUp: () => void;
  handleFinalizeFeatureDiscussion: () => Promise<void>;
  handleGenerateTests: () => Promise<void>;
  handleGenerateDocs: () => Promise<void>;
  onSaveGeneratedFile: (name: string, content: string) => void;
  handleExitChatMode: () => void;
  handleGenerateCommitMessage: () => Promise<void>;
  handleFinalizeComparison: () => void;
  handleDownloadOutput: () => void;
  handleAutoGenerateVersionName: (isSavingChat: boolean, onResult: (name: string) => void) => Promise<void>;
  handleGenerateAdversarialReport: (reconData: string, targetHostname: string) => Promise<void>;
  handleThreatVectorAnalysis: (targetUrl: string) => Promise<void>;
  handleExplainSelection: (selection: string) => void;
  handleReviewSelection: (selection: string) => void;
  handleChatSubmit: () => Promise<void>;
  handleLoadRevisionIntoEditor: (code: string) => void;
  onClearChatRevisions: () => void;
  onRenameChatRevision: (id: string, newName: string) => void;
  onDeleteChatRevision: (id: string) => void;
  onClearChatFiles: () => void;
  onRenameChatFile: (id: string, newName: string) => void;
  onDeleteChatFile: (id: string) => void;
  handleClearChatHistory: () => void;
  handleLoadSession: (sessionState: any) => void;
  featureDecisions: Record<string, FeatureDecisionRecord>; // Needs to be here for the setter
  allFeaturesDecided: boolean; // Derived state, but depends on decisions
}

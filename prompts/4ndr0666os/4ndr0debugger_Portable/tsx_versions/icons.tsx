// Segment 12/12
// Icons.tsx
import React from 'react';

export const SaveIcon = ({ className }: { className?: string }) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <title>Save</title>
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />
      <polyline strokeLinecap="round" strokeLinejoin="round" points="17 21 17 13 7 13 7 21" />
      <polyline strokeLinecap="round" strokeLinejoin="round" points="7 3 7 8 15 8" />
    </svg>
);

export const ImportIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <title>Import</title>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
    </svg>
);

export const ExportIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <title>Export</title>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
    </svg>
);

export const BoltIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <title>Bolt</title>
      <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
    </svg>
);

export const BugIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <title>Bug</title>
      <path strokeLinecap="round" strokeLinejoin="round" d="M20 12H4m16 0l-4 4m0 0l-4-4m4 4V4" />
    </svg>
);

export const CodeIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <title>Code</title>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
    </svg>
);

export const CompareIconSvg = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <title>Compare</title>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
    </svg>
);

export const ChevronDownIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
    </svg>
);

export const StopIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
    </svg>
);

export const FolderIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
    </svg>
);

export const PaperclipIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
    </svg>
);

export const DeleteIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
    </svg>
);

export const CheckIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
    </svg>
);

export const CopyIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5h12a2 2 0 012 2v12a2 2 0 01-2 2h-1M8 5v2m0 12v-2" />
    </svg>
);

export const CompareIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
    </svg>
);

export const ChatIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
    </svg>
);

export const CommitIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 0115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
    </svg>
);

export const RootCauseIcon = ({className}: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 17L9 20l-4 1 1-4L17.25 6.749a1.5 1.5 0 112.122-2.122L9.75 17zM15.5 5.5l3 3" />
    </svg>
);

export const ImportIcon = ({ className }: { className?: string }) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
        <title>Import</title>
        <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 9m4-4v12" />
    </svg>
);

export const JsonIcon = ({ className }: { className?: string }) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
        <title>JSON File</title>
        <path strokeLinecap="round" strokeLinejoin="round" d="M8 9l-3 3 3 3m8-6l3 3-3 3" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M10 20.5l4-17" />
    </svg>
);

export const MenuIcon = ({ className }: { className?: string }) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
    </svg>
);

// Button.tsx
import React from 'react';
import { LoadingSpinner } from './LoadingSpinner.tsx';

type ButtonProps = React.ComponentPropsWithoutRef<'button'> & {
  variant?: 'primary' | 'secondary' | 'danger';
  isLoading?: boolean;
  children: React.ReactNode;
};

export const Button = ({ 
  children, 
  variant = 'primary', 
  isLoading = false, 
  className, 
  disabled,
  ...props 
}: ButtonProps) => {
  const baseStyle = `
    px-6 py-2.5 font-semibold text-sm uppercase tracking-wider flex items-center justify-center 
    border transition-all duration-150 transform
    focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-black focus:ring-[var(--bright-cyan)]
    disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none disabled:transform-none
    active:scale-[0.97]
  `.trim().replace(/\s+/g, ' ');
  
  const variantStyles = {
    primary: `
      bg-transparent border-[var(--hud-color)] text-[var(--hud-color)]
      shadow-[0_0_8px_var(--shadow-cyan-light)] 
      hover:bg-[var(--hud-color)]/25 hover:shadow-[0_0_15px_var(--shadow-cyan-heavy)] hover:border-[var(--bright-cyan)] hover:-translate-y-px
      active:bg-[var(--hud-color)]/30 active:brightness-125
      disabled:border-[var(--hud-color-darker)] disabled:text-[var(--hud-color-darker)] disabled:bg-[var(--hud-color-darkest)]
    `,
    secondary: `
      bg-transparent border-[var(--hud-color-darker)] border-[var(--hud-color-darker)] text-[var(--hud-color-darker)]
      shadow-[0_0_5px_rgba(0,0,0,0.5)]
      hover:bg-[var(--hud-color)]/10 hover:border-[var(--hud-color)] hover:text-[var(--hud-color)] hover:shadow-[0_0_12px_var(--shadow-cyan-heavy)] hover:-translate-y-px
      active:bg-[var(--hud-color)]/20 active:brightness-125
      disabled:border-[var(--hud-color-darker)] disabled:text-[var(--hud-color-darker)] disabled:bg-[var(--hud-color-darkest)]
    `,
    danger: `
      bg-transparent border-[var(--red-color)] text-[var(--red-color)]
      shadow-[0_0_8px_var(--red-glow-color)]
      hover:shadow-[0_0_15px_var(--red-glow-color)] hover:bg-[var(--red-color)]/20 hover:-translate-y-px
      active:bg-[var(--red-color)]/30 active:brightness-125
      disabled:border-[var(--red-color)] disabled:opacity-50
    `,
  };

  return (
    <button
      type="button"
      className={`${baseStyle} ${variantStyles[variant]} ${className || ''}`}
      disabled={isLoading || disabled}
      {...props}
    >
      {isLoading && (
        <LoadingSpinner size="w-5 h-5" color="text-current" className="-ml-1 mr-3" />
      )}
      {children}
    </button>
  );
};

// Select.tsx
import React, { useState, useRef, useEffect, useCallback } from 'react';

interface SelectOption {
  value: string;
  label: string;
}

interface SelectProps {
  options: SelectOption[];
  label?: string;
  id?: string;
  className?: string;
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
  'aria-label'?: string;
}

export const Select = ({
  options,
  label,
  id,
  className,
  value,
  onChange,
  disabled = false,
  'aria-label': ariaLabel,
}: SelectProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const containerRef = useRef<HTMLDivElement>(null);
  const listRef = useRef<HTMLUListElement>(null);
  
  const selectedOption = options.find(o => o.value === value);

  const toggleOpen = useCallback(() => {
    if (!disabled) {
      setIsOpen(prev => !prev);
    }
  }, [disabled]);

  const handleSelectOption = useCallback((option: SelectOption) => {
    if (!disabled) {
      onChange(option.value);
      setIsOpen(false);
      containerRef.current?.querySelector('button')?.focus();
    }
  }, [disabled, onChange]);

  const handleClickOutside = useCallback((event: MouseEvent) => {
    if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
      setIsOpen(false);
    }
  }, []);

  useEffect(() => {
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      listRef.current?.focus();
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen, handleClickOutside]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggleOpen();
    } else if (e.key === 'Escape') {
      setIsOpen(false);
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setHighlightedIndex(prev => (prev + 1) % options.length);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setHighlightedIndex(prev => (prev - 1 + options.length) % options.length);
    } else if (e.key === 'Tab') {
      setIsOpen(false);
    }
  }, [toggleOpen, options.length]);

  const handleListKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && highlightedIndex >= 0) {
      e.preventDefault();
      handleSelectOption(options[highlightedIndex]);
    } else if (e.key === 'Escape' || e.key === 'Tab') {
      setIsOpen(false);
      containerRef.current?.querySelector('button')?.focus();
    }
  }, [highlightedIndex, options, handleSelectOption]);

  return (
    <div ref={containerRef} className={`relative ${className || ''}`}>
      {label && <label htmlFor={id} className="block text-sm font-medium text-[var(--hud-color-darker)] mb-1">{label}</label>}
      <button
        type="button"
        onClick={toggleOpen}
        onKeyDown={handleKeyDown}
        className="w-full flex justify-between items-center px-3 py-2 bg-black/70 border border-[var(--hud-color-darker)] text-[var(--hud-color)] text-sm focus:outline-none focus:ring-2 focus:ring-[var(--bright-cyan)] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        id={id}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        aria-label={ariaLabel}
        disabled={disabled}
      >
        <span className="truncate">{selectedOption ? selectedOption.label : 'Select an option'}</span>
        <svg className={`w-4 h-4 ml-2 transition-transform ${isOpen ? 'transform rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
        </svg>
      </button>
      {isOpen && (
        <ul
          ref={listRef}
          className="absolute z-10 w-full mt-1 bg-black/90 border border-[var(--hud-color-darkest)] max-h-60 overflow-y-auto focus:outline-none"
          role="listbox"
          aria-activedescendant={highlightedIndex >= 0 ? `option-${highlightedIndex}` : undefined}
          tabIndex={-1}
          onKeyDown={handleListKeyDown}
        >
          {options.map((option, index) => {
            const isHighlighted = highlightedIndex === index;
            return (
              <li
                key={option.value}
                id={`option-${index}`}
                className={`cursor-pointer select-none relative p-2 transition-all duration-150 ${
                  isHighlighted ? 'bg-[var(--hud-color)]/20' : 'bg-transparent'
                }`}
                role="option"
                aria-selected={value === option.value}
                onClick={() => handleSelectOption(option)}
                onMouseEnter={() => setHighlightedIndex(index)}
              >
                <span className={`block truncate ${value === option.value ? 'font-semibold text-[var(--primary-text)]' : 'font-normal text-[var(--secondary-text)]'}`}>
                  {option.label}
                </span>
                {value === option.value && (
                  <span className="absolute inset-y-0 right-0 flex items-center pr-3 text-[var(--hud-color)]">
                    <svg className="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
};

// Tooltip.tsx
import React, { useState, useId, useRef } from 'react';

interface TooltipProps {
  text: string;
  children: React.ReactElement;
  position?: 'top' | 'bottom' | 'left' | 'right';
}

export const Tooltip: React.FC<TooltipProps> = ({ text, children, position = 'top' }) => {
  const [isVisible, setIsVisible] = useState(false);
  const id = useId();
  const tooltipId = `tooltip-${id}`;
  const timeoutRef = useRef<number | null>(null);

  const handleMouseEnter = () => {
    if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
    }
    timeoutRef.current = window.setTimeout(() => {
        setIsVisible(true);
    }, 300); // 300ms delay before showing
  };

  const handleMouseLeave = () => {
    if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
    }
    setIsVisible(false);
  };

  const positionClasses = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
  };

  return (
    <div 
      className="relative flex items-center"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onFocus={() => setIsVisible(true)}
      onBlur={() => setIsVisible(false)}
    >
      {React.cloneElement(children, {
        "aria-describedby": isVisible && text ? tooltipId : undefined,
      } as any)}
      {isVisible && text && (
        <div
          id={tooltipId}
          role="tooltip"
          className={`absolute z-50 px-3 py-2 text-xs font-mono text-[var(--hud-color)] bg-black/90 border border-[var(--hud-color-darkest)] whitespace-nowrap animate-fade-in ${positionClasses[position]}`}
        >
          {text}
        </div>
      )}
    </div>
  );
};

// ContextFilesSelector.tsx
import React from 'react';
import { ProjectFile } from '../types.ts';
import { AccordionItem } from './AccordionItem.tsx';
import { usePersistenceContext } from '../contexts/PersistenceContext.tsx';

interface ContextFilesSelectorProps {
  selectedFileIds: string[];
  onSelectionChange: (fileId: string, isSelected: boolean) => void;
}

export const ContextFilesSelector: React.FC<ContextFilesSelectorProps> = ({ selectedFileIds, onSelectionChange }) => {
  const { projectFiles } = usePersistenceContext();

  const title = `Context Files (${selectedFileIds.length} selected)`;

  if (projectFiles.length === 0) {
    return (
        <div className="text-center text-xs text-[var(--hud-color-darker)] py-2">
            No project files available. Upload files via the main menu to use them as context.
        </div>
    );
  }

  return (
    <div className="animate-fade-in my-4">
      <AccordionItem title={title} defaultOpen={false}>
        <div className="space-y-2 max-h-48 overflow-y-auto pr-2">
          {projectFiles.map(file => (
            <div key={file.id} className="flex items-center">
              <input
                type="checkbox"
                id={`context-file-${file.id}`}
                checked={selectedFileIds.includes(file.id)}
                onChange={(e) => onSelectionChange(file.id, e.target.checked)}
                className="form-checkbox h-4 w-4 bg-black/50 border-[var(--hud-color-darkest)] text-[var(--hud-color)] focus:ring-[var(--hud-color)]"
              />
              <label htmlFor={`context-file-${file.id}`} className="ml-3 text-sm text-[var(--hud-color-darker)] cursor-pointer truncate" title={file.name}>
                {file.name}
              </label>
            </div>
          ))}
           {projectFiles.length > 5 && (
            <p className="text-center text-xs text-[var(--hud-color-darker)] pt-2">Scroll for more files</p>
           )}
        </div>
      </AccordionItem>
    </div>
  );
};

// ChatInterface.tsx
import React, { useEffect, useRef, memo } from 'react';
import { ChatMessage } from '../types.ts';
import { Button } from './Button.tsx';
import { LoadingSpinner } from './LoadingSpinner.tsx';
import { MarkdownRenderer } from './MarkdownRenderer.tsx';
import { ChatContext } from './ChatContext.tsx';
import { DeleteIcon, FolderIcon, PaperclipIcon } from './Icons.tsx';
import { useConfigContext, useActionsContext } from '../AppContext.tsx';
import { useChatStateContext, useLoadingStateContext, useOutputContext, useSessionActionsContext } from '../contexts/SessionContext.tsx';
import { Tooltip } from './Tooltip.tsx';

interface ChatInterfaceProps {
  onSaveChatSession?: () => void;
  onAttachFileClick: () => void;
  onOpenProjectFilesModal: () => void;
  onLoadCodeIntoWorkbench?: (code: string) => void;
  hideHeader?: boolean;
}

const AttachmentPreview: React.FC<{ file: File; onRemove: () => void; }> = ({ file, onRemove }) => {
    const isImage = file.type.startsWith('image/');
    const [previewUrl, setPreviewUrl] = React.useState<string | null>(null);

    useEffect(() => {
        if (isImage) {
            const url = URL.createObjectURL(file);
            setPreviewUrl(url);
            return () => URL.revokeObjectURL(url);
        }
    }, [file, isImage]);

    return (
        <div className="bg-black/50 border border-[var(--hud-color-darkest)] flex items-center justify-between p-1 rounded-sm">
            <div className="flex items-center space-x-2 truncate">
                {previewUrl ? (
                    <img src={previewUrl} alt={file.name} className="w-6 h-6 object-cover rounded-sm" />
                ) : (
                    <PaperclipIcon className="w-4 h-4 text-[var(--hud-color-darker)]" />
                )}
                <span className="text-xs truncate text-[var(--hud-color-darker)]" title={file.name}>{file.name}</span>
            </div>
            <button onClick={onRemove} className="p-1 hover:text-[var(--red-color)]" aria-label="Remove attachment">
                <DeleteIcon className="w-3 h-3" />
            </button>
        </div>
    );
};

const renderAttachments = (attachments: { name: string; mimeType: string; content: string }[] | undefined) => {
    if (!attachments || attachments.length === 0) return null;

    return (
        <div className="space-y-2 mt-2">
            {attachments.map((att, index) => (
                <div key={index} className="bg-black/50 border border-[var(--hud-color-darkest)] p-2 rounded-sm">
                    {att.mimeType.startsWith('image/') ? (
                        <img src={`data:${att.mimeType};base64,${att.content}`} alt={att.name} className="max-w-full h-auto rounded-sm" />
                    ) : (
                        <div className="flex items-center space-x-2">
                            <PaperclipIcon className="w-4 h-4 text-[var(--hud-color-darker)]" />
                            <span className="text-xs text-[var(--hud-color-darker)] truncate" title={att.name}>{att.name}</span>
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
};

export const ChatInterface: React.FC<ChatInterfaceProps> = memo(({ onSaveChatSession, onAttachFileClick, onOpenProjectFilesModal, onLoadCodeIntoWorkbench, hideHeader = false }) => {
  const { appMode } = useConfigContext();
  const { resetAndSetMode } = useActionsContext();
  const { isChatLoading } = useLoadingStateContext();
  const { chatMessages, chatInputValue, setChatInputValue, attachments, setAttachments, chatContext, chatRevisions, chatFiles } = useChatStateContext();
  const { handleChatSubmit, handleExitChatMode, onRenameChatRevision, onDeleteChatRevision, onRenameChatFile, onDeleteChatFile, handleLoadRevisionIntoEditor } = useSessionActionsContext();

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => setChatInputValue(e.target.value);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleChatSubmit();
    }
  };

  const handleAttach = (file: File) => {
    setAttachments(prev => [...prev, file]);
  };

  const removeAttachment = (index: number) => {
    setAttachments(prev => prev.filter((_, i) => i !== index));
  };

  const followUpButtonText = appMode === 'debug' ? 'Fix Code' : 'Follow Up';

  return (
    <div className="flex flex-col h-full min-h-0">
      {!hideHeader && (
        <div className="flex-shrink-0 flex items-center justify-between mb-4">
          <h2 className="text-xl">Chat Mode</h2>
          {onSaveChatSession && (
            <Button onClick={onSaveChatSession} variant="secondary" className="text-sm py-1 px-3">
              Save Chat
            </Button>
          )}
        </div>
      )}

      <div className="flex-grow overflow-y-auto space-y-4 pr-2 min-h-0">
        {chatMessages.map(message => (
          <div key={message.id} className={`p-3 rounded-sm ${message.role === 'user' ? 'bg-[var(--hud-color)]/10' : 'bg-black/50'}`}>
            <div className="font-bold mb-1">{message.role.toUpperCase()}</div>
            <MarkdownRenderer markdown={message.content} onLoadCodeIntoWorkbench={onLoadCodeIntoWorkbench} />
            {renderAttachments(message.attachments)}
          </div>
        ))}
        {isChatLoading && (
          <div className="flex justify-center py-4">
            <LoadingSpinner />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="flex-shrink-0 mt-4 space-y-2">
        {attachments.length > 0 && (
          <div className="space-y-1">
            {attachments.map((file, index) => (
              <AttachmentPreview key={index} file={file} onRemove={() => removeAttachment(index)} />
            ))}
          </div>
        )}

        <div className="flex items-end space-x-3">
          <textarea
            className="flex-grow p-3 font-mono text-sm text-[var(--hud-color)] bg-black/70 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-black focus:ring-[var(--bright-cyan)] resize-none border border-[var(--hud-color-darker)] min-h-[40px]"
            value={chatInputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            disabled={isChatLoading}
            rows={1}
          />
          {appMode !== 'debug' && chatContext !== 'finalization' && (
            <div className="flex flex-col space-y-2">
              <Tooltip text="Attach from Project Files">
                <button
                  onClick={onOpenProjectFilesModal}
                  disabled={isChatLoading}
                  className="p-3 border border-[var(--hud-color-darker)] text-[var(--hud-color-darker)] hover:text-[var(--hud-color)] hover:border-[var(--hud-color)] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  aria-label="Attach from Project Files"
                >
                  <FolderIcon className="w-5 h-5" />
                </button>
              </Tooltip>
              <Tooltip text="Attach new file">
                <button
                  onClick={onAttachFileClick}
                  disabled={isChatLoading}
                  className="p-3 border border-[var(--hud-color-darker)] text-[var(--hud-color-darker)] hover:text-[var(--hud-color)] hover:border-[var(--hud-color)] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  aria-label="Attach new file"
                >
                  <PaperclipIcon className="w-5 h-5" />
                </button>
              </Tooltip>
            </div>
          )}
          {appMode !== 'debug' && chatContext !== 'finalization' && (
              <Button onClick={handleChatSubmit} isLoading={isChatLoading} disabled={isChatLoading || (!chatInputValue?.trim() && (!attachments || attachments.length === 0))}>
                  Send
              </Button>
          )}
          {chatContext === 'finalization' && (
              <Button onClick={handleChatSubmit} isLoading={isChatLoading} disabled={isChatLoading}>
                  Generate Revision
              </Button>
          )}
        </div>
      </div>
    </div>
  );
});

// App.tsx
import React, { useState, useCallback, useEffect, useRef } from 'react';
import { useConfigContext, useInputContext, useActionsContext, useToast } from './AppContext.tsx';
import { usePersistenceContext } from './contexts/PersistenceContext.tsx';
import { useOutputContext, useLoadingStateContext, useChatStateContext, useSessionActionsContext } from './contexts/SessionContext.tsx';
import { Header } from './Components/Header.tsx';
import { CodeInput } from './Components/CodeInput.tsx';
import { ReviewOutput } from './Components/ReviewOutput.tsx';
import { Version, UIActions, ProjectFile, ImportedSession } from './types.ts';
import { DiffViewer } from './Components/DiffViewer.tsx';
import { ComparisonInput } from './Components/ComparisonInput.tsx';
import { VersionHistoryModal } from './Components/VersionHistoryModal.tsx';
import { SaveVersionModal } from './Components/SaveVersionModal.tsx';
import { ApiKeyBanner } from './Components/ApiKeyBanner.tsx';
import { DocumentationCenterModal } from './Components/DocumentationCenterModal.tsx';
import { ProjectFilesModal } from './Components/ProjectFilesModal.tsx';
import { SessionManagerModal } from './Components/SessionManagerModal.tsx';
import { AdversarialReportGenerator } from './Components/AdversarialReportGenerator.tsx';
import { SegmentedControl } from './Components/SegmentedControl.tsx';
import { LiveReconModal } from './Components/LiveReconModal.tsx';
import { PayloadCraftingModal } from './Components/PayloadCraftingModal.tsx';
import { ThreatVectorModal } from './Components/ThreatVectorModal.tsx';
import { HelpModal } from './Components/HelpModal.tsx';
import { DebugInput } from './Components/DebugInput.tsx';
import { b64EncodeUnicode } from './utils.ts';

const App = () => {
  const { appMode, setAppMode } = useConfigContext();
  const { resetInputs } = useActionsContext();
  const { isLoading } = useLoadingStateContext();
  const { reviewOutput, revisedCode, showDiff, setShowDiff, adversarialReportContent, setAdversarialReportContent, threatVectorReport, setThreatVectorReport } = useOutputContext();
  const { versions, projectFiles, importedSessions, setVersions, setProjectFiles, setImportedSessions } = usePersistenceContext();
  const { addToast } = useToast();
  const { handleAutoGenerateVersionName, handleLoadSession, registerUiActions, handleThreatVectorAnalysis } = useSessionActionsContext();

  const [isVersionHistoryModalOpen, setIsVersionHistoryModalOpen] = useState(false);
  const [isSaveModalOpen, setIsSaveModalOpen] = useState(false);
  const [isDocsModalOpen, setIsDocsModalOpen] = useState(false);
  const [isProjectFilesModalOpen, setIsProjectFilesModalOpen] = useState(false);
  const [isSessionManagerModalOpen, setIsSessionManagerModalOpen] = useState(false);
  const [isReportGeneratorModalOpen, setIsReportGeneratorModalOpen] = useState(false);
  const [isReconModalOpen, setIsReconModalOpen] = useState(false);
  const [isPayloadCraftingModalOpen, setIsPayloadCraftingModalOpen] = useState(false);
  const [isThreatVectorModalOpen, setIsThreatVectorModalOpen] = useState(false);
  const [isHelpModalOpen, setIsHelpModalOpen] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    registerUiActions({
      openReconModal: () => setIsReconModalOpen(true),
      openPayloadCraftingModal: () => setIsPayloadCraftingModalOpen(true),
      openThreatVectorModal: () => setIsThreatVectorModalOpen(true),
      openReportGenerator: () => setIsReportGeneratorModalOpen(true),
    });
  }, [registerUiActions]);

  const handleModeChange = useCallback((mode: AppMode) => {
    resetInputs();
    setAppMode(mode);
  }, [resetInputs, setAppMode]);

  const handleOpenSaveModal = () => setIsSaveModalOpen(true);

  const handleSaveVersion = useCallback((name: string) => {
    const newVersion: Version = {
      id: Date.now().toString(),
      name,
      code: userOnlyCode,
      reviewOutput,
      revisedCode,
      language,
      profile: reviewProfile,
      timestamp: Date.now(),
      appMode,
      // Add more fields as needed
    };
    setVersions(prev => [...prev, newVersion]);
    addToast('Version saved.', 'success');
    setIsSaveModalOpen(false);
  }, [userOnlyCode, reviewOutput, revisedCode, language, reviewProfile, appMode, addToast, setVersions]);

  const handleLoadVersion = useCallback((version: Version) => {
    setUserOnlyCode(version.code);
    setReviewOutput(version.reviewOutput);
    setRevisedCode(version.revisedCode);
    setLanguage(version.language);
    setReviewProfile(version.profile);
    // Load more as needed
    addToast('Version loaded.', 'success');
  }, [addToast]);

  const handleStartFollowUp = useCallback((version: Version) => {
    handleLoadVersion(version);
    // Enter chat mode
  }, [handleLoadVersion]);

  const handleDeleteVersion = useCallback((id: string) => {
    setVersions(prev => prev.filter(v => v.id !== id));
    addToast('Version deleted.', 'info');
  }, [addToast, setVersions]);

  const handleOpenProjectFilesModal = () => setIsProjectFilesModalOpen(true);

  const handleAttachProjectFileToChat = useCallback((file: ProjectFile) => {
    // Add to chatFiles
  }, []);

  const handleDownloadProjectFile = useCallback((file: ProjectFile) => {
    // Download
  }, []);

  const handleImportFile = useCallback((file: File) => {
    // Handle import
  }, []);

  const handleDeleteImportedSession = useCallback((id: string) => {
    setImportedSessions(prev => prev.filter(s => s.id !== id));
  }, [setImportedSessions]);

  const handleGenerateAdversarialReport = useCallback((reconData: string, targetHostname: string) => {
    // Call handler
  }, []);

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-black to-gray-900 text-[var(--hud-color)] font-mono">
      <ApiKeyBanner />
      <Header
        onImportClick={() => setIsSessionManagerModalOpen(true)}
        onExportSession={() => {}}
        onShare={() => {}}
        onOpenDocsModal={() => setIsDocsModalOpen(true)}
        onOpenProjectFilesModal={handleOpenProjectFilesModal}
        onToggleVersionHistory={() => setIsVersionHistoryModalOpen(true)}
        onOpenReportGenerator={() => setIsReportGeneratorModalOpen(true)}
        onOpenReconModal={() => setIsReconModalOpen(true)}
        onOpenPayloadCraftingModal={() => setIsPayloadCraftingModalOpen(true)}
        onOpenThreatVectorModal={() => setIsThreatVectorModalOpen(true)}
        onOpenHelpModal={() => setIsHelpModalOpen(true)}
        isToolsEnabled={true}
        onEndChatSession={handleExitChatMode}
        isInputPanelVisible={true}
        setIsInputPanelVisible={() => {}}
        isChatMode={isChatMode}
        reviewAvailable={!!reviewOutput}
        handleStartFollowUp={handleStartFollowUp}
        handleGenerateTests={handleGenerateTests}
      />
      <SegmentedControl currentMode={appMode} onModeChange={handleModeChange} disabled={isLoading} />
      <div className="flex-grow overflow-y-auto p-4">
        {appMode === 'single' && <CodeInput isActive={true} onOpenSaveModal={handleOpenSaveModal} onSaveChatSession={() => {}} onAttachFileClick={() => fileInputRef.current?.click()} onOpenProjectFilesModal={handleOpenProjectFilesModal} />}
        {appMode === 'comparison' && <ComparisonInput isActive={true} onAttachFileClick={() => fileInputRef.current?.click()} onOpenProjectFilesModal={handleOpenProjectFilesModal} />}
        {appMode === 'debug' && <DebugInput isActive={true} onOpenSaveModal={handleOpenSaveModal} onSaveChatSession={() => {}} onAttachFileClick={() => fileInputRef.current?.click()} onOpenProjectFilesModal={handleOpenProjectFilesModal} />}
        <ReviewOutput onSaveVersion={handleOpenSaveModal} onShowDiff={() => setShowDiff(true)} isActive={true} />
      </div>
      {showDiff && (
        <DiffViewer
          originalCode={userOnlyCode}
          revisedCode={revisedCode}
          language={language}
          onClose={() => setShowDiff(false)}
          onLoadCodeIntoWorkbench={handleLoadRevisionIntoEditor}
        />
      )}
      <input type="file" ref={fileInputRef} className="hidden" onChange={(e) => handleImportFile(e.target.files[0])} multiple accept="*/*" />
      {/* Modals */}
      <VersionHistoryModal
        isOpen={isVersionHistoryModalOpen}
        onClose={() => setIsVersionHistoryModalOpen(false)}
        onLoadVersion={handleLoadVersion}
        onDeleteVersion={handleDeleteVersion}
        onStartFollowUp={handleStartFollowUp}
        onRenameVersion={(id, name) => {}}
        isLoading={isLoading}
      />
      <SaveVersionModal
        isOpen={isSaveModalOpen}
        onClose={() => setIsSaveModalOpen(false)}
        onSave={handleSaveVersion}
        onAutoGenerate={handleAutoGenerateVersionName}
        isLoading={isLoading}
      />
      <DocumentationCenterModal
        isOpen={isDocsModalOpen}
        onClose={() => setIsDocsModalOpen(false)}
        onLoadVersion={handleLoadVersion}
        onDeleteVersion={handleDeleteVersion}
        onDownload={() => {}}
        isLoading={isLoading}
      />
      <ProjectFilesModal
        isOpen={isProjectFilesModalOpen}
        onClose={() => setIsProjectFilesModalOpen(false)}
        onAttachFile={handleAttachProjectFileToChat}
        onDownloadFile={handleDownloadProjectFile}
        isLoading={isLoading}
      />
      <SessionManagerModal
        isOpen={isSessionManagerModalOpen}
        onClose={() => setIsSessionManagerModalOpen(false)}
        onImportFile={handleImportFile}
        onLoadSession={(state) => { handleLoadSession(state); setIsSessionManagerModalOpen(false); }}
        onDeleteSession={handleDeleteImportedSession}
        isLoading={isLoading}
      <AdversarialReportGenerator
        isOpen={isReportGeneratorModalOpen}
        onClose={() => {
            setIsReportGeneratorModalOpen(false);
            setAdversarialReportContent(null);
        }}
        onGenerate={handleGenerateAdversarialReport}
        isLoading={isGeneratingReport || isLoading}
        reportContent={adversarialReportContent}
      />
      <LiveReconModal
        isOpen={isReconModalOpen}
        onClose={() => setIsReconModalOpen(false)}
      />
      <PayloadCraftingModal
        isOpen={isPayloadCraftingModalOpen}
        onClose={() => setIsPayloadCraftingModalOpen(false)}
      />
      <ThreatVectorModal
        isOpen={isThreatVectorModalOpen}
        onClose={() => setIsThreatVectorModalOpen(false)}
      />
      <HelpModal
        isOpen={isHelpModalOpen}
        onClose={() => setIsHelpModalOpen(false)}
      />
    </div>
  );
};

export default App;

// services.ts
import { GoogleGenAI, Type } from "@google/genai";
import { GEMINI_MODELS } from './constants.ts';
import { ProjectFile } from './types.ts';

class GeminiService {
  private ai: GoogleGenAI | null;

  constructor() {
    this.ai = process.env.API_KEY ? new GoogleGenAI({ apiKey: process.env.API_KEY }) : null;
  }

  isConfigured(): boolean {
    return this.ai !== null;
  }
  
  getAiClient(): GoogleGenAI | null {
    return this.ai;
  }

  buildPromptWithProjectFiles(mainPrompt: string, projectFiles: ProjectFile[], options: { textOnly?: boolean } = {}): string | { parts: any[] } {
    if (projectFiles.length === 0) {
      return mainPrompt;
    }

    let combinedText = `The user has provided the following project files for context. Use them to inform your response.\n\n`;
    const imageParts: { inlineData: { mimeType: string; data: string; } }[] = [];

    projectFiles.forEach(file => {
      if (file.mimeType.startsWith('image/') && !options.textOnly) {
        imageParts.push({
          inlineData: {
            mimeType: file.mimeType,
            data: file.content, // content is base64 for images
          },
        });
        combinedText += `- Image file attached: ${file.name}\n`;
      } else if (!file.mimeType.startsWith('image/')) {
        combinedText += `--- PROJECT FILE: ${file.name} ---\n\`\`\`\n${file.content}\n\`\`\`\n\n`;
      }
    });

    if (imageParts.length > 0) {
      return {
        parts: [
          { text: combinedText + mainPrompt },
          ...imageParts
        ]
      };
    }

    return combinedText + mainPrompt;
  }

  async generateContentStream(
    contents: string | { parts: any[] },
    systemInstruction: string,
    model: string,
    onChunk: (chunk: string) => void
  ): Promise<string> {
    if (!this.ai) {
      throw new Error("API Key not configured.");
    }

    const stream = await this.ai.models.generateContentStream({
      model: model,
      contents: contents,
      config: {
        systemInstruction: systemInstruction,
        temperature: 0.7,
        stream: true
      }
    });

    let fullResponse = '';
    for await (const chunk of stream) {
      const textChunk = chunk.text;
      fullResponse += textChunk;
      onChunk(textChunk);
    }

    return fullResponse;
  }

  async generateContentStreamWithSources(
    contents: string | { parts: any[] },
    systemInstruction: string,
    model: string,
    onChunk: (chunk: string) => void
  ): Promise<string> {
    if (!this.ai) {
      throw new Error("API Key not configured.");
    }

    const stream = await this.ai.models.generateContentStream({
      model: model,
      contents: contents,
      config: {
        systemInstruction: systemInstruction,
        temperature: 0.7,
        stream: true
      }
    });

    let fullResponse = '';
    for await (const chunk of stream) {
      const textChunk = chunk.text;
      fullResponse += textChunk;
      onChunk(textChunk);
    }

    // Append sources if available
    const sourcesList = stream.metadata?.sources || [];
    if (sourcesList.length > 0) {
      let sourcesText = '\n\n## Sources\n';
      sourcesList.forEach((source, index) => {
        sourcesText += `${index + 1}. ${source.url}\n`;
      });
      fullResponse += sourcesText;
      onChunk(sourcesText);
    }

    return fullResponse;
  }
  
  async generateJson(
    { contents, systemInstruction, model, schema }:
    { contents: string | { parts: any[] }; systemInstruction: string; model: string; schema: any }
  ): Promise<any> {
    if (!this.ai) {
      throw new Error("API Key not configured.");
    }
    
    const response = await this.ai.models.generateContent({
      model: model,
      contents: contents,
      config: {
        systemInstruction: systemInstruction,
        responseMimeType: 'application/json',
        responseSchema: schema,
      }
    });
    
    const rawJson = response.text;
    return JSON.parse(rawJson);
  }

  async generateText(
    { contents, systemInstruction, model }:
    { contents: string | { parts: any[] }; systemInstruction: string; model: string; }
  ): Promise<string> {
    if (!this.ai) {
        throw new Error("API Key not configured.");
    }
    
    const response = await this.ai.models.generateContent({
        model: model,
        contents: contents,
        config: {
            systemInstruction: systemInstruction,
            temperature: 0.7,
        }
    });

    return response.text;
  }
}

// Export a singleton instance of the service
export const geminiService = new GeminiService();

// utils.ts
// Unicode-safe Base64 encoding/decoding to prevent DOMException on special characters
export const b64EncodeUnicode = (str: string): string => {
    return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, (match, p1) => {
        return String.fromCharCode(parseInt(p1, 16));
    }));
};

export const b64DecodeUnicode = (str: string): string => {
    try {
        return decodeURIComponent(atob(str).split('').map((c) => {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
    } catch (e) {
        // Fallback for legacy ASCII-only exports
        return atob(str);
    }
};

// Extracts markdown files with filenames from a response.
export const extractGeneratedMarkdownFiles = (responseText: string): { name: string, content: string }[] => {
    const files: { name: string, content: string }[] = [];
    const codeBlockRegex = /```([a-zA-Z0-9-:]*)\n([\s\S]*?)\n```/g;
    const matches = [...responseText.matchAll(codeBlockRegex)];

    matches.forEach((match) => {
        const langInfo = match[1] || '';
        const code = match[2].trim();
        const language = langInfo.split(':')[0].trim().toLowerCase();

        if (language === 'markdown' || language === 'md') {
            let fileName = langInfo.split(':')[1]?.trim() || 'generated.md';
            files.push({ name: fileName, content: code });
        }
    });

    return files;
};

/**
 * extractFinalCodeBlock
 * Robust extraction of the final code revision block from LLM responses.
 * Prioritizes explicitly tagged "Revised Code" sections over line-count heuristics.
 */
export const extractFinalCodeBlock = (response: string, isInitialReview: boolean): string | null => {
    // Priority 1: Explicitly tagged revision blocks (HUD Standard)
    const revisedCodeRegex = /###\s*(?:Revised|Updated|Full|Optimized|Final)\s+(?:Code|Script|Revision)\s*`{3}(?:[a-zA-Z0-9-]*)?\n([\s\S]*?)\n`{3}/im;
    const headingMatch = response.match(revisedCodeRegex);
    if (headingMatch && headingMatch[1]) {
      return headingMatch[1].trim();
    }
    
    // Priority 2: Fallback for initial reviews (the last significant code block)
    if (isInitialReview) {
      const allCodeBlocksRegex = /`{3}(?:[a-zA-Z0-9-]*)?\n([\s\S]*?)\n`{3}/g;
      const matches = [...response.matchAll(allCodeBlocksRegex)];
      
      if (matches.length > 0) {
        const lastMatch = matches[matches.length - 1];
        if (lastMatch && lastMatch[1]) {
          const content = lastMatch[1].trim();
          // Smarter heuristic: must look like code (contain common syntax markers) or be significant length
          const looksLikeCode = /[{};()=>]/.test(content) || content.split('\n').length > 1;
          if (looksLikeCode) {
            return content;
          }
        }
      }
    }

    return null;
};

// PersistenceContext.tsx
import React, { createContext, useState, useContext, useMemo } from 'react';
import { ProjectFile, Version, ImportedSession } from '../types.ts';

// A custom hook to manage state with localStorage persistence.
export const usePersistentState = <T,>(storageKey: string, defaultValue: T): [T, React.Dispatch<React.SetStateAction<T>>] => {
    const [state, setState] = useState<T>(() => {
        try {
            const item = window.localStorage.getItem(storageKey);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error(`Error reading localStorage key "${storageKey}":`, error);
            return defaultValue;
        }
    });

    React.useEffect(() => {
        try {
            window.localStorage.setItem(storageKey, JSON.stringify(state));
        } catch (error) {
            console.error(`Error setting localStorage key "${storageKey}":`, error);
        }
    }, [storageKey, state]);

    return [state, setState];
};

interface PersistenceContextType {
  projectFiles: ProjectFile[];
  versions: Version[];
  importedSessions: ImportedSession[];
  setProjectFiles: React.Dispatch<React.SetStateAction<ProjectFile[]>>;
  setVersions: React.Dispatch<React.SetStateAction<Version[]>>;
  setImportedSessions: React.Dispatch<React.SetStateAction<ImportedSession[]>>;
}

const PersistenceContext = createContext<PersistenceContextType | undefined>(undefined);

export const PersistenceProvider: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const [projectFiles, setProjectFiles] = usePersistentState<ProjectFile[]>('projectFiles', []);
  const [versions, setVersions] = usePersistentState<Version[]>('codeReviewVersions', []);
  const [importedSessions, setImportedSessions] = usePersistentState<ImportedSession[]>('importedSessions', []);
  
  const value = useMemo(() => ({
    projectFiles, setProjectFiles,
    versions, setVersions,
    importedSessions, setImportedSessions,
  }), [projectFiles, versions, importedSessions, setProjectFiles, setVersions, setImportedSessions]);

  return <PersistenceContext.Provider value={value}>{children}</PersistenceContext.Provider>;
}

export const usePersistenceContext = (): PersistenceContextType => {
  const context = useContext(PersistenceContext);
  if (!context) {
    throw new Error('usePersistenceContext must be used within a PersistenceProvider');
  }
  return context;
};

// AdversarialReportGenerator.tsx
import React, { useState, useCallback } from 'react';
import { Button } from './Button.tsx';
import { MarkdownRenderer } from './MarkdownRenderer.tsx';
import { CheckIcon, CopyIcon, ImportIcon } from './Icons.tsx';
import { AnalysisProgress } from './AnalysisProgress.tsx';
import { useSessionActionsContext } from '../contexts/SessionContext.tsx';

interface AdversarialReportGeneratorProps {
  isOpen: boolean;
  onClose: () => void;
  onGenerate: (reconData: string, targetHostname: string) => void;
  isLoading: boolean;
  reportContent: string | null;
}

const reportGenerationSteps = [
  "Analyzing recon data...",
  "Identifying potential exploit chains...",
  "Estimating CVSS scores...",
  "Formatting high-impact report...",
];

export const AdversarialReportGenerator: React.FC<AdversarialReportGeneratorProps> = ({
  isOpen,
  onClose,
  onGenerate,
  isLoading,
  reportContent,
}) => {
  const [reconData, setReconData] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [targetHostname, setTargetHostname] = useState('');
  const [isCopied, setIsCopied] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFile = (file: File) => {
    setError(null);
    if (file && file.type === 'application/json') {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target?.result as string);
          setReconData(JSON.stringify(data, null, 2));
          setFileName(file.name);
        } catch {
          setError('Invalid JSON file');
        }
      };
      reader.readAsText(file);
    } else {
      setError('Please upload a JSON file');
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const handleCopy = async () => {
    if (reportContent) {
      await navigator.clipboard.writeText(reportContent);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    if (reportContent) {
      const blob = new Blob([reportContent], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'adversarial_report.md';
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  const handleGenerate = () => {
    if (reconData && targetHostname) {
      onGenerate(reconData, targetHostname);
    } else {
      setError('Please provide recon data and target hostname');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/90 backdrop-blur-md z-50 flex items-center justify-center p-4 animate-fade-in">
      <div className="hud-panel w-full max-w-4xl h-[80vh] flex flex-col relative">
        <div className="hud-corner corner-top-left"></div>
        <div className="hud-corner corner-top-right"></div>
        <div className="hud-corner corner-bottom-left"></div>
        <div className="hud-corner corner-bottom-right"></div>

        <div className="flex justify-between items-center mb-4 flex-shrink-0">
          <h2 className="text-xl">Adversarial Report Generator</h2>
          <button onClick={onClose} className="p-1 hover:bg-white/10" aria-label="Close report generator">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="flex-grow min-h-0 overflow-y-auto pr-2">
          {!reportContent ? (
            <div className="space-y-4">
              {error && <p className="text-[var(--red-color)] text-center">{error}</p>}
              <div 
                onDrop={handleDrop}
                onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                onDragLeave={() => setDragOver(false)}
                className={`border-2 border-dashed border-[var(--hud-color-darker)] p-6 text-center cursor-pointer transition-colors ${dragOver ? 'border-[var(--hud-color)] bg-[var(--hud-color)]/10' : ''}`}
              >
                <p className="text-lg mb-2">Drop Recon JSON Here</p>
                <p className="text-sm text-[var(--hud-color-darker)]">or</p>
                <Button onClick={() => document.getElementById('recon-file')?.click()} variant="secondary" className="mt-2">
                  Upload File
                </Button>
                <input type="file" id="recon-file" className="hidden" accept=".json" onChange={(e) => handleFile(e.target.files?.[0] as File)} />
                {fileName && <p className="mt-2 text-sm">Loaded: {fileName}</p>}
              </div>

              <input
                type="text"
                value={targetHostname}
                onChange={(e) => setTargetHostname(e.target.value)}
                placeholder="Target Hostname (e.g., example.com)"
                className="w-full p-3 bg-black/70 border border-[var(--hud-color-darker)] text-[var(--hud-color)] focus:ring-2 focus:ring-[var(--bright-cyan)]"
              />

              <Button onClick={handleGenerate} disabled={!reconData || isLoading} isLoading={isLoading}>
                Generate Report
              </Button>
            </div>
          ) : (
            <div className="flex-grow flex flex-col min-h-0">
                <div className="flex-grow overflow-y-auto pr-2 border border-[var(--hud-color-darkest)] p-3 bg-black/30">
                    {isLoading && !reportContent ? (
                        <AnalysisProgress steps={reportGenerationSteps} />
                    ) : (
                        <MarkdownRenderer markdown={reportContent || ''} />
                    )}
                </div>
                {!isLoading && reportContent && (
                    <div className="flex-shrink-0 mt-4 flex justify-end items-center gap-3 animate-fade-in">
                        <Button onClick={handleCopy} variant="secondary">
                            {isCopied ? <CheckIcon className="w-4 h-4 mr-2" /> : <CopyIcon className="w-4 h-4 mr-2" />}
                            {isCopied ? 'Copied' : 'Copy Markdown'}
                        </Button>
                        <Button onClick={handleDownload} variant="primary">
                            <ImportIcon className="w-4 h-4 mr-2" />
                            Download .md
                        </Button>
                    </div>
                )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// DocumentationCenterModal.tsx
import React, { useState } from 'react';
import { useConfigContext, useInputContext } from '../AppContext.tsx';
import { useSessionActionsContext } from '../contexts/SessionContext.tsx';
import { Version } from '../types.ts';
import { Button } from './Button.tsx';
import { BoltIcon, DeleteIcon, ImportIcon, SaveIcon as LoadIcon } from './Icons.tsx';
import { usePersistenceContext } from '../contexts/PersistenceContext.tsx';


interface DocumentationCenterModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLoadVersion: (version: Version) => void;
  onDeleteVersion: (versionId: string) => void;
  onDownload: (content: string, filename: string) => void;
  isLoading?: boolean;
}

type ActiveTab = 'generate' | 'saved';

const timeAgo = (timestamp: number): string => {
    const seconds = Math.floor((new Date().getTime() - timestamp) / 1000);
    if (seconds < 60) return "just now";
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
}


const TabButton: React.FC<{ active: boolean; onClick: () => void; children: React.ReactNode }> = ({ active, onClick, children }) => (
    <button
        onClick={onClick}
        className={`px-4 py-2 text-sm uppercase tracking-wider transition-all duration-150 ${
            active ? 'bg-[var(--hud-color)]/10 border-b-2 border-[var(--hud-color)]' : 'text-[var(--hud-color-darker)] hover:text-[var(--hud-color)]'
        }`}
    >
        {children}
    </button>
);

export const DocumentationCenterModal: React.FC<DocumentationCenterModalProps> = ({ isOpen, onClose, onLoadVersion, onDeleteVersion, onDownload, isLoading = false }) => {
  const [activeTab, setActiveTab] = useState<ActiveTab>('generate');
  const { generatedDocs } = useOutputContext();
  const { handleGenerateDocs } = useSessionActionsContext();
  const { versions } = usePersistenceContext();

  if (!isOpen) return null;

  const renderGenerateTab = () => (
    <div className="space-y-4">
      <Button onClick={handleGenerateDocs} disabled={isLoading} isLoading={isLoading}>
        <BoltIcon className="w-4 h-4 mr-2" />
        Generate Docs
      </Button>
      {generatedDocs && (
        <div className="border border-[var(--hud-color-darkest)] p-3 bg-black/30 overflow-y-auto max-h-96">
          <MarkdownRenderer markdown={generatedDocs} />
        </div>
      )}
    </div>
  );

  const renderSavedTab = () => (
    <div className="space-y-2 overflow-y-auto max-h-96 pr-2">
      {versions.map(version => (
        <div key={version.id} className="border border-[var(--hud-color-darkest)] p-3 flex items-center justify-between">
          <div>
            <p className="font-bold">{version.name}</p>
            <p className="text-sm text-[var(--hud-color-darker)]">{timeAgo(version.timestamp)}</p>
          </div>
          <div className="flex space-x-2">
            <Button onClick={() => onLoadVersion(version)} variant="secondary" className="p-1">
              <LoadIcon className="w-4 h-4" />
            </Button>
            <Button onClick={() => onDeleteVersion(version.id)} variant="danger" className="p-1">
              <DeleteIcon className="w-4 h-4" />
            </Button>
            <Button onClick={() => onDownload(version.reviewOutput, `${version.name}.md`)} variant="primary" className="p-1">
              <ImportIcon className="w-4 h-4" />
            </Button>
          </div>
        </div>
      ))}
      {versions.length === 0 && <p className="text-center text-[var(--hud-color-darker)]">No saved documentation yet.</p>}
    </div>
  );

  return (
    <div className="fixed inset-0 bg-black/90 backdrop-blur-md z-50 flex items-center justify-center p-4 animate-fade-in">
      <div className="hud-panel w-full max-w-3xl h-[70vh] flex flex-col relative">
        <div className="hud-corner corner-top-left"></div>
        <div className="hud-corner corner-top-right"></div>
        <div className="hud-corner corner-bottom-left"></div>
        <div className="hud-corner corner-bottom-right"></div>
        
        <div className="flex justify-between items-center flex-shrink-0 relative">
            <h2 id="docs-modal-title" className="text-xl">Documentation Center</h2>
            <button
                onClick={onClose}
                className="absolute -top-4 -right-4 p-1.5 rounded-full hover:bg-white/10 focus:outline-none focus:ring-1 focus:ring-[var(--hud-color)]"
                aria-label="Close documentation center"
                disabled={isLoading}
            >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>

        <div className="flex-shrink-0 border-b border-[var(--hud-color-darkest)] my-4">
            <TabButton active={activeTab === 'generate'} onClick={() => setActiveTab('generate')}>Generate New</TabButton>
            <TabButton active={activeTab === 'saved'} onClick={() => setActiveTab('saved')}>Saved Documentation</TabButton>
        </div>

        <div className="flex-grow min-h-0 overflow-y-auto">
            {activeTab === 'generate' ? renderGenerateTab() : renderSavedTab()}
        </div>
      </div>
    </div>
  );
};

// LoadingSpinner.tsx
import React, { useState, useEffect } from 'react';

interface LoadingSpinnerProps {
  size?: string; // e.g., 'w-8 h-8'
  color?: string; // e.g., 'text-[#15fafa]'
  className?: string; // Allow passing additional classes
}

const spinnerChars = ['●○○○○○○○○○', '○●○○○○○○○○', '○○●○○○○○○○', '○○○●○○○○○○', '○○○○●○○○○○', '○○○○○●○○○○', '○○○○○○●○○○', '○○○○○○○●○○', '○○○○○○○○●○', '○○○○○○○○○●'];

export const LoadingSpinner = ({ size = 'w-8 h-8', color = 'text-[#15fafa]', className = '' }: LoadingSpinnerProps) => {
  const [charIndex, setCharIndex] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCharIndex(prevIndex => (prevIndex + 1) % spinnerChars.length);
    }, 80);

    return () => clearInterval(intervalId);
  }, []);

  const getFontSizeClass = () => {
    if (size.includes('12')) return 'text-5xl';
    if (size.includes('10')) return 'text-4xl';
    if (size.includes('8')) return 'text-3xl';
    if (size.includes('6')) return 'text-2xl';
    if (size.includes('5')) return 'text-xl';
    return 'text-lg'; // default for smaller sizes
  }

  return (
    <div 
      className={`flex items-center justify-center ${size} ${className}`}
      role="status"
      aria-label="Loading"
    >
      <span className={`${color} ${getFontSizeClass()} leading-none`}>
        {spinnerChars[charIndex]}
      </span>
    </div>
  );
};

// CodeInput.tsx
import React, { useState, useRef } from 'react';
import { useConfigContext, useInputContext, useActionsContext } from '../AppContext.tsx';
import { useLoadingStateContext, useChatStateContext, useSessionActionsContext } from '../contexts/SessionContext.tsx';
import { SupportedLanguage, ReviewProfile } from '../types.ts';
import { Button } from './Button.tsx';
import { Select } from './Select.tsx';
import { SUPPORTED_LANGUAGES, generateReviewerTemplate, PLACEHOLDER_MARKER, REVIEW_PROFILES } from '../constants.ts';
import { ChatInterface } from './ChatInterface.tsx';
import { StopIcon } from './Icons.tsx';
import { ContextFilesSelector } from './ContextFilesSelector.tsx';
import { Tooltip } from './Tooltip.tsx';

interface CodeInputProps {
  isActive: boolean;
  onAttachFileClick: () => void;
  onOpenProjectFilesModal: () => void;
}

export const CodeInput: React.FC<CodeInputProps> = (props) => {
  const { isActive, onSaveChatSession, onAttachFileClick, onOpenProjectFilesModal } = props;
  const { isLoading, loadingAction } = useLoadingStateContext();
  const { isChatMode, contextFileIds } = useChatStateContext();
  const { 
    handleReviewSubmit, handleExplainSelection, handleReviewSelection,
    handleStopGenerating, handleContextFileSelectionChange
  } = useSessionActionsContext();
  
  const {
    language, setLanguage, reviewProfile, setReviewProfile,
    customReviewInstructions, setCustomReviewInstructions
  } = useConfigContext();
  const { userOnlyCode, setUserOnlyCode } = useInputContext();

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [selectedText, setSelectedText] = useState('');

  const handleCodeChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setUserOnlyCode(e.target.value);
  };

  const handleSelection = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      const text = textarea.value.substring(textarea.selectionStart, textarea.selectionEnd);
      setSelectedText(text.trim());
    }
  };

  if (!isActive) return null;

  return (
    <div className="flex flex-col h-full min-h-0">
      <div className="flex-grow min-h-0">
        <div className="flex space-x-4 mb-4">
          <Tooltip text="Select the language of your code.">
            <Select
              options={SUPPORTED_LANGUAGES}
              value={language}
              onChange={(value) => setLanguage(value as SupportedLanguage)}
              aria-label="Select language"
              disabled={isLoading}
            />
          </Tooltip>
          <Tooltip text="Select the review profile or use custom instructions.">
            <Select
              options={REVIEW_PROFILES}
              value={reviewProfile}
              onChange={(value) => setReviewProfile(value as ReviewProfile)}
              aria-label="Select review profile"
              disabled={isLoading}
            />
          </Tooltip>
        </div>

        {reviewProfile === ReviewProfile.CUSTOM && (
          <textarea
            className="w-full h-24 p-3 mb-4 font-mono text-sm text-[var(--hud-color)] bg-black/70 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-black focus:ring-[var(--bright-cyan)] resize-none border border-[var(--hud-color-darker)]"
            value={customReviewInstructions}
            onChange={(e) => setCustomReviewInstructions(e.target.value)}
            placeholder="Enter custom review instructions..."
            disabled={isLoading}
          />
        )}

        <div className="relative flex-grow">
          <textarea
            ref={textareaRef}
            className="block w-full h-full p-3 font-mono text-sm text-[var(--hud-color)] bg-black/70 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-black focus:ring-[var(--bright-cyan)] resize-none placeholder:text-transparent transition-all duration-150 border border-[var(--hud-color-darker)]"
            value={userOnlyCode}
            onChange={handleCodeChange}
            onMouseUp={handleSelection}
            onKeyUp={handleSelection}
            placeholder="Enter code here..."
            disabled={isLoading}
          />
        </div>
      </div>

      <ContextFilesSelector
        selectedFileIds={contextFileIds}
        onSelectionChange={handleContextFileSelectionChange}
      />

      <div className="flex-shrink-0 pt-4 mt-auto">
        {isLoading ? (
          <Button onClick={handleStopGenerating} variant="danger" className="w-full" aria-label="Stop generating review" title="Stop the current analysis.">
            <StopIcon className="w-5 h-5 mr-2" />
            Stop
          </Button>
        ) : (
          <Button onClick={handleReviewSubmit} disabled={!userOnlyCode.trim() || language === SupportedLanguage.OTHER || isLoading} className="w-full">
            Review Code
          </Button>
        )}
      </div>
      
      {selectedText && !isLoading && (
        <div className="bg-black/50 border border-[var(--hud-color-darkest)] p-3 space-y-2 animate-fade-in mt-3">
          <p className="text-xs text-center text-[var(--hud-color-darker)] uppercase tracking-wider">Action for selection:</p>
          <div className="flex items-center justify-center space-x-3">
            <Button 
              onClick={() => handleExplainSelection(selectedText)} 
              variant="secondary" 
              className="text-xs py-1.5 px-3"
              isLoading={isLoading && loadingAction === 'explain-selection'}
            >
              Explain
            </Button>
            <Button 
              onClick={() => handleReviewSelection(selectedText)} 
              variant="secondary" 
              className="text-xs py-1.5 px-3"
              isLoading={isLoading && loadingAction === 'review-selection'}
            >
              Review
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

// MarkdownRenderer.tsx
import React from 'react';
import { CodeBlock } from './CodeBlock.tsx';
import ErrorBoundary from './ErrorBoundary.tsx';
import { AccordionItem } from './AccordionItem.tsx';
import { GeneratedFile } from './GeneratedFile.tsx';

// Helper to parse simple inline markdown (bold, italic, code) into React nodes.
const parseInlineMarkdown = (text: string): React.ReactNode => {
  // Split the text by markdown delimiters, keeping them to check against.
  const parts = text.split(/(\*\*.*?\*\*|\*.*?\*|`[^`]+`)/g);
  
  return (
    <>
      {parts.map((part, index) => {
        if (!part) return null;
        if (part.startsWith('**') && part.endsWith('**')) {
          return <strong key={index} className="font-semibold text-white">{part.slice(2, -2)}</strong>;
        }
        if (part.startsWith('*') && part.endsWith('*')) {
          return <em key={index} className="italic text-[var(--hud-color)]">{part.slice(1, -1)}</em>;
        }
        if (part.startsWith('`') && part.endsWith('`')) {
          return <code key={index} className="bg-[var(--hud-color-darkest)] px-1.5 py-0.5 text-sm text-[var(--hud-color)] font-mono">{part.slice(1, -1)}</code>;
        }
        return part; // Return plain text as is
      })}
    </>
  );
};


// Component for rendering regular text blocks with inline markdown.
const TextBlock: React.FC<{ text: string }> = ({ text }) => (
  <p className="mb-4 leading-relaxed">{parseInlineMarkdown(text)}</p>
);

interface MarkdownRendererProps {
  markdown: string;
  onLoadCodeIntoWorkbench?: (code: string) => void;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ markdown, onLoadCodeIntoWorkbench }) => {
  // Split the markdown into parts: regular text and code blocks under headings.
  const parts = markdown.split(/(###\s*.+?)\n```/g);

  // Helper to render non-code parts (text with inline markdown).
  const renderRegularPart = (part: string, index: number) => {
    if (part.trim() === '') return null;

    if (part.startsWith('###')) {
      // It's a heading; the next part is its code block.
      return null; // Handled in main loop
    }

    // Split sub-parts by newlines for paragraphs.
    const subParts = part.split('\n\n');
    return (
      <React.Fragment key={index}>
        {subParts.map((subPart, subIndex) => (
          <TextBlock key={subIndex} text={subPart} />
        ))}
      </React.Fragment>
    );
  };

  return (
    <>
      {parts.map((part, index) => {
        if (index % 3 === 0) {
          return renderRegularPart(part, index);
        }
        
        if (index % 3 === 1) {
          const title = part.replace(/#+\s*/, '');
          const codeBlockPart = parts[index + 1];
          const codeBlockMatch = codeBlockPart?.match(/^([a-zA-Z0-9-]*)\n([\s\S]*?)$/);

          if (codeBlockMatch) {
            const [, language, code] = codeBlockMatch;
            return (
              <AccordionItem key={index} title={title} defaultOpen={false}>
                <ErrorBoundary>
                  <CodeBlock code={code.trim()} language={language} onLoadCodeIntoWorkbench={onLoadCodeIntoWorkbench} />
                </ErrorBoundary>
              </AccordionItem>
            );
          }
        }
        
        return null;
      })}
    </>
  );
};

// VersionHistoryModal.tsx
import React from 'react';
import { Version } from '../types.ts';
import { VersionHistory } from './VersionHistory.tsx';
import { usePersistenceContext } from '../contexts/PersistenceContext.tsx';

interface VersionHistoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLoadVersion: (version: Version) => void;
  onDeleteVersion: (versionId: string) => void;
  onStartFollowUp: (version: Version) => void;
  onRenameVersion: (versionId: string, newName: string) => void;
  isLoading?: boolean;
}

export const VersionHistoryModal = ({ isOpen, onClose, isLoading = false, ...versionHistoryProps }: VersionHistoryModalProps) => {
  const { versions } = usePersistenceContext();
  
  if (!isOpen) return null;

  const handleLoadVersion = (version: Version) => {
    versionHistoryProps.onLoadVersion(version);
    onClose();
  };

  const handleStartFollowUp = (version: Version) => {
    versionHistoryProps.onStartFollowUp(version);
    onClose();
  };

  return (
    <div
      className="fixed inset-0 bg-black/90 backdrop-blur-md z-50 flex items-center justify-center p-4 transition-opacity duration-300 animate-fade-in"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="version-history-modal-title"
    >
      <div
        className="hud-panel w-full max-w-4xl h-[70vh] flex flex-col relative"
        onClick={e => e.stopPropagation()}
      >
        <div className="hud-corner corner-top-left"></div>
        <div className="hud-corner corner-top-right"></div>
        <div className="hud-corner corner-bottom-left"></div>
        <div className="hud-corner corner-bottom-right"></div>

        <div className="flex justify-end items-center flex-shrink-0 relative">
          <button
            onClick={onClose}
            className="absolute -top-4 -right-4 p-1.5 rounded-full hover:bg-white/10 focus:outline-none focus:ring-1 focus:ring-[var(--hud-color)]"
            aria-label="Close version history"
            disabled={isLoading}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div className="flex-grow min-h-0 overflow-hidden mt-2">
            <VersionHistory 
                {...versionHistoryProps}
                versions={versions}
                onLoadVersion={handleLoadVersion} 
                onStartFollowUp={handleStartFollowUp}
                isLoading={isLoading}
            />
        </div>
      </div>
    </div>
  );
};

// ReviewOutput.tsx
import React, { useRef, useState, useEffect, useMemo } from 'react';
import { useConfigContext } from '../AppContext.tsx';
import { useOutputContext, useLoadingStateContext, useSessionActionsContext } from '../contexts/SessionContext.tsx';
import { MarkdownRenderer } from './MarkdownRenderer.tsx';
import { AppMode, ReviewProfile } from '../types.ts';
import { SaveIcon, CopyIcon, CheckIcon, CompareIcon, ChatIcon, CommitIcon, BugIcon, BoltIcon, ImportIcon, RootCauseIcon } from './Icons.tsx';
import { LoadingSpinner } from './LoadingSpinner.tsx';
import { Button } from './Button.tsx';
import { FeatureMatrix } from './FeatureMatrix.tsx';
import { Tooltip } from './Tooltip.tsx';

interface ReviewOutputProps {
  onSaveVersion: () => void;
  onShowDiff: () => void;
  isActive: boolean;
}

const analysisSteps = [
  'INITIATING ANALYSIS PROTOCOL',
  'PARSING ABSTRACT SYNTAX TREE',
  'CROSS-REFERENCING SECURITY VECTORS',
  'IDENTIFYING LOGIC FLAWS',
  'EVALUATING IDIOMATIC CONVENTIONS',
  'COMPILING FEEDBACK MATRIX',
  'GENERATING REVISION',
  'FINALIZING OUTPUT STREAM',
];

const AnalysisLoader: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(analysisSteps[0]);
  const [fade, setFade] = useState(true);

  useEffect(() => {
    let stepIndex = 0;
    const intervalId = setInterval(() => {
      setFade(false); // Start fade-out
      setTimeout(() => {
        stepIndex = (stepIndex + 1) % analysisSteps.length;
        setCurrentStep(analysisSteps[stepIndex]);
        setFade(true); // Fade-in new step
      }, 300);
    }, 2000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="text-center py-8">
      <LoadingSpinner size="w-16 h-16" className="mx-auto mb-4" />
      <p className={`text-lg transition-opacity duration-300 ${fade ? 'opacity-100' : 'opacity-0'}`}>
        {currentStep}
      </p>
    </div>
  );
};

export const ReviewOutput: React.FC<ReviewOutputProps> = ({ onSaveVersion, onShowDiff, isActive }) => {
  const { appMode } = useConfigContext();
  const {
    reviewOutput,
    revisedCode,
    generatedTests,
    generatedDocs,
    commitMessage,
    rootCauseAnalysis,
    features,
    featureDecisions,
    allFeaturesDecided,
    generatedFiles,
    showDiff: internalShowDiff,
    setShowDiff: setInternalShowDiff,
  } = useOutputContext();
  const { isLoading, loadingAction } = useLoadingStateContext();
  const {
    handleStartFollowUp,
    handleGenerateTests,
    handleGenerateDocs,
    handleGenerateCommitMessage,
    handleAnalyzeRootCause,
    handleFinalizeComparison,
    onSaveGeneratedFile,
  } = useSessionActionsContext();

  const [isCopied, setIsCopied] = useState(false);
  const [selectedText, setSelectedText] = useState('');

  const outputRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection()?.toString().trim();
      setSelectedText(selection || '');
    };
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, []);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(reviewOutput);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  const reviewAvailable = !!reviewOutput;
  const testsAvailable = !!generatedTests;
  const docsAvailable = !!generatedDocs;
  const commitMessageAvailable = !!commitMessage;
  const rootCauseAvailable = !!rootCauseAnalysis;
  const featuresAvailable = features.length > 0;

  const followUpButtonText = appMode === 'comparison' ? 'Finalize Features' : 'Follow Up';

  if (!isActive) return null;

  return (
    <div className="mt-8 flex flex-col h-full min-h-0">
      {isLoading ? (
        <AnalysisLoader />
      ) : reviewAvailable ? (
        <div className="border border-[var(--hud-color-darkest)] p-4 bg-black/30 overflow-y-auto flex-grow min-h-0 relative" ref={outputRef}>
          <MarkdownRenderer markdown={reviewOutput} onLoadCodeIntoWorkbench={() => {}} />
          {generatedFiles.map((file, index) => (
            <GeneratedFile key={index} name={file.name} content={file.content} onSave={onSaveGeneratedFile} />
          ))}
        </div>
      ) : (
        <p className="text-center text-[var(--hud-color-darker)] py-8">Submit code to begin analysis.</p>
      )}

      {featuresAvailable && (
        <div className="mt-4">
          <FeatureMatrix features={features} decisions={featureDecisions} onDecision={(feature, decision) => {
            setFeatureDecisions(prev => ({
              ...prev,
              [feature.name]: { decision, discussionHistory: [] }
            }));
          }} />
        </div>
      )}

      {reviewAvailable && !isLoading && (
        <div className="flex-shrink-0 mt-4 flex flex-wrap justify-center gap-3 animate-fade-in">
          <Tooltip text="View side-by-side diff of original and revised code.">
            <Button onClick={onShowDiff} variant="primary" className="post-review-button">
              <CompareIcon className="w-4 h-4 mr-2"/>
              Show Diff
            </Button>
          </Tooltip>
          <Tooltip text="Generate a conventional commit message based on the code changes.">
            <Button onClick={handleGenerateCommitMessage} disabled={!commitMessageAvailable} variant="primary" className="post-review-button">
                <CommitIcon className="w-4 h-4 mr-2" />
                Generate Commit
            </Button>
          </Tooltip>
          <Tooltip text="Start an interactive chat session to ask questions or request modifications.">
            <Button onClick={() => handleStartFollowUp()} variant="secondary" className="post-review-button">
                <ChatIcon className="w-4 h-4 mr-2" />
                {followUpButtonText}
            </Button>
          </Tooltip>
          <Tooltip text="Save this entire review session as a named version to load later.">
            <Button onClick={onSaveVersion} variant="secondary" className="post-review-button">
                <SaveIcon className="w-4 h-4 mr-2" />
                Save Version
            </Button>
          </Tooltip>
        </div>
      )}
    </div>
  );
};

// SegmentedControl.tsx
import React from 'react';
import { AppMode } from '../types.ts';
// FIX: Removed import for non-existent 'ShieldIcon'.
import { BugIcon, CodeIcon, CompareIconSvg } from './Icons.tsx';
import { Tooltip } from './Tooltip.tsx';

interface ModeOption {
  value: AppMode;
  label: string;
  Icon: React.FC<{ className?: string }>;
  description: string;
}

const MODES: ModeOption[] = [
  { value: 'debug', label: 'Debug', Icon: BugIcon, description: "Diagnose and fix code based on an error message." },
  { value: 'single', label: 'Single Review', Icon: CodeIcon, description: "Submit a single piece of code for a comprehensive analysis." },
  { value: 'comparison', label: 'Compare', Icon: CompareIconSvg, description: "Compare two codebases to merge and optimize them." },
];

interface SegmentedControlProps {
  currentMode: AppMode;
  onModeChange: (mode: AppMode) => void;
  disabled?: boolean;
}

export const SegmentedControl: React.FC<SegmentedControlProps> = ({ currentMode, onModeChange, disabled }) => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-6 animate-fade-in">
      <div className="flex items-center justify-center p-1 bg-black/30 backdrop-blur-md border border-[var(--hud-color-darkest)] space-x-1" role="tablist" aria-label="Application Modes">
        {MODES.map((mode) => {
          const isActive = currentMode === mode.value;
          return (
            <Tooltip key={mode.value} text={mode.description}>
              <button
                id={`tab-${mode.value}`}
                onClick={() => onModeChange(mode.value)}
                disabled={disabled}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-2 text-sm font-heading uppercase tracking-wider transition-all duration-200 border border-transparent
                  ${isActive
                    ? 'bg-[var(--hud-color)]/10 border-[var(--hud-color-darker)] text-[var(--hud-color)] animate-cyan-pulse'
                    : 'text-[var(--hud-color-darker)] hover:bg-[var(--hud-color)]/5 hover:text-[var(--hud-color)]'
                  }
                  ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
                `}
                role="tab"
                aria-selected={isActive}
                aria-controls={`panel-${mode.value}`}
              >
                <mode.Icon className="w-4 h-4" />
                <span className="hidden sm:inline">{mode.label}</span>
              </button>
            </Tooltip>
          );
        })}
      </div>
    </div>
  );
};

// ToastContainer.tsx
import React from 'react';
import { Toast } from '../types.ts';
import { ToastComponent } from './Toast.tsx';

interface ToastContainerProps {
  toasts: Toast[];
  onDismiss: (id: number) => void;
}

export const ToastContainer = ({ toasts, onDismiss }: ToastContainerProps) => {
  // Only show the last 3 toasts to prevent screen clutter during bulk operations
  const visibleToasts = toasts.slice(-3);

  return (
    <div
      className="fixed bottom-0 right-0 z-50 p-4 space-y-3 w-full max-w-md"
      aria-live="assertive"
    >
      {visibleToasts.map(toast => (
        <ToastComponent key={toast.id} toast={toast} onDismiss={onDismiss} />
      ))}
    </div>
  );
};

// Header.tsx
import React, { useState } from 'react';
import { ExportIcon, LogoIcon, ShareIcon, MenuIcon, StopIcon } from './Icons.tsx';
import { CommandMenu } from './CommandMenu.tsx';
import { Tooltip } from './Tooltip.tsx';
import { useLoadingStateContext, useSessionActionsContext } from '../contexts/SessionContext.tsx';

interface HeaderProps {
    onImportClick: () => void;
    onExportSession: () => void;
    onShare: () => void;
    onOpenDocsModal: () => void;
    onOpenProjectFilesModal: () => void;
    onToggleVersionHistory: () => void;
    onOpenReportGenerator: () => void;
    onOpenReconModal: () => void;
    onOpenPayloadCraftingModal: () => void;
    onOpenThreatVectorModal: () => void;
    onOpenHelpModal: () => void;
    isToolsEnabled: boolean;
    onEndChatSession: () => void;
    // Props that were previously from context
    isInputPanelVisible: boolean;
    setIsInputPanelVisible: React.Dispatch<React.SetStateAction<boolean>>;
    isChatMode: boolean;
    reviewAvailable: boolean;
    handleStartFollowUp: () => void;
    handleGenerateTests: () => void;
}

export const Header: React.FC<HeaderProps> = (props) => {
  const [isCommandMenuOpen, setIsCommandMenuOpen] = useState(false);
  const { isLoading, isChatLoading } = useLoadingStateContext();
  const { handleStopGenerating } = useSessionActionsContext();
  
  const showAbort = isLoading || isChatLoading;

  return (
    <header className="flex-shrink-0 p-4 border-b border-[var(--hud-color-darkest)] flex items-center justify-between animate-fade-in">
      <div className="flex items-center space-x-4">
        <LogoIcon className="w-8 h-8" />
        <h1 className="text-2xl font-heading">4ndr0 Debugger</h1>
      </div>
      <div className="flex items-center space-x-4">
        {showAbort && (
          <Tooltip text="Abort current operation">
            <button
              onClick={handleStopGenerating}
              className="p-2 text-[var(--red-color)] rounded-full transition-all duration-200 hover:bg-[var(--red-color)]/30 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-black focus:ring-[var(--red-color)]"
              aria-label="Abort Operation"
            >
              <StopIcon className="w-6 h-6" />
            </button>
          </Tooltip>
        )}
        <Tooltip text="Import session from JSON">
          <button onClick={props.onImportClick} className="p-2 text-[var(--hud-color)] rounded-full transition-all duration-200 hover:bg-[var(--hud-color)]/30 hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-black focus:ring-[var(--hud-color)]" aria-label="Import Session">
            <ImportIcon className="w-6 h-6" />
          </button>
        </Tooltip>
        <Tooltip text="Share session via URL">
          <button
            onClick={props.onShare}
            className="p-2 text-[var(--hud-color)] rounded-full transition-all duration-200 hover:bg-[var(--hud-color)]/30 hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-black focus:ring-[var(--hud-color)]"
            aria-label="Share Session via URL"
          >
            <ShareIcon className="w-6 h-6" />
          </button>
        </Tooltip>
        <Tooltip text="Export session to JSON">
          <button 
            onClick={props.onExportSession} 
            className="p-2 text-[var(--hud-color)] rounded-full transition-all duration-200 hover:bg-[var(--hud-color)]/30 hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-black focus:ring-[var(--hud-color)]"
            aria-label="Export Session"
          >
            <ExportIcon className="w-6 h-6" />
          </button>
        </Tooltip>
      </div>
    </header>

    <CommandMenu 
      isOpen={isCommandMenuOpen}
      onClose={() => setIsCommandMenuOpen(false)}
      {...props}
    />
  );
};

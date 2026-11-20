import React, { useState } from 'react';
import { 
  Copy, Check, Volume2, VolumeX, BookOpen, Sparkles, 
  Leaf, FlaskConical, ShieldAlert, Droplets, ShieldCheck, 
  ChevronRight, Info, CheckCircle2
} from 'lucide-react';

/**
 * FormattedAIMessage
 * High-performance, rich AI Markdown & agricultural card renderer.
 * Formats headings, bullet lists, numbered steps, bold highlights, 
 * dosage badges, callout cards (Organic, Chemical, Prevention),
 * copy-to-clipboard, and text-to-speech audio playback.
 */
export const FormattedAIMessage = ({ 
  content = '', 
  sender = 'assistant', 
  sources = [], 
  timestamp = '',
  lang = 'en'
}) => {
  const [copied, setCopied] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  // Copy plain text content to clipboard
  const handleCopy = () => {
    if (!content) return;
    navigator.clipboard.writeText(content).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }).catch(() => {});
  };

  // Text to Speech playback (Marathi & English)
  const handleToggleAudio = () => {
    if (!window.speechSynthesis) return;

    if (isPlayingAudio) {
      window.speechSynthesis.cancel();
      setIsPlayingAudio(false);
      return;
    }

    window.speechSynthesis.cancel();
    const cleanText = content
      .replace(/[#*`_~]/g, '')
      .replace(/\[.*?\]\(.*?\)/g, '')
      .trim();

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 0.95;

    // Detect language or Marathi characters
    const hasMarathiChars = /[\u0900-\u097F]/.test(cleanText);
    utterance.lang = (lang === 'mr' || hasMarathiChars) ? 'mr-IN' : 'en-US';

    utterance.onend = () => setIsPlayingAudio(false);
    utterance.onerror = () => setIsPlayingAudio(false);

    setIsPlayingAudio(true);
    window.speechSynthesis.speak(utterance);
  };

  // Helper to format inline bold, italic, and code badges
  const formatInlineText = (text) => {
    if (!text) return '';

    // Split by markdown patterns (**bold**, `code`, etc.)
    const parts = [];
    let remaining = text;
    let keyIdx = 0;

    // Regex for: **bold**, `code/dosage`, *italic*
    const inlineRegex = /(\*\*([^*]+)\*\*|`([^`]+)`|\*([^*]+)\*)/;

    while (remaining) {
      const match = remaining.match(inlineRegex);
      if (!match) {
        parts.push(<span key={keyIdx++}>{remaining}</span>);
        break;
      }

      const matchIdx = match.index;
      if (matchIdx > 0) {
        parts.push(<span key={keyIdx++}>{remaining.slice(0, matchIdx)}</span>);
      }

      const fullMatch = match[0];
      if (fullMatch.startsWith('**')) {
        parts.push(
          <strong key={keyIdx++} className="font-bold text-emerald-300 dark:text-emerald-400 light:text-emerald-700">
            {match[2]}
          </strong>
        );
      } else if (fullMatch.startsWith('`')) {
        parts.push(
          <span 
            key={keyIdx++} 
            className="px-1.5 py-0.5 mx-0.5 rounded-md font-mono text-[11px] font-semibold bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 dark:text-emerald-400 light:text-emerald-700"
          >
            {match[3]}
          </span>
        );
      } else if (fullMatch.startsWith('*')) {
        parts.push(
          <em key={keyIdx++} className="italic text-slate-300 dark:text-slate-300 light:text-slate-700">
            {match[4]}
          </em>
        );
      }

      remaining = remaining.slice(matchIdx + fullMatch.length);
    }

    return parts;
  };

  // Helper to detect specific section categories and return custom themed icons & headers
  const getHeadingMeta = (title) => {
    const lower = title.toLowerCase();
    if (lower.includes('organic') || lower.includes('सेंद्रिय') || lower.includes('bio') || lower.includes('neem')) {
      return {
        icon: <Leaf className="w-4 h-4 text-emerald-400" />,
        borderClass: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300 dark:text-emerald-300 light:text-emerald-800',
        badge: lang === 'mr' ? 'सेंद्रिय उपाय' : 'Organic Remedy'
      };
    }
    if (lower.includes('chemical') || lower.includes('रासायनिक') || lower.includes('spray') || lower.includes('fungicide') || lower.includes('pesticide')) {
      return {
        icon: <FlaskConical className="w-4 h-4 text-sky-400" />,
        borderClass: 'border-sky-500/30 bg-sky-500/10 text-sky-300 dark:text-sky-300 light:text-sky-800',
        badge: lang === 'mr' ? 'रासायनिक फवारणी' : 'Chemical Control'
      };
    }
    if (lower.includes('prevent') || lower.includes('प्रतिबंध') || lower.includes('काळजी') || lower.includes('precaution') || lower.includes('warning')) {
      return {
        icon: <ShieldCheck className="w-4 h-4 text-amber-400" />,
        borderClass: 'border-amber-500/30 bg-amber-500/10 text-amber-300 dark:text-amber-300 light:text-amber-800',
        badge: lang === 'mr' ? 'प्रतिबंधक काळजी' : 'Prevention'
      };
    }
    if (lower.includes('water') || lower.includes('पाणी') || lower.includes('irrigation') || lower.includes('सिंचन')) {
      return {
        icon: <Droplets className="w-4 h-4 text-cyan-400" />,
        borderClass: 'border-cyan-500/30 bg-cyan-500/10 text-cyan-300 dark:text-cyan-300 light:text-cyan-800',
        badge: lang === 'mr' ? 'पाणी व सिंचन' : 'Irrigation'
      };
    }
    return {
      icon: <Sparkles className="w-4 h-4 text-emerald-400" />,
      borderClass: 'border-emerald-500/20 bg-slate-800/40 text-emerald-300 dark:text-emerald-300 light:text-emerald-700',
      badge: null
    };
  };

  // Structured parser that turns raw markdown content into structured React elements
  const renderStructuredContent = () => {
    if (!content) return null;

    const lines = content.split('\n');
    const elements = [];
    let currentList = [];
    let currentListType = null; // 'ul' | 'ol'
    let elKey = 0;

    const flushList = () => {
      if (currentList.length > 0) {
        if (currentListType === 'ol') {
          elements.push(
            <div key={elKey++} className="my-2.5 space-y-2">
              {currentList.map((item, idx) => (
                <div key={idx} className="flex items-start gap-2.5 text-xs sm:text-sm">
                  <span className="shrink-0 w-5 h-5 rounded-full bg-emerald-500/20 border border-emerald-500/30 text-emerald-400 font-bold text-[11px] flex items-center justify-center mt-0.5">
                    {idx + 1}
                  </span>
                  <div className="flex-1 leading-relaxed text-slate-200 dark:text-slate-200 light:text-slate-800">
                    {item}
                  </div>
                </div>
              ))}
            </div>
          );
        } else {
          elements.push(
            <div key={elKey++} className="my-2.5 space-y-1.5">
              {currentList.map((item, idx) => (
                <div key={idx} className="flex items-start gap-2.5 text-xs sm:text-sm">
                  <span className="shrink-0 w-1.5 h-1.5 rounded-full bg-emerald-400 mt-2 shadow-sm shadow-emerald-400/50" />
                  <div className="flex-1 leading-relaxed text-slate-200 dark:text-slate-200 light:text-slate-800">
                    {item}
                  </div>
                </div>
              ))}
            </div>
          );
        }
        currentList = [];
        currentListType = null;
      }
    };

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      if (!line) {
        flushList();
        continue;
      }

      // 1. Headings (###, ##, #)
      if (line.startsWith('#')) {
        flushList();
        const headingLevel = line.match(/^#+/)[0].length;
        const cleanTitle = line.replace(/^#+\s*/, '').trim();
        const meta = getHeadingMeta(cleanTitle);

        elements.push(
          <div key={elKey++} className={`mt-3.5 mb-2 p-2.5 rounded-xl border flex items-center justify-between gap-2 ${meta.borderClass}`}>
            <div className="flex items-center gap-2 font-bold text-xs sm:text-sm">
              {meta.icon}
              <span>{formatInlineText(cleanTitle)}</span>
            </div>
            {meta.badge && (
              <span className="px-2 py-0.5 rounded-full bg-black/25 text-[10px] uppercase font-bold tracking-wider">
                {meta.badge}
              </span>
            )}
          </div>
        );
        continue;
      }

      // 2. Blockquotes or Callouts (> Note: or > )
      if (line.startsWith('>')) {
        flushList();
        const calloutText = line.replace(/^>\s*/, '').trim();
        elements.push(
          <div key={elKey++} className="my-2.5 p-3 rounded-xl bg-emerald-950/30 border-l-4 border-emerald-500 text-xs sm:text-sm leading-relaxed text-emerald-200/90 dark:text-emerald-200/90 light:text-emerald-900">
            {formatInlineText(calloutText)}
          </div>
        );
        continue;
      }

      // 3. Numbered lists (1. or 2.)
      const numMatch = line.match(/^(\d+)[.)]\s+(.+)/);
      if (numMatch) {
        if (currentListType && currentListType !== 'ol') {
          flushList();
        }
        currentListType = 'ol';
        currentList.push(formatInlineText(numMatch[2]));
        continue;
      }

      // 4. Bullet lists (-, *, •)
      const bulletMatch = line.match(/^[-*•]\s+(.+)/);
      if (bulletMatch) {
        if (currentListType && currentListType !== 'ul') {
          flushList();
        }
        currentListType = 'ul';
        currentList.push(formatInlineText(bulletMatch[1]));
        continue;
      }

      // 5. Standard paragraph
      flushList();
      elements.push(
        <p key={elKey++} className="my-1 text-xs sm:text-sm leading-relaxed text-slate-200 dark:text-slate-200 light:text-slate-800">
          {formatInlineText(line)}
        </p>
      );
    }

    flushList();
    return elements;
  };

  // If sender is user, render user bubble
  if (sender === 'user') {
    return (
      <div className="space-y-1">
        <p className="whitespace-pre-wrap text-xs sm:text-sm leading-relaxed font-medium">
          {content}
        </p>
        {timestamp && (
          <span className="text-[10px] text-white/70 block text-right">
            {timestamp}
          </span>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {/* Structured AI Message Content */}
      <div className="space-y-1">
        {renderStructuredContent()}
      </div>

      {/* Multi-Source Botanical Citations */}
      {sources && sources.length > 0 && (
        <div className="pt-2.5 mt-2 border-t border-slate-700/60 dark:border-white/[0.08] light:border-slate-200 space-y-1.5">
          <div className="flex items-center gap-1.5 text-[10px] font-bold text-emerald-400 dark:text-emerald-400 light:text-emerald-600">
            <BookOpen className="w-3 h-3" />
            <span>{lang === 'mr' ? 'तपासलेले कृषी संशोधन संदर्भ:' : 'Verified Agronomic Sources & Literature:'}</span>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {sources.map((src, sIdx) => (
              <a
                key={sIdx}
                href={src.url || '#'}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-[10px] text-slate-300 hover:text-emerald-400 transition"
                title={src.title}
              >
                <span className="font-semibold text-emerald-400">[{src.source || 'Ref'}]</span>
                <span className="max-w-[200px] truncate">{src.title}</span>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Action Footer (Copy, Audio Playback, Timestamp) */}
      <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 dark:border-white/[0.06] light:border-slate-200 text-[11px] text-slate-400">
        <div className="flex items-center gap-1.5">
          {/* Copy Button */}
          <button
            type="button"
            onClick={handleCopy}
            className="inline-flex items-center gap-1 px-2 py-1 rounded-lg hover:bg-slate-800 dark:hover:bg-slate-800 light:hover:bg-slate-100 transition text-[11px] text-slate-400 hover:text-emerald-400"
            title="Copy answer to clipboard"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span className="text-emerald-400 font-semibold">{lang === 'mr' ? 'प्रत तयार!' : 'Copied!'}</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>{lang === 'mr' ? 'प्रत करा' : 'Copy'}</span>
              </>
            )}
          </button>

          {/* Text-to-Speech Audio */}
          <button
            type="button"
            onClick={handleToggleAudio}
            className={`inline-flex items-center gap-1 px-2 py-1 rounded-lg transition text-[11px] ${
              isPlayingAudio 
                ? 'bg-emerald-500/20 text-emerald-400 font-bold animate-pulse' 
                : 'hover:bg-slate-800 dark:hover:bg-slate-800 light:hover:bg-slate-100 text-slate-400 hover:text-emerald-400'
            }`}
            title={isPlayingAudio ? 'Stop reading' : 'Listen to advisory'}
          >
            {isPlayingAudio ? (
              <>
                <VolumeX className="w-3.5 h-3.5" />
                <span>{lang === 'mr' ? 'थांबवा' : 'Stop'}</span>
              </>
            ) : (
              <>
                <Volume2 className="w-3.5 h-3.5" />
                <span>{lang === 'mr' ? 'ऐका' : 'Listen'}</span>
              </>
            )}
          </button>
        </div>

        {/* Timestamp */}
        {timestamp && (
          <span className="text-[10px] text-slate-500 dark:text-slate-500 light:text-slate-400">
            {timestamp}
          </span>
        )}
      </div>
    </div>
  );
};

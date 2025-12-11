import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

/**
 * Custom styled Markdown renderer matching Anote dark theme
 */
function MarkdownRenderer({ content }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      className="markdown-content"
      components={{
        // Headings
        h1: ({ node, ...props }) => (
          <h1 className="text-2xl font-bold text-anote-accent mb-3 mt-4" {...props} />
        ),
        h2: ({ node, ...props }) => (
          <h2 className="text-xl font-bold text-anote-accent mb-2 mt-3" {...props} />
        ),
        h3: ({ node, ...props }) => (
          <h3 className="text-lg font-semibold text-anote-text-primary mb-2 mt-2" {...props} />
        ),
        h4: ({ node, ...props }) => (
          <h4 className="text-base font-semibold text-anote-text-primary mb-1 mt-2" {...props} />
        ),

        // Paragraphs
        p: ({ node, ...props }) => (
          <p className="text-anote-text-primary mb-2 leading-relaxed" {...props} />
        ),

        // Bold and Italic
        strong: ({ node, ...props }) => (
          <strong className="font-bold text-anote-accent" {...props} />
        ),
        em: ({ node, ...props }) => (
          <em className="italic text-anote-text-primary" {...props} />
        ),

        // Links
        a: ({ node, ...props }) => (
          <a
            className="text-anote-accent hover:text-blue-300 underline"
            target="_blank"
            rel="noopener noreferrer"
            {...props}
          />
        ),

        // Lists
        ul: ({ node, ...props }) => (
          <ul className="list-disc list-inside mb-2 text-anote-text-primary space-y-1" {...props} />
        ),
        ol: ({ node, ...props }) => (
          <ol className="list-decimal list-inside mb-2 text-anote-text-primary space-y-1" {...props} />
        ),
        li: ({ node, ...props }) => (
          <li className="text-anote-text-primary ml-2" {...props} />
        ),

        // Code blocks
        code: ({ node, inline, ...props }) => {
          return inline ? (
            <code
              className="bg-gray-700 text-anote-accent px-1.5 py-0.5 rounded text-sm font-mono"
              {...props}
            />
          ) : (
            <code
              className="block bg-gray-900 text-anote-text-primary p-3 rounded-md overflow-x-auto text-sm font-mono mb-2"
              {...props}
            />
          );
        },
        pre: ({ node, ...props }) => (
          <pre className="bg-gray-900 rounded-md overflow-x-auto mb-2" {...props} />
        ),

        // Blockquotes
        blockquote: ({ node, ...props }) => (
          <blockquote
            className="border-l-4 border-anote-accent pl-4 py-1 italic text-anote-text-secondary mb-2"
            {...props}
          />
        ),

        // Horizontal rule
        hr: ({ node, ...props }) => (
          <hr className="border-gray-700 my-4" {...props} />
        ),

        // Tables
        table: ({ node, ...props }) => (
          <div className="overflow-x-auto mb-2">
            <table className="min-w-full border border-gray-700 rounded" {...props} />
          </div>
        ),
        thead: ({ node, ...props }) => (
          <thead className="bg-gray-700" {...props} />
        ),
        tbody: ({ node, ...props }) => (
          <tbody className="divide-y divide-gray-700" {...props} />
        ),
        tr: ({ node, ...props }) => (
          <tr className="hover:bg-gray-700 transition-colors" {...props} />
        ),
        th: ({ node, ...props }) => (
          <th className="px-4 py-2 text-left text-anote-text-primary font-semibold" {...props} />
        ),
        td: ({ node, ...props }) => (
          <td className="px-4 py-2 text-anote-text-secondary" {...props} />
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
}

export default MarkdownRenderer;

/**
 * Utility functions for handling Markdown text
 */

/**
 * Strips all Markdown formatting from text, leaving only plain content
 * @param {string} text - Text with Markdown formatting
 * @returns {string} - Plain text without Markdown
 */
export function stripMarkdown(text) {
  if (!text) return '';

  let stripped = text;

  // Remove bold (**text** or __text__)
  stripped = stripped.replace(/(\*\*|__)(.*?)\1/g, '$2');

  // Remove italic (*text* or _text_)
  stripped = stripped.replace(/(\*|_)(.*?)\1/g, '$2');

  // Remove strikethrough (~~text~~)
  stripped = stripped.replace(/~~(.*?)~~/g, '$1');

  // Remove headers (## Header or ### Header, etc.)
  stripped = stripped.replace(/^#{1,6}\s+/gm, '');

  // Remove inline code (`code`)
  stripped = stripped.replace(/`([^`]+)`/g, '$1');

  // Remove code blocks (```code```)
  stripped = stripped.replace(/```[\s\S]*?```/g, '');

  // Convert links [text](url) to just text
  stripped = stripped.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');

  // Remove images ![alt](url)
  stripped = stripped.replace(/!\[([^\]]*)\]\([^)]+\)/g, '$1');

  // Remove bullet points and list markers (-, *, +, 1.)
  stripped = stripped.replace(/^[\s]*[-*+]\s+/gm, '');
  stripped = stripped.replace(/^[\s]*\d+\.\s+/gm, '');

  // Remove blockquotes (> text)
  stripped = stripped.replace(/^>\s+/gm, '');

  // Remove horizontal rules (---, ***, ___)
  stripped = stripped.replace(/^[-*_]{3,}$/gm, '');

  // Clean up extra whitespace
  stripped = stripped.replace(/\n{3,}/g, '\n\n');
  stripped = stripped.trim();

  return stripped;
}

/**
 * Converts basic Markdown to HTML for display
 * @param {string} text - Text with Markdown formatting
 * @returns {string} - HTML string
 */
export function basicMarkdownToHtml(text) {
  if (!text) return '';

  let html = text;

  // Convert headers
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

  // Convert bold
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

  // Convert italic
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // Convert links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');

  // Convert line breaks
  html = html.replace(/\n/g, '<br>');

  return html;
}

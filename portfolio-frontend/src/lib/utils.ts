/**
 * Utility functions for the application
 */

/**
 * Highlights the main author name in a list of authors
 * This function searches for your name in the author list and wraps it in HTML to make it bold
 *
 * @param authors - Comma-separated list of author names
 * @param highlightName - The name to highlight (defaults to common author names)
 * @returns HTML string with the highlighted author
 */
export function highlightAuthor(authors: string, highlightName?: string): string {
  if (!authors) return '';

  // If no specific name provided, try to detect from common patterns
  // You can customize this to match your actual name
  const namesToHighlight = highlightName ? [highlightName] : [
    'Utsho Dey',
    'U. Dey',
    'Dey, U.',
    'Dey, Utsho'
  ];

  let result = authors;

  // Try to highlight any matching name
  for (const name of namesToHighlight) {
    const regex = new RegExp(`\\b(${name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})\\b`, 'gi');
    result = result.replace(regex, '<strong>$1</strong>');
  }

  return result;
}

import { profile } from '@/settings';

/**
 * Highlights the author's name in a list of authors by making it bold
 * @param authors - Comma-separated string of author names
 * @returns HTML string with the target author's name in bold
 */
export function highlightAuthor(authors: string): string {
  if (!authors) return '';

  const authorName = profile.author_name;
  if (!authorName) return authors;

  // Create a regex to match the author name (case-insensitive)
  const regex = new RegExp(`(${authorName})`, 'gi');

  // Replace the author name with a bold version
  return authors.replace(regex, '<strong>$1</strong>');
}

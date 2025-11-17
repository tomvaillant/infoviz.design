/**
 * API client for communicating with the FastAPI backend.
 */
import type {
  GraphicsExamplesResponse,
} from '$lib/types';

// Get API base URL from environment or default to empty for same-origin requests
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

/**
 * Handle API errors.
 */
function handleError(error: unknown): never {
  if (error instanceof Error) {
    throw error;
  }
  throw new Error('An unexpected error occurred');
}

/**
 * API Client for backend communication.
 */
export const apiClient = {
  /**
   * Fetch graphics inspiration examples from the backend.
   */
  async fetchGraphicsExamples(query: string): Promise<GraphicsExamplesResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/graphics/examples`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query })
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(error.detail || 'Failed to fetch graphics examples');
      }

      return await response.json();
    } catch (error) {
      return handleError(error);
    }
  }
};

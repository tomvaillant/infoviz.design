/**
 * API client for communicating with the FastAPI backend.
 */
import type {
  GraphicsExamplesResponse,
} from '$lib/types';
import { authStore } from '$lib/stores/auth';

// Get API base URL from environment or default to empty for same-origin requests
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

/**
 * Get the authorization header with Clerk token.
 */
async function getAuthHeaders(): Promise<HeadersInit> {
  const token = await authStore.getToken();
  if (!token) {
    throw new Error('Not authenticated');
  }

  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`
  };
}

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
   * Deduct credits for a scrape run.
   */
  async chargeCredits(amount: number): Promise<{ credits: number }> {
    try {
      const headers = await getAuthHeaders();

      const response = await fetch(`${API_BASE_URL}/api/scrapers/charge`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ amount })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to deduct credits');
      }

      return await response.json();
    } catch (error) {
      return handleError(error);
    }
  },

  /**
   * Get authentication status.
   */
  async getAuthStatus(): Promise<{ authenticated: boolean; user: any }> {
    try {
      const headers = {
        'Content-Type': 'application/json'
      };

      try {
        const authHeaders = await getAuthHeaders();
        Object.assign(headers, authHeaders);
      } catch {
        // No auth token available
      }

      const response = await fetch(`${API_BASE_URL}/api/auth/status`, {
        method: 'GET',
        headers
      });

      if (!response.ok) {
        return { authenticated: false, user: null };
      }

      return await response.json();
    } catch (error) {
      return { authenticated: false, user: null };
    }
  },

  /**
   * Fetch graphics inspiration examples from the backend.
   */
  async fetchGraphicsExamples(query: string): Promise<GraphicsExamplesResponse> {
    try {
      const headers = await getAuthHeaders();

      const response = await fetch(`${API_BASE_URL}/api/graphics/examples`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...headers
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

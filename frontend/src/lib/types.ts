/**
 * TypeScript type definitions for coJournalist frontend.
 */

// Auth types (Clerk-based)
export interface User {
	clerk_user_id: string;
	email: string;
	credits: number;
	timezone: string | null;
	needs_initialization: boolean;
	onboarding_completed: boolean;
}

export interface AuthState {
	authenticated: boolean;
	user: User | null;
}

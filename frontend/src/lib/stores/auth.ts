/**
 * Authentication store using Clerk.
 */
import { browser } from '$app/environment';
import { env as publicEnv } from '$env/dynamic/public';
import { writable, derived } from 'svelte/store';
import type { User, AuthState } from '$lib/types';
import type { Clerk } from '@clerk/clerk-js';
import { API_BASE_URL } from '$lib/config/api';

const clerkPublishableKey = publicEnv.PUBLIC_CLERK_PUBLISHABLE_KEY;
const apiBaseUrl = API_BASE_URL;
type SignInOptions = Parameters<Clerk['mountSignIn']>[1];
type SignUpOptions = Parameters<Clerk['mountSignUp']>[1];
type EmbeddedClerk = Clerk & {
	mountSignIn?: (element: HTMLElement, options?: SignInOptions) => Promise<void>;
	unmountSignIn?: (element: HTMLElement) => void;
	mountSignUp?: (element: HTMLElement, options?: SignUpOptions) => Promise<void>;
	unmountSignUp?: (element: HTMLElement) => void;
};

// Initialize Clerk client
let clerkClient: Clerk | null = null;
let clerkClientPromise: Promise<Clerk | null> | null = null;

type ClerkModule = typeof import('@clerk/clerk-js');
type ClerkConstructor = ClerkModule['Clerk'];

function resolveClerkConstructor(mod: ClerkModule): ClerkConstructor {
	if (typeof mod?.Clerk === 'function') {
		return mod.Clerk;
	}

	const defaultExport = (mod as Record<string, unknown>)?.default;

	if (typeof defaultExport === 'function') {
		return defaultExport as ClerkConstructor;
	}

	if (
		defaultExport &&
		typeof (defaultExport as Record<string, unknown>)?.Clerk === 'function'
	) {
		return (defaultExport as { Clerk: ClerkConstructor }).Clerk;
	}

	throw new Error('Unable to locate Clerk constructor');
}

async function initClerkClient(): Promise<Clerk | null> {
	if (!browser) return null;

	if (!clerkPublishableKey) {
		console.error('PUBLIC_CLERK_PUBLISHABLE_KEY is not set; Clerk cannot be initialized.');
		return null;
	}

	const mod = (await import('@clerk/clerk-js')) as ClerkModule;
	const ClerkConstructor = resolveClerkConstructor(mod);
	const clerk = new ClerkConstructor(clerkPublishableKey);

	await clerk.load();
	clerkClient = clerk;
	return clerkClient;
}

async function getClerkClient() {
	if (clerkClient || !browser) {
		return clerkClient;
	}

	if (!clerkClientPromise) {
		clerkClientPromise = initClerkClient().finally(() => {
			clerkClientPromise = null;
		});
	}

	return clerkClientPromise;
}

async function getSessionToken(clerkOverride?: Clerk | null): Promise<string | null> {
	const clerk = clerkOverride ?? (await getClerkClient());

	if (!clerk?.session) {
		return null;
	}

	let token: string | null = null;

	try {
		token = await clerk.session.getToken();
	} catch (error) {
		console.warn('Failed to read Clerk session token', error);
	}

	if (!token) {
		try {
			token = await (clerk.session.getToken as (options?: any) => Promise<string | null>)?.({
				skipCache: true
			});
		} catch (error) {
			console.warn('Failed to read Clerk session token with skipCache', error);
		}
	}

	// Validate token is not empty or literal "null"/"undefined"
	if (token && token.trim().length > 0 && token !== 'null' && token !== 'undefined') {
		return token;
	}

	return null;
}

function mapClerkUser(clerk: Clerk): User | null {
	const user = clerk?.user;

	if (!user || !user.emailAddresses?.length) {
		return null;
	}

	const publicMetadata = (user.publicMetadata as Record<string, unknown>) || {};
	const legacyMetadata =
		((user as { privateMetadata?: Record<string, unknown> })?.privateMetadata as
			| Record<string, unknown>
			| undefined) || {};
	const credits = Number(publicMetadata.credits ?? 0) || 0;
	const timezone =
		typeof publicMetadata.timezone === 'string'
			? publicMetadata.timezone
			: typeof legacyMetadata.timezone === 'string'
				? legacyMetadata.timezone
				: null;
	const needsInitialization = typeof publicMetadata.credits !== 'number';
	const onboardingCompleted =
		typeof publicMetadata.onboarding_completed === 'boolean'
			? (publicMetadata.onboarding_completed as boolean)
			: typeof legacyMetadata.onboarding_completed === 'boolean'
				? (legacyMetadata.onboarding_completed as boolean)
				: false;

	return {
		clerk_user_id: user.id,
		email: user.emailAddresses[0].emailAddress,
		credits,
		timezone,
		needs_initialization: needsInitialization,
		onboarding_completed: onboardingCompleted
	};
}

let backendUserSync: Promise<void> | null = null;

function createAuthStore() {
	const { subscribe, set, update } = writable<AuthState>({
		authenticated: false,
		user: null
	});

	async function syncUserFromBackend(clerk: Clerk, force = false) {
		if (!browser || !clerk?.session) return;

		const endpoint = `${apiBaseUrl}/auth/status`;

		if (backendUserSync && !force) {
			return backendUserSync;
		}

		backendUserSync = (async () => {
			try {
				const token = await getSessionToken(clerk);
				if (!token) return;

				const response = await fetch(endpoint, {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${token}`
					}
				});

				if (!response.ok) return;

				const payload = await response.json();
				if (!payload?.authenticated || !payload.user) return;

				console.log('[Auth] Synced user from backend, timezone:', payload.user.timezone);

				update((state) => {
					const existingUser =
						state.user ??
						({
							clerk_user_id: payload.user.clerk_user_id,
							email: payload.user.email ?? '',
							credits: 0,
							timezone: null,
							needs_initialization: Boolean(payload.user.needs_initialization),
							onboarding_completed: Boolean(payload.user.onboarding_completed)
						} satisfies User);

					const credits =
						typeof payload.user.credits === 'number'
							? payload.user.credits
							: existingUser.credits;
					const timezone =
						typeof payload.user.timezone === 'string'
							? payload.user.timezone
							: existingUser.timezone;
					const needsInitialization =
						typeof payload.user.needs_initialization === 'boolean'
							? payload.user.needs_initialization
							: existingUser.needs_initialization;
					const onboardingCompleted =
						typeof payload.user.onboarding_completed === 'boolean'
							? payload.user.onboarding_completed
							: existingUser.onboarding_completed;

					return {
						authenticated: true,
						user: {
							...existingUser,
							clerk_user_id: payload.user.clerk_user_id ?? existingUser.clerk_user_id,
							email: payload.user.email ?? existingUser.email,
							credits,
							timezone,
							needs_initialization: needsInitialization,
							onboarding_completed: onboardingCompleted
						}
					};
				});
			} catch (error) {
				console.warn('Failed to sync user metadata from backend', error);
			} finally {
				backendUserSync = null;
			}
		})();

		return backendUserSync;
	}

	async function mountSignInComponent(element: HTMLElement, options?: SignInOptions) {
		if (!browser || !element) return () => {};

		const clerk = (await getClerkClient()) as EmbeddedClerk | null;
		if (!clerk?.mountSignIn) {
			console.warn('Clerk SignIn component is not available.');
			return () => {};
		}

		await clerk.mountSignIn(element, options);
		return () => {
			try {
				clerk.unmountSignIn?.(element);
			} catch (error) {
				console.warn('Failed to unmount Clerk SignIn component', error);
			}
		};
	}

	async function mountSignUpComponent(element: HTMLElement, options?: SignUpOptions) {
		if (!browser || !element) return () => {};

		const clerk = (await getClerkClient()) as EmbeddedClerk | null;
		if (!clerk?.mountSignUp) {
			console.warn('Clerk SignUp component is not available.');
			return () => {};
		}

		await clerk.mountSignUp(element, options);
		return () => {
			try {
				clerk.unmountSignUp?.(element);
			} catch (error) {
				console.warn('Failed to unmount Clerk SignUp component', error);
			}
		};
	}

	async function persistTimezone(timezone: string) {
		if (!timezone) throw new Error('Timezone is required');

		console.log('[Auth] Persisting timezone:', timezone);

		const clerk = await getClerkClient();
		if (!clerk?.session) {
			throw new Error('You need to be signed in to set a timezone.');
		}

		const token = await getSessionToken(clerk);
		if (!token) {
			throw new Error(
				'Unable to verify your session. Please wait a moment and try again, or refresh the page.'
			);
		}

		const endpoint = `${apiBaseUrl}/auth/timezone`;

		const response = await fetch(endpoint, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			},
			body: JSON.stringify({ timezone })
		});

		if (!response.ok) {
			let message = 'Failed to update timezone.';
			try {
				const data = await response.json();
				if (data?.detail) message = data.detail;
			} catch {
				// ignore
			}
			throw new Error(message);
		}

		console.log('[Auth] Timezone saved to backend successfully');

		update((state) => {
			if (!state.user) return state;
			return {
				...state,
				user: {
					...state.user,
					timezone
				}
			};
		});

		// Refresh session and user to get updated token with new metadata
		console.log('[Auth] Reloading Clerk session and user...');
		await clerk.session?.reload();
		await clerk.user?.reload();

		// Give Clerk more time to propagate metadata
		await new Promise((resolve) => setTimeout(resolve, 600));

		// Sync from backend with retry logic
		console.log('[Auth] Syncing user from backend...');
		await syncUserFromBackend(clerk, true);

		// Verify timezone was set correctly
		let currentState: ReturnType<typeof get> | null = null;
		update((state) => {
			currentState = state;
			return state;
		});

		console.log('[Auth] Final timezone in store:', currentState?.user?.timezone);

		if (currentState?.user?.timezone !== timezone) {
			console.warn(
				'[Auth] Timezone mismatch after sync. Expected:',
				timezone,
				'Got:',
				currentState?.user?.timezone
			);
		}
	}

	return {
		subscribe,
		/**
		 * Initialize auth state from Clerk session.
		 */
		async init() {
			if (!browser) {
				return;
			}

			const clerk = await getClerkClient();

			const applyAuthState = () => {
				const user = clerk ? mapClerkUser(clerk) : null;
				set({
					authenticated: Boolean(user),
					user
				});
			};

			if (!clerk) {
				applyAuthState();
				return;
			}

			// Set initial state based on Clerk session
			// Only authenticated if clerk.user exists AND has email addresses
			applyAuthState();
			void syncUserFromBackend(clerk);

			// Listen for auth state changes
			clerk.addListener(() => {
				applyAuthState();
				void syncUserFromBackend(clerk);
			});
		},
		/**
		 * Mount Clerk UserButton component to a DOM element.
		 */
		mountUserButton(element: HTMLDivElement) {
			if (!browser) return;

			getClerkClient().then((clerk) => {
				clerk?.mountUserButton(element, {
					afterSignOutUrl: '/login'
				});
			});
		},
		/**
		 * Get session token for API calls.
		 */
		async getToken(): Promise<string | null> {
			return await getSessionToken();
		},
		/**
		 * Sign out the current user.
		 */
		async signOut() {
			const clerk = await getClerkClient();
			if (!clerk) return;
			await clerk.signOut();

			set({
				authenticated: false,
				user: null
			});
		},
		/**
		 * Open Clerk sign-in modal.
		 */
		async openSignIn() {
			const clerk = await getClerkClient();
			if (!clerk) return;
			await clerk.openSignIn({});
		},
		/**
		 * Open Clerk sign-up modal.
		 */
		async openSignUp() {
			const clerk = await getClerkClient();
			if (!clerk) return;
			await clerk.openSignUp({});
		},
		/**
		 * Mount inline Clerk Sign-In component.
		 */
		async mountSignIn(element: HTMLElement, options?: SignInOptions) {
			return await mountSignInComponent(element, options);
		},
		/**
		 * Mount inline Clerk Sign-Up component.
		 */
		async mountSignUp(element: HTMLElement, options?: SignUpOptions) {
			return await mountSignUpComponent(element, options);
		},
		/**
		 * Update the stored timezone for the current user.
		 */
		async updateTimezone(timezone: string) {
			await persistTimezone(timezone);
		},
		/**
		 * Initialize new user with default metadata (credits, timezone).
		 * Called after user signs up for the first time.
		 */
		async initializeUser(timezone?: string) {
			if (!timezone) {
				throw new Error('Please choose a timezone to finish onboarding.');
			}

			const clerk = await getClerkClient();
			if (!clerk) throw new Error('Clerk not initialized');

			const token = await getSessionToken(clerk);
			if (!token) throw new Error('No authentication token');

			const endpoint = `${apiBaseUrl}/onboarding/initialize`;

			const response = await fetch(endpoint, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				},
				body: JSON.stringify({ timezone })
			});

			const payload = await response.json();

			if (!response.ok) {
				throw new Error(payload?.detail || 'Failed to initialize user');
			}

			console.log('[Auth] User initialized, received timezone:', payload.timezone);

			update((state) => {
				const baseUser =
					state.user ??
					({
						clerk_user_id: payload.clerk_user_id,
						email: payload.email ?? '',
						credits: 0,
						timezone: null,
						needs_initialization: true,
						onboarding_completed: false
					} satisfies User);

				return {
					authenticated: true,
					user: {
						...baseUser,
						clerk_user_id: payload.clerk_user_id ?? baseUser.clerk_user_id,
						email: payload.email ?? baseUser.email,
						credits: typeof payload.credits === 'number' ? payload.credits : baseUser.credits,
						timezone: payload.timezone ?? baseUser.timezone,
						needs_initialization: false,
						onboarding_completed:
							typeof payload.onboarding_completed === 'boolean'
								? payload.onboarding_completed
								: true
					}
				};
			});

			// Reload session and user to get updated token with metadata
			console.log('[Auth] Reloading Clerk session and user after initialization...');
			await clerk.session?.reload();
			await clerk.user?.reload();

			// Give Clerk more time to propagate the updated metadata
			await new Promise((resolve) => setTimeout(resolve, 600));

			console.log('[Auth] Syncing user from backend after initialization...');
			await syncUserFromBackend(clerk, true);

			// Verify timezone was set correctly
			let currentState: ReturnType<typeof get> | null = null;
			update((state) => {
				currentState = state;
				return state;
			});

			console.log('[Auth] Final timezone after initialization:', currentState?.user?.timezone);

			return payload;
		},
		/**
		 * Refresh user metadata from backend (includes credits).
		 */
		async refreshUser() {
			const clerk = await getClerkClient();
			if (!clerk) return;
			await syncUserFromBackend(clerk, true);
		},
		/**
		 * Force-set the current credit balance.
		 */
		setCredits(credits: number) {
			update((state) => {
				if (!state.user) return state;
				return {
					...state,
					user: {
						...state.user,
						credits
					}
				};
			});
		}
	};
}

export const authStore = createAuthStore();

// Derived store for easy access to current user
export const currentUser = derived(
	authStore,
	($authStore) => $authStore.user
);

import { writable, derived } from 'svelte/store';
import type { Notification } from '$lib/types';

const STORAGE_KEY = 'coJournalist_notifications';

/**
 * Load notifications from localStorage
 */
function loadFromStorage(): Notification[] {
	if (typeof window === 'undefined') return [];

	try {
		const stored = localStorage.getItem(STORAGE_KEY);
		if (stored) {
			return JSON.parse(stored);
		}
	} catch (error) {
		console.error('Failed to load notifications from localStorage:', error);
	}
	return [];
}

/**
 * Save notifications to localStorage
 */
function saveToStorage(notifications: Notification[]): void {
	if (typeof window === 'undefined') return;

	try {
		localStorage.setItem(STORAGE_KEY, JSON.stringify(notifications));
	} catch (error) {
		console.error('Failed to save notifications to localStorage:', error);
	}
}

/**
 * Create notification store with localStorage persistence
 */
function createNotificationStore() {
	const { subscribe, set, update } = writable<Notification[]>(loadFromStorage());

	return {
		subscribe,

		/**
		 * Add a new notification
		 */
		addNotification: (scraperName: string) => {
			update(notifications => {
				const newNotification: Notification = {
					id: crypto.randomUUID(),
					scraperName,
					timestamp: Date.now()
				};
				const updated = [newNotification, ...notifications];
				saveToStorage(updated);
				return updated;
			});
		},

		/**
		 * Clear a specific notification by ID
		 */
		clearNotification: (id: string) => {
			update(notifications => {
				const updated = notifications.filter(n => n.id !== id);
				saveToStorage(updated);
				return updated;
			});
		},

		/**
		 * Clear all notifications
		 */
		clearAll: () => {
			set([]);
			saveToStorage([]);
		},

		/**
		 * Reload notifications from localStorage
		 */
		reload: () => {
			set(loadFromStorage());
		}
	};
}

export const notificationStore = createNotificationStore();

/**
 * Derived store for notification count
 */
export const notificationCount = derived(
	notificationStore,
	$notifications => $notifications.length
);

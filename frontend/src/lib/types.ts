/**
 * TypeScript type definitions for Infoviz frontend.
 */

// Graphics types
export interface GraphicsCard {
	title: string;
	description: string;
	thumbnail?: string;
}

export interface GraphicsExamplesResponse {
	query: string;
	items: GraphicsCard[];
	raw_html?: string;
}

/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
      fontFamily: {
        spacegrotesk: ['"Space Grotesk"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      letterSpacing: {
        tiniest: '0.01em',
        small: '0.05em',
        negative: '-0.02em',
      },
      fontSize: {
        'xs': ['10px', '13px'],
        'sm': ['12px', '15px'],
        'base': ['14px', '18px'],
        'lg': ['16px', '24px'],
        'xl': ['18px', '22px'],
        '2xl': ['20px', '26px'],
        '3xl': ['24px', '31px'],
        '4xl': ['30px', '42px'],
        '5xl': ['32px', '44.8px'],
        '6xl': ['34px', 'auto'],
        '7xl': ['48px', '61px'],
        '8xl': ['200px', '162px'],
      },
      fontWeight: {
        light: '300',
        normal: '400',
        medium: '500',
        semibold: '600',
        bold: '700',
      },
			colors: {
        black01: '#16191b',
        black02: '#1c1e1f',
        black03: '#272d30',
        black04: '#131414',
        grey01: '#636363',
        grey02: '#818181',
        grey03: '#d0d0d0',
        green01: '#a0ffcc',
        blue01: '#475aff',
        orange01: '#f86754',
			}
		}
	},
	plugins: []
};

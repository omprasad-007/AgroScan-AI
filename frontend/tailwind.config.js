/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // AgroScan AI Signature Theme: Vibrant Orange + Harvest Yellow + Royal Purple
        agro: {
          bg: 'rgb(var(--bg-canvas) / <alpha-value>)',
          card: 'rgb(var(--bg-card) / <alpha-value>)',
          surface: 'rgb(var(--bg-surface) / <alpha-value>)',
          hover: 'rgb(var(--bg-hover) / <alpha-value>)',
          border: 'var(--border-color)',
          borderStrong: 'var(--border-strong)',
          cream: 'rgb(var(--text-primary) / <alpha-value>)',
          muted: 'rgb(var(--text-muted) / <alpha-value>)',
          primary: 'rgb(var(--primary) / <alpha-value>)',
          primaryHover: 'rgb(var(--primary-hover) / <alpha-value>)',
          highlight: 'rgb(var(--highlight) / <alpha-value>)',
          accent: 'rgb(var(--accent) / <alpha-value>)',
        },

        // Theme palette specific tokens
        brand: {
          // Vibrant Orange
          orange: {
            DEFAULT: '#C94427',
            light: '#C94427',
            dark: '#E96747',
            hoverLight: '#B3391F',
            hoverDark: '#D65636',
          },
          // Harvest Yellow
          yellow: {
            DEFAULT: '#F2B942',
            light: '#F2B942',
            dark: '#FFD477',
          },
          // Royal Purple
          purple: {
            DEFAULT: '#7043C5',
            light: '#7043C5',
            dark: '#B99AFF',
          },
          // Light Mode Neutrals
          light: {
            bg: '#FAF9F6',
            card: '#FFFFFF',
            surface: '#F2F0EC',
            border: '#E6E2DC',
            text: '#39332F',
            muted: '#7D736A',
          },
          // Dark Mode Neutrals
          dark: {
            bg: '#292421',
            card: '#342D29',
            surface: '#403731',
            border: '#51463F',
            text: '#FFF9F3',
            muted: '#D1C6BC',
          }
        },

        // Guardrail: Alias standard palettes so NO blue, green, or pure black is ever rendered
        black: '#292421', // No pure black! Mapped to Deep Warm Charcoal

        // Warm neutral scale (mapped from slate/zinc/gray)
        slate: {
          50: '#FAF9F6',  // Warm White
          100: '#F2F0EC', // Soft Grey
          200: '#E6E2DC', // Light Border
          300: '#D6D0C8',
          400: '#B7B4A8', // Warm beige
          500: '#7D736A', // Muted brown
          600: '#51463F', // Soft Border
          700: '#403731', // Elevated Cocoa
          800: '#342D29', // Dark Cocoa
          900: '#292421', // Deep Warm Charcoal
          950: '#221E1B',
        },
        zinc: {
          50: '#FAF9F6',
          100: '#F2F0EC',
          200: '#E6E2DC',
          300: '#D6D0C8',
          400: '#B7B4A8',
          500: '#7D736A',
          600: '#51463F',
          700: '#403731',
          800: '#342D29',
          900: '#292421',
          950: '#221E1B',
        },
        gray: {
          50: '#FAF9F6',
          100: '#F2F0EC',
          200: '#E6E2DC',
          300: '#D6D0C8',
          400: '#B7B4A8',
          500: '#7D736A',
          600: '#51463F',
          700: '#403731',
          800: '#342D29',
          900: '#292421',
          950: '#221E1B',
        },

        // Remap emerald and green directly to Vibrant / Bright Orange
        emerald: {
          50: '#FFF5F2',
          100: '#FFE8E1',
          200: '#FFD1C4',
          300: '#FFAA94',
          400: '#E96747', // Dark mode Bright Orange
          500: '#C94427', // Light mode Vibrant Orange
          600: '#B3391F',
          700: '#8E2C17',
          800: '#6A2011',
          900: '#48150B',
          950: '#342D29',
        },
        green: {
          50: '#FFF5F2',
          100: '#FFE8E1',
          200: '#FFD1C4',
          300: '#FFAA94',
          400: '#E96747',
          500: '#C94427',
          600: '#B3391F',
          700: '#8E2C17',
          800: '#6A2011',
          900: '#48150B',
          950: '#342D29',
        },

        // Remap blue, indigo, cyan, sky, teal to Royal Purple & Light Purple
        blue: {
          50: '#FAF7FF',
          100: '#F2EBFF',
          200: '#E4D5FF',
          300: '#D0B5FF',
          400: '#B99AFF', // Dark mode Light Purple
          500: '#7043C5', // Light mode Royal Purple
          600: '#5B33A8',
          700: '#482787',
          800: '#371D67',
          900: '#261347',
          950: '#342D29',
        },
        indigo: {
          50: '#FAF7FF',
          100: '#F2EBFF',
          200: '#E4D5FF',
          300: '#D0B5FF',
          400: '#B99AFF',
          500: '#7043C5',
          600: '#5B33A8',
          700: '#482787',
          800: '#371D67',
          900: '#261347',
          950: '#342D29',
        },
        cyan: {
          50: '#FAF7FF',
          100: '#F2EBFF',
          200: '#E4D5FF',
          300: '#D0B5FF',
          400: '#B99AFF',
          500: '#7043C5',
          600: '#5B33A8',
          700: '#482787',
          800: '#371D67',
          900: '#261347',
          950: '#342D29',
        },
        sky: {
          50: '#FAF7FF',
          100: '#F2EBFF',
          200: '#E4D5FF',
          300: '#D0B5FF',
          400: '#B99AFF',
          500: '#7043C5',
          600: '#5B33A8',
          700: '#482787',
          800: '#371D67',
          900: '#261347',
          950: '#342D29',
        },
        teal: {
          50: '#FAF7FF',
          100: '#F2EBFF',
          200: '#E4D5FF',
          300: '#D0B5FF',
          400: '#B99AFF',
          500: '#7043C5',
          600: '#5B33A8',
          700: '#482787',
          800: '#371D67',
          900: '#261347',
          950: '#342D29',
        },

        // Remap amber and yellow to Harvest / Golden Yellow
        amber: {
          50: '#FFFDF5',
          100: '#FFF9E5',
          200: '#FFF0C2',
          300: '#FFE494',
          400: '#FFD477', // Dark mode Golden Yellow
          500: '#F2B942', // Light mode Harvest Yellow
          600: '#D99B28',
          700: '#B37815',
          800: '#8A590D',
          900: '#613C07',
          950: '#403731',
        },
        yellow: {
          50: '#FFFDF5',
          100: '#FFF9E5',
          200: '#FFF0C2',
          300: '#FFE494',
          400: '#FFD477',
          500: '#F2B942',
          600: '#D99B28',
          700: '#B37815',
          800: '#8A590D',
          900: '#613C07',
          950: '#403731',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Manrope', 'sans-serif'],
      },
      fontSize: {
        'main-heading': ['36px', { lineHeight: '44px', fontWeight: '800' }],
        'section-heading': ['26px', { lineHeight: '34px', fontWeight: '700' }],
        'card-heading': ['19px', { lineHeight: '26px', fontWeight: '600' }],
        'body-text': ['16px', { lineHeight: '24px', fontWeight: '400' }],
        'button-text': ['15px', { lineHeight: '20px', fontWeight: '600' }],
        'label-text': ['14px', { lineHeight: '18px', fontWeight: '500' }],
        'supporting-text': ['13px', { lineHeight: '18px', fontWeight: '400' }],
      },
      keyframes: {
        'laser-scan': {
          '0%': { transform: 'translateY(-100%)', opacity: '0.2' },
          '50%': { opacity: '0.9' },
          '100%': { transform: 'translateY(1000%)', opacity: '0.2' },
        },
        'pulse-subtle': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.65' },
        },
      },
      animation: {
        'laser': 'laser-scan 2.8s ease-in-out infinite',
        'pulse-subtle': 'pulse-subtle 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      boxShadow: {
        'theme-light': '0 4px 18px -2px rgba(57, 51, 47, 0.06), 0 1px 3px 0 rgba(57, 51, 47, 0.03)',
        'theme-light-hover': '0 12px 28px -4px rgba(57, 51, 47, 0.1), 0 4px 10px -2px rgba(57, 51, 47, 0.05)',
        'orange-glow': '0 4px 16px -2px rgba(201, 68, 39, 0.35)',
        'purple-glow': '0 4px 16px -2px rgba(112, 67, 197, 0.35)',
      },
    },
  },
  plugins: [],
}

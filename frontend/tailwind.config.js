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
        }
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

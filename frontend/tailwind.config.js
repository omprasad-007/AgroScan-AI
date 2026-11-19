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
        // Modern Balanced Product Palette
        agro: {
          bg: '#0B0F17',             // Modern sleek dark canvas
          card: '#111827',           // Clean elevated dark surface
          surface: '#1E293B',        // Interactive surface
          hover: '#26354A',          // Hover state
          high: '#334155',           // High-contrast
          border: 'rgba(255, 255, 255, 0.08)', // Frosted glass border
          borderStrong: 'rgba(255, 255, 255, 0.16)',
          borderHighlight: 'rgba(16, 185, 129, 0.4)',
          primary: '#10B981',        // Clean modern emerald green
          primaryHover: '#059669',   // Emerald hover
          'primary-hover': '#059669', // Alias for hyphenated usages
          primaryDark: '#047857',
          lime: '#34D399',           // Fresh mint/lime secondary accent
          limeDark: '#10B981',
          limeLight: '#6EE7B7',
          amber: '#F59E0B',          // Warning/harvest amber
          amberDark: '#D97706',
          amberLight: '#FBBF24',
          terracotta: '#F43F5E',     // Rose/coral alert
          terracottaDark: '#E11D48',
          terracottaLight: '#FB7185',
          cream: '#F8FAFC',          // Crisp white text in dark mode
          muted: '#94A3B8',          // Refined neutral slate muted
          mutedDark: '#64748B',      // Darker muted
          mutedLight: '#CBD5E1',     // Light muted

          // Light mode tokens
          lightBg: '#F8FAFC',        // Clean luminous modern white/slate canvas
          lightCard: '#FFFFFF',      // Pure white card
          lightSurface: '#F1F5F9',   // Soft light slate surface
          lightBorder: '#E2E8F0',    // Clean subtle light border
          lightText: '#0F172A',      // Deep charcoal/slate text
          lightMuted: '#64748B',     // Slate muted text
        },

        // Clean modern slate palette
        slate: {
          950: '#0B0F17',
          900: '#0F172A',
          850: '#161F30',
          800: '#1E293B',
          750: '#273549',
          700: '#334155',
          600: '#475569',
          500: '#64748B',
          400: '#94A3B8',
          300: '#CBD5E1',
          200: '#E2E8F0',
          100: '#F1F5F9',
          50: '#F8FAFC',
        },

        // Agri brand accent
        agri: {
          50: '#ECFDF5',
          100: '#D1FAE5',
          200: '#A7F3D0',
          300: '#6EE7B7',
          400: '#34D399',
          500: '#10B981',
          600: '#059669',
          700: '#047857',
          800: '#065F46',
          900: '#064E3B',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      keyframes: {
        'laser-scan': {
          '0%': { transform: 'translateY(-100%)', opacity: '0.2' },
          '50%': { opacity: '0.9' },
          '100%': { transform: 'translateY(1000%)', opacity: '0.2' },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'slide-up': {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'shimmer': {
          '100%': { transform: 'translateX(100%)' },
        },
        'pulse-subtle': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.65' },
        },
        'float-slow': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-6px)' },
        },
      },
      animation: {
        'laser': 'laser-scan 2.8s ease-in-out infinite',
        'fade-in': 'fade-in 0.25s ease-out forwards',
        'slide-up': 'slide-up 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'pulse-subtle': 'pulse-subtle 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float-slow 4s ease-in-out infinite',
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37), inset 0 1px 0 0 rgba(255, 255, 255, 0.08)',
        'glass-hover': '0 16px 40px -4px rgba(0, 0, 0, 0.5), inset 0 1px 0 0 rgba(255, 255, 255, 0.12)',
        'glass-light': '0 10px 30px -4px rgba(15, 23, 42, 0.06), 0 2px 6px -1px rgba(15, 23, 42, 0.03), inset 0 1px 0 0 rgba(255, 255, 255, 0.9)',
        'glass-light-hover': '0 16px 36px -4px rgba(15, 23, 42, 0.1), 0 4px 12px -2px rgba(15, 23, 42, 0.05)',
        'solid-dark': '4px 4px 12px rgba(0, 0, 0, 0.4), -2px -2px 8px rgba(255, 255, 255, 0.03)',
        'solid-light': '6px 6px 14px rgba(15, 23, 42, 0.06), -4px -4px 10px rgba(255, 255, 255, 0.9)',
        'primary-glow': '0 0 24px -2px rgba(16, 185, 129, 0.45)',
        'amber-glow': '0 0 20px -2px rgba(245, 158, 11, 0.4)',
      },
    },
  },
  plugins: [],
}

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
        // Warm Agricultural Design System
        agro: {
          bg: '#101510',             // Deep forest / near-black green
          card: '#182018',           // Elevated surface 1
          surface: '#202B20',        // Elevated surface 2
          hover: '#273527',          // Interactive / hover surface
          high: '#2F3F2F',           // High-contrast surface
          border: '#263326',         // Subtle organic border
          borderStrong: '#344734',   // Emphasized border
          borderHighlight: '#435C43',// Active / focused border
          primary: '#2FBF71',        // Natural emerald green (Strongest primary CTA)
          primaryHover: '#38D47F',   // Emerald hover
          primaryDark: '#239556',    // Emerald pressed
          lime: '#A6D85A',           // Fresh leaf / lime secondary accent
          limeDark: '#8DC244',
          limeLight: '#C3E78B',
          amber: '#F4B942',          // Harvest amber highlight/warning
          amberDark: '#DFA32B',
          amberLight: '#F7CB6D',
          terracotta: '#E76F51',     // Earthy terracotta error/destructive
          terracottaDark: '#CE573A',
          terracottaLight: '#EE8E77',
          cream: '#FAF7EF',          // Warm off-white main text
          muted: '#B7B4A8',          // Warm gray/beige muted text
          mutedDark: '#7A786E',      // Darker warm muted
          mutedLight: '#D6D3C8',     // Light warm muted

          // Light mode tokens
          lightBg: '#FAF7F0',        // Warm cream background
          lightCard: '#FFFFFF',      // Pure warm white surface
          lightSurface: '#F0ECE1',   // Sage / soft cream surface
          lightBorder: '#DDD8CB',    // Warm light border
          lightText: '#1A231A',      // Deep forest text
          lightMuted: '#676D63',     // Sage muted text
        },

        // Override slate to guarantee warm agriculture tones across all legacy classes
        slate: {
          950: '#101510',
          900: '#182018',
          850: '#1C251C',
          800: '#202B20',
          750: '#243024',
          700: '#273527',
          600: '#344734',
          500: '#7A786E',
          400: '#B7B4A8',
          300: '#D6D3C8',
          200: '#EAE7DE',
          100: '#FAF7EF',
          50: '#FDFCF7',
        },

        // Override blue/indigo/cyan/sky to map to emerald/lime/amber/forest green
        blue: {
          50: '#F0F9F3',
          100: '#D6EFE0',
          200: '#AEE0C2',
          300: '#75CA9A',
          400: '#38D47F',
          500: '#2FBF71',
          600: '#239556',
          700: '#1A7242',
          800: '#145632',
          900: '#0F3C23',
          950: '#101510',
        },
        indigo: {
          50: '#F5FAF0',
          100: '#E5F3D8',
          200: '#CFEAB4',
          300: '#B5DF8A',
          400: '#A6D85A',
          500: '#8DC244',
          600: '#709E33',
          700: '#547826',
          800: '#3B541B',
          900: '#233310',
          950: '#101510',
        },
        cyan: {
          50: '#F0F9F3',
          100: '#D6EFE0',
          200: '#AEE0C2',
          300: '#75CA9A',
          400: '#38D47F',
          500: '#2FBF71',
          600: '#239556',
          700: '#1A7242',
          800: '#145632',
          900: '#0F3C23',
          950: '#101510',
        },
        sky: {
          50: '#F0F9F3',
          100: '#D6EFE0',
          200: '#AEE0C2',
          300: '#75CA9A',
          400: '#38D47F',
          500: '#2FBF71',
          600: '#239556',
          700: '#1A7242',
          800: '#145632',
          900: '#0F3C23',
          950: '#101510',
        },

        // Agri brand green
        agri: {
          50: '#F0F9F3',
          100: '#D6EFE0',
          200: '#AEE0C2',
          300: '#75CA9A',
          400: '#38D47F',
          500: '#2FBF71',
          600: '#239556',
          700: '#1A7242',
          800: '#145632',
          900: '#0F3C23',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      keyframes: {
        'laser-scan': {
          '0%': { transform: 'translateY(-100%)', opacity: '0.2' },
          '50%': { opacity: '0.8' },
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
      },
      animation: {
        'laser': 'laser-scan 2.8s ease-in-out infinite',
        'fade-in': 'fade-in 0.25s ease-out forwards',
        'slide-up': 'slide-up 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'pulse-subtle': 'pulse-subtle 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      boxShadow: {
        'agro-sm': '0 1px 3px 0 rgba(0, 0, 0, 0.3)',
        'agro-md': '0 4px 16px -2px rgba(0, 0, 0, 0.4)',
        'agro-lg': '0 10px 30px -4px rgba(0, 0, 0, 0.5)',
        'agro-glow': '0 0 20px -2px rgba(47, 191, 113, 0.35)',
        'agro-amber-glow': '0 0 20px -2px rgba(244, 185, 66, 0.3)',
      },
    },
  },
  plugins: [],
}

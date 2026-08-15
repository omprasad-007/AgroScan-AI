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
        primary: {
          DEFAULT: "#0d631b",
          container: "#2e7d32",
          fixed: "#a3f69c",
          dim: "#88d982",
        },
        secondary: {
          DEFAULT: "#006e1c",
          container: "#91f78e",
        },
        tertiary: {
          DEFAULT: "#774c00",
          container: "#986200",
          fixed: "#ffddb5",
        },
        surface: {
          DEFAULT: "#f9f9f7",
          dim: "#dadad8",
          bright: "#f9f9f7",
          container: "#eeeeec",
          low: "#f4f4f2",
          lowest: "#ffffff",
          high: "#e8e8e6",
          highest: "#e2e3e1",
          variant: "#e2e3e1",
        },
        on: {
          surface: "#1a1c1b",
          "surface-variant": "#40493d",
          primary: "#ffffff",
          "primary-container": "#cbffc2",
        },
        outline: {
          DEFAULT: "#707a6c",
          variant: "#bfcaba",
        },
        agri: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#2e7d32',
          600: '#0d631b',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

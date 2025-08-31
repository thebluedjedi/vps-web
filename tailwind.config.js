/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'djedi': {
          50: '#e6f7ff',
          100: '#bae7ff',
          200: '#91d5ff',
          300: '#69c0ff',
          400: '#40a9ff',
          500: '#1890ff',
          600: '#096dd9',
          700: '#0050b3',
          800: '#003a8c',
          900: '#002766',
        },
        'temple': {
          'dark': '#0c0c0c',
          'mid': '#1a1a2e',
          'light': '#16213e',
          'accent': '#4fc3f7',
          'accent-dark': '#29b6f6',
          'success': '#81c784',
          'warning': '#ff9800',
          'error': '#f44336'
        }
      },
      fontFamily: {
        'clarendon': ['Clarendon', 'serif'],
        'inter': ['Inter', 'system-ui', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'glow': 'glow 3s ease-in-out infinite alternate',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 3s linear infinite',
        'gradient': 'gradient 15s ease infinite',
      },
      keyframes: {
        glow: {
          'from': { filter: 'drop-shadow(0 0 20px rgba(79, 195, 247, 0.3))' },
          'to': { filter: 'drop-shadow(0 0 40px rgba(79, 195, 247, 0.6))' }
        },
        gradient: {
          '0%, 100%': {
            'background-size': '200% 200%',
            'background-position': 'left center'
          },
          '50%': {
            'background-size': '200% 200%',
            'background-position': 'right center'
          }
        }
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}

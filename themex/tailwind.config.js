/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Templates in project apps
    './templates/**/*.html',
    '../templates/**/*.html',
    '../**/templates/**/*.html',
    
    // Templates in theme app
    '../theme/templates/**/*.html',
    
    // Include JavaScript files that might contain Tailwind CSS classes
    '../**/static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        // Gray palette
        'gray': {
          100: 'var(--gray-1)',
          200: 'var(--gray-2)',
          300: 'var(--gray-3)',
          400: 'var(--gray-4)',
          500: 'var(--gray-5)',
        },
        // Green palette
        'green': {
          100: 'var(--green-1)',
          200: 'var(--green-2)',
          300: 'var(--green-3)',
          400: 'var(--green-4)',
          500: 'var(--green-5)',
          600: 'var(--green-6)',
          700: 'var(--green-7)',
        },
        // Accent colors
        'accent': {
          'blue': 'var(--accent-blue)',
          'blue-light': 'var(--accent-blue-light)',
          'blue-dark': 'var(--accent-blue-dark)',
          'amber': 'var(--accent-amber)',
          'amber-light': 'var(--accent-amber-light)',
          'amber-dark': 'var(--accent-amber-dark)',
        },
        // Status colors
        'success': {
          DEFAULT: 'var(--success)',
          light: 'var(--success-light)',
        },
        'warning': {
          DEFAULT: 'var(--warning)',
          light: 'var(--warning-light)',
        },
        'error': {
          DEFAULT: 'var(--error)',
          light: 'var(--error-light)',
        },
        'info': {
          DEFAULT: 'var(--info)',
          light: 'var(--info-light)',
        },
        // Text colors
        'text': {
          'primary': 'var(--text-primary)',
          'secondary': 'var(--text-secondary)',
          'tertiary': 'var(--text-tertiary)',
          'light': 'var(--text-light)',
        },
        // Background colors
        'bg': {
          'primary': 'var(--bg-primary)',
          'secondary': 'var(--bg-secondary)',
          'tertiary': 'var(--bg-tertiary)',
          'dark': 'var(--bg-dark)',
        },
      },
      fontFamily: {
        'lora': ['Lora', 'serif'],
        'righteous': ['Righteous', 'cursive'],
      },
    },
  },
  plugins: [],
}

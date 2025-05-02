/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    '../templates/cotton/**/*.html',
    '../apps/**/templates/**/*.html',
    '../static/css/*.css',
  ],
  theme: {
    extend: {
      colors: {
        'cream-white': '#FFFDF6',
        'light-beige': '#FAF6E9',
        'lime-yellow': '#DDEB9D',
        'soft-green': '#A0C878',
        'soft-green-bright': '#A0C878',
        'soft-green-dark': '#355E3B',
      },
      fontFamily: {
        'righteous': ['Righteous', 'cursive'],
        'lora': ['Lora', 'serif'],
      },
      transitionProperty: {
        'width': 'width',
        'height': 'height',
        'spacing': 'margin, padding',
        'scale': 'scale',
        'transform': 'transform',
      },
      keyframes: {
        'pulse-subtle': {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.05)' },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'fade-in-up': {
          '0%': { 
            opacity: '0',
            transform: 'translateY(15px)'
          },
          '100%': { 
            opacity: '1',
            transform: 'translateY(0)'
          },
        },
        'fade-out-down': {
          '0%': { 
            opacity: '1',
            transform: 'translateY(0)'
          },
          '100%': { 
            opacity: '0',
            transform: 'translateY(15px)'
          },
        }
      },
      animation: {
        'pulse-subtle': 'pulse-subtle 2s ease-in-out infinite',
        'fade-in': 'fade-in 0.5s ease-out',
        'fade-in-up': 'fade-in-up 0.6s ease-out forwards',
        'fade-out-down': 'fade-out-down 0.4s ease-in-out forwards',
      },
    },
  },
  safelist: [
    'hover:bg-lime-yellow',
    'hover:text-soft-green-dark',
    'hover:-translate-y-1',
    'hover:scale-105',
    'hover:rotate-1',
    'hover:shadow-md',
    'hover:shadow-lg',
    'hover:bg-lime-yellow/50',
    'hover:text-soft-green',
    'hover:text-cream-white',
    'hover:border-transparent',
    'hover:border-b-2',
    'hover:border-lime-yellow',
    'hover:animate-pulse-subtle',
    'transform',
    'transition-all',
    'transition-transform',
    'duration-300',
    'translate-y-0',
    'translate-y-1',
    '-translate-y-1',
    'scale-x-0',
    'scale-x-100',
    'scale-100',
    'scale-105',
    'scale-110',
    'origin-left',
    'animate-fade-in-up',
    'animate-fade-out-down',
    'rotate-1',
    'overflow-hidden',
    'relative',
    'z-10',
    '-z-10',
    'bg-transparent'
  ],
  plugins: [],
}

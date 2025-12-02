/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'anote-primary': '#111827',
        'anote-accent': '#40C0FF',
        'anote-hover': '#DEFE47',
        'anote-sidebar': '#374151',
        'anote-text-primary': '#ffffff',
        'anote-text-secondary': '#D1D5DB',
        'anote-text-tertiary': '#9CA3AF',
      }
    },
  },
  plugins: [],
}

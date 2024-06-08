/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,ts,js,jsx,tsx}',
  ],
  safelist: [
    {
      pattern: /grid-cols-\d+/,
    },
  ],
  theme: {
    extend: {
      colors: {
        'theme-bg': '#36393f',
        'theme-nav': '#313339',
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
};

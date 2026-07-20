/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ghc: {
          blue: '#005C99',
          'blue-dark': '#004A7A',
          'blue-light': '#E8F0FE',
          teal: '#00A79D',
          'teal-dark': '#008B82',
          'teal-light': '#E0F7F5',
        },
        surface: '#F7F9FB',
        panel: '#FFFFFF',
        'panel-border': '#DCE3EA',
        text: '#1F2937',
        muted: '#6B7280',
        priority: {
          laranja: '#F9A825',
          vermelho: '#C62828',
          escuro: '#7F1D1D',
        },
        success: '#2E7D32',
        info: '#0288D1',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

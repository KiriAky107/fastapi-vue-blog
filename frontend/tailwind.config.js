/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 二次元风格配色
        'acg-pink': '#FFB7C5',
        'acg-pink-light': '#FFE4E9',
        'acg-blue': '#A8D8EA',
        'acg-purple': '#D4B5E6',
        'acg-yellow': '#FFF4BD',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}

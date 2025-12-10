/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx,js,jsx}"
  ],
  darkMode: "class", // optional; you can keep/remove
  theme: {
    extend: {
      colors: {
        // optional custom shades you’re already using
        slate: {},
      },
    },
  },
  plugins: [
    require("@tailwindcss/typography"),
  ],
};


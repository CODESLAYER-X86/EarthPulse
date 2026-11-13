/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        nasa: {
          blue: "#0b3d91",
          red: "#fc3d21",
          dark: "#0b0f19",
          panel: "#111827",
          border: "#1f2937",
          accent: "#38bdf8"
        }
      }
    },
  },
  plugins: [],
}

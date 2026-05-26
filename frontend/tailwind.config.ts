import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#18212f",
        brand: "#0f766e",
        coral: "#f97368",
      },
      boxShadow: {
        soft: "0 18px 55px rgba(24, 33, 47, 0.12)",
      },
    },
  },
  plugins: [],
};

export default config;

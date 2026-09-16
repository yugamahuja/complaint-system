import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#172033",
        muted: "#667085",
        brand: "#335CFF",
        canvas: "#F6F8FC"
      }
    }
  },
  plugins: []
};

export default config;


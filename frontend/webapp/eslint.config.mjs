import js from "@eslint/js";
import tseslint from "typescript-eslint";
import next from "eslint-plugin-next";

/** @type {import("eslint").Linter.FlatConfig[]} */
export default [
  // ─────────────────────────────────────────────
  // Base JavaScript rules
  js.configs.recommended,

  // ─────────────────────────────────────────────
  // TypeScript (safe & minimal)
  ...tseslint.configs.recommended,

  // ─────────────────────────────────────────────
  // Next.js (core rules only)
  {
    plugins: {
      next,
    },
    rules: {
      ...next.configs["core-web-vitals"].rules,
    },
  },

  // ─────────────────────────────────────────────
  // Project-specific rules
  {
    files: ["**/*.{ts,tsx,js,jsx}"],

    rules: {
      // 🚫 No noisy rules
      "no-console": "off",
      "no-unused-vars": "off",

      // ✅ Let TypeScript handle unused vars
      "@typescript-eslint/no-unused-vars": [
        "warn",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
        },
      ],

      // 🧠 Readability > dogma
      "@typescript-eslint/explicit-function-return-type": "off",
      "@typescript-eslint/explicit-module-boundary-types": "off",

      // ⚠️ Prevent real bugs
      "no-undef": "error",
      "no-redeclare": "error",
    },
  },

  // ─────────────────────────────────────────────
  // Ignore generated / external stuff
  {
    ignores: [
      "node_modules",
      ".next",
      "dist",
      "build",
      "coverage",
      "out",
      ".turbo",
    ],
  },
];

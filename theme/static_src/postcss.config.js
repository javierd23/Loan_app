module.exports = {
  darkMode: 'class',
    content: [
    './templates/**/*.html',
    './**/*.html',
    './**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: {
    "@tailwindcss/postcss": {},
    "postcss-simple-vars": {},
    "postcss-nested": {}
  },
}

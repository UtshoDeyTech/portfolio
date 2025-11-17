/** @type {import('tailwindcss').Config} */
export default {
    content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
    theme: {
        extend: {
            // Standardized spacing system for consistency
            spacing: {
                'section': '4rem',      // 64px - consistent section spacing
                'section-sm': '3rem',   // 48px - smaller section spacing
                'card': '1.5rem',       // 24px - card padding
                'card-sm': '1rem',      // 16px - smaller card padding
            },
            // Standardized container sizes
            maxWidth: {
                'content': '1280px',    // Main content max-width
                'prose-custom': '75ch', // Readable line length
            },
            // Typography system
            fontSize: {
                'display': ['3.5rem', { lineHeight: '1.1', fontWeight: '700' }],      // 56px
                'h1': ['2.5rem', { lineHeight: '1.2', fontWeight: '700' }],           // 40px
                'h2': ['2rem', { lineHeight: '1.3', fontWeight: '600' }],             // 32px
                'h3': ['1.5rem', { lineHeight: '1.4', fontWeight: '600' }],           // 24px
                'h4': ['1.25rem', { lineHeight: '1.5', fontWeight: '600' }],          // 20px
                'body-lg': ['1.125rem', { lineHeight: '1.7', fontWeight: '400' }],    // 18px
                'body': ['1rem', { lineHeight: '1.6', fontWeight: '400' }],           // 16px
                'body-sm': ['0.875rem', { lineHeight: '1.5', fontWeight: '400' }],    // 14px
                'caption': ['0.75rem', { lineHeight: '1.4', fontWeight: '500' }],     // 12px
            },
            // Animation and transitions
            transitionDuration: {
                'fast': '150ms',
                'normal': '250ms',
                'slow': '350ms',
            },
            // Enhanced shadows for depth
            boxShadow: {
                'card': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
                'card-hover': '0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1)',
                'card-active': '0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.1)',
            },
        },
    },
    plugins: [require("@tailwindcss/typography"), require("daisyui")],
    daisyui: {
        themes: [
            // "light", // Commented out - only dark mode active
            "dark",
        ],
    },
    // darkMode: ['selector', '[data-theme="synthwave"]']
};

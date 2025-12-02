# CLAUDE.md - AI Assistant Guide for ani-radar

## Project Overview

**Project Name:** ani-radar
**Repository:** bill3129066/ani-radar
**License:** MIT License (2025)
**Status:** Early stage - Initial setup
**Tech Stack:** Next.js, TypeScript, React

### Project Purpose
Based on the repository name "ani-radar", this project appears to be designed for anime tracking, monitoring, or discovery functionality.

---

## Repository Structure

### Current State
This is a new repository with minimal setup:
```
ani-radar/
├── .git/              # Git repository data
├── .gitignore         # Next.js/TypeScript ignore patterns
├── LICENSE            # MIT License
└── CLAUDE.md          # This file
```

### Expected Future Structure
As development progresses, the typical Next.js structure should emerge:
```
ani-radar/
├── .next/             # Next.js build output (gitignored)
├── node_modules/      # Dependencies (gitignored)
├── public/            # Static assets
├── src/               # Source code
│   ├── app/          # Next.js App Router pages
│   ├── components/   # React components
│   ├── lib/          # Utility functions
│   ├── hooks/        # Custom React hooks
│   ├── types/        # TypeScript type definitions
│   └── styles/       # CSS/styling files
├── .env.local         # Environment variables (gitignored)
├── .eslintrc.json     # ESLint configuration
├── .gitignore         # Git ignore patterns
├── CLAUDE.md          # This file
├── LICENSE            # MIT License
├── next.config.js     # Next.js configuration
├── package.json       # Dependencies and scripts
├── README.md          # Project documentation
├── tsconfig.json      # TypeScript configuration
└── tailwind.config.js # Tailwind CSS config (if used)
```

---

## Development Setup

### Prerequisites
- Node.js (v18+ recommended)
- npm, yarn, or pnpm package manager
- Git

### Initial Setup Commands
When setting up the project for the first time:
```bash
# Initialize Next.js with TypeScript
npx create-next-app@latest . --typescript --tailwind --app --src-dir

# Or manually install dependencies
npm init -y
npm install next@latest react@latest react-dom@latest
npm install -D typescript @types/react @types/node
```

### Development Workflow
```bash
npm run dev          # Start development server (typically port 3000)
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript compiler check
```

---

## Key Conventions for AI Assistants

### Code Style and Quality

1. **TypeScript First**
   - Use TypeScript for all new files
   - Define proper interfaces and types
   - Avoid `any` types; use `unknown` if type is truly dynamic
   - Use strict TypeScript configuration

2. **React/Next.js Best Practices**
   - Use React Server Components by default (Next.js 13+ App Router)
   - Use Client Components (`'use client'`) only when needed
   - Follow Next.js file-based routing conventions
   - Use Next.js Image component for images
   - Use Next.js Link component for navigation

3. **Component Structure**
   - One component per file
   - Use named exports for components
   - Co-locate related files (styles, tests, types)
   - Prefer functional components with hooks
   - Use composition over inheritance

4. **File Naming Conventions**
   - Components: `PascalCase.tsx` (e.g., `AnimeCard.tsx`)
   - Utilities: `camelCase.ts` (e.g., `formatDate.ts`)
   - Hooks: `useCamelCase.ts` (e.g., `useAnimeData.ts`)
   - Types: `camelCase.types.ts` (e.g., `anime.types.ts`)
   - Pages: Follow Next.js conventions (`page.tsx`, `layout.tsx`)

5. **Code Organization**
   - Keep components small and focused
   - Extract reusable logic into custom hooks
   - Create utility functions for common operations
   - Use barrel exports (index.ts) for cleaner imports

### Testing Strategy

When tests are implemented:
- Unit tests: Jest + React Testing Library
- E2E tests: Playwright or Cypress
- Test files: `*.test.ts` or `*.spec.ts`
- Aim for meaningful test coverage, not just high percentages

### Environment Variables

- Store sensitive data in `.env.local` (never commit)
- Use `NEXT_PUBLIC_` prefix for client-side variables
- Document required environment variables in README
- Provide `.env.example` template

### Git Workflow

1. **Branch Naming**
   - Feature: `feature/description`
   - Bug fix: `fix/description`
   - AI-generated: `claude/claude-md-miofa6r9dtynokun-01JkEq1V5HtybpnXiPT11sna`

2. **Commit Messages**
   - Use conventional commits format
   - Examples:
     - `feat: add anime search functionality`
     - `fix: resolve data fetching issue`
     - `docs: update README with setup instructions`
     - `refactor: optimize component rendering`

3. **Before Committing**
   - Run linter and fix issues
   - Run type checker
   - Test affected functionality
   - Remove console.logs and debug code

### API and Data Fetching

- Use Next.js Server Actions for mutations
- Use React Server Components for data fetching when possible
- Implement proper error handling and loading states
- Cache data appropriately
- Consider using SWR or React Query for client-side data fetching

### Performance Considerations

- Optimize images with Next.js Image component
- Implement proper code splitting
- Use dynamic imports for heavy components
- Minimize client-side JavaScript
- Implement proper caching strategies

---

## Security Best Practices

1. **Input Validation**
   - Validate and sanitize all user inputs
   - Use TypeScript for type safety
   - Implement server-side validation

2. **Authentication & Authorization**
   - Use established auth libraries (NextAuth.js recommended)
   - Store tokens securely
   - Implement proper session management

3. **API Security**
   - Never expose API keys in client code
   - Use environment variables
   - Implement rate limiting
   - Validate API responses

4. **Dependencies**
   - Keep dependencies updated
   - Regularly run `npm audit`
   - Review security advisories

---

## Common Tasks for AI Assistants

### Setting Up the Project
1. Initialize Next.js with TypeScript
2. Configure ESLint and Prettier
3. Set up Tailwind CSS (if using)
4. Create basic project structure
5. Add README with setup instructions

### Adding New Features
1. Create feature branch
2. Design component structure
3. Define TypeScript interfaces
4. Implement components
5. Add error handling
6. Test functionality
7. Update documentation
8. Commit and push changes

### Debugging Issues
1. Check browser console for errors
2. Review Next.js build output
3. Verify TypeScript compilation
4. Check network requests
5. Review server logs
6. Validate environment variables

### Refactoring Code
1. Ensure tests exist (or create them)
2. Make incremental changes
3. Verify functionality after each change
4. Update related documentation
5. Remove unused code and imports

---

## Anime/Radar Domain Context

Given the project name "ani-radar", development should focus on:

### Potential Features
- Anime search and discovery
- Tracking watched/watching anime
- Recommendations system
- Episode tracking
- Release notifications
- User reviews and ratings
- Social features (lists, sharing)

### Potential Data Sources
- MyAnimeList API
- AniList API
- Jikan API (unofficial MAL API)
- Custom backend service

### UI/UX Considerations
- Fast search functionality
- Responsive design for mobile
- Grid/list view toggles
- Filter and sort options
- Smooth animations
- Dark mode support (anime communities often prefer dark themes)

---

## Current Development Status

**Last Updated:** 2025-12-02

### Completed
- ✅ Repository initialization
- ✅ LICENSE file (MIT)
- ✅ .gitignore configuration (Next.js/TypeScript)
- ✅ CLAUDE.md documentation

### Immediate Next Steps
1. Initialize Next.js project structure
2. Set up TypeScript configuration
3. Configure ESLint and Prettier
4. Create README.md with project description
5. Set up basic component structure
6. Choose and integrate anime data API
7. Design initial UI/UX mockups
8. Implement core features (search, display)

### Open Questions
- Which anime API to use? (AniList vs MyAnimeList vs custom)
- Authentication strategy? (NextAuth.js, Clerk, custom)
- Database choice? (if needed: PostgreSQL, MongoDB, Supabase)
- Styling approach? (Tailwind CSS, CSS Modules, styled-components)
- State management? (React Context, Zustand, Redux)
- Hosting platform? (Vercel, Netlify, custom)

---

## AI Assistant Guidelines

### Do's ✅
- Read existing code before making changes
- Follow established patterns in the codebase
- Write type-safe TypeScript
- Create focused, single-responsibility components
- Add meaningful comments for complex logic
- Update documentation when making significant changes
- Test changes before committing
- Use Next.js and React best practices
- Consider performance implications
- Handle errors gracefully

### Don'ts ❌
- Don't commit sensitive data or API keys
- Don't use `any` type without justification
- Don't create overly complex abstractions prematurely
- Don't skip error handling
- Don't ignore TypeScript errors
- Don't commit commented-out code
- Don't make assumptions about user requirements
- Don't over-engineer solutions
- Don't bypass established patterns without discussion
- Don't commit directly to main branch

### When Uncertain
1. Check existing codebase patterns
2. Review Next.js and React documentation
3. Ask clarifying questions
4. Propose solution before implementing
5. Start with simplest working solution
6. Refactor iteratively based on feedback

---

## Resources

### Official Documentation
- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)

### Recommended Libraries
- **UI Components:** shadcn/ui, Radix UI, Headless UI
- **Styling:** Tailwind CSS, CSS Modules
- **Forms:** React Hook Form + Zod
- **Data Fetching:** SWR, TanStack Query
- **State Management:** Zustand, Jotai, React Context
- **Animation:** Framer Motion, React Spring
- **Auth:** NextAuth.js, Clerk, Supabase Auth

### Anime APIs
- [AniList API](https://anilist.gitbook.io/anilist-apiv2-docs)
- [Jikan API](https://docs.api.jikan.moe)
- [MyAnimeList API](https://myanimelist.net/apiconfig/references/api/v2)

---

## Maintenance Notes

This document should be updated whenever:
- Project structure changes significantly
- New conventions are established
- Technology choices are made
- Major features are added or removed
- Development workflow changes
- Common issues are discovered and resolved

**Maintained by:** AI assistants working on this project
**Last Review:** 2025-12-02

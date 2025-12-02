---
name: modern-fintech-design
description: Apply modern fintech design principles for creating professional, trustworthy, and sophisticated user interfaces. Use when designing or refining UI components, layouts, color schemes, interactive elements, implementing dark mode, or establishing consistent styling patterns. Activates for component design, UI/UX improvements, color/spacing/typography decisions, animations, and responsive design.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Modern Fintech Design Excellence

Apply modern fintech design principles for creating professional, trustworthy, and sophisticated user interfaces. Use when designing or refining UI components, layouts, color schemes, or interactive elements.

## When to Use This Skill

Activate when:
- Designing new components or pages
- Reviewing UI/UX for improvements
- Making decisions about colors, spacing, or typography
- Implementing dark mode
- Creating buttons, cards, forms, or navigation
- Adding animations or transitions
- Establishing responsive breakpoints
- Polishing visual hierarchy

## Core Design Philosophy

Create interfaces that balance **professional trust** with **approachable simplicity**, and **technical sophistication** with **accessible clarity**.

### Key Principles

1. **One Key Action Per Screen** - Reduce cognitive load by focusing user attention
2. **Generous Whitespace** - Let elements breathe, don't cram
3. **State-Based Feedback** - Show status through the UI itself, not separate messages
4. **Progressive Disclosure** - Reveal complexity only when needed
5. **Consistent Patterns** - Build learnable, predictable interfaces

---

## Color System

### Primary Palette

**Blue Primary** (trustworthy, energetic):
```
Primary: #00a3ff
Hover: #009bf2
Marketing: #0665FC
```

**Professional Grounding**:
```
Dark Navy: #273852
Dark Charcoal: #27272e
```

**Premium Accents**:
```
Gold: #FFBF00
Gold Light: #FFD966
Pink: #F85F97
Red: #F00A38
```

### Background System

**Light Mode**:
```
Base: #f2f4f6
Secondary: #EFF2F6
Foreground/Cards: #ffffff
```

**Dark Mode**:
```
Base: #1c1c21
Secondary: #27272E
Foreground/Cards: #34343d
```

### Semantic Colors

```
Success: #53BA95
Error: #e14d4d (hover: #d44c4d)
Warning: #EC8600
Warning BG: #FFFAE0
```

### Text Hierarchy

**Light Mode**:
```
Primary: #273852
Secondary: #7a8aa0
```

**Dark Mode**:
```
Primary: #ffffff
Secondary: rgba(255, 255, 255, 0.8)
```

### Usage Guidelines

- **Blue** for primary CTAs and key interactive elements
- **Gold** sparingly for premium features or highlights
- **Navy** for professional text and grounding elements
- **Gradients** for visual depth (blue → gold → pink)
- Use **opacity-based** borders: `rgba(0, 10, 61, 0.12)` to `0.48`

---

## Typography System

### Font Selection

**Primary**: Variable weight sans-serif (Manrope recommended)
- Supports weights 200-800 for precise hierarchy
- Modern, readable, professional

**Fallback Stack**:
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
             Roboto, Oxygen, Ubuntu, Cantarell,
             "Helvetica Neue", sans-serif;
```

### Type Scale

```
Main Heading: 40px / weight 800
Section Titles: 18px / weight 800
Body Text: 12px / weight 400
Button Text: 14px / weight 800
```

### Line Heights

```
Body: 1.6em (comfortable reading)
Headings: 1.3em (tight, impactful)
```

### Typography Rules

✅ **DO**:
- Use heavy weights (700-800) for headings and CTAs
- Maintain generous line-height (1.6em minimum for body)
- Create clear size hierarchy between levels
- Use variable fonts for performance

❌ **DON'T**:
- Mix too many font weights in one section
- Use line-height below 1.3em
- Go below 12px for body text
- Use decorative fonts for UI elements

---

## Spacing System

### Scale

Base-8 increments:
```
xs: 8px
sm: 12px
md: 16px
lg: 20px
xl: 32px
2xl: 60px
```

### Application

**Sections**: `32px` vertical margins between major sections

**Container Padding**:
- Desktop: `32px`
- Mobile: `20px`

**Cards**: `20px 32px` (vertical horizontal)

**Form Fields**: Match container padding (32px / 20px)

**Buttons**: `8px` gap between multiple buttons

**Icons**: `16px` left margin for spacing from text

**Disclaimers**: `20px` top / `60px` bottom

### Spacing Rules

✅ **DO**:
- Use consistent spacing scale throughout
- Group related elements with less space
- Separate unrelated elements with more space
- Maintain vertical rhythm

❌ **DON'T**:
- Use arbitrary spacing values
- Cram elements together
- Over-space within logical groups

---

## Layout Structure

### Container System

```css
max-width: 1424px;
padding: 32px; /* desktop */
padding: 20px; /* mobile */
```

**Focused Content**:
```css
max-width: 560px; /* for forms, text-heavy sections */
```

### Responsive Breakpoints

```
Mobile: max-width 479px
Tablet: max-width 767px
Desktop: 1424px+ container
```

### Grid Patterns

- Use **flexbox** for component-level layouts
- Apply **grid** for page-level structures
- Maintain **consistent gutters** (32px desktop / 20px mobile)

### Content Hierarchy Rules

✅ **DO**:
- Limit to one primary action per screen
- Place related info close together (proximity principle)
- Use visual weight to guide attention
- Create clear scanning patterns (F or Z layout)

❌ **DON'T**:
- Offer multiple competing CTAs
- Scatter related information
- Create ambiguous visual hierarchy

---

## Component Design

### Buttons

**Primary Button**:
```css
background: #00a3ff;
color: #ffffff;
padding: 20px 32px; /* desktop */
padding: 20px; /* mobile, full width often */
min-height: 40px;
border-radius: 20px;
font-size: 14px;
font-weight: 800;
transition: background 200ms ease;
```

**Hover State**:
```css
background: #009bf2;
```

**Secondary Button**:
```css
background: #ffffff; /* light mode */
color: #273852;
/* Same sizing as primary */
```

**Button States Through Text**:
- Default: "Connect Wallet"
- Validation: "Enter amount to stake"
- Error: "Insufficient ETH balance"
- Ready: "Stake"
- Loading: "Approving…"
- Processing: "Staking…"

**Button Rules**:

✅ **DO**:
- Use state-based text to communicate status
- Maintain 40px minimum height for touch targets
- Use heavy font weight (800) for prominence
- Provide clear hover states
- Disable when action isn't available

❌ **DON'T**:
- Show separate error messages (put in button text)
- Use technical jargon ("Submit" vs "Stake")
- Create tiny buttons (<40px height)
- Use subtle weight differences

### Cards

```css
background: var(--color-foreground);
border-radius: 20px;
padding: 20px 32px;
box-shadow: rgba(39, 56, 82, 0.08) 0px 4px 12px;
```

**Card Pattern**:
- Icon + Title + Description structure
- Subtle elevation shadow
- Consistent rounded corners (20px)
- Clickable containers use semantic links

### Form Inputs

```css
background: var(--color-controlBg);
padding: 16px;
border-radius: 12px;
border: 1px solid rgba(0, 10, 61, 0.12);
```

**Input Rules**:

✅ **DO**:
- Show validation only after user has typed
- Place feedback adjacent to input (proximity)
- Provide real-time calculation results nearby
- Support localized decimal formats

❌ **DON'T**:
- Show errors before user interaction
- Place error messages far from inputs
- Use overly technical validation messages

### Navigation

**Header Structure**:
```css
display: flex;
align-items: flex-end;
padding: 32px;
```

**Mobile Optimization**:
- Reduce logo size proportionally
- Collapse menu to hamburger if needed
- Maintain touch-friendly tap targets

---

## Visual Effects

### Shadows (Elevation System)

**Three Tiers**:

1. **Subtle** (cards, containers):
   ```css
   box-shadow: rgba(39, 56, 82, 0.08) 0px 4px 12px;
   ```

2. **Medium** (modals, dropdowns):
   ```css
   box-shadow: rgba(0, 0, 0, 0.25) 0px 8px 24px;
   ```

3. **Deep** (overlay backgrounds):
   ```css
   box-shadow: rgba(0, 0, 0, 0.5) 0px 16px 48px;
   ```

### Gradients

**Multi-Layer Philosophy**:
- Use radial gradients for dimensional effects
- Apply linear gradients for directional flow
- Layer gradients at varying opacities
- Combine blue → gold → pink for depth

**Example Background Gradient**:
```css
background: radial-gradient(
  circle at top right,
  rgba(0, 163, 255, 0.1),
  transparent 50%
),
radial-gradient(
  circle at bottom left,
  rgba(255, 191, 0, 0.08),
  transparent 50%
);
```

**Gradient Rules**:

✅ **DO**:
- Use gradients for depth and interest
- Keep opacity low (0.05-0.15) for backgrounds
- Layer multiple gradients for complexity
- Position with `fixed` and `pointer-events: none`

❌ **DON'T**:
- Overpower content with bright gradients
- Use gradients on interactive elements (confusing)
- Create jarring color transitions

### Border Radius

**Standard**: `20px` for most components (buttons, cards, containers)

**Smaller Elements**: `12px` for inputs, tags, small cards

**Icons/Avatars**: `50%` for circular elements

---

## Motion Design

### Timing & Easing

**Standard Transition**:
```css
transition: all 200ms ease;
```

**Property-Specific** (preferred):
```css
transition: background-color 200ms ease,
            transform 200ms ease;
```

### Animation Types

**State Changes**:
- Color transitions (hover, active, disabled)
- Icon rotations (expand/collapse): `rotate(180deg)`
- Opacity fades (modals, tooltips)

**Loading States**:
- Button text updates ("Loading…")
- Progress indicators
- Skeleton screens for content

**Entrance/Exit**:
- Toast notifications: slideInUp / slideOutDown
- Modals: fade in with slight scale
- Dropdowns: slideDown with fade

### Motion Rules

✅ **DO**:
- Use consistent timing (200ms standard)
- Apply purposeful motion to guide attention
- Keep animations subtle and smooth
- Provide loading feedback for async actions

❌ **DON'T**:
- Animate everything
- Use slow animations (>300ms for micro-interactions)
- Create distracting motion
- Animate on scroll excessively

---

## Responsive Design

### Mobile-First Approach

**Padding Reduction**:
```
Desktop: 32px → Mobile: 20px
```

**Container Calculations**:
```css
/* Desktop */
width: calc(100vw - 40px);
max-width: 1424px;

/* Mobile */
width: calc(100vw - 16px);
```

### Touch Optimization

- Minimum button height: `40px`
- Generous padding: `20px` minimum
- Clear tap targets with spacing
- Avoid hover-dependent interactions

### Breakpoint Strategy

```css
/* Mobile */
@media (max-width: 479px) {
  .container { padding: 16px; }
  .logo { width: 14px; }
}

/* Tablet */
@media (max-width: 767px) {
  .container { padding: 20px; }
}

/* Desktop */
@media (min-width: 1424px) {
  .container { max-width: 1424px; }
}
```

---

## Dark Mode Implementation

### CSS Custom Properties

Define tokens for theme switching:

```css
:root {
  --color-foreground: #ffffff;
  --color-background: #f2f4f6;
  --color-text-primary: #273852;
  --color-text-secondary: #7a8aa0;
}

[data-theme='dark'] {
  --color-foreground: #34343d;
  --color-background: #1c1c21;
  --color-text-primary: #ffffff;
  --color-text-secondary: rgba(255, 255, 255, 0.8);
}
```

### Dark Mode Rules

✅ **DO**:
- Design dark mode from day one
- Use CSS custom properties for all colors
- Test both modes equally
- Maintain contrast ratios (WCAG AA minimum)
- Adjust shadow opacity for dark backgrounds

❌ **DON'T**:
- Simply invert colors
- Use pure black (#000000)
- Forget to adjust shadows
- Make dark mode an afterthought

---

## Accessibility Standards

### Color Contrast

- **Text**: Minimum 4.5:1 ratio (WCAG AA)
- **Large Text**: Minimum 3:1 ratio
- **Interactive Elements**: 3:1 against background

### Interactive Elements

- Minimum touch target: `40px × 40px`
- Keyboard navigation support
- Focus indicators visible and clear
- Semantic HTML elements

### Content

- Alt text for images
- Labels for form inputs
- ARIA labels where needed
- Heading hierarchy (h1 → h2 → h3)

---

## Common Patterns

### Hero Section

- Large heading (40px, weight 800)
- Subheading with secondary color
- Single primary CTA
- Optional background gradient
- Generous vertical padding (60px+)

### Feature Cards Grid

```css
display: grid;
grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
gap: 32px;
```

Each card:
- Icon at top
- Bold title (18px, weight 800)
- Description text (12-14px, weight 400)
- Consistent padding (20px 32px)

### Form Layouts

- Label above input
- Input with adjacent output/feedback
- Primary button full-width on mobile
- Validation messages near inputs
- Progress indicators for multi-step

### Section Headers

```css
display: flex;
align-items: flex-end;
margin-bottom: 12px;
```

- Title on left
- Controls/filters on right
- Clear separation from content (12px margin)

---

## Anti-Patterns to Avoid

❌ **Separate Error Messages**
- ✅ Instead: Update button text with validation state
- Example: "Insufficient ETH balance" in button, not below form

❌ **Multiple Competing CTAs**
- ✅ Instead: One primary action, secondary actions less prominent

❌ **Cluttered Screens**
- ✅ Instead: Progressive disclosure, one key function per view

❌ **Inconsistent Spacing**
- ✅ Instead: Use the 8px base spacing system consistently

❌ **Generic Button Text**
- ✅ Instead: Use domain-specific language ("Stake" not "Submit")

❌ **Time Estimates**
- ✅ Instead: Show block confirmations or progress indicators

❌ **Hover-Dependent Mobile UI**
- ✅ Instead: Design for touch-first interaction

❌ **Pure Black Dark Mode**
- ✅ Instead: Use dark charcoal (#1c1c21) for less eye strain

---

## Quick Reference Checklist

When designing a new component, verify:

- [ ] Uses colors from the defined palette
- [ ] Maintains 32px spacing between major sections
- [ ] Has 20px border-radius on containers
- [ ] Typography uses heavy weights (800) for emphasis
- [ ] Buttons are minimum 40px height
- [ ] State communicated through UI (not separate messages)
- [ ] One primary action clearly defined
- [ ] Works in both light and dark mode
- [ ] Responsive padding (32px → 20px on mobile)
- [ ] Transitions use 200ms ease timing
- [ ] Shadows use defined elevation system
- [ ] Touch targets meet 40px minimum
- [ ] Text contrast meets WCAG AA standards

---

## Implementation Tips

### Getting Started

1. **Set up CSS custom properties** for theming first
2. **Define spacing scale** as reusable values
3. **Choose primary blue** and test with gold accents
4. **Implement dark mode toggle** early
5. **Create button component** as foundation

### Development Workflow

1. Design mobile-first, enhance for desktop
2. Use design tokens (CSS vars) for all colors/spacing
3. Test both light and dark modes continuously
4. Validate accessibility with tools (axe, Lighthouse)
5. Maintain component library/Storybook if possible

### Testing

- Test on actual mobile devices (not just browser resize)
- Verify touch targets are comfortable
- Check color contrast in both modes
- Validate keyboard navigation
- Test with screen readers

---

## Summary

Modern fintech design excellence comes from:

1. **Vibrant blue primary** (#00a3ff) with gold accents
2. **Generous whitespace** and 32px spacing system
3. **Rounded corners** (20px standard) for friendly feel
4. **Bold typography** (weight 800) for clear hierarchy
5. **State-based interactions** with contextual feedback
6. **Comprehensive dark mode** via CSS custom properties
7. **One primary action** per screen for clarity
8. **Subtle motion** (200ms transitions) for polish
9. **Accessible design** (40px touch targets, WCAG contrast)
10. **Professional trust** balanced with approachable simplicity

Apply these principles consistently to create interfaces that feel simultaneously **sophisticated and simple**, **professional and approachable**, **modern and timeless** - perfect for fintech applications requiring user trust while democratizing complex technology.

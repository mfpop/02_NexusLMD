# NexusLMD Color Guide

This document provides guidance on how to use the modern color scheme in your project for maximum readability and design consistency.

## Color Palette Overview

### Base Grays
- **Gray-100** `#f5f7f4`: Lightest gray, useful for subtle backgrounds
- **Gray-200** `#DFE6DA`: Light gray borders, dividers
- **Gray-300** `#CBD5C0`: Medium-light gray, secondary dividers
- **Gray-400** `#ADB7A4`: Medium gray, subtle text
- **Gray-500** `#8D968A`: Darker gray, secondary text

### Primary Green Palette
- **Green-100** `#e8f0e0`: Very light green background
- **Green-200** `#b4bdb0`: Light green borders
- **Green-300** `#a5b298`: Mid-tone green, secondary buttons
- **Green-400** `#9CAF88`: Medium green, primary buttons
- **Green-500** `#5a6b56`: Dark green, hover states
- **Green-600** `#3e503a`: Darker green, active states
- **Green-700** `#2c3a28`: Darkest green, shadows/depth

### Accent Colors
- **Blue** `#84A9C0`: Primary blue accent
- **Blue-Light** `#D1E4F3`: Light blue background
- **Blue-Dark** `#4B7494`: Dark blue for hover states
- **Amber** `#D4B483`: Warm accent color
- **Amber-Light** `#F0E4C9`: Light warm background
- **Amber-Dark** `#A08250`: Dark amber for hover states

### Status Colors
- **Success** `#6AB547`: Positive actions, confirmations
- **Success-Light** `#E3F1D9`: Background for success messages
- **Warning** `#F0C05A`: Caution indicators
- **Warning-Light** `#FDF5DD`: Background for warning messages
- **Error** `#D9534F`: Error states, destructive actions
- **Error-Light** `#F9DCDA`: Background for error messages
- **Info** `#5BC0DE`: Information indicators
- **Info-Light** `#DCF2F8`: Background for info messages

### Text & Background Colors
- **Text-Primary** `#1E2B1B`: Main text color, headings
- **Text-Secondary** `#4A5547`: Secondary text, subheadings
- **Text-Tertiary** `#777F74`: Lower emphasis text, captions
- **Text-Light** `#FFFFFF`: Text on dark backgrounds
- **BG-Primary** `#FFFFFF`: Main background
- **BG-Secondary** `#F9FAF8`: Alternating sections
- **BG-Tertiary** `#EEF2EB`: Card backgrounds, highlights
- **BG-Dark** `#2c3a28`: Dark mode backgrounds

## Usage Guidelines

### Text Readability
- Use `text-primary` on light backgrounds
- Use `text-light` on dark backgrounds
- Maintain a minimum contrast ratio of 4.5:1 for body text and 3:1 for large text
- Apply the `.text-readable` utility class for optimal line spacing

### Components
- **Buttons**:
  - Primary: `bg-green-400 text-light`
  - Secondary: `bg-green-100 text-primary border-green-300`
  - Danger: `bg-error text-light`
  - Disabled: `bg-gray-300 text-gray-500`

- **Cards**:
  - Standard: `bg-bg-primary border-gray-200 .card`
  - Highlighted: `bg-bg-tertiary border-green-200 .card`

- **Alerts**:
  - Success: `bg-success-light text-success border-success`
  - Warning: `bg-warning-light text-warning-dark border-warning`
  - Error: `bg-error-light text-error border-error`
  - Info: `bg-info-light text-info border-info`

### Accessibility Notes
- Always maintain adequate contrast between text and background
- Use the status colors to reinforce meaning, but don't rely solely on color
- Consider adding patterns or icons for color-blind users

## Tailwind Usage Examples

```html
<!-- Primary Button -->
<button class="bg-green-400 hover:bg-green-500 active:bg-green-600 text-text-light px-4 py-2 rounded-md">
  Submit
</button>

<!-- Card with Elevation -->
<div class="bg-bg-primary border border-gray-200 rounded-lg p-4 elevated">
  Card content
</div>

<!-- Alert -->
<div class="bg-warning-light border-l-4 border-warning p-4 mb-4">
  <p class="text-warning-dark">Please review your submission before continuing.</p>
</div>

<!-- Navigation Link -->
<a href="#" class="text-accent-blue hover:text-accent-blue-dark">View details</a>
```
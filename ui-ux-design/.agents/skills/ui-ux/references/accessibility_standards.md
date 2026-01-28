# Accessibility (WCAG 2.1) Audit Checklist

Ensure all designs meet AA (essential) or AAA (optimal) standards.

## 1. Perceivable

- **Text Contrast (AA):** Normal text must have a 4.5:1 ratio; Large text 3:1.
- **Non-Text Contrast:** Icons and interface components need a 3:1 ratio against the background.
- **Color Independence:** Never use color alone to convey meaning (e.g., use text labels or icons alongside error red).
- **Alt Text:** All meaningful images must have descriptive alternative text.

## 2. Operable

- **Keyboard Accessible:** All interactive elements (links, buttons, forms) must be navigable via Tab key.
- **Focus States:** Clearly visible focus indicators for keyboard users (do not remove `outline: none` without replacement).
- **Target Size:** Touch targets should be at least 44x44 CSS pixels (Mobile).

## 3. Understandable

- **Labels & Instructions:** Form fields must have visible labels (placeholders are not replacements).
- **Error Identification:** Errors must be described in text and the error field clearly identified.
- **Consistent Navigation:** Navigation mechanisms should occur in the same order across pages.

## 4. Robust

- **Parsing:** IDs must be unique to ensure assistive technologies can parse the DOM correctly.
- **Screen Reader Testing:** Verify content order makes sense when read linearly.

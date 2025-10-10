# Assets Folder

This folder contains all static assets for the Wine Quality Prediction application.

## Structure

```
assets/
├── favicon.svg          # Website favicon
└── images/
    ├── wine-bottle.svg  # Wine bottle illustration
    ├── wine-glass.svg   # Wine glass illustration
    ├── grape.svg        # Grape cluster illustration
    └── hero-image.svg   # Hero banner image
```

## Image Descriptions

### favicon.svg
- 32x32 px SVG favicon
- Wine glass design with gradient fill
- Used in browser tabs and bookmarks

### wine-bottle.svg
- Detailed wine bottle illustration
- Burgundy/red gradient colors
- Can be used for decorative purposes

### wine-glass.svg
- Wine glass filled with red wine
- Realistic glass appearance with highlights
- Perfect for result displays

### grape.svg
- Purple grape cluster with leaf
- Decorative element for wine theme
- Can be used in headers or footers

### hero-image.svg
- 800x400 px banner image
- Gradient background with wine glass
- Used as header/hero section background

## Usage

Reference these assets in HTML templates using Flask's `url_for()`:

```html
<!-- Favicon -->
<link rel="icon" type="image/svg+xml" href="{{ url_for('static', filename='assets/favicon.svg') }}">

<!-- Images -->
<img src="{{ url_for('static', filename='assets/images/wine-glass.svg') }}" alt="Wine Glass">
```

## Customization

All images are in SVG format and can be easily customized by:
1. Opening the SVG file in a text editor
2. Modifying colors in the gradient definitions
3. Adjusting sizes and positions

## Credits

All graphics created specifically for the Wine Quality Prediction project.

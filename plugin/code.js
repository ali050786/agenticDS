"use strict";
(() => {
  // src/extractors/colors.ts
  var extractColors = () => {
    return figma.getLocalPaintStyles().map((style) => {
      const paint = style.paints[0];
      if (paint.type === "SOLID") {
        const { r, g, b } = paint.color;
        return {
          name: style.name,
          value: `rgb(${Math.round(r * 255)}, ${Math.round(g * 255)}, ${Math.round(b * 255)})`,
          description: style.description
        };
      }
      return null;
    }).filter(Boolean);
  };

  // src/extractors/typography.ts
  var extractTypography = () => {
    return figma.getLocalTextStyles().map((style) => ({
      name: style.name,
      fontFamily: style.fontName.family,
      fontSize: style.fontSize,
      fontWeight: style.fontName.style,
      lineHeight: style.lineHeight.unit === "AUTO" ? "auto" : style.lineHeight.value
    }));
  };

  // src/code.ts
  figma.showUI(__html__, { width: 400, height: 600 });
  figma.ui.onmessage = async (msg) => {
    if (msg.type === "collect-data") {
      const colors = extractColors();
      const typography = extractTypography();
      const components = figma.root.findAllWithCriteria({
        types: ["COMPONENT", "COMPONENT_SET"]
      }).map((c) => ({
        id: c.id,
        name: c.name,
        description: c.description || "",
        type: c.type
      }));
      const designSystem = {
        version: "1.0.0",
        lastUpdated: (/* @__PURE__ */ new Date()).toISOString(),
        tokens: {
          colors,
          typography,
          spacing: []
          // Will be extracted from components later
        },
        components
      };
      console.log("Design System Extracted:", designSystem);
      figma.ui.postMessage({ type: "data-collected", data: designSystem });
    }
  };
})();

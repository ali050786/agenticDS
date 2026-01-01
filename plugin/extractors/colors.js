"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.extractColors = void 0;
const extractColors = () => {
    return figma.getLocalPaintStyles().map(style => {
        const paint = style.paints[0];
        if (paint.type === 'SOLID') {
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
exports.extractColors = extractColors;

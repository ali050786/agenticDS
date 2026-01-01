"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.extractTypography = void 0;
const extractTypography = () => {
    return figma.getLocalTextStyles().map(style => ({
        name: style.name,
        fontFamily: style.fontName.family,
        fontSize: style.fontSize,
        fontWeight: style.fontName.style,
        lineHeight: style.lineHeight.unit === 'AUTO' ? 'auto' : style.lineHeight.value
    }));
};
exports.extractTypography = extractTypography;

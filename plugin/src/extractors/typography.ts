export const extractTypography = () => {
    return figma.getLocalTextStyles().map(style => ({
        name: style.name,
        fontFamily: style.fontName.family,
        fontSize: style.fontSize,
        fontWeight: style.fontName.style,
        lineHeight: style.lineHeight.unit === 'AUTO' ? 'auto' : style.lineHeight.value
    }));
};

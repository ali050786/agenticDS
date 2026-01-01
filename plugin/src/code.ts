import { extractColors } from './extractors/colors';
import { extractTypography } from './extractors/typography';

figma.showUI(__html__, { width: 400, height: 600 });

figma.ui.onmessage = async (msg) => {
    if (msg.type === 'collect-data') {
        const colors = extractColors();
        const typography = extractTypography();

        const components = figma.root.findAllWithCriteria({
            types: ['COMPONENT', 'COMPONENT_SET']
        }).map(c => ({
            id: c.id,
            name: c.name,
            description: (c as ComponentNode).description || '',
            type: c.type
        }));

        const designSystem = {
            version: '1.0.0',
            lastUpdated: new Date().toISOString(),
            tokens: {
                colors,
                typography,
                spacing: [] // Will be extracted from components later
            },
            components
        };

        console.log('Design System Extracted:', designSystem);
        figma.ui.postMessage({ type: 'data-collected', data: designSystem });
    }
};

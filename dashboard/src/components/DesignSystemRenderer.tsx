import React from 'react';

interface DesignSystemRendererProps {
    designSystem: any;
    mode: 'display' | 'edit';
}

const ColorToken = ({ name, value }: { name: string, value: string }) => (
    <div className="flex items-center space-x-2 p-2 rounded border border-gray-200">
        <div
            className="w-8 h-8 rounded border border-gray-300"
            style={{ backgroundColor: value }}
        />
        <div>
            <div className="font-semibold text-sm">{name}</div>
            <div className="text-xs text-gray-500">{value}</div>
        </div>
    </div>
);

const TypographyToken = ({ token }: { token: any }) => (
    <div className="p-4 rounded border border-gray-200">
        <div className="font-semibold text-sm mb-2">{token.name}</div>
        <div style={{
            fontFamily: token.fontFamily || 'inherit',
            fontWeight: token.fontWeight || 400,
            fontSize: token.fontSize ? `${token.fontSize}px` : '16px',
            lineHeight: token.lineHeight ? `${token.lineHeight}px` : '1.5',
        }}>
            The quick brown fox jumps over the lazy dog
        </div>
        <div className="mt-2 text-xs text-gray-500 grid grid-cols-2 gap-2">
            {Object.entries(token).map(([key, val]) => {
                if (key === 'name') return null;
                return (
                    <div key={key}>
                        <span className="font-medium">{key}:</span> {String(val)}
                    </div>
                );
            })}
        </div>
    </div>
);

const Section = ({ title, children }: { title: string, children: React.ReactNode }) => (
    <div className="mb-8">
        <h3 className="font-bold text-lg mb-4 capitalize border-b pb-2">{title}</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {children}
        </div>
    </div>
);

const ComponentTreeRenderer = ({ node }: { node: any }) => {
    if (!node) return null;

    // Handle string content
    if (typeof node === 'string') return <span>{node}</span>;

    const { type, props, content, children } = node;

    // safeProps ensures we don't pass undefined/null to style if not intended or handle style mapping
    const style: React.CSSProperties = { ...props?.style };

    // Simple mapping of "Design System" components to HTML/Tailwind
    // In a real app, these would be your actual React components

    if (type === 'Container') {
        const bg = props?.background || props?.backgroundColor || 'transparent';
        const p = props?.padding || '1rem';
        return (
            <div style={{ backgroundColor: bg, padding: p, ...style }} className="border border-dashed border-gray-300 rounded">
                {content && <div>{content}</div>}
                {children && children.map((child: any, i: number) => <ComponentTreeRenderer key={i} node={child} />)}
            </div>
        );
    }

    if (type === 'Button') {
        // Fallback for primary/secondary logic if tokens aren't resolved here (simplification)
        const variant = props?.variant === 'primary' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800';
        // Allow direct color override if provided (heuristic)
        const styleOverride = { ...style };
        if (props?.backgroundColor) styleOverride.backgroundColor = props.backgroundColor;

        return (
            <button className={`px-4 py-2 rounded ${variant}`} style={styleOverride}>
                {content || props?.label || 'Button'}
            </button>
        );
    }

    if (type === 'Text') {
        return (
            <p style={style} className="my-2">
                {content || props?.children}
            </p>
        );
    }

    if (type === 'Input') {
        return (
            <input
                type="text"
                placeholder={props?.placeholder || 'Input'}
                className="border p-2 rounded w-full"
                style={style}
            />
        );
    }

    // Default fallback
    return (
        <div className="p-2 border border-red-200 bg-red-50 text-red-800 text-xs">
            Unknown Component: {type}
        </div>
    );
};

export const DesignSystemRenderer: React.FC<DesignSystemRendererProps> = ({ designSystem }) => {
    if (!designSystem) {
        return <div className="p-4 text-gray-500">No content loaded.</div>;
    }

    // Heuristic: If it has "type" (like "Container"), treat as component tree
    if (designSystem.type) {
        return (
            <div className="p-8 border border-gray-200 rounded-lg shadow-sm bg-white min-h-[400px]">
                <ComponentTreeRenderer node={designSystem} />
            </div>
        );
    }

    const { tokens, components } = designSystem;

    return (
        <div className="space-y-8 p-6">
            <h1 className="text-3xl font-bold border-b pb-4">Design System Explorer</h1>

            {/* Metadata */}
            <div className="text-sm text-gray-500 flex space-x-4">
                <span>Version: {designSystem.version}</span>
                <span>Last Updated: {designSystem.updated_at ? new Date(designSystem.updated_at).toLocaleString() : 'N/A'}</span>
            </div>

            {/* Tokens */}
            {tokens && (
                <div className="space-y-6">
                    <h2 className="text-2xl font-semibold">Tokens</h2>

                    {tokens.colors && Array.isArray(tokens.colors) && (
                        <Section title="Colors">
                            {tokens.colors.map((color: any, idx: number) => (
                                <ColorToken key={idx} name={color.name} value={color.value} />
                            ))}
                        </Section>
                    )}

                    {tokens.typography && Array.isArray(tokens.typography) && (
                        <Section title="Typography">
                            {tokens.typography.map((typo: any, idx: number) => (
                                <TypographyToken key={idx} token={typo} />
                            ))}
                        </Section>
                    )}

                    {tokens.spacing && Array.isArray(tokens.spacing) && (
                        <Section title="Spacing">
                            {tokens.spacing.map((space: any, idx: number) => (
                                <div key={idx} className="p-2 border border-gray-200 rounded">
                                    <div className="font-semibold">{space.name}</div>
                                    <div className="text-gray-500">{space.value}</div>
                                    <div className="mt-1 h-4 bg-gray-200" style={{ width: space.value }}></div>
                                </div>
                            ))}
                        </Section>
                    )}
                </div>
            )}

            {/* Components fallback or list */}
            {components && Array.isArray(components) && (
                <div className="space-y-6">
                    <h2 className="text-2xl font-semibold">Components</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {components.map((comp: any, idx: number) => (
                            <div key={idx} className="p-4 border rounded shadow-sm">
                                <h3 className="font-bold">{comp.name}</h3>
                                <div className="text-xs text-gray-500">ID: {comp.id}</div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Fallback for generic structure if not matching above */}
            {!tokens && !components && (
                <pre className="bg-gray-100 p-4 rounded overflow-auto text-xs">
                    {JSON.stringify(designSystem, null, 2)}
                </pre>
            )}
        </div>
    );
};

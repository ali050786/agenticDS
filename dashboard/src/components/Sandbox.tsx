import React, { useState } from 'react';
import { DesignSystemRenderer } from './DesignSystemRenderer';

const API_BASE_URL = 'http://localhost:8000';

export const Sandbox: React.FC = () => {
    const [prompt, setPrompt] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    const handleGenerate = async () => {
        if (!prompt.trim()) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await fetch(`${API_BASE_URL}/api/sandbox/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Failed to generate design');
            }

            const data = await response.json();
            console.log('Sandbox generation response:', data);

            if (data.status === 'error') {
                throw new Error(data.message || 'Backend service reported an error');
            }

            setResult(data);
        } catch (err: any) {
            console.error('Generation failed:', err);
            setError(err.message || 'An unknown error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-8">
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <h2 className="text-xl font-bold mb-4">Sandbox Generator</h2>
                <div className="flex gap-4">
                    <input
                        type="text"
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        placeholder="Describe the UI you want effectively (e.g., 'A login form with email and password')"
                        className="flex-1 p-3 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:outline-none"
                        onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
                    />
                    <button
                        onClick={handleGenerate}
                        disabled={loading || !prompt.trim()}
                        className={`px-6 py-3 rounded font-medium text-white transition-colors ${loading || !prompt.trim()
                            ? 'bg-blue-300 cursor-not-allowed'
                            : 'bg-blue-600 hover:bg-blue-700'
                            }`}
                    >
                        {loading ? 'Generating...' : 'Generate'}
                    </button>
                </div>
                {error && (
                    <div className="mt-4 p-3 bg-red-50 text-red-700 rounded border border-red-200">
                        {error}
                    </div>
                )}
            </div>

            {result && (
                <div className="space-y-8 animate-fade-in">
                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                        <h3 className="text-lg font-semibold mb-4 text-gray-700">Preview</h3>
                        <DesignSystemRenderer designSystem={result.design} mode="display" />
                    </div>

                    <div className="bg-gray-900 text-gray-100 p-6 rounded-lg shadow-sm overflow-hidden">
                        <h3 className="text-lg font-semibold mb-4 text-gray-300">Generated Code</h3>
                        <pre className="overflow-x-auto text-sm font-mono whitespace-pre-wrap">
                            {result.code}
                        </pre>
                    </div>
                </div>
            )}
        </div>
    );
};

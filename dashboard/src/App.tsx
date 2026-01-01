import React, { useState } from 'react';
import { useDesignSystem } from './hooks/useDesignSystem';
import { DesignSystemRenderer } from './components/DesignSystemRenderer';
import { Sandbox } from './components/Sandbox';

function App() {
    const { designSystem, loading, error } = useDesignSystem();
    const [activeTab, setActiveTab] = useState<'explorer' | 'sandbox'>('explorer');

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-50">
                <div className="text-xl font-semibold text-gray-600">Loading Design System...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-red-50">
                <div className="text-red-600 border border-red-200 bg-white p-6 rounded shadow-sm">
                    <h2 className="text-lg font-bold mb-2">Error Loading Design System</h2>
                    <p>{error}</p>
                    <p className="text-sm mt-4 text-gray-500">Ensure the backend is running at http://localhost:8000</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
            {/* Navigation Bar */}
            <div className="bg-white border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="flex space-x-8">
                        <button
                            onClick={() => setActiveTab('explorer')}
                            className={`py-4 px-2 border-b-2 font-medium text-sm transition-colors ${activeTab === 'explorer'
                                    ? 'border-blue-500 text-blue-600'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                }`}
                        >
                            Design System Explorer
                        </button>
                        <button
                            onClick={() => setActiveTab('sandbox')}
                            className={`py-4 px-2 border-b-2 font-medium text-sm transition-colors ${activeTab === 'sandbox'
                                    ? 'border-blue-500 text-blue-600'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                }`}
                        >
                            Sandbox
                        </button>
                    </div>
                </div>
            </div>

            <div className="max-w-7xl mx-auto py-8">
                {activeTab === 'explorer' ? (
                    <DesignSystemRenderer designSystem={designSystem} mode="display" />
                ) : (
                    <Sandbox />
                )}
            </div>
        </div>
    );
}

export default App;

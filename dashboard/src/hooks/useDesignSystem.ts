import { useState, useEffect } from 'react';

export function useDesignSystem() {
    const [designSystem, setDesignSystem] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchDesignSystem = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/design-system/latest');
                if (!response.ok) {
                    throw new Error('Failed to fetch design system');
                }
                const data = await response.json();
                setDesignSystem(data);
            } catch (err: any) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchDesignSystem();
    }, []);

    return { designSystem, loading, error };
}

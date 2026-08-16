// Shmry AI Integration for Shmry Platform
// Connects local AI models (Ollama/Jan AI) with Shmry services

class OllamaIntegration {
    constructor() {
        this.baseUrl = 'http://localhost:11434'; // Default Ollama API endpoint
        this.model = 'deepseek-r1:8b'; // Use available model instead of non-existent badrpk/shmry
        this.apiKey = 'abfbcd5d54fb4f49b2e1a87312650684.Mq2rHj_t-9O3wCbstnJicOik'; // Shmry API key
        this.isConnected = false;
        this.connectionStatus = 'disconnected';
    }

    // Check if AI models are running and accessible
    async checkConnection() {
        try {
            const response = await fetch(`${this.baseUrl}/api/tags`, {
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'X-Shmry-API-Key': this.apiKey
                }
            });
            if (response.ok) {
                this.isConnected = true;
                this.connectionStatus = 'connected';
                console.log('✅ Shmry AI connected successfully');
                return true;
            }
        } catch (error) {
            console.error('❌ Shmry AI connection failed:', error);
            this.isConnected = false;
            this.connectionStatus = 'error';
        }
        return false;
    }

    // Get available models
    async getModels() {
        try {
            const response = await fetch(`${this.baseUrl}/api/tags`, {
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'X-Shmry-API-Key': this.apiKey
                }
            });
            if (response.ok) {
                const data = await response.json();
                return data.models || [];
            }
        } catch (error) {
            console.error('Error fetching models:', error);
            return [];
        }
    }

    // Generate AI response using local AI models
    async generateResponse(prompt, options = {}) {
        if (!this.isConnected) {
            await this.checkConnection();
        }

        if (!this.isConnected) {
            throw new Error('AI models are not connected. Please ensure your local AI service is running.');
        }

        const requestBody = {
            model: this.model,
            prompt: prompt,
            stream: false,
            options: {
                temperature: options.temperature || 0.7,
                top_p: options.top_p || 0.9,
                max_tokens: options.max_tokens || 2048,
                ...options
            }
        };

        try {
            const response = await fetch(`${this.baseUrl}/api/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.apiKey}`,
                    'X-Shmry-API-Key': this.apiKey
                },
                body: JSON.stringify(requestBody)
            });

            if (response.ok) {
                const data = await response.json();
                return {
                    success: true,
                    response: data.response,
                    model: data.model,
                    usage: data.usage,
                    done: data.done
                };
            } else {
                throw new Error(`AI API error: ${response.status}`);
            }
        } catch (error) {
            console.error('Error generating response:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    // AI Search functionality
    async search(query, context = '') {
        const searchPrompt = `You are Shmry's AI search assistant. Help users find information about: ${query}

Context: ${context}

Please provide:
1. A clear, helpful answer
2. Relevant information and examples
3. Additional resources if applicable
4. Keep it concise but informative

Query: ${query}`;

        return await this.generateResponse(searchPrompt, {
            temperature: 0.3,
            max_tokens: 1500
        });
    }

    // AI Coding assistance
    async codeAssist(prompt, language = 'javascript', context = '') {
        const codingPrompt = `You are Shmry's AI coding assistant. Help users with ${language} programming.

Context: ${context}

User Request: ${prompt}

Please provide:
1. Clear, working code examples
2. Explanations of the solution
3. Best practices and tips
4. Alternative approaches if applicable

Focus on practical, production-ready code.`;

        return await this.generateResponse(codingPrompt, {
            temperature: 0.2,
            max_tokens: 2500
        });
    }

    // Code review and improvement
    async codeReview(code, language = 'javascript') {
        const reviewPrompt = `You are Shmry's AI code reviewer. Review this ${language} code and provide improvements:

Code to review:
\`\`\`${language}
${code}
\`\`\`

Please provide:
1. Code quality assessment
2. Specific improvements and suggestions
3. Security considerations
4. Performance optimizations
5. Best practices recommendations
6. Improved version of the code`;

        return await this.generateResponse(reviewPrompt, {
            temperature: 0.1,
            max_tokens: 3000
        });
    }

    // Debugging assistance
    async debugHelp(error, code, language = 'javascript') {
        const debugPrompt = `You are Shmry's AI debugging assistant. Help fix this ${language} error:

Error:
${error}

Code:
\`\`\`${language}
${code}
\`\`\`

Please provide:
1. Root cause analysis
2. Step-by-step solution
3. Corrected code
4. Prevention tips
5. Common debugging strategies`;

        return await this.generateResponse(debugPrompt, {
            temperature: 0.1,
            max_tokens: 2500
        });
    }

    // Documentation generation
    async generateDocs(code, language = 'javascript') {
        const docsPrompt = `You are Shmry's AI documentation generator. Create comprehensive documentation for this ${language} code:

Code:
\`\`\`${language}
${code}
\`\`\`

Please generate:
1. Function/class documentation
2. Parameter descriptions
3. Return value explanations
4. Usage examples
5. API reference format
6. JSDoc or similar standard format`;

        return await this.generateResponse(docsPrompt, {
            temperature: 0.2,
            max_tokens: 2000
        });
    }

    // Test case generation
    async generateTests(code, language = 'javascript', framework = 'jest') {
        const testPrompt = `You are Shmry's AI test generator. Create comprehensive tests for this ${language} code using ${framework}:

Code:
\`\`\`${language}
${code}
\`\`\`

Please generate:
1. Unit tests for all functions/methods
2. Edge case testing
3. Error handling tests
4. Mock data and setup
5. Test descriptions and assertions
6. Coverage considerations`;

        return await this.generateResponse(testPrompt, {
            temperature: 0.3,
            max_tokens: 3000
        });
    }

    // Performance optimization
    async optimizeCode(code, language = 'javascript') {
        const optimizePrompt = `You are Shmry's AI performance optimizer. Analyze and optimize this ${language} code:

Original Code:
\`\`\`${language}
${code}
\`\`\`

Please provide:
1. Performance analysis
2. Bottleneck identification
3. Optimization strategies
4. Optimized code version
5. Performance metrics improvements
6. Best practices for ${language}`;

        return await this.generateResponse(optimizePrompt, {
            temperature: 0.2,
            max_tokens: 2500
        });
    }

    // Get system status
    async getStatus() {
        try {
            const response = await fetch(`${this.baseUrl}/api/tags`, {
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'X-Shmry-API-Key': this.apiKey
                }
            });
            if (response.ok) {
                const data = await response.json();
                return {
                    connected: true,
                    models: data.models || [],
                    status: 'running',
                    timestamp: new Date().toISOString()
                };
            }
        } catch (error) {
            return {
                connected: false,
                error: error.message,
                status: 'error',
                timestamp: new Date().toISOString()
            };
        }
    }

    // Health check
    async healthCheck() {
        return await this.checkConnection();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OllamaIntegration;
} else {
    // Browser environment
    window.OllamaIntegration = OllamaIntegration;
}

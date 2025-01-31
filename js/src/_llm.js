/**
 *
 */

export default class LLM {
    constructor({
        model,
        apiUrl = 'https://api.example.com/v1/',
        apiKey,
        cache = true,
        cachePrefix = 'llm-cache:',
    } = {}) {
        if (!model) {
            throw new Error('model is required');
        }
        this.model = model;
        this.apiUrl = apiUrl;
        this.apiKey = apiKey;
        this.cache = cache;
        this.cachePrefix = cachePrefix;
        
        // Initialize cache if needed
        if (this.cache) {
            this.cache = {
                get: (key) => this.getCache(key),
                set: (key, value) => this.setCache(key, value),
            };
        }
    }

    async complete(body = {}) {
        const isChat = 'messages' in body;
        const endpoint = isChat ? 'v1/chat/completions' : 'v1/completions';
        const mergedOptions = {
            ...this.defaultCompleteOptions,
            ...body,
            model: this.model,
        };
        
        const ckey = this.generateCacheKey(mergedOptions, endpoint);
        let result;
        
        if (this.cache) {
            const cached = await this.cache.get(ckey);
            if (cached) {
                result = cached;
            }
        }
        
        if (!result) {
            result = await this.request(endpoint, mergedOptions);
            if (this.cache) {
                this.cache.set(ckey, result);
            }
        }
        
        return result;
    }

    async embed(body = {}) {
        const mergedOptions = {
            ...this.defaultEmbedOptions,
            ...body,
        };
        
        const ckey = this.generateCacheKey(mergedOptions, 'v1/embeddings');
        let result;
        
        if (this.cache) {
            const cached = await this.cache.get(ckey);
            if (cached) {
                result = cached;
            }
        }
        
        if (!result) {
            result = await this.request('v1/embeddings', mergedOptions);
            if (this.cache) {
                this.cache.set(ckey, result);
            }
        }
        
        return result;
    }

    async generateCacheKey(options, endpoint) {
        const keyStr = JSON.stringify({
            ...options,
            endpoint,
        }, Object.keys(options).sort());
        const encoder = new TextEncoder();
        const data = encoder.encode(keyStr);
        const hashBuffer = await window.crypto.subtle.digest("SHA-256", data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return `${this.cachePrefix}${btoa(String.fromCharCode(...hashArray))}`;
    }

    async request(endpoint, options) {
        let url;
        if (endpoint === 'complete') {
            if (options.messages) {
                url = `${this.apiUrl}v1/chat/completions`;
            } else {
                url = `${this.apiUrl}v1/completions`;
            }
        } else if (endpoint === 'embed') {
            url = `${this.apiUrl}v1/embeddings`;
        } else {
            url = `${this.apiUrl}${endpoint}`;
        }
        const headers = {
            'Content-Type': 'application/json',
        };
        
        if (this.apiKey) {
            headers['Authorization'] = `Bearer ${this.apiKey}`;
        }

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers,
                body: JSON.stringify(options),
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            throw new Error(`API request failed: ${error.message}`);
        }
    }

    async setCache(key, value) {
        const cacheEntry = {
            value,
            timestamp: Date.now(),
            expires: Date.now() + (7 * 24 * 60 * 60 * 1000), // 1 week
        };
        localStorage.setItem(key, JSON.stringify(cacheEntry));
    }

    async getCache(key) {
        const cached = localStorage.getItem(key);
        if (!cached) return null;
        
        const cacheEntry = JSON.parse(cached);
        
        if (Date.now() > cacheEntry.expires) {
            localStorage.removeItem(key);
            return null;
        }
        
        return cacheEntry.value;
    }

    get defaultCompleteOptions() {
        return {
            max_tokens: 300,
            temperature: 0.0,
            frequency_penalty: 0,
            presence_penalty: 0,
        };
    }

    get defaultEmbedOptions() {
        return {};
    }
}

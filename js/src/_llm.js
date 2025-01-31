import CryptoJS from 'crypto-js';

export default class LLM {
    constructor({
        model,
        apiUrl = 'https://api.example.com/v1/',
        apiKey,
        cache = true,
        cachePrefix = 'llm-cache:',
    } = {}) {
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

    async complete(prompt, options = {}) {
        const mergedOptions = {
            ...this.defaultCompleteOptions,
            ...options,
        };
        
        const ckey = this.generateCacheKey(mergedOptions);
        let result;
        
        if (this.cache) {
            const cached = await this.cache.get(ckey);
            if (cached) {
                result = cached;
            }
        }
        
        if (!result) {
            result = await this.request('complete', mergedOptions);
            if (this.cache) {
                this.cache.set(ckey, result);
            }
        }
        
        return result;
    }

    async embed(inputs, options = {}) {
        const mergedOptions = {
            ...this.defaultEmbedOptions,
            ...options,
        };
        
        const ckey = this.generateCacheKey(mergedOptions);
        let result;
        
        if (this.cache) {
            const cached = await this.cache.get(ckey);
            if (cached) {
                result = cached;
            }
        }
        
        if (!result) {
            result = await this.request('embed', mergedOptions);
            if (this.cache) {
                this.cache.set(ckey, result);
            }
        }
        
        return result;
    }

    generateCacheKey(options) {
        const keyStr = JSON.stringify(options, Object.keys(options).sort());
        const hash = CryptoJS.SHA256(keyStr);
        return `${this.cachePrefix}${hash.toString(CryptoJS.enc.Base64)}`;
    }

    async request(endpoint, options) {
        const url = `${this.apiUrl}${endpoint}`;
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

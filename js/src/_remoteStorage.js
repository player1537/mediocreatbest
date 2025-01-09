/**
 *
 */

import Keyvalue from './_keyvalue.js';


class RemoteStorage {
    constructor({
        prefix = null,
        ...options
    } = {}) {
        this.prefix = prefix;
        this.options = options;
    }

    configure({
        prefix,
        ...options
    }) {
        if (prefix !== undefined) {
            this.prefix = prefix;
        }

        this.options = {
            ...this.options,
            ...options,
        };
    }

    async getItem(k) {
        if (this.prefix !== null) {
            k = `${this.prefix}${k}`;
        }

        return await Keyvalue.get(k, {
            ...this.options,
            otherwise: null,
        });
    }

    async setItem(k, v) {
        if (this.prefix !== null) {
            k = `${this.prefix}${k}`;
        }

        await Keyvalue.put(k, v, {
            ...this.options,
        });
    }
}

let remoteStorage = new RemoteStorage();

export default remoteStorage;

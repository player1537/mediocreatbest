/**
 * 
 */

import assert from 'node:assert';
import { describe, it } from 'node:test';
import mediocreatbest from './src/index.js';


describe('Prompt', function() {
    it('should return 1 message', function() {
        let p = mediocreatbest.Prompt(`
            {% call user() -%}
            Hello {{ who }}!
            {%- endcall %}
        `, {
            who: 'world',
        });

        let expected = {
            messages: [
                {
                    role: 'user',
                    content: 'Hello world!',
                },
            ],
        };

        assert.deepStrictEqual(p, expected);
    });

    it('should return 2 messages', function() {
        let p = mediocreatbest.Prompt(`
            {% call user() -%}
            Hello {{ who }}!
            {%- endcall %}
            {% call assistant() -%}
            Hi there!
            {%- endcall %}
        `, {
            who: 'world',
        });

        let expected = {
            messages: [
                {
                    role: 'user',
                    content: 'Hello world!',
                },
                {
                    role: 'assistant',
                    content: 'Hi there!',
                },
            ],
        };

        assert.deepStrictEqual(p, expected);
    });

    it('should return 1 prompt', function() {
        let p = mediocreatbest.Prompt(`
            {% call prompt() -%}
            Hello, world!
            {%- endcall %}
        `);

        let expected = {
            prompt: 'Hello, world!',
        };

        assert.deepStrictEqual(p, expected);
    });

    it('should return 1 grammar', function() {
        let p = mediocreatbest.Prompt(`
            {% call grammar() -%}
            Hello, world!
            {%- endcall %}
        `);

        let expected = {
            grammar: 'Hello, world!',
        };

        assert.deepStrictEqual(p, expected);
    });
});


//--- Keyvalue

mediocreatbest.Keyvalue.configure({
    verbose: false,
    apiKey: process.env.VAINL_API_KEY,
});


describe('Keyvalue', function() {
    it('should return known value', async function() {
        let k = `98e49b97-61a1-491b-8f80-d55bad7403ea`;
        let exp = `31dabb10-ea84-475c-b51a-2941eca8e10c`;
        let got = await mediocreatbest.Keyvalue(k);

        assert.strictEqual(got, exp);
    });

    it('should return default for new keys', async function() {
        let k = `c5463181-bee3-472a-832b-6b568aacda85-${Date.now()}`;
        let exp = `28fa6ba0-d7df-405b-abb2-deaf53b44b3f`;

        let got = await mediocreatbest.Keyvalue(k, {
            otherwise: exp,
        });

        assert.strictEqual(got, exp);
    });

    it('should return known json', async function() {
        let k = `a2700076-f2e3-4d60-b2ea-7069fad1d893`;
        let exp = {
            hello: `a78b1a5e-0ac3-4013-883c-41b1f026a99a`,
        };

        let got = await mediocreatbest.Keyvalue.json(k);

        assert.deepStrictEqual(got, exp);
    });

    it('should return default json', async function() {
        let k = `05832fd2-9a02-4ad0-8ab6-29072bfe21b7-${Date.now()}`;
        let exp = {
            hello: `008badaf-8339-4bc3-b0a8-d4ee9bd5d482`,
        };

        let got = await mediocreatbest.Keyvalue.json(k, {
            otherwise: exp,
        });

        assert.deepStrictEqual(got, exp);
    });
});


//--- remoteStorage

mediocreatbest.remoteStorage.configure({
    apiKey: process.env.VAINL_API_KEY,
});


describe('remoteStorage', function() {
    it('should return known value', async function() {
        mediocreatbest.remoteStorage.configure({
            prefix: `98e49b97-`,
        });

        let k = `61a1-491b-8f80-d55bad7403ea`;
        let exp = `31dabb10-ea84-475c-b51a-2941eca8e10c`;
        let got = await mediocreatbest.remoteStorage.getItem(k);

        assert.strictEqual(got, exp);
    });
});

/**
 * 
 */

import assert from 'assert';
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



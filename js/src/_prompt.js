/**
 *
 */

import nunjucks from './external/_nunjucks.js';


let __Prompt_environment = new nunjucks.Environment(null, {
    autoescape: false,
    throwOnUndefined: true,
    trimBlocks: true,
    lstripBlocks: true,
});

let __Prompt_cache = new Map();

function Prompt(s, context) {
    let ckey = s;
    if (!__Prompt_cache.has(ckey)) {
        let template = nunjucks.compile(s, __Prompt_environment);

        __Prompt_cache.set(ckey, template);
    }

    let template = __Prompt_cache.get(ckey);

    let messages = null;
    function AddMessage(role, content) {
        if (messages === null) {
            messages = [];
        }

        messages.push({
            role,
            content,
        });
    }

    let prompt = null;
    function AddPrompt(content) {
        if (prompt === null) {
            prompt = '';
        }

        prompt += content;
    }

    let grammar = null;
    function AddGrammar(content) {
        if (grammar === null) {
            grammar = '';
        }

        grammar += content;
    }

    context = {
        ...context,
        system({ caller }) {
            let { val } = caller();
            AddMessage('system', val);
            return '<system>';
        },
        user({ caller }) {
            let { val } = caller();
            AddMessage('user', val);
            return '<user>';
        },
        assistant({ caller }) {
            let { val } = caller();
            AddMessage('assistant', val);
            return '<assistant>';
        },
        prompt({ caller }) {
            let { val } = caller();
            AddPrompt(val);
            return '<prompt>';
        },
        grammar({ caller }) {
            let { val } = caller();
            AddGrammar(val);
            return '<grammar>';
        },
    };

    template.render(context);

    let ret = {};
    if (messages !== null) {
        ret.messages = messages;
    }
    if (prompt !== null) {
        ret.prompt = prompt;
    }
    if (grammar !== null) {
        ret.grammar = grammar;
    }

    return ret;
}


export default Prompt;

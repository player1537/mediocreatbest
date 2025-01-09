/**
 *
 */

async function Keyvalue(k, vOrOptions, options) {
    let v;
    if (vOrOptions === undefined) {
        v = undefined;
    } else if (typeof vOrOptions === 'string' || vOrOptions instanceof String) {
        v = vOrOptions;
    } else {
        v = undefined;
        options = vOrOptions;
    }

    if (v === undefined) {
        return Keyvalue.get(k, options);
    
    } else {
        return Keyvalue.put(k, v, options);

    }
}

Keyvalue.config = {
    apiUrl: `https://sdoh.with.vainl.in.production.is.mediocreatbest.xyz/vainl/kind_violet/keyvalue/`,
    apiKey: null,
    verbose: true,
};

Keyvalue.configure = function __Keyvalue_configure(config) {
    Keyvalue.config = {
        ...Keyvalue.config,
        ...config,
    };
};


Keyvalue.json = async function __Keyvalue_json(k, vOrOptions, options) {
    let v;
    if (vOrOptions === undefined) {
        v = undefined;
    } else if (typeof vOrOptions === 'string' || vOrOptions instanceof String) {
        v = vOrOptions;
    } else {
        v = undefined;
        options = vOrOptions;
    }

    if (options === undefined) {
        options = {};
    }

    if (v !== undefined) {
        v = JSON.stringify(v);
    }

    let {
        otherwise = null,
        otherwiseSentinel = `817fa677-7b62-47bb-bf68-afc7228c6d3b`,
        ...rest
    } = options;
    options = rest;

    if (v === undefined) {
        v = await Keyvalue.get(k, {
            ...options,
            otherwise: otherwiseSentinel,
        });
    
    } else {
        v = await Keyvalue.put(k, v, {
            ...options,
            otherwise: otherwiseSentinel,
        });
    }

    if (v === otherwiseSentinel) {
        v = otherwise;
    } else {
        v = JSON.parse(v);
    }

    return v;
};


Keyvalue.get = async function __Keyvalue_get(k, {
    apiUrl = Keyvalue.config.apiUrl,
    apiKey = Keyvalue.config.apiKey,
    verbose = Keyvalue.config.verbose,
    otherwise = null,
    otherwiseSentinel = `4685b44b-bf3b-4da1-9e6e-acaaaa011e5b`,
} = {}) {
    if (verbose) {
        console.log('GET', k);
    }

    let url = new URL(apiUrl);
    url.pathname += encodeURIComponent(k);
    url.searchParams.append('default', otherwiseSentinel);
    url = url.toString();

    let headers = {};
    headers['Authorization'] = `Bearer ${apiKey}`;

    let request = new Request(url, {
        method: 'GET',
        headers,
    });

    let response = await fetch(request);

    let v = await response.text();

    if (v === otherwiseSentinel) {
        v = otherwise;
    }

    return v;
}


Keyvalue.put = async function __Keyvalue_put(k, v, {
    apiUrl = Keyvalue.config.apiUrl,
    apiKey = Keyvalue.config.apiKey,
    verbose = Keyvalue.config.verbose,
    otherwise = null,
    otherwiseSentinel = `a283551e-9661-4365-b5a2-b7e5df89f00c`,
} = {}) {
    if (verbose) {
        console.log('PUT', k);
    }

    let url = new URL(apiUrl);
    url.pathname += encodeURIComponent(k);
    url.searchParams.append('default', otherwiseSentinel);
    url = url.toString();

    let headers = {};
    headers['Authorization'] = `Bearer ${apiKey}`;

    let request = new Request(url, {
        method: 'PUT',
        headers,
        body: v,
    });

    let response = await fetch(request);

    v = await response.text();

    if (v === otherwiseSentinel) {
        v = otherwise;
    }

    return v;
}


export default Keyvalue;

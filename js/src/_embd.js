/**
 *
 */

function embd() {
    throw new Error('Not implemented');
}


function embd_loads(s) {
    let u8 = Uint8Array.fromBase64(s);
    let f16 = new Float16Array(u8.buffer);
    let f32 = Float32Array.from(f16);
    return f32;
}

embd.loads = embd_loads;


async function embd_aloads(s) {
    let url = `data:application/octet-stream;base64,${s}`;
    let request = new Request(url);
    let response = await fetch(request);
    let arrayBuffer = await response.arrayBuffer();
    let f16array = new Float16Array(arrayBuffer);
    let f32array = Float32Array.from(f16array);
    return f32array;
}

embd.aloads = embd_aloads;


function embd_dumps(v) {
    let f16 = Float16Array.from(v);
    let u8 = new Uint8Array(f16.buffer);
    let b = u8.toBase64();
    return b;
}

embd.dumps = embd_dumps;


export default embd;

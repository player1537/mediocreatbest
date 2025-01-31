"""Populate the model metadata JSON file with the latest data from the OpenRouter API.

{
    "openrouter/meta-llama/llama-3.2-3b-instruct": {
        "max_tokens": 100000,
        "max_input_tokens": 100000,
        "max_output_tokens": 100000,
        "input_cost_per_token":  0.000000015,
        "output_cost_per_token": 0.000000025,
        "litellm_provider": "openrouter",
        "mode": "chat"
    }
}

"""

from __future__ import annotations
from .._auto import autoinstall as auto


def Models(
    *,
    href: str = (
        'https://openrouter.ai/api/v1/models'
    ),
) -> auto.pd.DataFrame:
    """Get the models from the OpenRouter API.

    {
      "id": "deepseek/deepseek-r1-distill-qwen-1.5b",
      "name": "Deepseek: Deepseek R1 Distill Qwen 1.5B",
      "created": 1738328067,
      "description": "DeepSeek R1 Distill Qwen 1.5B is a distilled large language model based on  [Qwen 2.5 Math 1.5B](https://huggingface.co/Qwen/Qwen2.5-Math-1.5B), using outputs from [DeepSeek R1](/deepseek/deepseek-r1). It's a very small and efficient model which outperforms [GPT 4o 0513](/openai/gpt-4o-2024-05-13) on Math Benchmarks.\n\nOther benchmark results include:\n\n- AIME 2024 pass@1: 28.9\n- AIME 2024 cons@64: 52.7\n- MATH-500 pass@1: 83.9\n\nThe model leverages fine-tuning from DeepSeek R1's outputs, enabling competitive performance comparable to larger frontier models.",
      "context_length": 131072,
      "architecture": {
        "modality": "text->text",
        "tokenizer": "Other",
        "instruct_type": null
      },
      "pricing": {
        "prompt": "0.00000018",
        "completion": "0.00000018",
        "image": "0",
        "request": "0"
      },
      "top_provider": {
        "context_length": 131072,
        "max_completion_tokens": 2048,
        "is_moderated": false
      },
      "per_request_limits": null
    },
    
    """

    with auto.requests.request(
        'GET',
        href,
    ) as r:
        json = auto.json.loads(r.text)
    
    rows = []
    for json in json['data']:
        name = 'openrouter/' + json['id']
        max_tokens = json['top_provider']['context_length']
        max_input_tokens = max_tokens
        max_output_tokens = max_tokens
        input_cost_per_token = float(json['pricing']['prompt'])
        output_cost_per_token = float(json['pricing']['completion'])
        litellm_provider = 'openrouter'
        mode = 'chat'
        
        rows.append((
            name,
            max_tokens,
            max_input_tokens,
            max_output_tokens,
            input_cost_per_token,
            output_cost_per_token,
            litellm_provider,
            mode,
        ))
    
    df = auto.pd.DataFrame(
        rows,
        columns=[
            'name',
            'max_tokens',
            'max_input_tokens',
            'max_output_tokens',
            'input_cost_per_token',
            'output_cost_per_token',
            'litellm_provider',
            'mode',
        ],
    )
    
    df.set_index([
        'name',
    ], inplace=True)
    
    return df


def main(
    debug: bool,
):
    src_root = auto.pathlib.Path.home()
    src_path = src_root / '.aider.model.metadata.json'
    
    dst_root = src_root
    dst_path = src_root / (src_path.name + '.bak')
    
    if dst_path.exists():
        dst_path.unlink()
    
    with src_path.open('rb') as f, dst_path.open('wb') as g:
        auto.shutil.copyfileobj(f, g)

    with src_path.open('r') as f:
        json = auto.json.load(f)

    df = Models()
    
    for name, row in df.iterrows():
        json[name] = row.to_dict()

    if debug:
        print(auto.json.dumps(json, indent=4))
    
    else:
        with src_path.open('w') as f:
            auto.json.dump(json, f, indent=4)


def cli(args: list[str] | None = None):
    parser = auto.argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    
    args = vars(parser.parse_args(args))
    
    main(**args)

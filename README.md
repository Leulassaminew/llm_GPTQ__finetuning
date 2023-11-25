
<a name="readme-top"></a>
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="meetplace.png" alt="Logo" width="200" height="200">
  </a>
<h3 align="center">Finetuning our quantized model for specific task</h3>
</div>

This repository contains a convenient wrapper for fine-tuning GPTQ models and will be used to fine tune our quantized model.

This repo is built upon these materials:

* [alpaca-lora](https://github.com/tloen/alpaca-lora) for the original training script.
* [GPTQ-for-LLaMa](https://github.com/qwopqwop200/GPTQ-for-LLaMa) for the efficient GPTQ quantization method.
* [exllama](https://github.com/turboderp/exllama) for the high-performance inference engine.

## Key Features

* Fine tuning GPTQ model and retrieving a LORA
* we will use the LORA retrieved from this fine tuning to create a mutli task head for our LLM
* Memory-efficient fine-tuning to make our lora smaller and faster.

## Usage
First you will need a GPU instance 

### Setup
1. Clone the repository

   ```bash
   git clone https://github.com/Leulassaminew/llm_GPTQ__finetuning.git
   ```
2. Change to the directory

   ```bash
   cd llm_GPTQ__finetuning
   ```

3. Install default dependencies

   ```bash
   pip install -r requirements.txt
   ```
4. Install quant dependencies

   ```bash
   pip install -r cuda_quant_requirements.txt
   ```
5. Disable Wandb

   ```bash
   wandb disabled
   ```
6. make a directory to store the model

   ```bash
   mkdir models
   ```
7. download the GPTQ model

   ```bash
   python download_private.py
   ```
8. Now we will start fine tuning by selecting specific data set from the hub

   ```bash
   python finetune.py \
    --base_model models/meetplacesales \
    --data_path 'meetplace1/classification' \
    --output_dir 'output_lora' \
    --batch_size 128 \
    --micro_batch_size 4 \
    --train_on_inputs True \
    --num_epochs 10 \
    --learning_rate 2e-4 \
    --cutoff_len 1600 \
    --group_by_length \
    --val_set_size 0.05 \
    --eval_steps 0 \
    --logging_steps 5 \
    --save_steps 5 \
    --gradient_checkpointing 1 \
    --mode gptq \
   ```

You can change the dataset used by simply changing the data_path parameter
Note that the installation of above packages requires the installation of CUDA to compile custom kernels. If you have issue, looks for help in the original repos [GPTQ](https://github.com/qwopqwop200/GPTQ-for-LLaMa), [exllama](https://github.com/turboderp/exllama) for advices.

### Data Preparation

We have Prepared the instruction data to fine-tune the model in the following JSON format.

```json
[
{
    "description": "Template used by Alpaca-LoRA.",
    "prompt_input": "Below is an instruction that describes a task, Write a response that appropriately completes the request.\n\n### Instruction:\n Categorize the input text based on the sales technique used in it from one of these categories only and offer no explanation:\n\nBUILDING RAPPORT\nNEEDS ASSESMENT\nCREATING URGENCY\nSOCIAL PROOF\nOVERCOMING OBJECTION\nCROSS SELLING OR UPSELLING\nVALUE BASED SELLING\nSPIN SELLING\nNEURAL SELLING\nNONE.\n\n### Input:\n{input}\n\n### Response:\n",
    "response_split": "### Response:"
}
]
```

You can supply a single JSON file if you want to change the instruction format.


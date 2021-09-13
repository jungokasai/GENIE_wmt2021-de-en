# GENIE WMT 2021 DE-EN data and baselines

[GENIE](https://genie.apps.allenai.org/) collaborated with [WMT 2021](http://statmt.org/wmt21/) and provided human evaluations of WMT 2021 German-English submissions for the news translation task. To ease the future use of the WMT21-de-en dataset, we provide raw and preprocessed data and transformer baseline models.

## Data
    - [wmt2021-de-en_bpe32k.tar.gz](https://arkdata.cs.washington.edu/GENIE/wmt2021-de-en/data/wmt2021-de-en_bpe32k.tar.gz). We applied [Moses](https://github.com/moses-smt/mosesdecoder) tokenization and fastBPE with 32K BPE operations that are learned from the training data.
    - [wmt2021-de-en_bpe32k_data-bin.tar.gz](https://arkdata.cs.washington.edu/GENIE/wmt2021-de-en/data/wmt2021-de-en_bpe32k_data-bin.tar.gz). Data binarized with [Fairseq-preprocess](https://github.com/pytorch/fairseq). If you train your model with [fairseq](https://github.com/pytorch/fairseq), you only need this data.
    - [wmt2021-de-en.tar.gz](https://arkdata.cs.washington.edu/GENIE/wmt2021-de-en/data/wmt2021-de-en.tar.gz). Raw training data. It is created by concatenating all WMT 2021 DE-EN datasets. The dev data are a concatenation of newstest2019deen and newstest2020deen. Since newstest2019, de-en data are all originally German text to mitigate the translationese effect in evaluation ([Barrault et al., 2019](https://aclanthology.org/W19-5301/)).

## Transformer Baselines
    - [GENIE-large.de-en_6-6.tar.gz](https://arkdata.cs.washington.edu/GENIE/wmt2021-de-en/models/GENIE-large.de-en_6-6.tar.gz). A transformer large model with 6-layer encoder and decoder (trained for 7 epochs.)
    - [GENIE-base.de-en_6-6.tar.gz](https://arkdata.cs.washington.edu/GENIE/wmt2021-de-en/models/GENIE-base.de-en_6-6.tar.gz). A transformer base model with 6-layer encoder and decoder (trained for 7 epochs.)
    - [GENIE-base.de-en_3-3.tar.gz](https://arkdata.cs.washington.edu/GENIE/wmt2021-de-en/models/GENIE-base.de-en_3-3.tar.gz). A transformer base model with 6-layer encoder and decoder (trained for 7 epochs.)
    - [GENIE-base.de-en_1-1.tar.gz](https://arkdata.cs.washington.edu/GENIE/wmt2021-de-en/models/GENIE-base.de-en_1-1.tar.gz). A transformer base model with 6-layer encoder and decoder (trained for 7 epochs.)


## Installation
All baselines models are trained with the [fairseq](https://github.com/pytorch/fairseq) library.
Follow their instruction to install the library. We provide an example installation process here.
```bash
git clone https://github.com/pytorch/fairseq
cd fairseq
pip install --editable ./
```
## Training
The following assumes 8-GPU training. Adjust `--update-freq` based on the number of GPUs. For example, `--update-freq 2` for 4-GPU training.
```bash
wget https://arkdata.cs.washington.edu/GENIE/wmt2021-de-en/data/wmt2021-de-en_bpe32k_data-bin.tar.gz
```
```bash
fairseq-train wmt2021-de-en_bpe32k_data-bin/  --arch transformer_vaswani_wmt_en_de_big --share-all-embeddings     --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0     --lr 0.0005 --lr-scheduler inverse_sqrt --warmup-updates 4000 --warmup-init-lr 1e-07     --dropout 0.1 --weight-decay 0.0     --criterion label_smoothed_cross_entropy --label-smoothing 0.1     --max-tokens 4096    --fp16 --save-dir GENIE-large.de-en_6-6/ --seed 1  --encoder-embed-dim 1024 --encoder-ffn-embed-dim 4096 --encoder-attention-heads 16 --decoder-embed-dim 1024  --decoder-ffn-embed-dim 4096 --decoder-attention-heads 16  --max-epoch 7
```
```bash
fairseq-train wmt2021-de-en_bpe32k_data-bin/    --arch transformer_wmt_en_de --share-all-embeddings      --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0       --lr-scheduler inverse_sqrt --warmup-init-lr 1e-07 --warmup-updates 4000        --lr 0.0005 --stop-min-lr 1e-09    --criterion label_smoothed_cross_entropy --label-smoothing 0.1 --weight-decay 0.0       --max-tokens 8192  --save-dir GENIE-base.de-en_3-3/ --dropout 0.1 --max-source-positions 1024 --max-target-positions 1024 --fp16 --max-update 500000 --seed 1 --decoder-layers 3 --encoder-layers 3
```
## Inference
```bash
fairseq-generate wmt2020-en-de_bpe32k_data-bin/ --path GENIE-base.de-en_3-3/checkpoint.pt --beam 5 --remove-bpe --lenpen 0.6 > test.out
```
## GENIE Submission
```bash
cat test.out | grep -P '^H' | cut -c1- | sort -n -k 1 |uniq | cut -f3 > test.txt
perl mosesdecoder/scripts/tokenizer/detokenizer.perl <  test.txt >  test.detok.txt
python convert_text2jsonl.py --ref-file data/references/newstest2021.de-en.ref.A.en --sys-file test.detok.txt --ref-file-sgm data/sources/newstest2021.src.de-en.xml --out-file newstest2021.de-en.GENIE-large-6-6.en.json 
```

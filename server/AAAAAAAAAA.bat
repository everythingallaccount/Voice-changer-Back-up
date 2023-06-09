python MMVCServerSIO.py ^
    -p 18888 ^
     --https false ^
     --content_vec_500 pretrain/checkpoint_best_legacy_500.pt ^
    --content_vec_500_onnx pretrain/checkpoint_best_legacy_500.onnx ^
    --content_vec_500_onnx_on false ^
    --hubert_base pretrain/hubert_base.pt ^
     --hubert_base_jp pretrain/rinna_hubert_base_jp.pt ^
     --hubert_soft pretrain/hubert/hubert-soft-0d54a1f4.pt ^
     --nsf_hifigan pretrain/nsf_hifigan/model ^
     --model_dir models ^
     --samples samples.json



 python MMVCServerSIO.py -p 18888 --https true --content_vec_500 pretrain/checkpoint_best_legacy_500.pt --hubert_base pretrain/hubert_base.pt --hubert_soft pretrain/hubert/hubert-soft-0d54a1f4.pt --nsf_hifigan pretrain/nsf_hifigan/model --hubert_base_jp pretrain/rinna_hubert_base_jp.pt --model_dir model_dir
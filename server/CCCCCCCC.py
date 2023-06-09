import subprocess
print('CCC')
command = 'python MMVCServerSIO.py -p 18888 --https true --content_vec_500 pretrain/checkpoint_best_legacy_500.pt --hubert_base pretrain/hubert_base.pt --hubert_soft pretrain/hubert/hubert-soft-0d54a1f4.pt --nsf_hifigan pretrain/nsf_hifigan/model --hubert_base_jp pretrain/rinna_hubert_base_jp.pt --model_dir model_dir'

process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

print(output.decode('utf-8'))
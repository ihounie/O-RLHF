for learning_rate in 0.00001 0.0005 
do
    for kl_beta in 0.01 0.05
    do
        echo $learning_rate $kl_beta
        python3 lolrl_qlora_llama_hh.py --learning_rate $learning_rate --kl_beta $kl_beta --output_dir ./results/lr-$learning_rate-kl-$kl_beta
    done
done
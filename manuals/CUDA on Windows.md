# Installare supporto Pytorch con CUDA (NVIDIA) su Windows

Utilizzare la GPU localmente per far girare librerie come Pytorch è possibile anche su Windows, purché si mantengano tutte le compatibilità del caso.



## Installare CUDA
Per prima cosa controlliamo la versione di CUDA Toolkit mediante il comando
```sh
nvcc --version
```
È importante controllare la versione, e se necessario cambiarla, compatibilmente con le [dipendenze](https://pytorch.org/get-started/locally/). Scorrendo in basso nella pagina di Pytorch sono indicate eventuali incompatibilità, come quella, ad oggi, con Python 3.12 e 2.x su Windows.

In caso si voglia scaricare una nuova versione di CUDA (o switchare tra le versioni) bisogna cambiare le variabili d'ambiente, come mostrato in questa [guida](https://github.com/bycloudai/SwapCudaVersionWindows).

Nel caso in cui voglia sfogliare altre versioni, come ad esempio quella per CUDA 11.8, esiste la [pagina dedicata alle versioni precedenti](https://pytorch.org/get-started/previous-versions/#:~:text=Linux%20and%20Windows-,%23%20CUDA%2011.8,-conda%20install%20pytorch%3D%3D2.3.1).

Installare la versione desiderata mediante la pagina ufficiale [NVIDIA](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/). Necessario anche controllare [cuDNN](https://docs.nvidia.com/deeplearning/cudnn/latest/installation/windows.html), che sia compatibile con la versione interessata.

ℹ️ Ricorda che un riavvio non fa mai male a Windows.



## Crare ambiente Python

Questa è la normale prassi per qualsiasi progetto. Se hai installato Pyenv assicurati di aver selezionato la versione di Python compatibile (ad esempio la 3.11.9) e crea un nuovo ambiente (che chiameremo "env") con la seguente istruzione
```sh
python -m venv .pyenv
```
e attiviamolo digitando
```sh
./.pyenv/Scripts/activate
```
se questo comando non dovesse funzionare perché magari usi Linux, riprovare con
```sh
source ./.pyenv/Scripts/activate
```


## Installare libreria PyTorch con supporto CUDA

Seguendo le compatibilità di cui sopra, installare la libreria Pytorch e tutto quel che ne consegue con le proprie dipendenze.
> Se è installato CUDA 11.8, il comando che dovrà essere lanciato è il seguente, ma è **fondamentale** assicurarsi che le compatibilità siano corrette.
> ```sh
> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
> ```
Le librerie superano abbondantemente il GB di spazio, quindi ci vorrà un po' di tempo.



### Test di CUDA

Per assicurarsi che tutto sia stato installato correttamente, e che la GPU sia utilizzabile da Pytorch è necessario effettuare quello che ho battezzato come "test di CUDA", ossia semplicemente eseguire queste istruzioni con Python
```python
import torch
print(torch.cuda.is_available())
```
> Altro comando più immediato
> ```sh
> python -c "import torch; print(torch.rand(2,3).cuda())"
> ```
È possibile inserire questo script anche in un file .py, l'importante è che il risultato sia proprio `True`


### Possibili problemi

In caso di problemi, come la mancanza di librerie di supporto, compilatore g++ o altro, provare ad installare il necessario e reinstallare la versione di Python utilizzata. Se ad esempio si utilizza Pyenv digitare
```sh
pyenv uninstall 3.x
pyenv install 3.x
pyenv global 3.x
```

Per problemi più avanzati (come ad esempio problemi al file [fbgemm.dll](https://discuss.pytorch.org/t/failed-to-import-pytorch-fbgemm-dll-or-one-of-its-dependencies-is-missing/201969), potrebbe essere necessario l'utilizzo di tool avanzati come [Dependencies](https://github.com/lucasg/Dependencies) per trovare il problema e risolverlo).

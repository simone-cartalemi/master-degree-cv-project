# Smarty Vision on Urban Smog
## Progetto di Tesi di Laurea Magistrale (LM-18)

Questa repository contiene tutto il materiale relativo alla mia tesi di laurea magistrale in Informatica dal titolo "Smart Vision on Urban Smog".


### Abstract

Il monitoraggio e la quantificazione delle emissioni veicolari rappresentano una sfida cruciale per mitigare l’inquinamento atmosferico e promuovere la sostenibilità ambientale. In questo progetto è stato proposto un approccio basato sulla visione artificiale per stimare in tempo reale le emissioni prodotte dai veicoli a motore.

La presente ricerca si propone di sviluppare e validare un sistema innovativo per la stima dell'inquinamento atmosferico generato dal traffico veicolare, basato esclusivamente sull'analisi di immagini acquisite da telecamere di videosorveglianza urbana. Tramite tecniche di stima della profondità e di correzione prospettica, è possibile determinare con precisione la velocità di ciascun veicolo e, di conseguenza, quantificare le emissioni generate.

I risultati ottenuti attraverso la sperimentazione dimostrano l'efficacia e la robustezza del metodo proposto, aprendo nuove prospettive per lo sviluppo di sistemi di monitoraggio ambientale avanzati e per l’implementazione di strategie di mitigazione dell’inquinamento veicolare. Inoltre, il sistema proposto può essere integrato in sistemi di controllo del traffico più complessi, fornendo informazioni in tempo reale sullo stato del traffico e sulla qualità dell'aria.


#### Citazione

Se utilizzi questo repository, considera di citarlo come referenza:
```latex
@online{svousbysimonecartalemi,
    author    = {Simone Cartalemi},
    title     = {Smart Vision on Urban Smog},
    year      = {2024},
    publisher = {simone-cartalemi},
    url       = {https://github.com/simone-cartalemi/master-degree-cv-project}
}
```

## Introduzione

Il presente repository ha lo scopo di:
- Tenere traccia dell'implementazione completa del progetto, inclusi tutti i moduli, le classi e le funzioni;
- Strutturare in modo chiaro e coerente tutti i file e le cartelle che compongono il progetto;
- Spiegazione dettagliata delle funzionalità, delle interfacce e delle logiche interne del codice;
- Visualizzare i principali risultati ottenuti e consentire di sperimentare su di essi;
- Conservazione del codice e libertà di visione

I dataset non sono inclusi, ma sono presenti dei manuali su come ottenerli e gestirli (vedi istruzioni per l'utilizzo).


### Struttura

La struttura della cartella `maseter-degree-cv-project` è la seguente:
```
maseter-degree-cv-project/
├── datasets/
│   └── Cartella dei dataset e script di preparazione e riorganizzazione
├── detection/
│   ├── test/
│   │   └── Script di test delle architetture YOLO
│   ├── weights/
│   │   └── Cartella di destinazione dei pesi delle architetture YOLO
│   └── Script di esempio per il training e manifest .yaml per i dataset
├── homography/
│   └── File di sperimentazione sull'omografia e matrice per il dataset thailandese
├── manuals/
│   └── Markdown con guide da seguire o indicazioni su questo progetto
├── notebooks/
│   └── File notebook Jupyter utilizzati durante gli esperimenti, in fase di studio,
│       vecchi codici storici conservati o visualizzazione dei risultati
├── results/
│   └── File di output di tracking, speed estimation, emissioni e video dimostrativi
├── src/
│   ├── architectures/
│   │   └── Classi per architetture YOLO 5 e 8
│   ├── config/
│   │   └── Script contenente le variabili di base del progetto
│   ├── dataset/
│   │   └── Classi di gestione dataset GRAM-RTM e MIO-TCD
│   ├── estimator/
│   │   └── Classi di supporto contenenti funzioni utilizzate
│   ├── sort/
│   │   └── Repository esterno      # https://github.com/abewley/sort
│   ├── util/
│   │   └── Script di gestione contenuti esterni al progetto (file system)
│   ├── validator/
│   │   └── Classi di validazione dei risultati (benchmarking)
│   ├── yolov5/
│   │   └── Repository esterno      # https://github.com/ultralytics/yolov5
│   ├── calculate_speed.py          # Script di conversione tracce in velocità e
│   │                                 generazione file di validazione benchmarking
│   ├── convert_labels.py           # Script di conversione label dei dataset
│   ├── export_pollutions.py        # Script di conversione velocità in stime di emissione
│   ├── split.py                    # Script di separazione dataset in train e test
│   ├── track_vehicles.py           # Script generatore di tracce veicoli dei video
│   └── videomaker.py               # Script di creazione video dimostrativi
├── tutorial.ipynb                  # Notebook Jupyter dimostrativo di utilizzo
└── requirements.txt
```

---


### Istruzioni per l'utilizzo

#### Fase 1: Preparazione dataset, modelli e venv
1.  Scaricare i dataset di addestramento.

    Seguendo il manuale [Prepare dataset](manuals/Prepare%20dataset.md) scaricare i dataset e riorganizzarli come descritto dalla struttura delle cartelle e convertire le label per l'addestramento.

    Utilizzando i comandi descritti nella [guida](manuals/Prepare%20dataset.md) saranno effettuati in automatico il download, la gestione e il labeling dei datasets (assicurarsi che i link siano corretti).

2.  Scaricare e organizzare il dataset di benchmarking.

    > Il dataset thailandese discusso e utilizzato è disponibile su [Google Drive](https://drive.google.com/drive/u/1/folders/12F7AlJiv2AMiJ1DZ4PiOlAZlEXzSUPS7) a carico degli autori del relativo [paper](https://ieeexplore.ieee.org/abstract/document/10381710), quindi potrebbe non essere rintracciabile in futuro.

    Il modo più rapido e affidabile di scaricarlo è utilizzando Google Colab con accesso al proprio account Google e autorizzazioni ad interfacciarsi con esso. Il [notebook](notebooks/datasets/create%20benchmarking%20video%20archive%20drive.ipynb) è stato scritto per aiutare questo processo, creando un unico file zip di 15 GB sul proprio archivio e dando la possibilità di essere scaricato rendendolo condiviso a chiunque abbia accesso al relativo link.
    Eseguire le istruzioni del notebook su Google Colab, rendere il file generato condivisibile e scaricare tramite pacchetto Python `gdown`.
    
    Estrarre il contenuto dell'archivio mediante il comando
    ```sh
    unzip Videos.zip -d ./dataset/thai/
    ```

    In alternativa è possibile creare un proprio dataset di video, configurando il file delle [variabili di benchmarking](src/config/defaults.py) e creando la [matrice di omografia](notebooks/homography/manual_homography.ipynb).

3.  Configurare l'ambiente Python.

    Per sfruttare la potenza di calcolo della GPU e utilizzare i driver CUDA su scheda grafica NVIDIA è necessaro seguire la [guida](manuals/CUDA%20on%20Windows.md). Lo script è specifico per sistema operativo Windows, ma può essere adattato anche su altri sistemi.

    Dopo aver creato l'ambiente per Python, installare manualmente YOLO seguendo la [guida apposita](manuals/Yolo%20by%20ultralytics.md).

    > È stato predisposto il file `requirements.txt`, ma potrebbe essere specifico per il sistema operativo utilizzato, si consiglia comunque di controllare i pacchetti necessari.

4.  Scaricare il modulo SORT.

    Modulo non integrato in questo progetto è quello di tracciamento chiamato *SORT*. È stato utilizzato un [progetto esterno](https://github.com/abewley/sort) sviluppato da un utente di GitHub, che è necessario clonare all'interno della cartella [src/](src/) per permettere all'apposito script di tracciare i veicoli.
    Installare anche le dipendenze del progetto come suggerito nel README, tenendo conto di eventuali aggiornamenti degli stessi. Eseguire
    ```sh
    # lap è stato cambiato in lapx
    pip install lapx filterpy scikit-image
    ```

    È possibile integrare qualsiasi altro modulo dedicato al tracciamento, purché si mantenga la logica di quello utilizzato, al fine di mantenere la compatibilità dell'intero sistema. L'unico script che ne richiama le funzioni è [track_vehicles.py](src/track_vehicles.py).


#### Fase 2: Addestramento modelli
> Per addestrare i modelli è consigliato seguire le indicazioni da documentazione ufficiale.

Si raccomandano alcuni accorginemti essenziali:
-   Per addestrare il modello *YOLO v5* è necessario aver clonato il repository come descritto nella fase precedente; per il modello *YOLO v8* è necessario aver installato il pacchetto all'interno dell'ambiente virtuale di Python.
-   Scegliere i parametri (*batch*, *epochs*, *imgsz*, etc) in maniera adeguata.
-   È necessario controllare la correttezza dei path all'interno dei file `.yaml` all'interno della cartella [detection](detection/) prima di avviare la fase di training. Alcuni comandi utilizzati sono quelli all'interno degli script di shell nella stessa cartella.
-   Potrebbe essere necessario dover silenziare i warning generati durante l'esecuzione del training del modello *YOLO v5*. Aggiungere all'interno del file `train.py` (se il repository è stato già clonato si troverà in [src/yolov5/train.py](src/yolov5/train.py)) le seguenti righe più o meno all'inizio del file
    ```python
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)
    ```

-   Potrebbe essere necessario dover cambiare il path di `settings.yaml` se l'esecuzione del training del modello *YOLO v8* lo richiede. Cambiare la variabile `datasets_dir: /path/to/master-degree-cv-project` impostando il path corretto alla cartella del progetto.
-   Su ambiente Linux (da remoto con SSH) è consigliato l'utilizzo di **Screen**, che serve a mantenere attività in background, assicurandone la non interruzione alla chiusura della sessione.
I comandi sono
    ```sh
    # Avvia la sessione
    screen
    
    # Riprendi la sessione
    screen -r
    ```
    Digitando i tasti `Ctrl+A` e `D` sarà fatto il detach della sessione, lasciandola in esecuzione.


#### Fase 3: Creazione matrice omografica
Nel caso in cui sia necessario creare la matrice omografica per un nuovo dataset di benchmarking o per un video su cui eseguire gli script, sono stati aggiunti al progetto dei notebook Jupyter che si occuperanno della generazione [automatica](notebooks/homography/homography_by_sift.ipynb) tramite SIFT (se le immagini soddisfano certi requisiti) oppure tramite generazione [manuale](notebooks/homography/manual_homography.ipynb), come per il caso del dataset thailandese.

Un ulteriore [notebook](notebooks/homography/verifier_matrix.ipynb) aiuterà a verificare la correttezza della matrice generata, visualizzando la trasformazione e il remapping dei punti.


#### Fase 4: Esecuzione degli script
Gli script descritti di seguito sono da eseguire sequenzialmente. Essi esporteranno i risultati nella cartella `results/`.

1.  Tracking.

    Lo script di tracking supporta sia un singolo file che un'intera cartella di video.
    Ecco alcuni comandi di esempio per lanciare lo script
    ```sh
    python ./src/track_vehicles.py v5m_gram "./datasets/thai/Videos/IMG_0606.MOV" -v

    python ./src/track_vehicles.py v5m_mio "./datasets/thai/Videos/IMG_0606.MOV" -v

    python ./src/track_vehicles.py v8s_mio "./datasets/thai/Videos" -v
    ```
    
2.  Speed estimation.

    Lo script prende in input la cartella di origine dei `json` esportati dal precedente script, e la cartella di destinazione. Qui di seguito un esempio.
    ```sh
    python ./src/calculate_speed.py "./results/tracks/v8s_mio_2024-09-26_10-05-16/" -b -v
    ```
    
3.  Emissioni.

    Lo script di calcolo delle emissioni supporta sia un singolo file che un'intera cartella di video.
    Ecco un comando di esempio per lanciare lo script
    ```sh
    python ./src/export_pollutions.py "./results/speed/v8s_mio_2024-09-26_10-05-16/" "./results/pollution/v8s_mio_2024-09-26_10-05-16/" -v
    ```

4.  Visualizzare i risultati

    Per visualizzare un video con tracking, bounding box, labels e altro, eseguire il comando seguente con i relativi setting desiderati.
    ```sh
    python ./src/videomaker.py "./datasets/thai/Videos/IMG_0606.MOV" "results/tracks/v8s_mio_2024-09-26_10-05-16/IMG_0606.json" -b -t -v
    ```

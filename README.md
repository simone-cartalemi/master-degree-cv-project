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
│   ├── utils/
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
│   ├── videomaker.py               # Script di creazione video dimostrativi
│   └── ########.py
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

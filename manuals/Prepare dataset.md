# Preparazione dei dataset di addestramento
Per questo progetto, utilizzeremo i dataset GRAM-RTM e MIO-TCD, selezionati appositamente per il nostro obiettivo. Per esperimenti personali va bene qualunque dataset di veicoli su strada.

## Procedura
1.  **Download:** Scaricare i dataset [GRAM-RTM](https://gram.web.uah.es/data/datasets/rtm/index.html) e [MIO-TCD](https://tcd.miovision.com/challenge/dataset.html) dai relativi link.
2.  **Organizzazione:** Creare la cartella `datasets/` nella directory principale del progetto.\
Copiare i file scaricati all'interno della cartella `datasets/`.\
**⚠️ Attenzione**: Assicurarsi che la struttura finale delle cartelle corrisponda a quanto segue:
    ```markdown
    root/
    └── datasets/
        ├── MIO-TCD-Localization/
        │   ├── images/
        │   │   ├── train/
        │   │   │   ├── 00000000.jpg
        │   │   │   └── ...
        │   │   └── val/
        │   │       ├── 00000005.jpg
        │   │       └── ...
        │   └── labels/
        │       │   ├── 00000000.txt
        │       │   └── ...
        │       └── val/
        │           ├── 00000005.txt
        │           └── ...
        └── GRAM-RTMv4/
            ├── images/
            │   ├── train/
            │   │   ├── image000003.jpg
            │   │   └── ...
            │   └── val/
            │       ├── image000001.jpg
            │       └── ...
            └── labels/
                │   ├── image000003.txt
                │   └── ...
                └── val/
                    ├── image000001.txt
                    └── ...
    ```
    La struttura è importante per il motore di YOLO.

3.  **Creazione labels e Split:** Prima di utilizzare i dataset per addestrare la rete YOLO, sarà necessario eseguire alcune operazioni di preprocessing per adattarli al formato richiesto dalla rete.


    ### GRAM
    Dopo aver scaricato gli archivi zip, estrarli in sequenza in modo tale che i dataset siano inclusi all'interno della cartella `datasets/GRAM-RTMv4/Images/`. Le annotazioni, le maschere ROI e gli altri file saranno presenti all'interno di `datasets/GRAM-RTMv4/`

    ```sh
    unzip GRAM-RTMv4.zip -d datasets/
    unzip m30.zip -d datasets/GRAM-RTMv4/Images/
    unzip m30hd.zip -d datasets/GRAM-RTMv4/Images/
    unzip urban1.zip -d datasets/GRAM-RTMv4/Images/
    ```

    Per convertire le label nel formato richiesto è necessario cambiare un po' la struttura delle cartelle per tutti e tre i dataset `M-30`, `M-30-HD` e `Urban1`.

    ```sh
    # Per ognuna delle tre cartelle eseguire questi comandi sostituendo <dataset_name>
    dataset_name="<dataset_name>"
    mv ./datasets/GRAM-RTMv4/Images/"$dataset_name"/ ./datasets/GRAM-RTMv4/Images/images/
    mkdir ./datasets/GRAM-RTMv4/Images/"$dataset_name"/
    mv ./datasets/GRAM-RTMv4/Images/images/ ./datasets/GRAM-RTMv4/Images/"$dataset_name"/images/

    python ./detection/src/convert_labels.py gram ./datasets/GRAM-RTMv4/Images/"$dataset_name"/images/ ./datasets/GRAM-RTMv4/Annotations/"$dataset_name"/xml/
    ```

    Ora è possibile effettuare lo split (0.8 è il valore di default).

    ```sh
    # Per ognuna delle tre cartelle eseguire questo comando sostituendo <dataset_name> e <split_rate> con un float (0.8 suggerito)
    python ./detection/src/split.py ./datasets/GRAM-RTMv4/Images/"$dataset_name"/ <split_rate>
    ```

    ℹ️   Nel caso in cui si voglia fare un merge dei tre dataset per crearne uno più corposo, si ricorda che è necessario rinominare i file nel modo adeguato.


    ### MIO-TCD Dataset

    Estrarre i file tar scaricato con il comando
    ```sh
    tar -xvf MIO-TCD-Localization.tar -C datasets/
    ```

    Il dataset estratto è diviso in due cartelle `train/` e `test/`. I file della cartella `train/` hanno una corrispondenza con i record del file `gt_train.csv`. Quindi per convertire le label eseguire il comando seguente.

    ```sh
    python ./detection/src/convert_labels.py mio-tcd ./datasets/MIO-TCD-Localization/train/ ./datasets/MIO-TCD-Localization/gt_train.csv
    ```

    Rinominare `train/` in `images/` prima di eseguire lo split. Effettua la divisione randomica del dataset, impostando un rate per il validation set a 80%
    ```sh
    # Sostituire <split_rate> con un float (0.8 suggerito)
    python ./detection/src/split.py ./datasets/MIO-TCD-Localization/ <split_rate>
    ```



4.  **Verifica della correttezza dei Bounding Box [opzionale]:** Questo comando permette di fare un check sulle label dei dataset, visualizzando i bounding box.
    ```sh
    # Sostituire <dataset_name> e <index_img>
    python ./detection/src/test/check_bndbox.py ./datasets/gram/<dataset_name>/images/ <index_img>
    ```
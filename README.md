# How many pools are in São Paulo? 

In this project we estimate the total pool count in São Paulo through Statistics, Machine Learning and satellite imagery.

### 1. Data
#### 1.1 Pool detection
Since this is an object detection task, the annotation corresponds to the bounding boxes of the target class, in this case there is just one: "pool".

The final dataset is a mix of Kaggle's "Swimming Pool detection - Algarve's Landscape" dataset (https://www.kaggle.com/datasets/cici118/swimming-pool-detection-algarves-landscape), that was used to train the base model and corresponds to 289 images, and images annotated by ourselves from Google Maps satellite images from São Paulo (1036), totalizing  1325 annotated images.

#### 1.2 São Paulo districs and socioeconomic features
The data was obtained from São Paulo's GeoSampa open data:
https://geosampa.prefeitura.sp.gov.br/PaginasPublicas/_SBC.aspx

We used the `geoportal_setor_censitario.geojson`, that corresponds to the socioeconomic data and for the districts' geometry `limites_adm_geoportal_distrito_municipal.geojson`

### 2. Model

#### 2.1 Task modeling
Since this is a counting problem the natural way of modeling it is through an object detector trained to locate the desired class' instances in the input image.

#### 2.2 Architecture
For the object detection task we chose to fine-tune YOLO v11 small due to its proven great detection capacities, small size, high throughput and ease to train.

#### 2.3 Training results
The final model was able to reach a mAP50 score of ~0.87

![Results](./models/vision/results.png)

Some detections samples:

![Detections](./models/vision/val_batch0_pred.jpg)

![Detections](./models/vision/val_batch2_pred.jpg)

### 3. Pool count
São Paulo has approximately 48621 pools!

This count was obtained through the following process:

1. For each district, iterate over all its sample points and detect the pools in them using the trained detector

2. Find the total sampled area (km^2) by adding up the area of each sampled tile

3. Estimate the pool density (pools/km^2) for the district by dividing the pool count by the sampled area

4. Find each district's total pool count by multiplying its pool density by its area

5. Sum all district's pool count

### 4. Statistical analysis

### 5. Steps to reproduce
#### 5.1 Get stratified samples (by district)
1. Run `data/sample_districts.ipynb` to access the EDA and generate the sampled dataframes at `samples/*geojson`

2. Run `data/get_region_samples.py` to generate the `unified_points.csv`

3. Run `data/download_satellite_images.py` to download the satellite image tiles from the samples points

4. Run `data/get_pool_count.ipynb` to access the pool count logic and visualization

### 6. Further work
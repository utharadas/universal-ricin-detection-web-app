<h1 align="center">Universal Ricin Detection Model</h1>
<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/e/e4/Ricin_structure.png" alt="Ricin Structure" width="150"/>
</div>


<table>
<tr>
<td>
Impedance spectroscopy is a technique where a current is passed through a mixture to detect the presence of specific molecules and chemical reactions within a sample. Our task was to use machine learning to analyze impedance spectroscopy data provided by Dr. Takhistov, an associate professor of food science, to develop a cost-effective method for detecting Ricin, a common biotoxin in many foods. We applied data scraping and cleaning techniques to prepare the data, followed by various forms of analysis to identify the variables that best indicate the presence of Ricin. After reducing the dimensionality of the problem, we used machine learning models, including random forests, and logistic regression, to train a classifier to determine whether Ricin is present in the samples.
</td>
</tr>
</table>



## File Structure 

- [data/](/data): Raw and cleaned data files
- [scripts/](/scripts): Scripts for data analysis and visualizations
- [models/](/scripts): Final Random Forest Classifier model, Logistic Regression, XGBoost Model
- [driver.py](driver.py): Script where new food products can be tested
  
## Usage & Installation
### Environment
To use this model, you need to set up your environment by installing the required dependencies listed in the `requirements.txt` file. Run this:

```
git clone https://github.com/utharadas/universal-ricin-detection-model.git
cd universal-ricin-detection-model
pip install -r requirements.txt
```
More details on the current model can be found in [finalmodel.ipynb](/models/finalmodel.ipynb)
### Using Model
To use this model with different food products and your own data, please refer to the `driver.py` script:
```
cd universal-ricin-detection-model
python driver.py
```
You will have the option to either manually enter your data or to upload a csv file if you're using a large amount of data. If uploading a csv file, please follow the format of [test.xlsx](/data/test.xlsx). If you are manually entering data you will be asked to enter the following information in the terminal:
```
Z at 25123:
PA at 25123:
Z at 19954:
PA at 19954:
Z at 31634:
PA at 31634:
Time (Works best at 10 minutes):
pH: 
carbs: 
orp: 
do(ppm): 
cond100:
cond100kh: 
b*:
a*: 
```


## Data
### Files
- [data/raw data/Impedance](/data/raw20%data/Impedance) - Files containing raw data of food products' Z and PA values when tested for Ricin and without Ricin
- [data/final data](/data/final20%data) - File with all food products and their properties, and PA and Z values from 5-20 minutes
- [data/raw data/Food contents, pH & ORP.xls](/data/raw20%data/Food20%contents,20%ph20%&20%ORP.xls): File with food data such as pH, conductivity, fat, sodium, etc.

### Dimension Reduction
- Features with low feature importance with Z were dropped: 'Sodium', 'Protein', 'Cholesterol', 'Fat', 'Potassium','L'
<img src="/images/feat-importance.png" alt="Impedance Chart" width="550"/>

### Feature Engineering
```
df['Last5freq'] = df.groupby('Food')['Freq(Hz)'].transform(lambda x: x.shift(-2) - x.shift(2))
```
Calculates the difference between the frequency values, shifted by 2 rows forward and 2 rows backward within each group of food.
```
df['Last5increase'] = df.groupby('Food')['Z(Ohm)'].transform(lambda x: x.shift(-2) - x.shift(2))
```
Calculates the difference in impedance values, shifted by 2 rows forward and 2 rows backward within each group of food.
```
df['Last5Z'] = df.groupby('Food')['Z(Ohm)'].transform(lambda x: x.rolling(window=5, center=True).mean())
```
Computes the centered rolling mean of impedance over a window of 5 data points within each group of food.
```
df['Last5slope'] = df['Last5increase'] / df['Last5freq']
```
Calculates the slope of impedance over frequency using the features Last5increase and Last5freq.
```
df['Last5increasePA'] = df.groupby('Food')['PA'].transform(lambda x: x.shift(-2) - x.shift(2))
```
Calculates the difference in phase angle values, shifted by 2 rows forward and 2 rows backward within each group of food.
```
df['Last5PA'] = df.groupby('Food')['PA'].transform(lambda x: x.rolling(window=5, center=True).mean())
```
Computes the centered rolling mean of the phase angle over a window of 5 data points within each group of food.
```
df['Last5slopePA'] = df['Last5increasePA'] / df['Last5freq']
```
Calculates the slope of phase angle over frequency using the features Last5increasePA and Last5freq.

## Results
- <b>Variable Importance:</b> Through feature importance analysis, the most significant variables indicating the presence of Ricin were found to have a mutual importance score over 1

![rsults](/images/feat-analysis-bar.png) <img src="/images/feat-analysis-table.png" alt="Impedance Chart" width="200"/>


- <b>Random Forest Classifier:</b> Decided to use random forest model for final model because it provided robust results, identifying Ricin presence with high accuracy and recall, making it effective for detection.

|          | precision | recall | f1-score | support |
|----------|-----------|--------|----------|---------|
| **0**    |  0.92     |  0.92  |  0.92    |    1457 |
| **1**    |    0.91   | 0.91   |    0.91  |   1285  |
| **accuracy**    |    |        |     0.92 |   2742  |
| **macro avg**    |0.92|   0.92 |     0.92 |  2742  |
| **weighted avg** |0.92|   0.92 |    0.92  |   2742 |


## Reccomendations
- **Expand the Dataset**: Collect more data from diverse food samples to improve model accuracy.

- **Implement Additional Machine Learning Algorithms**: Explore algorithms like SVM and Gradient Boosting to compare their effectiveness.

- **Incorporate More Feature Engineering Techniques**: Apply advanced techniques to extract more informative features from the data.


## References
- Chai, Changhoon, Jooyoung Lee, and Paul Takhistov. 2010. [Direct Detection of the Biological Toxin in Acidic Environment by Electrochemical Impedimetric Immunosensor](https://doi.org/10.3390/s101211414) Sensors 10, no. 12: 11414-11427.

## Team
 - Aiman Koli
 - Sowmiya Veluswamy
 - Mark Tawfik
 - Uthara Das

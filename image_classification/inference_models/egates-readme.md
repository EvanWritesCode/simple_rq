### What and how
BX classifier / egate classifier utilizes a deep neural net built by google (inception v3) to classify egate images.

### Pre-requisites

Please note: this code requires python 3.x and `tensorflow`.

1. Download model content from S3, e.g. `s3://ipts-computer-vision/tf_models/`
1. Clone project
1. Install tensorflow with `pip3 install tensorflow`

The inference engine runs fine on CPU only instances, it has been tested on t2.micro and bigger instances. It should run on your development PC as well.

### Using the `egates` API

Sample code below. Note the `ImageDescriptor` takes the image path and a key. The key could be any string, typically the url for the image. The key has no use inside the egates API.

Output result is a `dict` where each `key` has a True/False entry.

Using the API involves there lines.

1. import `egate`
2. instantiate `Egate`
3. Invoke `is_egate()`

```
# import API
from egate import Egate, ImageDescriptor

# instantiate the inference class
eg = Egate(model_dir="/path/to/model_data")

# Try a few images
res = eg.is_egate([
    ImageDescriptor("/path/to/1.jpg", "1001"),
    ImageDescriptor("/path/to/2.jpg", "s3://buncket/path/etc"),
    ImageDescriptor("/path/to/3.jpg", "https://url.com/path/name/etc"),
    ])
print(res)

{
  '1001': True,
 'https://url.com/path/name/etc': False,
 's3://buncket/path/etc': True
}
```

### Batch processig with `egates` inference engine

Running the inference engine this way can be used for large batch processing of images.

```
# sample command
python egate.py \
  --wild-images-dir /path/to/images \
  --model-dir /path/to/model_data/ \
  --csv-filename output_results.csv

# check the results
cat output_results.csv

image,is_egate
key1,False
key2,False
...
keyX,False
```

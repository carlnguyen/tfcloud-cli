import json
import yaml
from types import SimpleNamespace
from munch import DefaultMunch

# data = yaml.load(open("clouds_config.yaml"), Loader=yaml.FullLoader)
data = json.loads("open")
x = DefaultMunch.fromDict(data, object())
#x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

print("inmotion" in x.clouds)

"""Update exactly one Kustomize image entry for a GitHub Actions deployment."""
import os
from pathlib import Path
import yaml

environment = os.environ['ENVIRONMENT_NAME']
component = os.environ['COMPONENT']
if environment not in {'staging', 'production'} or component not in {'frontend', 'api'}:
    raise SystemExit('Invalid environment or component')
path = Path('environments') / environment / 'kustomization.yaml'
data = yaml.safe_load(path.read_text(encoding='utf-8'))
images = [entry for entry in data.get('images', []) if entry.get('name') == 'rightproperty-' + component]
if len(images) != 1:
    raise SystemExit('Expected exactly one matching image mapping')
images[0]['newName'] = os.environ['IMAGE']
images[0]['newTag'] = os.environ['IMAGE_TAG']
path.write_text(yaml.safe_dump(data, sort_keys=False), encoding='utf-8')
